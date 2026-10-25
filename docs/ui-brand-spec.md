# Nobody Builds brand → UI: design-system spec

How the Nobody Builds brand becomes an interface: every token and where it comes from, contrast, states,
status pills, type scale, shape and logo use.

**Source rule.** Every visual decision comes from one source: the builder illustration
(`brand/source/avatar-460.png`). The palette is built around its two strongest colours, the blue zzz and the
yellow hard hat, with the bricks and the background as supporting colours. The only colours outside it are the
status green and red, because the drawing has neither.

**Reproducibility.** Every number in this document comes from `scripts/build-tokens.py`. It holds the values,
checks every documented text pair against WCAG 2.2 (4.5:1 text, 3:1 non-text UI) and refuses to write
`tokens/tokens.css` and `tokens/tokens.json` if any pair fails. Run `python scripts/build-tokens.py -v` to print
every ratio.

---

## 0. Key decisions

| # | Decision | Why |
|---|---|---|
| D1 | The light canvas is **Paper** `#F5F7FB`, a cool blue-white, with white cards. Dark mode is **Night Shift**, a deep navy, with raised surfaces stepped toward blue-grey. No black. | Keeps the dark side of the palette blue. |
| D2 | `accent` = **Blueprint** `#2457A6`, the zzz blue `#3976C4` taken deeper. In dark mode the accent is a lighter blue `#7FA8E8` with Night Shift labels. | The zzz blue itself fails small text both ways (4.20:1 with Paper). Blueprint reaches 6.41:1 with Paper; on Night Shift it is only 2.32:1, so dark mode lightens it. |
| D3 | `brand` defaults to the accent and may be overridden per project. **`emphasis` = Hard Hat**, Nobody Builds' own, never overridden: one bold moment per layout. | Same contract as the Space Works kit. Yellow is louder as one moment than as every button. |
| D4 | **Sky** `#CFE0F7` is the big light fill: the hero, the sidebar and `info`. **Butter** `#FFE8A3` is a small highlight. | Both take Night Shift text above 12:1. |
| D5 | `warn` = **Brick**. `success` is a soft green and `danger` a red, outside the seven. | The drawing has no green or red; status needs them. |
| D6 | Token names are identical to the Space Works kit (53 per theme). | A project can switch kits without code changes. |

## A. Tokens

Light and dark, with the contrast that matters for each. `on-*` is measured against its fill; `*-ink` against
`bg` and its own soft fill.

| Token | Light | Light contrast | Dark | Dark contrast |
|---|---|---|---|---|
| `bg` | `#F5F7FB` |  | `#172033` |  |
| `surface` | `#ECF0F7` |  | `#1D2840` |  |
| `panel` | `#FFFFFF` |  | `#22304B` |  |
| `hover` | `#E4E9F2` |  | `#2A3957` |  |
| `line` | `#D3DAE6` |  | `#3E4D6B` |  |
| `outline` | `#7D8699` | 3.41 on `bg` (non-text) | `#8592AD` | 5.20 on `bg` (non-text) |
| `ink` | `#172033` | 15.17 on `bg`, 16.27 on `panel` | `#F5F7FB` | 15.17 on `bg`, 12.30 on `panel` |
| `muted` | `#4F5A70` | 6.46 on `bg`, 6.93 on `panel` | `#C3C8D2` | 9.69 on `bg`, 7.86 on `panel` |
| `focus` | `#2457A6` | 6.55 on `bg` (non-text) | `#FDC521` | 10.21 on `bg` (non-text) |
| `accent` | `#2457A6` |  | `#7FA8E8` |  |
| `accent-hover` | `#1F4C92` |  | `#92B5EC` |  |
| `accent-active` | `#1A417E` |  | `#A5C2EF` |  |
| `on-accent` | `#F5F7FB` | 6.55 on `accent` | `#172033` | 6.72 on `accent` |
| `accent-soft` | `#E3ECF8` |  | `#263A5C` |  |
| `accent-ink` | `#2457A6` | 6.55 on `bg`, 5.90 on `accent-soft` | `#A9C8F0` | 9.46 on `bg`, 6.63 on `accent-soft` |
| `brand` | `#2457A6` |  | `#7FA8E8` |  |
| `brand-hover` | `#1F4C92` |  | `#92B5EC` |  |
| `brand-active` | `#1A417E` |  | `#A5C2EF` |  |
| `on-brand` | `#F5F7FB` | 6.55 on `brand` | `#172033` | 6.72 on `brand` |
| `brand-soft` | `#E3ECF8` |  | `#263A5C` |  |
| `brand-ink` | `#2457A6` | 6.55 on `bg`, 5.90 on `brand-soft` | `#A9C8F0` | 9.46 on `bg`, 6.63 on `brand-soft` |
| `brand-boundary` | `#2457A6` | 6.55 on `bg` (non-text) | `#A9C8F0` | 9.46 on `bg` (non-text) |
| `emphasis` | `#FDC521` |  | `#FDC521` |  |
| `emphasis-hover` | `#FDCD45` |  | `#FDCD45` |  |
| `emphasis-active` | `#FED66A` |  | `#FED66A` |  |
| `on-emphasis` | `#172033` | 10.21 on `emphasis` | `#172033` | 10.21 on `emphasis` |
| `emphasis-soft` | `#FFF6D6` |  | `#3A3424` |  |
| `success` | `#A6D98F` |  | `#A6D98F` |  |
| `success-hover` | `#95CA7E` |  | `#95CA7E` |  |
| `success-active` | `#84BA6E` |  | `#84BA6E` |  |
| `on-success` | `#172033` | 10.03 on `success` | `#172033` | 10.03 on `success` |
| `success-soft` | `#F1F9EC` |  | `#26382F` |  |
| `success-ink` | `#3B6B2B` | 5.89 on `bg`, 5.87 on `success-soft` | `#A6D98F` | 10.03 on `bg`, 7.66 on `success-soft` |
| `warn` | `#EA724A` |  | `#EA724A` |  |
| `warn-hover` | `#EC8261` |  | `#EC8261` |  |
| `warn-active` | `#EF9377` |  | `#EF9377` |  |
| `on-warn` | `#172033` | 5.43 on `warn` | `#172033` | 5.43 on `warn` |
| `warn-soft` | `#FCEBE4` |  | `#3B2C2B` |  |
| `warn-ink` | `#A3412A` | 5.85 on `bg`, 5.42 on `warn-soft` | `#F2A88E` | 8.34 on `bg`, 6.81 on `warn-soft` |
| `info` | `#CFE0F7` |  | `#CFE0F7` |  |
| `info-hover` | `#BDD3F1` |  | `#BDD3F1` |  |
| `info-active` | `#ABC6EB` |  | `#ABC6EB` |  |
| `on-info` | `#172033` | 12.13 on `info` | `#172033` | 12.13 on `info` |
| `info-soft` | `#EEF4FC` |  | `#24344F` |  |
| `info-ink` | `#2457A6` | 6.55 on `bg`, 6.35 on `info-soft` | `#CFE0F7` | 12.13 on `bg`, 9.33 on `info-soft` |
| `danger` | `#B91C1C` |  | `#FCA5A5` |  |
| `danger-hover` | `#991B1B` |  | `#FDB9B6` |  |
| `danger-active` | `#851E1D` |  | `#FDC9C3` |  |
| `on-danger` | `#F5F7FB` | 6.03 on `danger` | `#172033` | 8.57 on `danger` |
| `danger-line` | `#FCA5A5` |  | `#7C6261` |  |
| `sidebar` | `#CFE0F7` |  | `#121A2B` |  |
| `sidebar-hover` | `#E0EBFA` |  | `#2A3957` |  |
| `sidebar-active` | `#2457A6` |  | `#7FA8E8` |  |

