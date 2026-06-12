# mgmt-app-h5-release 离线包与双端架构详解

本文基于 `mgmt-app-h5-release` 代码、相邻的 `ssc-fe-version-mgr-sdk-master` SDK 代码，以及 `mgmt` 目录下的离线包、APP 升级、多应用离线包、双端适配、PC FMS 异步加载等 PDF 梳理而成。

目标不是简单复述方案，而是把“为什么要做、代码怎么做、APP 怎么识别、线上怎么发布、出了问题怎么兜底、双端应用怎么复用代码”串成一条完整链路。

## 1. 一句话总览

Management App 是一个 Hybrid APP：Native APP 内部打开 H5 页面。离线包方案把 H5 的 `html/js/css/image/i18n` 等静态资源预先打成 zip 包，让 APP 提前下载到本地，用户打开页面时优先读本地文件，弱网下也能更快展示。

这个项目后来又从“一个 APP 只有一个离线包应用 ID”演进到“一个 APP 下面有多个业务 app_id”，让不同业务可以独立发布、灰度、回滚，减少大包和跨业务互相影响的问题。

PC/H5 双端方案则是另一条主线：用一套业务页面和数据逻辑，同时适配移动端 WebView 和 PC Dashboard。共用逻辑放在 `applications` 和页面层，端侧差异放在 `isolate`，构建时通过 alias 选择 `index.h5` 或 `index.pc`。

## 2. 资料和代码对应关系

### 2.1 主要 PDF

- `Management App - 离线包方案设计.pdf`：早期 H5 离线包完整方案，覆盖构建、BFF、APP 存储升级、回滚、灰度。
- `多应用离线包方案.pdf`：从单 app_id 演进到 `biz_id -> 多 app_id` 的整体方案。
- `多应用离线包：SPX-mgmt的Order tracking业务拆分.pdf`：以 Order Tracking 为试点的业务拆分、路径兼容、发布与回滚策略。
- `切换到多应用离线包后的 APP 升级方案.pdf`：新旧 APP 与新旧离线包不兼容时的升级策略。
- `离线包灰度与即时版本更新方案.pdf`：从 device_id 灰度改为 user_id 灰度，并讨论即时更新机制。
- `mgmt APP 版本升级问题及优化方案.pdf`：减少强制弹窗重启、优化升级体验的方案比较。
- `PC和移动端适配技术方案.pdf`、`双端适配集成研发模式技术分析方案.pdf`：双端研发模式、分层、适配层、构建隔离。
- `Mgmt PC FMS 异步化加载技术方案调研.pdf`：PC Dashboard Module Federation 加载和按需加载分析。
- `离线包 SDK 技术方案.pdf`：抽象成 `@scfe-common/version-mgr` SDK 的方向。

### 2.2 当前代码里最重要的目录

```text
mgmt-app-h5-release/
  packages/main/              # SPX Management APP H5 主应用
  packages/order-tracking/    # Order Tracking 独立业务入口，当前也被 main 临时兼容打入
  packages/dashboard/         # SPX PC Dashboard，webpack + Module Federation
  packages/multi-end/         # SPX Dashboard 双端复用业务逻辑和适配层
  packages/wms-mgmt/          # WMS/SBS Management，H5/PC 双端，已接入 version-mgr SDK
  packages/common/            # jsBridge、i18n、request、tracking、layout 等公共能力
  vite/plugins/               # main 使用的本地 Vite 插件，包括 build-offline
  scripts/                    # 根构建、移动产物、上传、压缩等脚本
  deploy/                     # Space/DMS 部署配置

../ssc-fe-version-mgr-sdk-master/
  src/core/plugins/vite/      # SDK 版离线包构建、PC remoteEntry 版本管理插件
  src/core/version/           # 创建版本、获取版本、灰度选择、加载 remoteEntry
  src/core/node-scripts/      # DMS/Space 里创建版本并通知 Seatalk 的脚本
```

## 3. 先理解几个术语

### 3.1 离线包

离线包本质是静态资源 zip。APP 下载 zip、解压到本地，再拦截 WebView 内部资源请求，判断该请求是否可以映射到本地文件。如果能映射且校验通过，就读本地；如果不能，就走线上 CDN/ALB。

一个离线包版本通常包含：

```json
{
  "packages": [
    {
      "id": "vendor",
      "md5": "zip 文件 md5",
      "CDN": "https://.../vendor.zip"
    },
    {
      "id": "bundle",
      "md5": "zip 文件 md5",
      "CDN": "https://.../bundle.zip"
    }
  ]
}
```

zip 内还会有 `verify.json`，记录每个资源文件路径到 md5 的映射，供 APP 校验解压后的单文件是否完整。

### 3.2 `_offl_id`

`_offl_id` 是资源 URL 上的离线包分包标识，例如：

```text
/mgmt/assets/app-xxx.js?_offl_id=bundle
/mgmt/vendor/vendor_react-xxx.js?_offl_id=vendor
```

APP 看到 `_offl_id=bundle`，就知道这个资源应从当前应用版本的 `bundle.zip` 解压目录里找；看到 `_offl_id=vendor`，就从 `vendor.zip` 找。

### 3.3 `biz_id` 和 `app_id`

这是多应用离线包后的核心概念。

- `biz_id`：代表一个 Native APP 或一个大的业务容器，例如 `spx-mgmt-app`、`sbs-mgmt-app`。
- `app_id`：代表这个 APP 内的某个业务离线包，例如 `dashboard`、`tool`、`sbs-mgmt-h5-dashboard`。

早期模型：

```text
一个 APP = 一个 app_id = 一组 vendor/bundle
get_version?app_id=spx-mgmt-app
```

多应用模型：

```text
一个 APP/biz_id = 多个 app_id
get_version?biz_id=spx-mgmt-app

返回：
  dashboard -> vendor/bundle
  tools     -> vendor/bundle
  order-tracking -> vendor/bundle
```

资源 URL 需要同时告诉 APP “这是哪个业务应用的哪个包”：

```text
react-xxx.js?_app_id=dashboard&_offl_id=vendor
```

### 3.4 Version Service / BFF / Apollo

早期方案里 BFF 承担了 H5 和 APP 之间的版本数据传递：前端构建完离线包，把 manifest 交给 BFF 创建版本；APP 通过 BFF 拉取最新版本配置。

后续抽成了更通用的 Version Service，SDK 里接口路径是：

```text
/version/api/static/v2/info/create_app_version
/version/api/static/v2/info/create_pc_version
/version/api/static/v2/info/get_pc_version_config
/version/api/static/v3/openapi/get_app
```

Apollo 用来配置：

- 当前全量版本。
- 灰度版本。
- 灰度用户或区域。
- 离线包开关。
- 业务 app_id 与 biz_id 的绑定关系。

### 3.5 JSBridge

H5 与 Native 通讯通过 `@ssc-ui/jsbridge-sdk`，项目在 `packages/common/utils/js-bridge/index.ts` 里做了一层业务封装。

