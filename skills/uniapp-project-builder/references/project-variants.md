# Project Variants

This skill is based on the structure observed in `pet_shop_uniapp`, but it turns the business-heavy pet shop codebase into a reusable Vue 3 uni-app starter.

## Shared Base

All variants use:

- Vue 3 Composition API with `createSSRApp`.
- Vite and `@dcloudio/vite-plugin-uni`.
- Pinia plus `pinia-plugin-persistedstate` with uni storage.
- `uni.request` wrappers in `utils/request.js`.
- `uview-plus` by default because the source project uses it heavily; pass `--no-uview` if a very small starter is requested.
- Directory aliases through `@` and `jsconfig.json`.

## Mini Program

Use for 小程序, 微信小程序, mp-weixin. Generate:

- `pages/launch`, `pages/login`, `pages/index`, `pages/mine`.
- `pages_user`, `pages_merchant`, and `pages_common` as subpackage roots.
- `manifest.json` with `mp-weixin` only by default.
- `pages.json` with `subPackages` and `easycom`.

Do not add sensitive permissions from the pet shop project by default. Add `permission` and `requiredPrivateInfos` only when the user's requested feature needs location, camera, Bluetooth, etc.

## Web / H5

Use for 网站, H5, 网页. Generate:

- Only base folders and `pages/index`, `pages/about`.
- `manifest.json` with `h5` config.
- No `pages_user`, `pages_merchant`, `pages_common`, mini-program permissions, custom tabbar, or subpackages.

## Multi Platform

Use for 多端 or 跨端. Generate the mini-program style directory layout plus:

- `h5`, `mp-weixin`, and `app-plus` sections in `manifest.json`.
- Scripts for H5, WeChat mini program, and App builds.
- Pages that avoid platform-specific APIs unless guarded with conditional compilation.

When a user does not name exact targets, treat "multi" as H5 + WeChat mini program + App.
