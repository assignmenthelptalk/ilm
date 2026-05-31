// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

const CORE_T1 = new Set([
  'ilm-assignment-help',
  'ilm-level-3-assignment-help',
  'ilm-level-5-assignment-help',
  'ilm-level-7-assignment-help',
  'ilm-coaching-and-mentoring-assignment-help',
]);

const CORE_T2_PROCESS = new Set([
  'ilm-reflective-account-writing-help',
  'ilm-work-based-evidence-guide',
  'ilm-assignment-referral-and-resubmission-guide',
  'ilm-assignment-harvard-referencing-guide',
  'leadership-styles-and-theories-for-ilm-assignments',
]);

const CORE_T2_SPECIALIST = new Set([
  'ilm-level-5-leadership-unit-assignment-help',
  'ilm-level-5-management-unit-assignment-help',
  'ilm-level-7-strategic-leadership-assignment-help',
  'ilm-level-3-team-leader-assignment-help',
  'ilm-level-4-assignment-help',
]);

function getSlug(url) {
  return url.replace(/^https?:\/\/[^/]+\//, '').replace(/\/$/, '');
}

export default defineConfig({
  site: 'https://www.ilmassignment.help',
  integrations: [
    sitemap({
      serialize(item) {
        const slug = getSlug(item.url);

        if (slug === '') {
          item.priority = 1.0;
          item.changefreq = 'weekly';
        } else if (CORE_T1.has(slug)) {
          item.priority = 0.9;
          item.changefreq = 'weekly';
        } else if (CORE_T2_PROCESS.has(slug)) {
          item.priority = 0.8;
          item.changefreq = 'monthly';
        } else if (CORE_T2_SPECIALIST.has(slug)) {
          item.priority = 0.75;
          item.changefreq = 'monthly';
        } else {
          item.priority = 0.6;
          item.changefreq = 'monthly';
        }

        return item;
      },
    }),
  ],
});