代码里会用到：

- `getAppInfo()`
- `getOfflineInfo(appId?)`
- `checkUpgradeInfo()`
- `updateOfflinePkg(...)`
- `syncBadges(...)`
- `navigate(...)`
- `setStatusBarColor(...)`
- `offlineResourceRefresh(...)`

其中离线包升级红点、主动更新、翻译资源刷新都依赖 JSBridge。

## 4. 项目整体结构

### 4.1 `main`：SPX APP H5 主应用

入口：

- `packages/main/index.tsx`
- `packages/main/src/App.tsx`
- `packages/main/build/vite.config.ts`

特点：

- Vite 4 + React 18。
- H5 WebView 运行，`BrowserRouter basename=/mgmt/main`。
- 构建时默认 `OFFLINE=1`，会产出离线包。
- 通过本地 `vite/plugins/build-offline` 插件打包离线资源。
- `cssInjectedByJsPlugin` 把 CSS 注入 JS，避免离线包样式加载问题。
- `multiHTML` 生成多个 HTML 入口，如 `index.html`、`login.html`、`jsapi.html`。
- 当前还临时把 `order-tracking` 的 HTML 入口映射进 main，以兼容拆分过程中的老路径。

### 4.2 `order-tracking`：试点拆分业务

入口：

- `packages/order-tracking/index.tsx`
- `packages/order-tracking/src/app.tsx`
- `packages/order-tracking/src/routes/index.tsx`

PDF 目标是把 Order Tracking 从 `main` 中拆出来，作为多应用离线包第一个试点，降低主包体积，并让该业务独立发布。

当前代码里可以看到它已有独立入口和路由，但 `packages/order-tracking/package.json` 在这个快照里没有 `serve/build` 脚本；同时 `main` 的 Vite 配置还把它的 HTML 入口映射进来：

```ts
multiHTML(__dirname, {
  'order-tracking': path.resolve(__dirname, '../../order-tracking/index.html'),
  'order-details': path.resolve(__dirname, '../../order-tracking/index.html'),
  'photo-details': path.resolve(__dirname, '../../order-tracking/index.html'),
  'parcel-photo-details': path.resolve(__dirname, '../../order-tracking/index.html'),
})
```

这与 PDF 中的迁移策略一致：先兼容老 `.html` 路径，避免 Apollo 路由一改就 404；等新版 APP 与新版离线包稳定后，再真正独立。

### 4.3 `dashboard`：SPX PC Dashboard

入口：

- `packages/dashboard/src/moduleEntries/pc-dashboard.tsx`
- `packages/dashboard/config/moduleFederationConfig.js`
- `packages/dashboard/config/webpack.config.js`

特点：

- React 17 + webpack 5 Module Federation。
- 暴露 `./module` 给 FMS 基座。
- `remoteEntry.react.js` 构建后会重命名成带 commit/tag 的文件，例如 `remoteEntry.react.v_xxxxx_tag.js`。
- `version-info.json` 记录 remote entry 文件名，用来创建 PC 版本。
- FMS 基座加载 remoteEntry 后拿到 routes，再注册到 PC 主框架。

### 4.4 `multi-end`：双端复用业务层

入口形态：

- `packages/multi-end/src/applications/*`
- `packages/multi-end/src/isolate/*`

设计核心：

- 页面和业务逻辑尽量共用。
- 端侧差异放在 `isolate`。
- 业务层只引用 `@applications/*` 或 `@adapter/*`。
- H5 构建时 `@adapter/*` 指向 `index.h5`。
- PC 构建时 `@adapter/*` 指向 `index.pc`。

例如：

```ts
// H5
@adapter/rules -> src/isolate/rules/index.h5

// PC
@adapter/rules -> src/isolate/rules/index.pc
```

### 4.5 `wms-mgmt`：WMS/SBS 双端应用

入口：

- H5：`packages/wms-mgmt/h5/index.tsx`
- PC：`packages/wms-mgmt/pc/index.tsx`
- H5 构建：`packages/wms-mgmt/build/vite.config.h5.ts`
- PC 构建：`packages/wms-mgmt/build/vite.config.pc.ts`

特点：

- 同一个包内有 PC/H5 两套入口。
- 使用自己的 `@wms-adapter/*` 隔离端侧差异。
- H5 离线包已接入 `@scfe-common/version-mgr` 的 `buildOfflinePlugin`。
- PC 灰度版本已接入 `versionMgrPlugins`。
- i18n 可以拆成独立静态资源包。

## 5. 离线包方案的核心目标

离线包最初要解决的是弱网性能问题。

Management APP 在东南亚等弱网环境下使用，如果每次打开 H5 都从网络下载 HTML、JS、CSS、图片、翻译文件，首屏会慢甚至失败。离线包把静态资源提前下载到 APP 本地，用户打开页面时减少网络依赖。

后来又出现新问题：

1. 包越来越大，下载成功率变差。
2. 业务越来越多，一个版本牵一发动全身。
3. 灰度和回滚只能按整个 APP 离线包做，业务之间相互阻塞。
4. 版本升级需要重启或强弹窗，影响操作体验。
5. 新旧 APP 与新旧离线包协议不兼容。
6. PC 与 H5 重复开发，交付成本高。

所以方案演进为：

```text
单应用离线包
  -> vendor/bundle 拆包
  -> 多 app_id 业务拆包
  -> SDK 化 version-mgr
  -> 独立静态资源包/i18n 包
  -> PC/H5 双端适配与 PC 版本灰度
```

## 6. 早期单应用离线包架构

早期架构里，一个 APP 只有一个离线包应用 ID。以前端 `main` 为例，构建后默认分两个包：

- `vendor.zip`：React、MobX、ECharts、UI 组件库等低频变化依赖。
- `bundle.zip`：业务 JS、HTML、图片、语言资源等高频变化内容。

资源请求上只需要 `_offl_id`：

```text
/mgmt/assets/index-xxx.js?_offl_id=bundle
/mgmt/vendor/vendor_react-xxx.js?_offl_id=vendor
```

APP 侧用一个版本号管理这组 `vendor/bundle`。

优点：

- 实现成本低。
- APP 请求映射简单。
- 一次版本配置就能覆盖全部 H5 资源。

缺点：

- 任意业务改动都要发布整个 APP 离线包。
- 灰度、回滚、下线粒度太粗。
- 包体积持续膨胀。
- 多团队并行发布互相干扰。

## 7. 多应用离线包架构

多应用方案引入 `biz_id` 与 `app_id`。

旧模型：

```text
spx-mgmt-app
  version 100
    vendor.zip
    bundle.zip
```

新模型：

```text
biz_id = spx-mgmt-app
  app_id = main
    version 100
      vendor.zip
      bundle.zip
  app_id = order-tracking
    version 23
      vendor.zip
      bundle.zip
  app_id = tools
    version 56
      vendor.zip
      bundle.zip
```

资源请求变成：

