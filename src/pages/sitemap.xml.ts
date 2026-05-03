import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import type { APIRoute } from 'astro';

const BASE_URL = 'https://www.ilmassignment.help';

interface PageEntry {
  slug: string;
}

export const GET: APIRoute = () => {
  let slugs: string[] = [];
  try {
    const raw = readFileSync(resolve(process.cwd(), 'content.json'), 'utf-8');
    const data = JSON.parse(raw);
    slugs = (data.pages ?? []).map((p: PageEntry) => p.slug);
  } catch {
    // content.json unavailable — sitemap will only include homepage
  }

  const urls = [
    `<url><loc>${BASE_URL}/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>`,
    ...slugs.map(
      (slug) =>
        `<url><loc>${BASE_URL}/${slug}/</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>`
    ),
  ].join('\n  ');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  ${urls}
</urlset>`;

  return new Response(xml, {
    headers: { 'Content-Type': 'application/xml' },
  });
};
