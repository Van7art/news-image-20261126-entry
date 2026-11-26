# The World — Thursday 26 November 2026

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/Van7art/news-image-20261126-entry/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/Van7art/news-image-20261126-entry/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

A one-image summary of the world's news on Thursday 26 November 2026, drawn as a classic newspaper front page — **"THE WORLD"**.

The lead story is the US announcing sweeping new tariffs on China, the EU, Japan and India under a Section 301 probe. Around it, 12 more stories cover the day's biggest headlines, plus a footer noting the Macy's Thanksgiving Day Parade postponement and Rocket Lab's Electron flight 101. Every story was verified against reporting in the 26 November 2026 news cycle; the dated source list is in [NOTES.md](NOTES.md).

## How it was made

`gen.py` renders the image deterministically with Python and Pillow — no network, no clock, no randomness. The chosen variant is the broadsheet (`vA/`); `vB/` (poster grid) and `vC/` (lead-image poster) are the alternates.

## Run it

```sh
python3 main.py
```

This copies `entry.png` to `output/entry.png` (or `$MAKEFUN_OUTPUT_DIR` if set) and verifies the copy byte-for-byte with SHA-256, checking the image is a 1024×1024 PNG under 1 MiB.

## License

MIT — see [LICENSE](LICENSE).

<sub>Entered on [make.fun](https://make.fun/?ref=4e96xqxt&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>