```text
xxx.js?_app_id=order-tracking&_offl_id=bundle
vendor_react.js?_app_id=order-tracking&_offl_id=vendor
```

APP 通过 `_app_id` 先定位业务应用，再通过 `_offl_id` 定位该业务应用下的分包。

多应用解决的问题：

- 业务独立部署：Order Tracking 发版不必牵动 main。
- 独立灰度：一个业务继续灰度，另一个业务可以全量。
- 独立回滚：灰度业务异常只回滚该 app_id。
- 降低单包体积：拆出去的业务不再进入主包。
- 多团队并行：减少发布窗口冲突。

## 8. 离线包构建流程

以下以 `packages/main` 和 `packages/wms-mgmt` 为主说明。

### 8.1 根命令如何分发构建

根 `package.json`：

```json
{
  "build": "node scripts/run.js build",
  "build:pc": "node scripts/run.js build dashboard",
  "build-wms": "node ./packages/wms-mgmt/build/run.js  --build --offline"
}
```

`scripts/run.js` 会：

1. 解析命令中的 app 名称，默认是 `main`。
2. 通过 `lerna --scope @mgmt-app/{pkg} run {script}` 执行子包脚本。
3. 子包 build 完成后执行 `scripts/mv.js`，把子包 dist 汇总到根 `dist`。

`main` 的 build 脚本：

```json
"build": "OFFLINE=1 vite build -c ./build/vite.config.ts"
```

也就是说生产构建默认打开离线包构建。

### 8.2 Vite 构建先做普通产物

Vite 先正常生成：

- HTML。
- 入口 JS。
- chunk JS。
- 图片、svg 等 asset。
- vendor chunk。

`splitVendorChunk()` 会把第三方库拆到 `vendor/` 目录下，例如：

```text
vendor/vendor_react-xxx-0621.js
vendor/vendor_mobx-xxx-0621.js
assets/index-xxx-0621.js
assets/logo-xxx-0621.svg
```

文件名中带日期标记，是为了排查线上资源未命中离线包时能快速定位构建批次。

### 8.3 `multiHTML` 处理多 HTML 入口

Vite 默认按入口路径输出 HTML，monorepo 多包场景容易生成深层目录。`vite/plugins/multi-html.ts` 做了两件事：

1. build 时把多个 HTML 都打到 dist 根目录。
2. dev server 时把 `/xxx.html` 请求映射回真实 HTML 文件。

`main` 配置了：

```ts
index: packages/main/html/index.html
login: packages/main/html/login.html
login_callback: packages/main/html/login_callback.html
jsapi: packages/main/html/jsapi.html
order-tracking: packages/order-tracking/index.html
...
```

这样线上可以访问多个 HTML，同时离线包也能为多个历史路径复制对应 HTML。

### 8.4 `buildOffline` 插件改写资源 URL

`vite/plugins/build-offline/index.ts` 是 `main` 当前使用的本地插件。

核心发生在 `generateBundle`：

1. 遍历 Vite 生成的所有文件。
2. 对 JS/HTML 内容做字符串替换：把引用到的文件名追加离线参数。
3. 根据文件路径判断属于 `vendor` 还是 `bundle`。
4. 按 APP 真实请求路径复制到离线包目录。
5. 记录每个文件的 md5 到 `verify.json`。

简化后逻辑类似：

```text
for each bundle file:
  pkgName = file startsWith "vendor/" ? "vendor" : "bundle"
  reqPath = assetsPublicPath + fileName

  if html:
    给 html 内资源加 ?_offl_id=...
    按 htmlOutDirs 复制成多个请求路径下的 html
  else if js:
    给 js 内引用的静态资源加 ?_offl_id=...
    复制到 dist/{pkgName}/{reqPath}
  else:
    复制到 dist/{pkgName}/{reqPath}

  verify[pkgName][reqPath] = md5(content)
```

### 8.5 HTML 为什么要复制到很多路径

离线包加载时，APP 是按 WebView 请求路径找本地文件的。

用户可能打开：

```text
https://spx.test.shopee.sg/mgmt/main
https://spx.test.shopee.sg/mgmt/main/operation
https://spx.test.shopee.sg/mgmt/main/operation/fm-hub
https://spx.test.shopee.sg/mgmt/login
```

这些路径本质上很多都应该返回同一个 SPA `index.html`。因此 `packages/main/build/offline-config.js` 的 `htmlOutDirs` 把 `index.html` 映射到大量业务路由路径下。

如果某个路由没有配置，APP 在本地离线包里找不到对应 HTML，就会 fallback 到线上资源。

这也是为什么“新增页面后要记得补离线包路径”：否则 H5 浏览器开发没问题，但 APP 离线包命中不了。

### 8.6 生成 `verify.json`

`vite/plugins/build-offline/verify.ts`：

```ts
verifyJSON[pkgName][sourceReqUrl] = md5(code)
```

最终每个包里都有：

```text
vendor/
  verify.json
  ...
bundle/
  verify.json
  ...
```

`verify.json` 的 key 是文件存储路径，不带 query 参数。也就是说：

```text
请求 URL:
/mgmt/assets/index.js?_offl_id=bundle

verify key:
/mgmt/assets/index.js
```

APP 解压后用它校验文件是否完整。

### 8.7 closeBundle 阶段打包 zip 和 manifest

`closeBundle` 做最终收尾：

1. 拉取 i18n 语言资源并写入离线包。
2. 输出每个包的 `verify.json`。
3. 把每个目录压成 zip。
4. 计算 zip md5。
5. 生成 `offline_manifest.json`。
6. 删除中间目录，只留下 zip 和 manifest。

结果大致是：

```text
dist/
  mgmtapph5/
    index.html
    assets/...
  mgmt_offline_171xxx/
    vendor.zip
    bundle.zip
    mgmtapph5/offline_manifest.json
```

manifest 内容类似：

```json
{
  "packages": [
    {
      "id": "vendor",
      "md5": "...",
      "CDN": "https://deo.shopeemobile.com/.../mgmt_offline_xxx/vendor.zip"
    },
    {
      "id": "bundle",
      "md5": "...",
      "CDN": "https://deo.shopeemobile.com/.../mgmt_offline_xxx/bundle.zip"
    }
  ]
}
```

### 8.8 CSS 为什么要注入 JS

`main` 和 `wms-mgmt` 都用了 `vite-plugin-css-injected-by-js`。

原因是离线包环境下，单独 CSS 文件的相对路径、加载顺序、WebView 缓存和跨域更容易出问题。把 CSS 注入 JS 后，APP 只要能加载 JS，样式也会随 JS 注入页面，减少离线场景样式丢失概率。

配置里注释也写明：离线包必须如此，否则样式加载有问题。

### 8.9 i18n 怎么进离线包

本地插件和 SDK 插件都会在 `closeBundle` 拉取语言 JSON。

`main` 的配置：

