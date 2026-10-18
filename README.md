# Laus Wullum

A minimal static personal website for https://lauswullum.github.io/.

Typewriter style with a side index on wide screens.

## View locally

Double-click `index.html` to open it in your browser. Navigation and math also work directly from local files. No installation or build is required.

Alternatively, open a terminal in this folder and run:

```sh
python3 -m http.server 8002 --bind 127.0.0.1
```

Then visit http://127.0.0.1:8002/ . Stop the server with Ctrl+C.

## Edit

Edit the HTML files directly and refresh the browser. `styles.css` controls appearance. To add a post, copy the existing post's HTML, change the title and article, and add its link to `blogfront.html`. Adjust relative asset paths if you change folder depth.

## Math

Open [math-preview.html](math-preview.html) to see inline math, displayed math, and aligned equations. This reference page is intentionally outside the blog listing.

Copy its two deferred script tags to pages requiring math, adjusting paths if nested. Configuration must come before the renderer. Use `$...$` or `\(...\)` inline, and `$$...$$` or `\[...\]` for displayed formulas. Escape HTML special characters in formulas (`&amp;`, `&lt;`). Wrap wide equations in `<div class="math-block">` for horizontal scrolling.

MathJax 3.2.2's TeX-to-SVG bundle is included in `assets/mathjax/`, together with its Apache 2.0 license. Its built-in base and AMS math support works offline; automatic loading of additional TeX packages is disabled. The math menu is disabled to avoid loading extra menu or accessibility components from the network. Further extensions would need to be bundled and configured explicitly.

The profile image, unused PDF, Relearning Turing post, and its dataset are excluded.

## Publish

This repository serves the website directly from its root, without Quarto or a build step. `.nojekyll` disables Jekyll processing.

In GitHub, open **Settings → Pages** and choose **Deploy from a branch**, branch **master**, folder **/ (root)**, then save.

For updates, edit these files, commit, and push to `master`. GitHub Pages publishes to https://lauswullum.github.io/. Check the repository's Actions tab for deployment progress.

```sh
git add -A
git commit -m "Replace Quarto site with minimal static website"
git push origin master
```

Review `git status` before committing. Local editor history and old generated caches are ignored. The previous source remains available in Git history.

## Mobile layout

At 760px and below, the side index becomes top navigation and the page uses a single column with 16px body text. Navigation links have at least 44px of height for touch. Long links wrap, while code blocks and display equations scroll within their own containers. The viewport allows browser zoom.
