# Brand sources

| File | What it is |
|---|---|
| `logo-masters.png` | The one-page logo overview: lockups in full colour and reversed, the app tile, the seven colours, Gilroy and Unbounded |
| `source/avatar-460.png` | The Nobody Builds GitHub avatar, untouched. The only copy of the artwork |
| `source/builder-cutout.png` | The builder cut out of the avatar's cream background by `scripts/cutout.py` |

Everything in `logo/`, `icons/`, `mascot/` and `logo-masters.png` is generated from `source/` by
`python scripts/build-assets.py`. Edit the sources, never the outputs.

There are no brand guidelines pages or PDF yet. When there are, put the pages in `guidelines/png/` and the
PDF here; the site picks them up on the next build.