```ts
offlineLangConf: {
  reqPath: offlineI18nReqPath,
  resourceId: 1769,
  tspName: 'spx-mgmt',
  langs: ['en', 'ms-my', 'th', 'zh-Hant', 'id', 'vi', 'ph', 'pt-BR'],
}
```

`wms-mgmt` 的配置：

```ts
offlineLangConf: {
  reqPath: offlineI18nReqPath,
  resourceId: 1832,
  tspName: 'wmsmgmtapp',
  langs: ['en', 'ms-my', 'th', 'zh-Hant', 'id', 'vi', 'ph', 'es-MX', 'pt-BR', 'zh-CN'],
}
```

WMS 还支持 `enableIndependentStatic: true`，可以把 i18n 拆成独立静态资源包。

## 9. SDK 版离线包构建有什么增强

`ssc-fe-version-mgr-sdk-master/src/core/plugins/vite/vite-build-offline-packages.ts` 是抽象后的版本。

相比 `main` 的本地插件，SDK 增强点主要有：

### 9.1 默认写入 `_app_id`

SDK 如果传了 `appId`，默认资源参数是：

```ts
{
  _offl_id: getOfflinePackageName(filePath),
  _app_id: appId
}
```

这就是多应用离线包需要的资源标识。

### 9.2 记录构建环境信息

SDK 生成 manifest 时会附带 `envs`：

```json
{
  "packages": [...],
  "envs": [
    {
      "PFB_NAME": "...",
      "ENV": "...",
      "GIT_COMMIT": "...",
      "GIT_TAG": "...",
      "PIPELINE_URL": "..."
    }
  ]
}
```

后面创建版本时，如果部署阶段环境变量缺失，可以从 manifest 里恢复构建信息，Seatalk 通知也更完整。

### 9.3 独立静态资源包

WMS H5 配置：

```ts
buildOfflinePlugin({
  appId: 'sbs-mgmt-h5-dashboard',
  staticAppId: 'sbs-mgmt-h5-assets',
  enableIndependentStatic: true,
  staticPackageNames: ['i18n'],
})
```

这会生成：

```text
offline_manifest.json                     # 主业务 app_id 的包
static-manifest-sbs-mgmt-h5-assets.json   # 静态资源 app_id 的包
```

好处：

- i18n 这类稳定或可独立刷新的资源不跟业务 bundle 强绑定。
- 翻译更新可以走独立静态资源版本。
- APP 触发 `offlineResourceRefresh` 后，H5 重新加载翻译即可，不一定要刷新整个业务页面。

## 10. 创建离线包版本

构建只生成 zip 和 manifest，还不等于 APP 能用。还要把 manifest 写入版本服务。

### 10.1 旧版创建版本

`scripts/create-offline-version.js` 是旧脚本，但当前文件已标注“废弃”。旧逻辑大致是：

1. 读取 `offline_manifest.json`。
2. 请求 BFF `create_version`。
3. 传入 `app_id` 和 manifest。
4. 成功后 Seatalk 通知版本号和 Apollo 配置链接。

### 10.2 SDK 创建版本

WMS 使用：

```js
const { createVersionScript } = require('@scfe-common/version-mgr');
```

`packages/wms-mgmt/build/scripts/create-offline-version.js`：

```js
createVersionScript({
  versionFilePath: offlineManifestPath,
  appId: 'sbs-mgmt-h5-dashboard',
  bizId: 'sbs-mgmt-app',
  enableIndependentStatic: true,
})
```

SDK 逻辑在 `ssc-fe-version-mgr-sdk-master/src/core/node-scripts/create-version-dms-script.ts`：

1. 读取 manifest。
2. 删除 APP 不需要的 `envs` 字段。
3. 通过 `get_app?app_id=...&biz_id=...` 获取 access key。
4. 请求 `create_app_version` 或 `create_pc_version`。
5. 如果有独立静态资源包，再为 static app id 创建版本。
6. Seatalk 通知主版本号、配置链接、版本列表链接。

### 10.3 app_id 安全

多应用后，一个 app_id 不能被其他业务乱用。PDF 里提到 app_id 需要注册，创建阶段需要带 token 或签名。

SDK 当前实现是：

1. 用 `CREATE_OFFLINE_VERSION_SECRET` 生成 JWT。
2. 调 Version Service 的 `get_app` 获取 `access_key`。
3. 创建版本时在 header 带：

```text
X-Version-App-Id
X-Version-Biz-Id
X-Version-Access-Key
```

这样可以避免 A 业务拿 B 业务的 app_id 创建版本。

## 11. APP 运行时如何加载离线包

### 11.1 冷启动或定时拉取配置

APP 会通过 BFF/Version Service 获取离线包版本配置。

早期是：

```text
get_version?app_id=managementApp
```

多应用后是：

```text
get_version?biz_id=spx-mgmt-app
```

返回一个或多个 app_id 的版本信息，每个 app_id 下有 `vendor/bundle` 的 CDN 和 md5。

PDF 中强调：为了加载效率，APP 会优先使用本地缓存配置，再异步拉取最新配置和下载资源。因此离线包发布后不是所有用户立即生效。

### 11.2 APP 下载并校验 zip

APP 拿到版本后：

1. 判断本地是否已有该 app_id 的该版本。
2. 对每个 package 比较 zip md5。
3. 未下载或 md5 变化则下载 zip。
4. 下载后校验 zip md5。
5. 解压。
6. 用 zip 内 `verify.json` 校验单文件。
7. 校验成功后把版本置为可用。

### 11.3 WebView 请求资源时如何命中本地文件

H5 页面里资源 URL 已经带了标识：

```text
/mgmt/assets/index.js?_app_id=sbs-mgmt-h5-dashboard&_offl_id=bundle
```

APP 拦截请求：

1. 读取 `_app_id`，定位业务应用。
2. 读取 `_offl_id`，定位分包。
3. 去当前可用版本目录找同路径文件。
4. 校验文件存在且 md5 正确。
5. 返回本地文件内容。
6. 如果任一步失败，走线上 URL。

对于旧单应用方案，没有 `_app_id`，APP 用默认 app_id 处理。

### 11.4 HTML 为什么是核心

APP 首次打开的是 HTML。只要 HTML 命中本地，HTML 里的 JS/CSS/图片再通过 `_offl_id/_app_id` 继续命中本地。

如果 HTML 路由没有配置到 `htmlOutDirs`，APP 找不到本地 HTML，就会直接走线上；这会让“离线包覆盖率”下降。

### 11.5 跳转时为什么要保留离线参数

`packages/wms-mgmt/src/hooks/use-app-navigate.ts` 中：

```ts
const fixedParams = [env.debugTag, env.offlineTag, env.appId];
```

跳转时会把当前 URL 的固定参数追加到新 URL。

原因是：如果一个页面带着 `_offl_id/_app_id` 被 APP 离线识别，跳转到下一个 WebView 或新路径时丢了这些参数，APP 可能不知道该按哪个 app_id/package 去找资源，导致回落线上。

## 12. iOS 26 / 同域路径问题

代码里有两处明显注释：

