# make-fun-news-image-20261118-the-world

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/cassian27/make-fun-news-image-20261118-the-world/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/cassian27/make-fun-news-image-20261118-the-world/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

THE WORLD — a one-page newspaper front page summing up Wednesday 18 November 2026: Xi greets Trump on the tarmac at APEC in Shenzhen, US–Iran strikes widen across the Gulf, Cyclone Akvan bears down on Andhra Pradesh, Israel opens a new operation in central Gaza, the Quad meets in Manila, and Nvidia posts a $115.8bn quarter. Every story was verified against two or more outlets; all art was drawn for this page.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

This copies `entry.png` (1024×1024, validated as a whole PNG under 1 MiB) to `out/entry.png`. The image itself was drawn at build time by `render.py` (Pillow + Liberation fonts, deterministic); the submitted program needs no network, no keys and no dependencies beyond Node 22 stdlib.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
