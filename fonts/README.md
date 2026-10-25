# Font files

Brand typography: Gilroy Regular (400), Medium (500), Semibold (600), Bold (700), and Unbounded Medium/Semibold (500–600). The same files as the Space Works kit.

The four `Gilroy-*.woff` files are format conversions of the owner's installed TTF files, included at the owner's request. Glyph outlines, family metadata and character coverage were preserved. CSS assigns each face its intended weight. Their inclusion does not make the full Gilroy family an open-source font; use them under the applicable Gilroy license.

`Unbounded-Variable.woff2` is covered by `LICENSES/OFL-Unbounded.txt`.

Legacy `Gilroy-Light.woff2`, `Gilroy-ExtraBold.woff2` and `Outfit-Variable.woff2` are kept for consumers that already use them. `LICENSES/Gilroy-Free-Font-EULA.txt` applies to the original free Light/ExtraBold release, not the other weights. New surfaces use the roles in `tokens/tokens.css`.

`scripts/build-assets.py` reads these files directly (decoding WOFF/WOFF2 in memory with fontTools) to set the wordmark.
