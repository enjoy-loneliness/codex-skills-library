#!/usr/bin/env python3
"""Create a Vue 3 uni-app project starter for H5, mini program, or multi-platform work."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path


UVIEW_VERSION = "^3.6.29"


def normalize_package_name(value: str) -> str:
    name = value.strip().lower()
    name = re.sub(r"[^a-z0-9._-]+", "-", name)
    name = re.sub(r"-+", "-", name).strip("-._")
    return name or "uniapp-project"


def pascal_title(value: str) -> str:
    words = re.split(r"[-_\s]+", value.strip())
    return "".join(word[:1].upper() + word[1:] for word in words if word) or "UniApp"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def ensure_empty_or_force(target: Path, force: bool, creation_parent: Path | None = None) -> None:
    if target.exists() and any(target.iterdir()):
        if not force:
            raise SystemExit(
                f"Target directory is not empty: {target}\n"
                "Use --force to replace it, or choose an empty directory."
            )

        resolved_home = Path.home().resolve()
        resolved_cwd = Path.cwd().resolve()
        resolved_creation_parent = (creation_parent or resolved_cwd).resolve()
        forbidden_targets = {Path(target.anchor).resolve(), resolved_home, resolved_cwd}
        if target in forbidden_targets or target in resolved_cwd.parents:
            raise SystemExit(f"Refusing to replace a broad or protected directory: {target}")

        forbidden_creation_parents = {Path(target.anchor).resolve(), resolved_home}
        if resolved_creation_parent in forbidden_creation_parents:
            raise SystemExit(
                f"Refusing to use a broad or protected creation parent: {resolved_creation_parent}"
            )
        if not target.is_relative_to(resolved_creation_parent):
            raise SystemExit(
                f"Refusing to replace a target outside the creation parent: {target}\n"
                f"Creation parent: {resolved_creation_parent}"
            )
        if (target / ".git").exists():
            raise SystemExit(f"Refusing to replace a Git repository root: {target}")

        project_markers = (
            target / "package.json",
            target / "manifest.json",
            target / "pages.json",
        )
        if not all(marker.is_file() for marker in project_markers):
            raise SystemExit(
                f"Refusing to replace an unmarked directory: {target}\n"
                "Expected package.json, manifest.json, and pages.json from an existing starter."
            )
        print(f"Replacing existing generated project at {target}")
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)


def package_json(project_name: str, variant: str, with_uview: bool) -> dict:
    scripts: dict[str, str] = {}
    dependencies: dict[str, str] = {
        "@dcloudio/uni-app": "latest",
        "@dcloudio/uni-components": "latest",
        "pinia": "latest",
        "pinia-plugin-persistedstate": "latest",
        "vue": "latest",
    }
    dev_dependencies: dict[str, str] = {
        "@dcloudio/vite-plugin-uni": "latest",
        "sass": "latest",
        "vite": "latest",
    }

    if with_uview:
        dependencies["uview-plus"] = UVIEW_VERSION

    if variant in {"web", "multi"}:
        scripts.update(
            {
                "dev:h5": "uni",
                "build:h5": "uni build",
                "preview:h5": "vite preview --host 127.0.0.1",
            }
        )
        dependencies["@dcloudio/uni-h5"] = "latest"

    if variant in {"miniapp", "multi"}:
        scripts.update(
            {
                "dev:mp-weixin": "uni -p mp-weixin",
                "build:mp-weixin": "uni build -p mp-weixin",
            }
        )
        dependencies["@dcloudio/uni-mp-weixin"] = "latest"

    if variant == "multi":
        scripts.update(
            {
                "dev:app": "uni -p app",
                "build:app": "uni build -p app",
            }
        )
        dependencies["@dcloudio/uni-app-plus"] = "latest"

    if not scripts:
        scripts["dev:h5"] = "uni"

    return {
        "name": project_name,
        "version": "1.0.0",
        "private": True,
        "type": "module",
        "scripts": scripts,
        "dependencies": dict(sorted(dependencies.items())),
        "devDependencies": dict(sorted(dev_dependencies.items())),
    }


def manifest_json(args: argparse.Namespace, project_name: str) -> dict:
    data: dict = {
        "name": project_name,
        "appid": args.appid,
        "description": "",
        "versionName": "1.0.0",
        "versionCode": "100",
        "transformPx": False,
        "vueVersion": "3",
        "uniStatistics": {"enable": False},
    }

    if args.type in {"web", "multi"}:
        data["h5"] = {
            "title": args.title,
            "router": {"mode": "hash"},
            "devServer": {"port": args.port},
        }

    if args.type in {"miniapp", "multi"}:
        data["mp-weixin"] = {
            "appid": args.mp_weixin_appid,
            "setting": {"urlCheck": False},
            "usingComponents": True,
        }

    if args.type == "multi":
        data["app-plus"] = {
            "usingComponents": True,
            "nvueStyleCompiler": "uni-app",
            "compilerVersion": 3,
            "splashscreen": {
                "alwaysShowBeforeRender": True,
                "waiting": True,
                "autoclose": True,
                "delay": 0,
            },
            "modules": {},
            "distribute": {
                "android": {"permissions": []},
                "ios": {},
                "sdkConfigs": {},
            },
        }

    return data


def pages_json(variant: str, with_uview: bool) -> dict:
    if variant == "web":
        data: dict = {
            "pages": [
                {
                    "path": "pages/index/index",
                    "style": {"navigationBarTitleText": "首页"},
                },
                {
                    "path": "pages/about/index",
                    "style": {"navigationBarTitleText": "关于"},
                },
            ],
            "globalStyle": {
                "navigationBarTextStyle": "black",
                "navigationBarTitleText": "uni-app",
                "navigationBarBackgroundColor": "#FFFFFF",
                "backgroundColor": "#F7F8FA",
            },
            "uniIdRouter": {},
        }
    else:
        data = {
            "pages": [
                {
                    "path": "pages/launch/index",
                    "style": {
                        "navigationStyle": "custom",
                        "navigationBarTitleText": "",
                    },
                },
                {
                    "path": "pages/login/index",
                    "style": {
                        "navigationStyle": "custom",
                        "navigationBarTitleText": "登录",
                    },
                },
                {
                    "path": "pages/index/index",
                    "style": {
                        "navigationStyle": "custom",
                        "navigationBarTitleText": "首页",
                    },
                },
                {
                    "path": "pages/mine/index",
                    "style": {
                        "navigationStyle": "custom",
                        "navigationBarTitleText": "我的",
                        "enablePullDownRefresh": False,
                    },
                },
            ],
            "subPackages": [
                {
                    "root": "pages_user",
                    "pages": [
                        {
                            "path": "profile/index",
                            "style": {"navigationBarTitleText": "用户中心"},
                        }
                    ],
                },
                {
                    "root": "pages_merchant",
                    "pages": [
                        {
                            "path": "dashboard/index",
                            "style": {"navigationBarTitleText": "商家工作台"},
                        }
                    ],
                },
                {
                    "root": "pages_common",
                    "pages": [
                        {
                            "path": "settings/index",
                            "style": {"navigationBarTitleText": "设置"},
                        }
                    ],
                },
            ],
            "globalStyle": {
                "navigationBarTextStyle": "black",
                "navigationBarTitleText": "uni-app",
                "navigationBarBackgroundColor": "#F8F8F8",
                "backgroundColor": "#F8F8F8",
            },
            "tabBar": {
                "color": "#7A7E83",
                "selectedColor": "#FFB820",
                "borderStyle": "black",
                "backgroundColor": "#FFFFFF",
                "list": [
                    {"pagePath": "pages/index/index", "text": "首页"},
                    {"pagePath": "pages/mine/index", "text": "我的"},
                ],
            },
            "uniIdRouter": {},
        }

    data["easycom"] = {"autoscan": True}

    if with_uview:
        data["easycom"]["custom"] = {
            "^up-(.*)": "uview-plus/components/u-$1/u-$1.vue",
            "^u-(.*)": "uview-plus/components/u-$1/u-$1.vue",
        }

    return data


def app_vue() -> str:
    return """<script setup>
