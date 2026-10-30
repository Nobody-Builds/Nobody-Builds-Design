// Copies the design kit from the repository root into the site before every dev or build run,
// so the site always shows the real masters and never a hand-maintained copy of them.
//
//   logo/ icons/ fonts/ tokens/ mascot/ screenshots/  ->  public/kit/...  (served for preview and download)
//   brand/logo-masters.png, brand/guidelines/png/      ->  public/kit/brand/  (guidelines only once they exist)
//   logo/*.svg, tokens/tokens.json                     ->  src/assets/kit/   (header logo, hero art, colours)
//   docs/*.md                                          ->  src/content/docs/specs/  (rendered spec pages)
//
// Every destination is generated and git-ignored. Edit the sources at the repository root.
import { cpSync, existsSync, mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const site = join(dirname(fileURLToPath(import.meta.url)), '..');
const root = join(site, '..');
const kit = join(site, 'public', 'kit');
const assets = join(site, 'src', 'assets', 'kit');
const specs = join(site, 'src', 'content', 'docs', 'specs');
const repo = 'https://github.com/Nobody-Builds/Nobody-Builds-Design';

for (const dir of [kit, assets, specs]) {
  rmSync(dir, { recursive: true, force: true });
  mkdirSync(dir, { recursive: true });
}

for (const folder of ['logo', 'icons', 'fonts', 'tokens', 'mascot', 'screenshots']) {
  cpSync(join(root, folder), join(kit, folder), { recursive: true });
}
cpSync(join(root, 'brand', 'logo-masters.png'), join(kit, 'brand', 'logo-masters.png'));
// The brand guidelines pages and PDF don't exist yet; pick them up automatically once they're added.
if (existsSync(join(root, 'brand', 'guidelines', 'png'))) {
  cpSync(join(root, 'brand', 'guidelines', 'png'), join(kit, 'brand', 'guidelines'), { recursive: true });
}
for (const file of readdirSync(join(root, 'brand')).filter((f) => f.endsWith('.pdf'))) {
  cpSync(join(root, 'brand', file), join(kit, 'brand', file));
}

for (const file of readdirSync(join(root, 'logo')).filter((f) => f.endsWith('.svg'))) {
  cpSync(join(root, 'logo', file), join(assets, file));
}
cpSync(join(root, 'tokens', 'tokens.json'), join(assets, 'tokens.json'));

// Spec pages: the first "# Heading" becomes the page title; the rest is published unchanged.
const specPages = [
  { file: 'ui-brand-spec.md', slug: 'ui-brand-spec', order: 1, label: 'UI brand spec' },
  { file: 'ux-spec.md', slug: 'ux-patterns', order: 2, label: 'Nobody Builds UX spec' },
  { file: 'ux-screens-longtail.md', slug: 'ux-long-tail-screens', order: 3, label: 'Long-tail screens' },
];
for (const { file, slug, order, label } of specPages) {
  const source = readFileSync(join(root, 'docs', file), 'utf8').replace(/^﻿/, '');
  const match = source.match(/^#\s+(.+)\r?\n/);
  if (!match) throw new Error(`docs/${file} must start with a "# Title" line`);
  const title = match[1].trim().replace(/"/g, '\\"');
  const frontmatter = [
    '---',
    `title: "${title}"`,
    `sidebar: { order: ${order}, label: "${label}" }`,
    `editUrl: ${repo}/edit/main/docs/${file}`,
    '---',
    '',
    `:::note[Source]\nThis page is published from [\`docs/${file}\`](${repo}/blob/main/docs/${file}). Edit it there.\n:::`,
    '',
  ].join('\n');
  writeFileSync(join(specs, `${slug}.md`), frontmatter + source.slice(match[0].length));
}

console.log('sync-kit: copied logo, icons, fonts, tokens, mascot, screenshots, logo masters and 3 specs');
