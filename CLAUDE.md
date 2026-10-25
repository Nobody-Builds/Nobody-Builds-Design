# NobodyBuilds-Design

Design system for the Nobody Builds GitHub org, modelled on SpaceWorks-HQ/SpaceWorks-Design (same folders,
token names and Starlight site). Brand content is Nobody Builds' own.

- **Artwork is raster and never redrawn.** The only source is `brand/source/avatar-460.png` (460 px GitHub
  avatar) and its cut-out `brand/source/builder-cutout.png`. Every file in `logo/`, `icons/`, `mascot/` and
  `brand/logo-masters.png` is generated: `python scripts/build-assets.py`. Don't edit outputs by hand.
- **Tokens are generated:** edit values in `scripts/build-tokens.py`, run it; it refuses to write
  `tokens/tokens.css`/`tokens.json` if any WCAG pair fails. Keep the 53 token names per theme identical to the
  Space Works kit.
- **Site:** `site/` (Astro 7 + Starlight). `npm run build` runs `scripts/sync-kit.mjs` first, which copies the
  kit into git-ignored `public/kit`, `src/assets/kit` and `src/content/docs/specs`. CSS prefix is `nb-`.
  The site palette in `site/src/styles/custom.css` is maintained by hand to match the tokens.
- Base path is `/NobodyBuilds-Design`; frontmatter links and raw `<img src>` must include it.
- Python deps: `scripts/requirements.txt` (Pillow, fontTools, brotli). Run Python with `-P` on Windows if a
  local file shadows a module.
- Placeholders (`nb-todo`): what Nobody Builds makes, the builder's name, UX pages/specs, guidelines PDF.
- Theme toggle (`site/src/components/ThemeSelect.astro` + the `nb-theme-*` rules at the end of
  `custom.css`) ports the Space Works Events reveal: View Transition circle from the button, cross-fade
  fallback, instant for reduced motion. In a hidden/background tab the transition waits for the next frame.