import { onHide, onLaunch, onShow } from '@dcloudio/uni-app';
import { useAppStore } from '@/store/modules/app';

const appStore = useAppStore();

onLaunch(() => {
  appStore.bootstrap();
});

onShow(() => {
  console.log('App Show');
});

onHide(() => {
  console.log('App Hide');
});
</script>

<style lang="scss">
page {
  min-height: 100%;
  background-color: #f7f8fa;
  color: #1f2933;
  font-family:
    -apple-system,
    BlinkMacSystemFont,
    'Helvetica Neue',
    Helvetica,
    Segoe UI,
    Arial,
    Roboto,
    'PingFang SC',
    'Hiragino Sans GB',
    'Microsoft Yahei',
    sans-serif;
  font-size: 28rpx;
  line-height: 1.5;
}

image {
  display: block;
  will-change: transform;
}

.text-primary {
  color: $brand-primary;
}

.bg-primary {
  background-color: $brand-primary;
}

.u-line-1 {
  display: block;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  word-break: break-all;
}

.u-line-2 {
  display: -webkit-box;
  overflow: hidden;
  text-overflow: ellipsis;
  word-break: break-all;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

.safe-bottom-space {
  height: calc(120rpx + env(safe-area-inset-bottom));
  width: 100%;
  flex-shrink: 0;
}
</style>
"""


def main_js(with_uview: bool) -> str:
    imports = [
        "import { createSSRApp } from 'vue';",
        "import App from './App.vue';",
        "import pinia from './store';",
    ]
    setup = ["  app.use(pinia);"]

    if with_uview:
        imports.extend(
            [
                "import uviewPlus from 'uview-plus';",
                "import 'uview-plus/index.scss';",
            ]
        )
        setup.append("  app.use(uviewPlus);")

    return (
        "\n".join(imports)
        + "\n\nexport function createApp() {\n"
        + "  const app = createSSRApp(App);\n"
        + "\n".join(setup)
        + "\n\n  return { app };\n"
        + "}\n"
    )


def vite_config(port: int) -> str:
    return f"""import uni from '@dcloudio/vite-plugin-uni';
import {{ defineConfig }} from 'vite';

export default defineConfig({{
  plugins: [uni()],
  css: {{
    preprocessorOptions: {{
      scss: {{
        silenceDeprecations: ['legacy-js-api', 'color-functions', 'import', 'mixed-decls'],
      }},
    }},
  }},
  server: {{
    host: '127.0.0.1',
    port: {port},
  }},
}});
"""


def index_html(title: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <script>
      var coverSupport =
        'CSS' in window &&
        typeof CSS.supports === 'function' &&
        (CSS.supports('top: env(a)') || CSS.supports('top: constant(a)'));
      document.write(
        '<meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0' +
          (coverSupport ? ', viewport-fit=cover' : '') +
          '" />'
      );
    </script>
    <title>{title}</title>
    <!--preload-links-->
    <!--app-context-->
  </head>
  <body>
    <div id="app"><!--app-html--></div>
    <script type="module" src="/main.js"></script>
  </body>
</html>
"""


def uni_scss(with_uview: bool) -> str:
    prefix = "@import 'uview-plus/theme.scss';\n\n" if with_uview else ""
    return prefix + """$brand-primary: #ffaa00;
$brand-primary-light: #fff1d4;
$brand-bg: #f7f8fa;

$uni-color-primary: $brand-primary;
$uni-color-success: #19be6b;
$uni-color-warning: #ff9900;
$uni-color-error: #fa3534;

$uni-text-color: #1f2933;
$uni-text-color-inverse: #ffffff;
$uni-text-color-grey: #909399;
$uni-text-color-placeholder: #c0c4cc;

$uni-bg-color: #ffffff;
$uni-bg-color-grey: $brand-bg;
$uni-bg-color-hover: #f1f1f1;
$uni-bg-color-mask: rgba(0, 0, 0, 0.4);

$uni-border-color: #ebeef5;

$uni-font-size-sm: 24rpx;
$uni-font-size-base: 28rpx;
$uni-font-size-lg: 32rpx;

$uni-border-radius-sm: 4rpx;
$uni-border-radius-base: 8rpx;
$uni-border-radius-lg: 16rpx;
$uni-border-radius-circle: 50%;

$uni-spacing-row-sm: 10rpx;
$uni-spacing-row-base: 20rpx;
$uni-spacing-row-lg: 30rpx;

$uni-spacing-col-sm: 8rpx;
$uni-spacing-col-base: 16rpx;
$uni-spacing-col-lg: 24rpx;
"""


def store_index_js() -> str:
    return """import { createPinia } from 'pinia';
import { createPersistedState } from 'pinia-plugin-persistedstate';

const pinia = createPinia();

pinia.use(
  createPersistedState({
    storage: {
      getItem(key) {
        return uni.getStorageSync(key);
      },
      setItem(key, value) {
        uni.setStorageSync(key, value);
      },
      removeItem(key) {
        uni.removeStorageSync(key);
      },
    },
  })
);

export default pinia;
"""


def app_store_js() -> str:
    return """import { defineStore } from 'pinia';

const TOKEN_KEY = 'UNIAPP_TOKEN';
const USER_KEY = 'UNIAPP_USER';

export const useAppStore = defineStore('app', {
  state: () => ({
    token: uni.getStorageSync(TOKEN_KEY) || '',
    userInfo: uni.getStorageSync(USER_KEY) || null,
    bootstrapped: false,
  }),

  getters: {
    isLogin: state => !!state.token,
  },

  actions: {
    bootstrap() {
      this.bootstrapped = true;
    },

    setToken(token) {
      this.token = token || '';
      if (this.token) {
        uni.setStorageSync(TOKEN_KEY, this.token);
      } else {
        uni.removeStorageSync(TOKEN_KEY);
      }
    },

    setUserInfo(userInfo) {
      this.userInfo = userInfo || null;
      if (this.userInfo) {
        uni.setStorageSync(USER_KEY, this.userInfo);
      } else {
        uni.removeStorageSync(USER_KEY);
      }
    },

    logout() {
      this.setToken('');
      this.setUserInfo(null);
      uni.reLaunch({ url: '/pages/login/index' });
    },
  },

  persist: true,
});
"""


def request_js() -> str:
    return """import { useAppStore } from '@/store/modules/app';

export const BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

const ERROR_CODE_MAP = {
  401: '登录已过期',
  403: '拒绝访问',
  404: '资源不存在',
  500: '服务器错误',
};

const buildQuery = params => {
  return Object.keys(params)
    .filter(key => params[key] !== undefined && params[key] !== null && params[key] !== '')
    .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
    .join('&');
};

const request = options => {
  const {
    url,
    method = 'GET',
    data = {},
    params = {},
    header = {},
    showLoading = false,
    showError = true,
    noAuth = false,
    fullRes = false,
  } = options;

  if (showLoading) {
    uni.showLoading({ title: '加载中...', mask: true });
  }

  const appStore = useAppStore();
  const upperMethod = method.toUpperCase();
  const finalParams = upperMethod === 'GET' ? { ...params, ...data } : params;
  const isAbsoluteUrl = /^https?:\\/\\//i.test(url);
  let queryUrl = isAbsoluteUrl ? url : `${BASE_URL}${url}`;
  const authHeader = {};
  if (!noAuth && !isAbsoluteUrl && appStore.token) {
    authHeader.Authorization = `Bearer ${appStore.token}`;
  }
  const queryString = buildQuery(finalParams);

  if (queryString) {
    queryUrl += (queryUrl.includes('?') ? '&' : '?') + queryString;
  }

  return new Promise((resolve, reject) => {
    uni.request({
      url: queryUrl,
      method: upperMethod,
      data: upperMethod === 'POST' || upperMethod === 'PUT' ? data : {},
      header: {
        'Content-Type': 'application/json',
        ...authHeader,
        ...header,
      },
      success: response => {
        if (showLoading) uni.hideLoading();

        const { statusCode, data: responseData } = response;
        if (statusCode !== 200) {
          const message = ERROR_CODE_MAP[statusCode] || `网络错误(${statusCode})`;
          if (showError) uni.showToast({ title: message, icon: 'none', duration: 2500 });
          reject(new Error(message));
          return;
        }

        const code = responseData?.code;
        if (code === undefined || code === 200 || code === '200') {
          resolve(fullRes ? responseData : responseData?.data ?? responseData);
          return;
        }

        if (code === 401 || code === '401') {
          appStore.logout();
        }

        const message = responseData?.msg || responseData?.message || '操作失败';
        if (showError) uni.showToast({ title: message, icon: 'none', duration: 2500 });
        reject(new Error(message));
      },
      fail: () => {
        if (showLoading) uni.hideLoading();
        const message = '连接服务器失败';
        if (showError) uni.showToast({ title: message, icon: 'none', duration: 2500 });
        reject(new Error(message));
      },
    });
  });
};

export const http = {
  get: (url, data = {}, options = {}) => request({ url, method: 'GET', data, ...options }),
  post: (url, data = {}, options = {}) => request({ url, method: 'POST', data, ...options }),
  put: (url, data = {}, options = {}) => request({ url, method: 'PUT', data, ...options }),
  delete: (url, data = {}, options = {}) => request({ url, method: 'DELETE', data, ...options }),
};

export default http;
"""


def env_js() -> str:
    return """export const getPlatform = () => {
  // #ifdef H5
  return 'h5';
  // #endif

  // #ifdef MP-WEIXIN
  return 'mp-weixin';
  // #endif

  // #ifdef APP-PLUS
  return 'app-plus';
  // #endif

  return 'unknown';
};
"""


def api_common_js() -> str:
    return """import http from '@/utils/request';

export const getHealth = () => {
  return http.get('/health', {}, { noAuth: true });
};
"""


def hook_js() -> str:
    return """import { ref } from 'vue';

export const usePageLoading = (initialValue = false) => {
  const loading = ref(initialValue);

  const runWithLoading = async task => {
    loading.value = true;
    try {
      return await task();
    } finally {
      loading.value = false;
    }
  };

  return {
    loading,
    runWithLoading,
  };
};
"""


def layout_page_vue() -> str:
    return """<template>
  <view class="layout-page">
    <slot />
  </view>
</template>

<style scoped lang="scss">
.layout-page {
  min-height: 100vh;
  box-sizing: border-box;
  background: #f7f8fa;
}
</style>
"""


def empty_component_vue() -> str:
    return """<template>
  <view class="app-empty">
    <text class="app-empty__text">{{ text }}</text>
  </view>
</template>

<script setup>
defineProps({
  text: {
    type: String,
    default: '暂无数据',
  },
});
</script>

<style scoped lang="scss">
.app-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 240rpx;
  padding: 40rpx;
  color: #909399;
}

.app-empty__text {
  font-size: 28rpx;
}
</style>
"""


def home_page_vue(variant: str) -> str:
    subtitle = {
        "web": "H5 Website",
        "miniapp": "WeChat Mini Program",
        "multi": "Multi Platform",
    }[variant]
    return f"""<template>
  <layout-page>
    <view class="home">
      <view class="hero">
        <text class="eyebrow">{subtitle}</text>
        <text class="title">{{{{ appTitle }}}}</text>
        <text class="desc">Vue 3 uni-app starter</text>
      </view>

      <view class="panel">
        <view class="panel-row" @tap="goAbout">
          <text class="panel-title">基础页面</text>
          <text class="panel-arrow">›</text>
        </view>
      </view>
    </view>
  </layout-page>
</template>

<script setup>
import {{ ref }} from 'vue';

const appTitle = ref('首页');

const goAbout = () => {{
  const url = {about_url(variant)!r};
  uni.navigateTo({{ url }});
}};
</script>

<style scoped lang="scss">
.home {{
  padding: 64rpx 32rpx;
}}

.hero {{
  padding: 48rpx 0;
}}

.eyebrow {{
  display: block;
  color: $brand-primary;
  font-size: 24rpx;
  font-weight: 600;
}}

.title {{
  display: block;
  margin-top: 16rpx;
  color: #1f2933;
  font-size: 52rpx;
  font-weight: 700;
}}

.desc {{
  display: block;
  margin-top: 12rpx;
  color: #606266;
  font-size: 28rpx;
}}

.panel {{
  margin-top: 32rpx;
  overflow: hidden;
  border-radius: 16rpx;
  background: #ffffff;
}}

.panel-row {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 104rpx;
  padding: 0 28rpx;
}}

.panel-title {{
  color: #1f2933;
  font-size: 30rpx;
  font-weight: 600;
}}

.panel-arrow {{
  color: #c0c4cc;
  font-size: 44rpx;
}}
</style>
"""


def about_url(variant: str) -> str:
    if variant == "web":
        return "/pages/about/index"
    return "/pages_common/settings/index"


def simple_page_vue(title: str, body: str = "") -> str:
    body_text = body or title
    return f"""<template>
  <layout-page>
    <view class="page">
      <text class="title">{title}</text>
      <text class="body">{body_text}</text>
    </view>
  </layout-page>
</template>

<script setup>
</script>

<style scoped lang="scss">
.page {{
  min-height: 100vh;
  box-sizing: border-box;
  padding: 64rpx 32rpx;
}}

.title {{
  display: block;
  color: #1f2933;
  font-size: 40rpx;
  font-weight: 700;
}}

.body {{
  display: block;
  margin-top: 20rpx;
  color: #606266;
  font-size: 28rpx;
  line-height: 1.7;
}}
</style>
"""


def launch_page_vue() -> str:
    return """<template>
  <view class="launch">
    <text class="launch__title">正在启动</text>
  </view>
</template>

<script setup>
import { onLoad } from '@dcloudio/uni-app';

onLoad(() => {
  setTimeout(() => {
    uni.reLaunch({ url: '/pages/index/index' });
  }, 300);
});
</script>

<style scoped lang="scss">
.launch {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: #ffffff;
}

.launch__title {
  color: $brand-primary;
  font-size: 34rpx;
  font-weight: 700;
}
</style>
"""


def login_page_vue() -> str:
    return """<template>
  <layout-page>
    <view class="login">
      <text class="title">登录</text>
      <button class="login-button" type="primary" @tap="handleLogin">进入应用</button>
    </view>
  </layout-page>
</template>

<script setup>
import { useAppStore } from '@/store/modules/app';

const appStore = useAppStore();

const handleLogin = () => {
  appStore.setToken('demo-token');
  uni.reLaunch({ url: '/pages/index/index' });
};
</script>

<style scoped lang="scss">
.login {
  box-sizing: border-box;
  min-height: 100vh;
  padding: 160rpx 48rpx 48rpx;
}

.title {
  display: block;
  color: #1f2933;
  font-size: 52rpx;
  font-weight: 700;
}

.login-button {
  margin-top: 80rpx;
  background: $brand-primary;
}
</style>
"""


def gitignore() -> str:
    return """node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

dist/
.cache/
.temp/
unpackage/
*.log

project.private.config.json
miniprogram_npm/
wechat_devtools_*

.idea/
.vscode/
.DS_Store

.env.local
.env.development.local
.env.production.local
"""


def jsconfig_json() -> dict:
    return {
        "compilerOptions": {
            "baseUrl": ".",
            "paths": {
                "@/*": ["./*"],
            },
        },
        "exclude": ["node_modules", "dist", "unpackage"],
    }


def write_project(args: argparse.Namespace) -> None:
    target = args.target.resolve()
    ensure_empty_or_force(target, args.force, args.creation_parent)

    project_name = normalize_package_name(args.name or target.name)
    args.title = args.title or pascal_title(project_name)

    write_json(target / "package.json", package_json(project_name, args.type, not args.no_uview))
    write_json(target / "manifest.json", manifest_json(args, project_name))
    write_json(target / "pages.json", pages_json(args.type, not args.no_uview))
    write_json(target / "jsconfig.json", jsconfig_json())

    write_text(target / "App.vue", app_vue())
    write_text(target / "main.js", main_js(not args.no_uview))
    write_text(target / "vite.config.js", vite_config(args.port))
    write_text(target / "index.html", index_html(args.title))
    write_text(target / "uni.scss", uni_scss(not args.no_uview))
    write_text(target / ".gitignore", gitignore())
    write_text(target / ".env.development", "VITE_API_BASE_URL=")
    write_text(target / ".env.production", "VITE_API_BASE_URL=")

    write_text(target / "store/index.js", store_index_js())
    write_text(target / "store/modules/app.js", app_store_js())
    write_text(target / "utils/request.js", request_js())
    write_text(target / "utils/env.js", env_js())
    write_text(target / "api/common/index.js", api_common_js())
    write_text(target / "hooks/usePageLoading.js", hook_js())
    write_text(target / "components/layout-page/layout-page.vue", layout_page_vue())
    write_text(target / "components/app-empty/app-empty.vue", empty_component_vue())
    write_text(target / "static/.gitkeep", "")

    if args.type == "web":
        write_text(target / "pages/index/index.vue", home_page_vue(args.type))
        write_text(target / "pages/about/index.vue", simple_page_vue("关于", "H5 页面"))
    else:
        write_text(target / "pages/launch/index.vue", launch_page_vue())
        write_text(target / "pages/login/index.vue", login_page_vue())
        write_text(target / "pages/index/index.vue", home_page_vue(args.type))
        write_text(target / "pages/mine/index.vue", simple_page_vue("我的", "用户信息与偏好设置"))
        write_text(target / "pages_user/profile/index.vue", simple_page_vue("用户中心", "用户端分包页面"))
        write_text(target / "pages_merchant/dashboard/index.vue", simple_page_vue("商家工作台", "商家端分包页面"))
        write_text(target / "pages_common/settings/index.vue", simple_page_vue("设置", "通用分包页面"))

    print(f"Created Vue 3 uni-app {args.type} project at {target}")
    print("Next steps:")
    print(f"  cd {target}")
    print("  npm install")
    if args.type in {"web", "multi"}:
        print("  npm run dev:h5")
    if args.type in {"miniapp", "multi"}:
        print("  npm run dev:mp-weixin")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="Directory to create the project in.")
    parser.add_argument(
        "--type",
        choices=["web", "miniapp", "multi"],
        required=True,
        help="Project target: web/H5, WeChat mini program, or multi-platform.",
    )
    parser.add_argument("--name", help="Package/project name. Defaults to target directory name.")
    parser.add_argument("--title", help="Display title. Defaults to a title-cased project name.")
    parser.add_argument("--appid", default="__UNI__0000000", help="uni-app appid placeholder.")
    parser.add_argument("--mp-weixin-appid", default="", help="WeChat mini program appid.")
    parser.add_argument("--port", type=int, default=5100, help="H5 dev server port.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace a non-empty target only when it contains existing uni-app starter markers.",
    )
    parser.add_argument(
        "--creation-parent",
        type=Path,
        default=Path.cwd(),
        help="Parent boundary for --force replacement. Defaults to the current working directory.",
    )
    parser.add_argument("--no-uview", action="store_true", help="Do not include uview-plus.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    write_project(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
