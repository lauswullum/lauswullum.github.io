---
title: "P8 Jazz"
date: "2026-10-26"
draft: false
---

Lyt til DR P8 og DR P2

```{=html}
<audio id="p8-radio" controls preload="none" aria-label="DR P8 Jazz live" src="https://live-icy.dr.dk/A/A22H.mp3"></audio>
<button id="p8-button" type="button" aria-controls="p8-radio" aria-pressed="false" hidden style="font: inherit; padding: .6em 1em; border: 1px solid currentColor; border-radius: 3px; background: #703996; color: #fff; cursor: pointer; min-height: 44px;">▶ Play P8</button>
<p id="p8-status" role="status"></p>
<audio id="p2-radio" controls preload="none" aria-label="DR P2 live" src="https://live-icy.dr.dk/A/A04H.mp3"></audio>
<button id="p2-button" type="button" aria-controls="p2-radio" aria-pressed="false" hidden style="font: inherit; padding: .6em 1em; border: 1px solid currentColor; border-radius: 3px; background: #15499d; color: #fff; cursor: pointer; min-height: 44px;">▶ Play P2</button>
<p id="p2-status" role="status"></p>
<script src="radio.js" defer></script>
```


Live radio fra [DR P8 Jazz](https://www.dr.dk/lyd/p8jazz) og [DR P2](https://www.dr.dk/lyd/p2).
