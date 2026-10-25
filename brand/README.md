# Brand sources

| File | What it is |
|---|---|
| `nobody-builds-brand-guidelines-v1.pdf` | The brand guidelines, all 17 pages in one PDF |
| `guidelines/png/01.png` … `17.png` | The same pages as 1440 × 1000 PNGs |
| `logo-masters.png` | The one-page logo overview: lockups in full colour and reversed, the app tile, the seven colours, Gilroy and Unbounded |
| `source/avatar-460.png` | The Nobody Builds GitHub avatar, untouched. The only copy of the artwork |
| `source/builder-cutout.png` | The builder cut out of the avatar's cream background by `scripts/cutout.py` |

Everything in `logo/`, `icons/`, `mascot/` and `logo-masters.png` is generated from `source/` by
`python scripts/build-assets.py`; the guidelines pages and PDF by `python scripts/build-guidelines.py`
(run it after `build-assets.py`). Edit the sources and scripts, never the outputs.
