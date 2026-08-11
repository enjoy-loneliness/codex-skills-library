---
name: uniapp-project-builder
description: Initialize Vue 3 uni-app projects for H5 websites, WeChat mini programs, or multi-platform apps. Use when the user says 用 uniapp 开发网站, 开发小程序, 微信小程序, H5, 多端开发, 跨端开发, or asks Codex to scaffold/init a uni-app project with folders, pages.json, manifest.json, Vite config, Pinia, request utilities, and base directories.
---

# UniApp Project Builder

## Default Workflow

1. Infer the target from the user's words:
   - `web`: 网站, H5, 网页, web.
   - `miniapp`: 小程序, 微信小程序, mp-weixin.
   - `multi`: 多端, 跨端, 同时支持网站/小程序/App.
2. Always generate a Vue 3 + Vite uni-app CLI project. Do not create Vue 2 or legacy HBuilderX-only structure.
3. Prefer the bundled script:

```bash
python3 <skill-dir>/scripts/create_uniapp_project.py <target-dir> --type miniapp --name my-project
```

Use `--type web` for H5 websites and `--type multi` for cross-platform projects. Add `--title`,
`--appid`, `--mp-weixin-appid`, `--port`, or `--no-uview` only when useful.

`--force` is destructive. Use it only after showing the user the resolved target and confirming that
it is the intended existing generated project. By default, replacement is limited to the current
working directory. When the target lives elsewhere, pass its narrow parent explicitly with
`--creation-parent <parent-dir>`. The script refuses filesystem/home/workspace or Git repository
roots, targets outside that parent, and non-empty directories that do not contain `package.json`,
`manifest.json`, and `pages.json`.

## What The Script Generates

- `package.json` with Vue 3, Vite, `@dcloudio/vite-plugin-uni`, Pinia, persisted state, Sass, and target-specific uni-app runtime packages.
- Core files: `App.vue`, `main.js`, `manifest.json`, `pages.json`, `vite.config.js`, `index.html`, `uni.scss`, `.gitignore`, `jsconfig.json`, `.env.development`, `.env.production`.
- Shared folders: `api/`, `components/`, `hooks/`, `pages/`, `static/`, `store/modules/`, `utils/`.
- `miniapp` and `multi` additionally include role/subpackage style folders inspired by the current `pet_shop_uniapp` project: `pages_user/`, `pages_merchant/`, and `pages_common/`.
- `web` keeps the folder set lean and excludes mini-program-only subpackages and permissions.

## After Generation

Run a local sanity check before handing off:

```bash
python3 -m json.tool <target-dir>/package.json >/dev/null
python3 -m json.tool <target-dir>/pages.json >/dev/null
python3 -m json.tool <target-dir>/manifest.json >/dev/null
```

If dependencies are already installed or the user asks you to run it, use the generated scripts:

```bash
npm install
npm run dev:h5
npm run dev:mp-weixin
```

Only run target scripts that exist in the generated `package.json`.

## Customization Rules

- Keep `manifest.json` with `"vueVersion": "3"`.
- Keep `main.js` using `createSSRApp`, Pinia from `./store`, and optional `uview-plus`.
- Keep request code based on `uni.request` so it works across H5, mini programs, and App.
- Add WeChat private info declarations only when the requested feature needs them, such as location or camera.
- For web projects, avoid mini-program-only folders, subpackages, custom tab bars, privacy permissions, and platform-specific APIs unless the user explicitly asks.
- For multi-platform projects, use conditional compilation comments (`#ifdef H5`, `#ifdef MP-WEIXIN`, `#ifdef APP-PLUS`) around platform-specific code.

Read `references/project-variants.md` before changing the default directory layout or platform assumptions.
