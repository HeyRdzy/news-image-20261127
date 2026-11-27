# Friday 27 November 2026: 43 stories, 9 regions — Storm cuts power to 961,000, Zelensky calls Trump–Putin friendship 'strange', Poland signs Palantir AI deal

[![news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/HeyRdzy/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/HeyRdzy/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127)

One image summing up the world's news of Friday 27 November 2026: 43 stories across 9 regions and 12 fields, drawn as a dense newspaper front page — masthead, the day in UTC, the day in numbers, 3 lead stories, 10 secondary stories, a world map, 30 numbered briefs and a date check. Every figure was checked against a primary source (Reuters, AP, BBC, Euronews, Davis Cup, FIDE, PHIVOLCS, Global Fund, PowerOutage.us, market data).

The three leads: a Thanksgiving storm that left 961,000 without power as Black Friday dawned; Zelensky's BBC interview calling the Trump–Putin friendship 'strange' and saying US Patriot delays cost lives; Poland signing a Palantir AI defence deal at noon in the Warsaw Citadel. Thursday's big news — the Kuwait attack, the Aramco fire, Argentina's votes, the EU budget collapse — is named in DATE CHECK and kept off the page, because it is not Friday's news.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies `entry.png` to the output directory and verifies the PNG (magic, size, IHDR dimensions) before copying. The image itself is drawn by `render.py` (Python + PIL, no network).

## Entry

- Competition: [news-image-20261127](https://make.fun/bounty/news-image-20261127) — "Sum up 27 November's world news in one image"
- License: MIT (SPDX-License-Identifier: MIT)
