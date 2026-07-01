---
name: tvbox-automation
description: "Use when working on Fang Xing's TVBox/影视仓 automation: n8n tvbox_sources ingestion, source health backfill, GitHub Actions update.js, Cloudflare KV FINAL_CONFIG/MULTI_CONFIG, local resource JSON files, or TVBox multi-source usability."
---

# TVBox Automation

## Project Map

- Repo: `<local-tvbox-auto-updater-repo>`
- GitHub repo: `<github-owner>/<tvbox-auto-updater-repo>`
- Main script: `update.js`
- Action: `.github/workflows/update.yml`
- Worker example: `cloudflare-worker.js`
- Local resource export often lives at `<local-resource-json-path>`

## n8n Map

- Data table: `tvbox_sources`
- Table ID: `<tvbox_sources_table_id>`
- Project ID: `<n8n_project_id>`
- Columns: `url`, `source_type`, `status`, `unavailable_reason`, `last_checked_at`
- TG ingestion workflow: `<telegram_ingestion_workflow_name>`, ID `<telegram_ingestion_workflow_id>`
- Maintenance workflow: `<maintenance_workflow_name>`, ID `<maintenance_workflow_id>`

Do not hardcode webhook auth tokens in code or skill text. Check GitHub Secrets or n8n workflow config when needed.

## Core Behavior

- `https://worker-domain/` returns Cloudflare KV key `FINAL_CONFIG`.
- `https://worker-domain/multi` returns KV key `MULTI_CONFIG`.
- Optional generated per-source configs use KV keys like `SOURCE_CONFIG_<hash>`.
- `N8N_ALL_SOURCES_URL` should return all `tvbox_sources` rows, including disabled rows.
- `N8N_HEALTH_UPDATE_URL` receives `{ updates: [...] }` and updates health fields by `id`.
- The TG workflow only extracts URLs from Telegram `text` and `caption`; it does not parse uploaded JSON files.

## Resource JSON Rule

If the user has a local `资源.json` with top-level `sites`, do not paste/upload the file into TG and expect ingestion. Convert or host it as a public URL, then add that URL to `tvbox_sources`.

Preferred public n8n-hosted URL for a private repo setup:

```text
https://<your-n8n-host>/webhook/<tvbox-curated-resources-public>
```

If the GitHub repo is public, the repo-hosted raw URL can also work:

```text
https://raw.githubusercontent.com/<github-owner>/<tvbox-auto-updater-repo>/main/configs/resources.json
```

For exported resource lists:

- Keep ordinary TVBox fields: `key`, `name`, `type`, `api`.
- Respect `isActive` when present: only `true`, `1`, or `"1"` should remain.
- Exclude bad tags by default: `差`, `无法搜索`, `搜索混乱`.
- Keep at least `MIN_SOURCE_SITES` usable sites, default `5`.

## Edit Workflow

1. Start with `git status -sb` and read the relevant part of `update.js`.
2. Preserve the Worker routing model unless the user explicitly wants Cloudflare changes.
3. For source parsing changes, keep behavior compatible with normal TVBox configs that do not have `isActive`.
4. Validate with `node --check update.js`.
5. Validate JSON files with `JSON.parse`.
6. If using n8n tools, prefer table/workflow IDs above instead of rediscovering them.
7. If pushing, commit narrowly and push `main`.

## Common Checks

Useful commands:

```bash
git status -sb
node --check update.js
node -e "const fs=require('fs'); const d=JSON.parse(fs.readFileSync('configs/resources.json','utf8')); console.log(d.name, d.sites.length)"
```

Expected healthy maintenance chain:

1. Action reads `N8N_ALL_SOURCES_URL`.
2. Script validates source URLs and creates health results.
3. Script POSTs health results to `N8N_HEALTH_UPDATE_URL`.
4. Script writes generated source configs, `FINAL_CONFIG`, and `MULTI_CONFIG` to Cloudflare KV.