`packages/main/build/config.js`：

```js
// 为了处理 ios26 的兼容性问题，需要将离线包的请求路径映射到新路径下
const newPackagePath = `${getDomainName()}/mgmt`;
```

`packages/wms-mgmt/build/scripts/build-config.js`：

```js
// 把cdn的package字段都打包到同域名的离线包目录下，
// 避免离线包js请求跨域导致IOS 26的storage访问受限问题
const useNewOfflinePackage = true;
const newPackagePath = `sbs-mgmt.ssc.${envPart}shopee.sg/${deployModuleName}`;
const newAssetsPublicPath = `/${deployModuleName}`;
```

含义是：离线包内保存的请求路径尽量与页面所在域名/路径保持一致，避免 WebView 或浏览器新策略把跨域资源当成不同 storage 上下文，导致 cookie/localStorage/sessionStorage 行为异常。

这也是为什么 `main` 的 Vite base 从 CDN 改成了 `/mgmt`，WMS H5 也支持 `newAssetsPublicPath`。

## 13. 灰度与即时更新

### 13.1 灰度从 device_id 改为 user_id

早期灰度按 device_id。问题是：

- 用户登录前才知道设备，但灰度往往想按人。
- device_id 与真实用户不强绑定。
- 指定目标用户灰度不准确。

新方案改成 BFF/Version Service 支持 device_id 与 user_id，优先用 user_id 灰度。

PC 版本管理 SDK 中 `getVersion` 也体现了类似思路：

1. 从配置取全量版本、灰度版本、内部灰度版本、区域名单、用户名单。
2. 对用户名做 SHA256。
3. 先判断内部灰度。
4. 再判断外部灰度。
5. 不命中灰度则用 live version。
6. 如果 live version 没配，使用 latest version。

### 13.2 为什么需要即时更新

PDF 中指出，旧离线包机制没有强制即时更新：用户可能要二次冷启动才应用新版本。如果下载未完成就退出，或者用户很久不重启，就可能长期停留在旧版本。

这带来两个问题：

- 新功能覆盖慢，紧急修复也覆盖慢。
- 后端接口不能轻易做不兼容改动，因为前端多版本长期并存。

### 13.3 即时更新方案取舍

PDF 对比了四类方式：

- WebSocket：实时性高，但连接、心跳、重连、资源消耗和维护成本高。
- SSE：实时性高，但同样需要维护长连接循环。
- 轮询：简单，但低频版本更新会产生大量无效请求。
- 特定场景检测：比如业务请求返回最新版本信息，实时性较弱但维护成本低。

最终倾向“特定场景检测 + APP 每 10 分钟定时检测兜底”。

代码当前体现的是弱提醒/红点逻辑：

- `packages/main/src/utils/feature-badge/config/version-upgrade.ts`
- `packages/wms-mgmt/src/utils/feature-badge/config/version-upgrade.ts`

它们调用：

```ts
jsBridge.checkUpgradeInfo()
```

如果返回有升级，就通过 `syncBadges` 同步底部 tab 红点给 Native。

### 13.4 主动更新

`packages/main/src/pages/jsapi/app.tsx` 测试页里可以看到：

```ts
jsBridge.updateOfflinePkg(999, '1')
jsBridge.getOfflineInfo()
```

这说明 Native 已提供主动更新离线包的 bridge 能力。PDF 中的目标流程是：

1. H5 检测到新版本。
2. H5 通过 JSAPI 提示或触发更新。
3. APP 下载并切换离线包。
4. APP 通知 H5 更新完成。
5. H5 清理/刷新当前 WebView，打开用户有权限的第一个 tab 或 reload 当前页。

当前业务代码更多是红点提醒，是否直接强制触发刷新需要产品和 Native 策略共同决定。

## 14. APP 版本升级体验问题

PDF 里提到用户反馈：使用 APP 过程中频繁弹窗提示重启升级，主要来自 H5 离线包升级，体验不好。

因此方案分成几个维度：

- 有弹窗 vs 无弹窗。
- 强提醒 vs 弱提醒。
- 重操作：需要重启 APP。
- 弱操作：不重启，只确认刷新或后台切换刷新。

几种方案：

1. 弹窗重启：更新覆盖快，实现简单，但体验差。
2. 弹窗刷新：不用重启，覆盖快，但实现成本和稳定性风险较高。
3. 红点升级：弱提醒，不打断操作，但覆盖慢、碎片化较严重。
4. 切后台刷新：无感，但时效不可控。

代码中的 `FeatureBadge` 走的是红点提醒方向：

1. `checkUpgradeInfo()` 判断是否有升级。
2. `statusResult` 缓存在用户 storage。
3. `syncBadges()` 把红点同步到 Native tab。

这是一种折中：不强行打断用户，但通过 Native tab 红点引导用户升级。

## 15. 回滚与快速降级

### 15.1 旧单应用模式下的回滚

如果当前全量版本有问题，可以在 Apollo/Version Service 配置里把 live version 切回上一个稳定版本。

APP 后续拉取配置后会：

- 如果本地已有旧版本，直接切回。
- 如果没有，重新下载旧版本 zip。
- 如果下载或校验失败，走线上兜底。

### 15.2 灰度版本回滚

灰度版本出问题时，最理想：

- 停止灰度名单。
- 或把 gray version 指向稳定版本。
- 不影响非灰度用户。

这就是多应用离线包的重要收益：只回滚某个 app_id，不影响整个 APP 里的其他业务。

### 15.3 多应用切换期不能随便回滚到旧架构

Order Tracking 拆分 PDF 里明确指出：新版 APP 支持多应用离线包后，不再支持旧版离线包；旧版 APP 也不支持新版多个离线包。

因此如果用户已经升级到新版 APP，全量版本不能直接回滚到旧离线包资源，否则 APP 匹配不上，会走线上资源，灰度也会失效。

切换期的回滚策略：

- 灰度包问题：回滚到当前架构下的全量稳定包。
- 全量包问题且短时间能修：基于当前全量分支修复并重新发布。
- 新架构重大问题：启用兜底预案，重新发布兼容包，引导用户升级或恢复配置。
- 未升级 APP 的旧用户：旧表和旧 Apollo 配置保持最后可用版本，并通过公告引导升级。

### 15.4 “快速降级”真实依赖什么

快速降级不是单纯前端操作，它依赖四件事：

1. 版本服务能把当前版本指回旧版本。
2. APP 能及时拉取版本配置。
3. APP 本地有旧版本，或能成功下载旧版本。
4. 新旧协议兼容。

如果第 4 点不成立，例如单应用协议和多应用协议不兼容，就不能靠简单回滚解决，只能发兼容修复包或强引导 APP 升级。

## 16. Order Tracking 拆分逻辑

### 16.1 拆分目标

Order Tracking 是多应用离线包的第一个试点：

- 从 H5 main 中拆出来。
- 降低 main 包体积。
- 让 Order Tracking 独立构建、发布、灰度、回滚。
- 作为新多应用协议的验证样板。

