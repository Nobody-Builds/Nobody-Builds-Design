# NobodyBuilds-Design

The Nobody Builds design system: brand, logo masters, the builder mascot, icons, fonts, design tokens and the
UI specs. Use it as a git submodule in any Nobody Builds project so every surface draws from one source.

```bash
git submodule add https://github.com/Nobody-Builds/NobodyBuilds-Design.git design
```

**Browse it at [nobody-builds.github.io/NobodyBuilds-Design](https://nobody-builds.github.io/NobodyBuilds-Design/)**:
the logo masters, the mascot, colours, type, voice, every design token and the UI specs, published from this
repository by `site/` on every push to `main`. To run it locally: `cd site && npm install && npm run dev`.

## Contents

| Folder | What it holds |
|---|---|
| `brand/` | `logo-masters.png` (the one-page overview) and `source/`: the untouched GitHub avatar and the builder cut out of it, the only sources of the artwork |
| `logo/` | Seven masters as PNG, each with an SVG that wraps it: `symbol`, `symbol-dark`, `lockup-stacked`, `lockup-stacked-reversed`, `lockup-horizontal`, `lockup-horizontal-reversed`, `app-icon` |
| `mascot/` | **The builder**: `builder.png` (cut out), `dark/builder.png` (Paper sticker border, for dark surfaces only) and `original/builder.png` (the avatar, byte for byte). Usage rules in `mascot/README.md` |
| `icons/` | `favicon.svg`, PNG app icons (16, 32, 180, 192, 512) and the 1200×630 social card |
| `fonts/` | Gilroy Regular, Medium, Semibold and Bold (WOFF), plus Unbounded (WOFF2). Legacy faces retained. See `fonts/README.md`. |
| `tokens/` | `tokens.css` (`@font-face` + light/dark colour variables as RGB triplets) and `tokens.json` (the same colours as hex, plus the seven brand colours) |
| `docs/` | `ui-brand-spec.md` (token derivations, contrast ratios, states, status pills, type scale, logo use), `ux-spec.md` and `ux-screens-longtail.md` (placeholders until there's a product) |
| `screenshots/ux/` | Screenshots for the site's UX pages, once there are screens |
| `scripts/` | `build-assets.py` (every logo, icon and mascot file), `build-tokens.py` (tokens + contrast checks), `cutout.py` |
| `site/` | The Starlight website published to GitHub Pages; `scripts/sync-kit.mjs` copies the kit in at build time |

## Brand at a glance

- **Colours ("Daylight"):** Night Shift `#172033`, Blueprint `#2457A6`, Hard Hat `#FDC521`, Sky `#CFE0F7`,
  Butter `#FFE8A3`, Brick `#EA724A`, Paper `#F5F7FB`, built from the builder's blue zzz and yellow hard hat.
  Blue does the work, yellow is the one bold moment. Never yellow or Brick text on Paper. Every status
  pairs colour with a word or icon.
- **Type:** Gilroy Semibold/Bold for headings, Gilroy Regular/Medium for body and interface text,
  Unbounded for one short accent phrase per layout.
- **Logo:** the builder, used as supplied: no stretching, rotating, recolouring, redrawing or effects. Clear
  space is a quarter of the builder's height on every side. Builder at least 48 px and at most 280 px tall;
  primary lockup at least 180 px wide.
- **Mascot:** the same builder, asleep on the job on a half-built brick wall. It's the joke in the name. The
  friendly face for empty states, onboarding and merch. See [mascot/README.md](mascot/README.md).
- **Voice:** clear, warm and specific, with a dry sense of humour, never in an error. "Nothing built yet. Lay
  the first brick." Brand name in copy: Nobody Builds. Wordmark: nobody builds.

> **To fill in:** one line on what Nobody Builds makes and who it's for.

## Using the tokens

```css
@import "design/tokens/tokens.css";

body { background: rgb(var(--color-bg)); color: rgb(var(--color-ink)); font-family: var(--font-sans); }
h1, h2, h3 { font-family: var(--font-display); font-weight: 600; }
.button-primary { background: rgb(var(--color-accent)); color: rgb(var(--color-on-accent)); }
```

Add the class `dark` to `<html>` for dark mode. The font URLs in `tokens.css` are relative to the
`tokens/` folder. The token names match the Space Works kit, so a project can switch between the two.

## Rebuilding the kit

```bash
pip install -r scripts/requirements.txt
python scripts/build-tokens.py    # tokens.css + tokens.json, fails if any text pair loses contrast
python scripts/build-assets.py    # logo/, icons/, mascot/, brand/logo-masters.png
```

The builder only exists as the 460 × 460 GitHub avatar. If a higher-resolution original turns up, cut it out
with `python scripts/cutout.py <file> brand/source` (rename the result to `builder-cutout.png`) and rebuild.

## Credits

The structure of this kit and site follows the
[Space Works design system](https://github.com/SpaceWorks-HQ/SpaceWorks-Design). The site's light/dark switch uses the
same animation as [Space Works Events](https://github.com/SpaceWorks-HQ/SpaceWorks-Events): the new theme is
revealed as a soft-edged circle growing from the toggle (View Transitions), with a colour cross-fade where
that isn't supported and an instant switch for reduced motion. The visual identity — colour,
type, logo, mascot and voice — is Nobody Builds' own, taken from the builder illustration.

## License

Nobody Builds design assets in this repository are licensed under the
**[GNU Affero General Public License v3](LICENSE)** (`AGPL-3.0-or-later`).

Third-party material keeps its own licence and is not relicensed: the fonts in `fonts/` (see
`fonts/LICENSES/` and [fonts/README.md](fonts/README.md)).
