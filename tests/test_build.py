"""Exercise the publishing workflow against isolated temporary websites."""
from html.parser import HTMLParser
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which('pandoc'), 'Pandoc is required')
class BuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name)
        shutil.copy2(ROOT / 'build.py', self.site)
        shutil.copytree(ROOT / 'templates', self.site / 'templates')
        (self.site / 'posts').mkdir()

    def run_build(self, *args, success=True):
        result = subprocess.run([sys.executable, str(self.site / 'build.py'), *args],
                                cwd='/tmp', capture_output=True, text=True)
        self.assertEqual(result.returncode, 0 if success else 1, result.stdout + result.stderr)
        return result

    def post(self, slug, title='A post', date='2026-10-18', body='Some **words**.', extra=''):
        folder = self.site / 'posts' / slug
        folder.mkdir(exist_ok=True)
        path = folder / 'index.md'
        path.write_text(f'---\ntitle: {json.dumps(title)}\ndate: "{date}"\n{extra}---\n\n{body}\n')
        return path

    def test_plain_posts_order_escape_and_shared_layout(self):
        self.post('old', date='2020-01-01')
        self.post('new', title='A < B & "C"')
        self.run_build()
        listing = (self.site / 'blogfront.html').read_text()
        page = (self.site / 'posts/new/index.html').read_text()
        self.assertLess(listing.index('posts/new/'), listing.index('posts/old/'))
        self.assertIn('A &lt; B &amp; &quot;C&quot;', page)
        self.assertIn('<strong>words</strong>', page)
        self.assertIn('href="../../styles.css"', page)
        self.assertIn('<footer>', page)
        self.assertNotIn('<script', page)
        self.assertIn('aria-current="page"', listing)
        before = (self.site / 'posts/new/index.html').read_bytes()
        self.run_build()
        self.assertEqual(before, (self.site / 'posts/new/index.html').read_bytes())

    def test_math_is_detected_but_code_does_not_trigger_it(self):
        self.post('equations', body=r'''Inline $\mu < 1$.

$$
\begin{aligned}
y_i &\sim \mathcal{N}(\mu,1) \\
\mu &\sim \mathcal{N}(0,1)
\end{aligned}
$$''')
        self.post('code', body='```text\n$not math$\n```')
        self.run_build()
        equation = (self.site / 'posts/equations/index.html').read_text()
        self.assertIn('class="math inline"', equation)
        self.assertIn('class="math display"', equation)
        self.assertIn(r'\begin{aligned}', equation)
        self.assertIn('&amp;', equation)
        self.assertIn('&lt;', equation)
        self.assertLess(equation.index('src="../../math-config.js"'),
                        equation.index('src="../../assets/mathjax/tex-svg.js"'))
        self.assertNotIn('<script', (self.site / 'posts/code/index.html').read_text())

    def test_drafts_and_deleted_sources_remove_only_generated_pages(self):
        source = self.post('active')
        manual = self.site / 'posts/manual'
        manual.mkdir()
        (manual / 'index.html').write_text('<p>Hand-written</p>')
        asset = source.parent / 'image.png'
        asset.write_bytes(b'keep')
        self.run_build()
        source.write_text(source.read_text().replace('---\n\n', 'draft: true\n---\n\n'))
        self.run_build()
        self.assertFalse(source.with_suffix('.html').exists())
        self.assertNotIn('posts/active/', (self.site / 'blogfront.html').read_text())
        self.assertEqual(asset.read_bytes(), b'keep')
        self.assertEqual((manual / 'index.html').read_text(), '<p>Hand-written</p>')
        source.write_text(source.read_text().replace('draft: true', 'draft: false'))
        self.run_build()
        source.unlink()
        self.run_build()
        self.assertFalse(source.with_suffix('.html').exists())

    def test_bad_metadata_leaves_existing_outputs_unchanged(self):
        self.post('good')
        self.run_build()
        previous = (self.site / 'blogfront.html').read_bytes()
        self.post('bad', date='2026-02-30')
        result = self.run_build(success=False)
        self.assertIn('posts/bad/index.md', result.stderr)
        self.assertEqual(previous, (self.site / 'blogfront.html').read_bytes())
        self.assertFalse((self.site / 'posts/bad/index.html').exists())

    def test_new_command_and_overwrite_protection(self):
        self.run_build('new', 'my-post', '--title', 'A "quoted" title')
        source = self.site / 'posts/my-post/index.md'
        before = source.read_bytes()
        self.run_build('new', 'my-post', success=False)
        self.assertEqual(before, source.read_bytes())
        self.run_build('new', '../unsafe', success=False)
        self.run_build()
        self.assertIn('A &quot;quoted&quot; title', source.with_suffix('.html').read_text())
        source.with_suffix('.html').write_text('Hand-written')
        self.run_build(success=False)
        self.assertEqual(source.with_suffix('.html').read_text(), 'Hand-written')


if __name__ == '__main__':
    unittest.main()