### 16.2 路径兼容

旧路径：

```text
/mgmt/order-tracking.html
/mgmt/order-detail.html
```

新路径：

```text
/mgmt/order-tracking
/mgmt/order-tracking/detail
```

兼容问题：

- 老 Apollo 配置可能还指向 `.html`。
- 旧 APP 不懂多应用。
- 新 APP 不支持旧离线包。
- 线上资源和离线资源都要能平滑过渡。

策略：

1. 先发版，再修改 Apollo 路径配置，避免新路径还没上线就 404。
2. 新离线包里把 `order-tracking/index.html` 克隆成旧 `order-tracking.html`。
3. 注意是克隆 HTML，不是把整个 order-tracking 入口配置进 main，否则会把完整业务资源重新打回 main。
4. HTML 内做旧路径到新路由的跳转。
5. Apollo 更新后，新路径正常访问独立业务。

当前 `main` 的 Vite 配置仍有临时兼容入口，可以看作迁移期实现。

### 16.3 发布顺序

PDF 建议：

```text
BFF/版本管理服务 -> 前端 main/order-tracking -> APP
```

发布前 checklist：

- 是否有正在灰度的需求；如果有，需要基于上次全量 tag 分全量和灰度两个分支。
- Apollo 的 tab URL 加 `_app_id` 离线包参数。
- 确认 order-tracking live 环境服务和 ALB。
- 确认旧 APP 升级公告文案。

发布后：

- 修改 Apollo tool 里 order-tracking 路由配置。
- 修改新离线包版本配置。
- 提供 main 和 order-tracking 的全量离线包给 APP 作为新版内置包。
- APP 内部体验 OK 后再开放外部。
- APP 发布后配置旧版本升级公告。

## 17. 双端适配原理

### 17.1 双端适配要解决什么

SPX/WMS Dashboard 后续需要同时支持 PC 和移动端。如果每个需求分别开发 PC 和 H5：

- 研发成本高。
- 业务逻辑容易分叉。
- 两端体验和数据口径容易不一致。
- 后续维护成本高。

目标是：

```text
一次业务研发，双端运行。
```

但这不是说所有代码完全一样，而是把共用逻辑和差异逻辑分层。

### 17.2 分层模型

PDF 和代码共同体现的分层：

```text
框架/路由/构建层
  - 端侧入口、路由、构建模式、离线包构建、PC remoteEntry

pages 页面层
  - 业务页面组合，不直接写端侧差异

applications 应用层
  - 页面依赖的业务组件、hooks、rules、handlers 统一出口
  - 可以组合通用逻辑

isolate 适配层
  - 端侧差异的真实实现
  - index.h5 / index.pc 对外暴露相同接口

基础组件库层
  - H5: ssc-mobile-ui-react / @ssc-ui/med h5
  - PC: ssc-ui-react / react-pro-components / @ssc-ui/med pc

service/API 层
  - 与 BFF 通信，尽量无端侧差异
```

### 17.3 `multi-end` 的实现方式

`packages/multi-end/tsconfig.json` 默认指向 H5：

```json
"@adapter/components": ["src/isolate/components/index.h5"],
"@adapter/hooks": ["src/isolate/hooks/index.h5"],
"@adapter/rules": ["src/isolate/rules/index.h5"],
"@adapter/handlers": ["src/isolate/handlers/index.h5"]
```

`packages/dashboard/tsconfig.json` 指向 PC：

```json
"@adapter/components": ["packages/multi-end/src/isolate/components/index.pc"],
"@adapter/hooks": ["packages/multi-end/src/isolate/hooks/index.pc"],
"@adapter/rules": ["packages/multi-end/src/isolate/rules/index.pc"],
"@adapter/handlers": ["packages/multi-end/src/isolate/handlers/index.pc"]
```

因此业务代码可以写：

```ts
import { useNavigate } from '@adapter/hooks';
import { getMultiEndProps } from '@adapter/rules';
import { showHelpInfo } from '@adapter/handlers';
import { Wrapper, Link } from '@applications/components';
```

构建 H5 时拿 H5 实现，构建 PC 时拿 PC 实现。

### 17.4 `applications` 是稳定依赖口

`packages/multi-end/src/applications/components/index.tsx`：

```ts
export * from '@adapter/components';
export { default as LineChart } from './line-chart';
export { default as ColumnChart } from './column-chart';
```

页面更推荐依赖 `@applications/*`，因为它既能暴露 adapter，也能组合双端通用业务逻辑。

这样页面不需要知道：

- H5 用哪个组件库。
- PC 用哪个组件库。
- H5 跳转走 JSBridge。
- PC 跳转走 `window.open` 或 `history.push`。
- H5 图表高度需要 `p2w`。
- PC 图表高度是固定像素。

### 17.5 `getMultiEndProps`

这是最常见的双端分支工具。

H5：

```ts
export function getMultiEndProps<T>(h5Props: T, _?: T): T {
  return h5Props;
}
```

PC：

```ts
export function getMultiEndProps<T>(h5Props: T, pcProps: T): T {
  return pcProps;
}
```

业务代码可以写：

```ts
const chartHeight = getMultiEndProps(120, 250);
const extra = getMultiEndProps(null, pcExtraContent);
```

构建出来的代码自然只保留当前端要用的值。

### 17.6 路由前缀差异

H5：

```ts
ROUTE_PREFIX = '/mgmt/main'
```

PC：

```ts
ROUTE_PREFIX = '/#/dashboard'
```

H5 是 APP WebView 的真实 path，PC 是 FMS/hash 路由。业务不要硬编码前缀，而应通过 rules 获取。

### 17.7 跳转差异

H5：

```ts
useNavigate -> common/hooks/use-app-navigate -> jsBridge.navigate
```

PC：

```ts
useNavigate -> react-router history 或 window.open
```

同一个业务点击“查看详情”，在 H5 是打开 Native WebView，在 PC 是新 tab 或应用内 hash 跳转。

### 17.8 用户/区域/站点来源差异

H5 和 PC 获取 user、region、station 的位置不一样：

- H5 可能来自 APP cookie、JSBridge、本地缓存。
- PC 可能来自浏览器 cookie、localStorage、FMS 注入上下文。

因此 `get-user-id/index.h5.ts` 与 `index.pc.ts` 分开：

```ts
// H5
docCookies.getItem(USER_EMAIL)

// PC
localStorage.getItem('useremail') || docCookies.getItem('spx_dn')
```

这类逻辑应下沉到 adapter/rules，不要散落在页面。

## 18. WMS 的双端实现

WMS 使用与 `multi-end` 类似但独立的 `@wms-adapter/*`。

`packages/wms-mgmt/tsconfig.json` 默认：

```json
"@wms-adapter/*": ["src/isolate/*/index.h5"]
```

PC Vite 配置里覆盖 alias：

```ts
{
  find: /@wms-adapter\/components/,
  replacement: 'src/isolate/components/index.pc',
}
```