`--shadow-color` is Night Shift in both themes (CSS only; shadows are off by default, see E).

## B. Interaction states

- **Hover and active** are two small steps of the same fill: darker for Blueprint in light mode and for the
  green and Sky fills, lighter for Hard Hat, Brick and the dark-mode blue. Every label still passes 4.5:1 on
  every state; the script checks all three.
- **Focus** is a 2 px outline, offset 3 px: Blueprint on light, Hard Hat on dark. Both clear 3:1 against
  `bg` and `panel`.
- **Disabled** controls use `muted` text on `surface`, and never rely on opacity alone.

## C. Status pills

Every status is a word (or an icon with a label) on a soft fill, never colour alone.

| Status | Fill | Text |
|---|---|---|
| Success | `success-soft` | `success-ink` |
| Warning | `warn-soft` | `warn-ink` |
| Info | `info-soft` | `info-ink` |
| Danger | `danger` | `on-danger` |
| Brand / selected | `accent-soft` | `accent-ink` |

## D. Typography

| Role | Face | Size / line |
|---|---|---|
| Display | Gilroy Semibold | 72 / 76 |
| Heading | Gilroy Semibold | 48 / 52 |
| Subheading | Gilroy Semibold | 32 / 38 |
| Body | Gilroy Regular | 16 / 24 |
| Label | Gilroy Semibold | 14 / 20 |
| Accent | Unbounded Semibold | 48 / 56, one short phrase per layout |

Headings use letter-spacing −0.025em. The wordmark is Gilroy Bold, lowercase, and only ever appears as logo
artwork.

## E. Shape, borders, shadow, spacing, motion

| Element | Rule |
|---|---|
| Controls | 10 px radius |
| Cards and windows | 16 px radius |
| Tags and pills | Fully round |
| Hairlines | `line`, or Night Shift at 18 % on brand fills |
| Shadows | None |
| Motion | Short and functional; respect `prefers-reduced-motion` |

## F. Logo in product

- **Header:** `logo/lockup-horizontal` on light, `lockup-horizontal-reversed` on dark.
- **Favicon and app icon:** `icons/`, the builder ≈ 66 % of a Paper square (app tile: ≈ 62 % with a 22 %
  corner radius).
- **Empty states and errors:** the builder alone (`mascot/`), `mascot/dark/` on dark surfaces.
- The artwork is raster (460 px source). Never show the builder taller than 280 px.

## G. Icons

24 px grid, 2 px stroke, rounded ends. Icons use `ink` or `muted`; never yellow or Brick for small icons that
carry meaning on Paper. Pair unfamiliar icons with labels.

## J. Open decisions

- What Nobody Builds makes, and for whom (copy on the introduction page and README).
- The builder's name.
- Whether to commission a vector or higher-resolution version of the builder.
