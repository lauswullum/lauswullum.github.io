# Laus Wullum

A minimal static personal website at https://lauswullum.github.io/.
The homepage is HTML; blog posts are written in Markdown and converted to HTML with Pandoc. All pages share `styles.css`.

## Write a new post

Open a terminal in this repository and run:

```sh
python3 build.py new my-new-post --title "My new post"
```

Edit `posts/my-new-post/index.md`. It starts with:

```yaml
---
title: "My new post"
date: "2026-10-18"
draft: false
---
```

Use a date in `YYYY-MM-DD` format. The folder name determines the URL. The title and date appear automatically on the page. Optional `author:` overrides Laus Wullum.

Write paragraphs, `## Section headings`, **bold**, *italics*, links, lists, tables, and fenced code blocks using Markdown. Your title is already the page's main heading, so start sections at `##`.

Build after editing:

```sh
python3 build.py
```

This generates each post's `index.html` and rebuilds `blogfront.html`, newest first. Open the homepage or generated post in your browser and refresh. Do not edit generated HTML: edit the Markdown source or `templates/page.html` instead. The script works even when launched from a different folder.

To add an image, put it beside the Markdown file and write `![Description](image.png)`. For a local PDF, use `[Download](document.pdf)`. Asset paths are relative to the post folder. Images, code, tables, and displayed math adapt to narrow screens.

## Math

Math is detected automatically. Use the same build command for posts with and without equations. No HTML script tags are needed in Markdown.

Inline:

```text
The mean is $\mathbb{E}[X] = \mu$.
```

Displayed (leave blank lines before and after):

```text
$$
p(\theta \mid y) \propto p(y \mid \theta)\,p(\theta)
$$
```

Aligned equations:

```text
$$
\begin{aligned}
y_i &\sim \mathcal{N}(\alpha + \beta x_i, \sigma^2) \\
\alpha, \beta &\sim \mathcal{N}(0, 10^2)
\end{aligned}
$$
```

Use ordinary `&` and `<` inside Markdown equations; Pandoc handles HTML escaping. For a literal dollar sign in prose, write `\$`. Code blocks containing dollar signs are not treated as math. Optional `math: true` in the header loads MathJax for manually written HTML equations as well.

MathJax 3.2.2 is bundled in `assets/mathjax/` with its Apache 2.0 license. Base and AMS math work offline. Extra TeX package downloads and the math menu are disabled. The standalone `math-preview.html` remains available as a reference.

## Drafts and removal

Set `draft: true` to exclude a Markdown post from the next build. A draft is not listed, and its previously generated HTML is removed. Deleting a Markdown source also removes its generated HTML on the next build. Other files in the post folder are preserved.

Draft Markdown and assets are still public if committed to this public repository; this is a publishing convenience, not private storage. Keep private drafts outside the repository.

The builder handles only `posts/*/index.md`; existing manually written HTML posts are left untouched and are not added to the listing automatically. It refuses to overwrite a manually written HTML page when you add Markdown alongside it. Move the old HTML aside first if you want to convert it. The existing `posts/aakjaer/index.html` is left as it was.

## Requirements

Python 3 and Pandoc are needed only for building. Both were available when this workflow was set up. Installation instructions: https://pandoc.org/installing.html . No Python packages, Quarto, R, or Julia are required. Code blocks are displayed as text and are not executed.

`templates/post.md` is the starter copied by the new-post command. `templates/page.html` controls the shared layout of generated posts and the blog index. Edit `index.html` directly for homepage changes and `styles.css` for styling.

## View locally

Double-click `index.html` or any generated post's `index.html`. No server is required, including for math.

Optionally, run:

```sh
python3 -m http.server 8002 --bind 127.0.0.1
```

Then open http://127.0.0.1:8002/ . Stop with Ctrl+C.

## Publish

Build, review, commit both Markdown sources and generated HTML, and push:

```sh
python3 build.py
git status
git add -A
git commit -m "Update blog"
git push origin master
```

GitHub Pages should use **Deploy from a branch → master → / (root)**. `.nojekyll` allows GitHub to serve the static files without running a generator. There is no GitHub build workflow; conversion happens locally before committing.

This repository (`lauswullum.github.io`) is the working website. The sibling `minimal_website` folder is an earlier standalone copy and is not synchronized.

## Checks

```sh
python3 -m unittest discover -s tests -v
```

## Painting background

The entire site uses Jens Juel's *Landskab ved Øresund*. The supplied JPEG is retained in `assets/images/jens-juel-landskab-ved-oresund.jpg`, and the original Downloads file is untouched. The browser loads compressed WebP copies: `jens-juel-landskab-ved-oresund.webp` on desktop (about 403 KB) and `jens-juel-landskab-ved-oresund-mobile.webp` on screens 760px or narrower (about 46 KB). The original 3.9 MB JPEG is not downloaded by the pages.

`styles.css` places the painting in a fixed, full-viewport decorative layer behind the content, with a white overlay. The image is cropped to cover the screen without stretching, including on mobile. It is omitted when printing.

Change `--background-wash: .50` near the top of `styles.css` to adjust the effect: higher values such as `.90` make it fainter; lower values make it more visible. Refresh the page after editing; rebuilding Markdown is unnecessary. All pages using the shared stylesheet receive the background automatically.