H5 入口 `packages/wms-mgmt/h5/app.tsx`：

- `BrowserRouter basename={__APP_MODE__}`。
- `Routes` 来自 `@wms-adapter/routes`。
- `Layout/Anchor` 来自 `@wms-adapter/components`。
- 初始化 APP store、权限、离线包信息、预加载、版本缓存。
- 监听 `offlineResourceRefresh` 更新翻译。

PC 入口 `packages/wms-mgmt/pc/index.tsx`：

- 先加载 PC 语言资源。
- 再渲染 PC App。
- PC HTML 模板会被 version-mgr 插件注入远程入口加载脚本。

## 19. PC Dashboard / FMS 加载原理

### 19.1 `dashboard` Module Federation

`packages/dashboard/config/moduleFederationConfig.js`：

```js
module.exports = {
  name: 'SPXDashboard',
  filename: 'remoteEntry.react.js',
  exposes: {
    './module': paths.mfModule,
  },
  remotes: {
    Shared: 'promise window.LOAD_REMOTE_ENTRY("Shared", "admin", "sharedEntry.js")',
  },
}
```

`packages/dashboard/src/moduleEntries/pc-dashboard.tsx` 暴露：

```ts
{
  isReact: true,
  routes: vueRoutes,
  reactRoutes,
  packageInfo: { name, dependencies: {} }
}
```

FMS 基座加载流程：

1. 动态创建 script 加载 `remoteEntry.react.xxx.js`。
2. Webpack MF runtime 在 `window.SPXDashboard` 上放 `init/get`。
3. FMS `import('SPXDashboard/module')`。
4. 拿到 routes。
5. 注册到 FMS 路由。

### 19.2 remoteEntry 为什么要带版本后缀

`packages/dashboard/scripts/build.js` 构建后会把：

```text
remoteEntry.react.js
```

重命名为：

```text
remoteEntry.react.v_{gitCommitHash}_{gitTag}.js
```

同时写 `version-info.json`：

```json
{
  "remoteEntryFileName": "remoteEntry.react.v_xxx_tag.js",
  "gitCommitHash": "...",
  "gitTag": "...",
  "time": "..."
}
```

好处：

- 避免 remoteEntry 缓存污染。
- 版本服务可以精确配置某个 remoteEntry。
- 灰度时不同用户加载不同 remoteEntry。

### 19.3 FMS 异步加载调研结论

PDF 里分析：目前初始化时加载 remoteEntry 只是拿路由信息，真正“按需加载页面资源”的关键不在 FMS 加载 remoteEntry，而在子应用路由内部要用动态 import 和 Suspense。

结论：

- 目标 1：Dashboard 页面按需加载，可以通过路由组件动态 import 实现。
- 目标 2：把灰度版本匹配逻辑迁移到 Dashboard 内部，风险较大，暂不实现。

原因是如果 remoteEntry 自己再动态判断版本并加载另一个入口，就会绕开 Module Federation 的共享机制，Shared 模块、VueStore 等需要重新注入，改造风险很高。

## 20. WMS PC version-mgr 原理

WMS PC 不是用 `dashboard` 这套 webpack MF 脚本，而是用 SDK 的 Vite 插件：

```ts
...getVersionMgrPlugins({ useCDN, dev: isLocal })
```

它包含两个插件：

```ts
generateRemoteEntry()
loadEntryByVersionMgr()
```

### 20.1 `generateRemoteEntry`

作用：

1. 扫描 Vite bundle。
2. 找到入口 JS、chunk、CSS。
3. 生成一个 remoteEntry JS。
4. 写 `version-info.json`。

remoteEntry 的内容是一个自执行脚本，会依次加载：

- CSS。
- 入口 JS。
- modulepreload chunk。

### 20.2 `loadEntryByVersionMgr`

作用：

1. 读取 PC HTML 模板。
2. 把 `load-remote-entry.umd.js` 注入 HTML。
3. 页面运行时调用 `window.__load_remote_entry(...)`。
4. 根据用户/区域/环境获取版本配置。
5. 选择最终 remoteEntry 文件。
6. 动态加载 remoteEntry。

### 20.3 CDN/IDC 双构建

`packages/wms-mgmt/build/run.js` 对 PC build 做两次构建：

1. 第一次默认 `useCDN=true`，资源路径走 CDN。
2. 成功后第二次 `useCDN=false`，生成一份 IDC 路径的入口。

`version-mgr-pc.ts` 里根据配置的 `use_idc` 决定加载：

```text
CDN: //deo.shopeemobile.com/.../{remoteEntry}
IDC: /mgmt/dashboard/wmsmgmtpc/idc.{remoteEntry}
```

这样 PC 端可以在 CDN 异常或策略需要时切 IDC。

## 21. 发布流程

### 21.1 H5 离线包发布

通用流程：

```text
1. 前端构建
2. 生成在线资源 + 离线 zip + offline_manifest.json
3. 上传 dist 到 CDN/IDC
4. 创建 app version
5. Apollo/Version Service 配置全量或灰度版本
6. APP 拉取版本配置
7. APP 下载/校验/解压
8. 用户打开页面命中本地离线资源
```

### 21.2 Space/DMS 配置

`deploy/mgmtapph5.json`：

```json
"commands": [
  "pnpm i --registry=https://npm.shopee.io",
  "pnpm build"
],
"upload_static": {
  "static_dir": "dist",
  "enable_cdn": true
},
"idc_exclude_patterns": ["*.zip"]
```

含义：

- 构建产物统一在 `dist`。
- 静态资源上传 CDN。
- zip 不上传 IDC，只走 CDN。

`deploy/mgmtdashboard.json` 里有 finish hook 创建 PC 版本：

```json
"cmd": "node $WORKSPACE/scripts/dashboard/create-pc-version.js ..."
```

WMS 的版本创建脚本在代码里存在，但当前 `deploy/wmsmgmth5.json` 片段没有显式展示调用位置，注释写的是 “After Upload LB Commands 阶段执行”。实际要以 Space/DMS 配置为准。

## 22. 常见问题与解决方式

### 22.1 弱网首屏慢

原因：HTML/JS/CSS/图片都走网络。

解决：

- 静态资源打成离线包。
- APP 提前下载。
- WebView 请求优先命中本地。
- 失败再 fallback 线上。

### 22.2 包体积越来越大

原因：业务增多，依赖和业务代码都在一个包里。

解决：

- `vendor/bundle` 拆包。
- 低频三方依赖进 `vendor`。
- 高频业务进 `bundle`。
- 进一步按业务拆 app_id，例如 Order Tracking。
- i18n 等静态资源可拆独立 static app_id。

### 22.3 业务之间互相影响发布

原因：一个 APP 只有一个离线包版本，任何业务发版都要更新全量包。

解决：

- `biz_id -> 多 app_id`。
- 每个业务 app_id 独立版本。
- Apollo 配置粒度从 APP 变为 app_id。

### 22.4 旧 APP 和新离线包不兼容

原因：旧 APP 不认识 `_app_id` 和多 app_id；新 APP 也不支持旧单应用离线包协议。

解决：

- 新老接口和 DB 隔离。
- 老 `get_version` 保持最后可用旧版本，不继续更新。
- 新版本使用 `get_version_v3` 或 Version Service 新接口。
- 对旧 APP 用户展示最高优先级公告，引导升级。
- 新 APP 内置全量新版离线包。

### 22.5 新页面离线包访问 404 或走线上

原因：新增路由没有配置到 `htmlOutDirs`。

解决：

- 在对应 `offline-config.js` 补 HTML 路径。
- 确认 APP 打开路径和 `htmlOutDirs` 完全匹配。
- 自测时看 URL 是否带 `_offl_id/_app_id`。

### 22.6 样式在离线包里丢失

原因：CSS 单独加载时路径、顺序、WebView 缓存或跨域可能出问题。

解决：

- 使用 `vite-plugin-css-injected-by-js`。
- CSS 随 JS 注入。

### 22.7 翻译更新后页面不刷新

原因：i18n 被缓存或独立资源更新后 H5 未重新加载。

解决：

- 独立静态资源包。
- APP 通过 `offlineResourceRefresh` 通知 H5。
- H5 调 `loadResource()` 并触发 i18n `languageChanged`。

WMS H5 已有此逻辑。

### 22.8 iOS storage/cookie 异常

原因：iOS 26 相关策略下，跨域资源可能导致 storage 访问受限或上下文不一致。

解决：

- 离线包请求路径映射到同域名/ALB 路径。
- `main` 使用 `newPackagePath = domain/mgmt`。
- WMS 使用 `newPackagePath = sbs-mgmt.../{deployModuleName}` 和 `base=/{deployModuleName}`。

### 22.9 离线包升级弹窗打断操作

原因：旧升级方式偏强提醒、重启生效。

解决：

- 采用红点弱提醒。
- `checkUpgradeInfo()` 检测升级。
- `syncBadges()` 同步 Native tab 红点。
- 必要时通过 bridge 主动更新并 reload，而不是重启整个 APP。

### 22.10 PC 灰度版本导致预加载失效

原因：remoteEntry 文件名不稳定，FMS 预加载难以提前知道最终版本入口。

解决：

- 页面资源按需加载，减少初始化成本。
- PC version-mgr 运行时根据用户/区域选择 remoteEntry。
- 暂不把所有版本匹配逻辑强行迁入 Dashboard remoteEntry 内部，避免破坏 MF 共享机制。

## 23. 自测和排查建议

### 23.1 H5 main 离线包构建后看什么

执行：

```bash
pnpm build
```

关注：

```text
dist/
  mgmtapph5/
  mgmt_offline_xxx/
    vendor.zip
    bundle.zip
    mgmtapph5/offline_manifest.json
```

检查：

- `offline_manifest.json` 是否有 `vendor` 和 `bundle`。
- zip md5 是否生成。
- zip 内是否有 `verify.json`。
- `verify.json` 是否包含关键 HTML 路径。
- JS 中资源引用是否带 `_offl_id`。

### 23.2 WMS H5 离线包构建后看什么

执行：

```bash
pnpm build-wms
```

关注：

- 主 manifest 是否生成。
- `static-manifest-sbs-mgmt-h5-assets.json` 是否生成。
- i18n 是否进入 `i18n.zip`。
- 资源 URL 是否带 `_app_id=sbs-mgmt-h5-dashboard&_offl_id=...`。

### 23.3 APP 内排查

可以打开 JSAPI 测试页：

```text
/mgmt/main/jsapi
```

看：

- `getOfflineInfo()`
- `checkUpgradeInfo()`
- `updateOfflinePkg()`
- `getAppInfo()`

如果离线包没命中：

1. 看当前 URL 是否带 `_offl_id/_app_id`。
2. 看 APP 当前版本配置里是否有对应 app_id。
3. 看本地是否下载成功。
4. 看 `verify.json` 是否包含该路径。
5. 看路径是否因为 ALB/basePath 改动不一致。
6. 看是否 fallback 到线上资源。

### 23.4 PC version-mgr 排查

看：

- `version-info.json` 是否存在。
- remoteEntry 是否带版本后缀。
- Version Service 是否能返回 `get_pc_version_config`。
- `use_idc` 配置是否符合预期。
- 用户名 hash / region 是否命中灰度。
- 加载日志是否上报到 `/mgmt/api/sys/log`。

## 24. 建议的阅读顺序

如果你是第一次理解这个项目，建议按这个顺序看代码：

1. `packages/main/build/vite.config.ts`：先看 H5 构建入口。
2. `vite/plugins/build-offline/index.ts`：理解离线包怎么生成。
3. `packages/main/build/offline-config.js`：理解 HTML 路由为什么要列这么多。
4. `packages/common/utils/js-bridge/index.ts`：理解 H5 和 Native 怎么交互。
5. `packages/main/src/utils/feature-badge/index.ts`：理解升级红点怎么同步给 APP。
6. `ssc-fe-version-mgr-sdk-master/src/core/plugins/vite/vite-build-offline-packages.ts`：理解 SDK 版多 app_id 构建。
7. `ssc-fe-version-mgr-sdk-master/src/core/node-scripts/create-version-dms-script.ts`：理解版本创建。
8. `packages/order-tracking/src/routes/index.tsx` 与 `packages/main/build/vite.config.ts`：理解业务拆分兼容。
9. `packages/multi-end/src/isolate/*`：理解双端适配。
10. `packages/dashboard/config/moduleFederationConfig.js` 与 `packages/dashboard/src/moduleEntries/pc-dashboard.tsx`：理解 PC FMS 接入。
11. `packages/wms-mgmt/build/vite.config.h5.ts` 与 `packages/wms-mgmt/build/vite.config.pc.ts`：理解 WMS 双端与 SDK 接入。

## 25. 最后的心智模型

可以把整个项目想成三层闭环。

第一层是资源闭环：

```text
Vite/Webpack 构建
  -> 改写资源 URL
  -> 生成 zip + verify + manifest
  -> 上传 CDN
  -> 创建版本
  -> APP 下载
  -> WebView 请求命中本地
```

第二层是版本闭环：

```text
app_id 注册
  -> 创建版本
  -> Apollo/Version Service 配置 live/gray
  -> APP 拉取版本
  -> user/region 灰度匹配
  -> 更新提醒或主动更新
  -> 回滚/降级
```

第三层是双端闭环：

```text
页面写一套业务逻辑
  -> applications 统一出口
  -> adapter/isolate 隐藏端差异
  -> H5 构建选 index.h5
  -> PC 构建选 index.pc
  -> 两端共享 API/model/tracking/i18n 口径
```

理解这三层后，mgmt-app-h5-release 就不再是一堆散乱包和脚本，而是一套从构建、发布、APP 加载、业务拆分、双端复用到版本治理的完整工程体系。
