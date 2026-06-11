# 翻译接口：TSP → UTM 迁移说明

## 背景与目标

- **平台合并**：TSM 与 TSP 合并至 **UTM**；TSP 计划在 **2026 Q2** 起废弃，相关 API 预计在 **2026 年底前**停止服务。
- **业务要求**：各业务需在截止日前完成 **TSP SDK 升级**及主应用侧 **翻译资源配置**从 Resource/Collection 到 UTM Collection 的切换。

## 改动概览

| 维度 | 说明 |
|------|------|
| SDK | 包名由 `tsp-sdk` 调整为 `@shopee/tsp-sdk`，并增加 `defaultCdnPath` |
| 翻译配置 | `resources` / `collections` / `lazyResources` / `lazyCollections` 改为 `utmCollections` / `utmLazyCollections` |
| 请求域名 | 初始化请求从原 TSP 路径切到 UTM 侧 CDN 路径（见下文「升级后行为」） |
| ID 映射 | 旧 Resource ID 与 UTM Collection ID 需按映射表替换（见「Resource 与 UTM ID 映射」） |

---

## 一、micro-base：升级 TSP SDK

在 **micro-base** 仓库中升级依赖，并在创建 TSP 实例时设置 `defaultCdnPath: 'tsp-default'`。

**升级前：**

```javascript
import TSP from 'tsp-sdk';

const tsp = new TSP({
  // ...其他配置
});
```

**升级后：**

```javascript
import TSP from '@shopee/tsp-sdk';

const tsp = new TSP({
  // ...其他配置
  defaultCdnPath: 'tsp-default',
});
```

---

## 二、主应用：`tsp.create` 翻译配置

业务在升级 tsp-sdk 后，需将 `translation` 中基于 Resource/Collection 的字段改为 UTM Collection 字段。

**升级前（示例）：**

```javascript
const res = await tsp.create({
  // ...其他配置
  translation: {
    // 业务主要关注以下字段
    resources: [880],
    collections: [2],
    lazyResources: [24],
    lazyCollections: [111],
  },
});
```

**升级后（示例）：**

```javascript
const res = await tsp.create({
  // ...其他配置
  translation: {
    utmCollections: [2],
    utmLazyCollections: [111],
  },
});
```

### Resource 与 UTM ID 映射

请根据内部映射表，将原 `resources` / `collections` 等对应到 **utm_collection_id**，再填入 `utmCollections` / `utmLazyCollections`：

[Resource ↔ UTM ID 映射表（Google Sheets）](https://docs.google.com/spreadsheets/d/1MOGfMYj_0HwcnQt6xK5dK_K4LaPjWpc7u79QDeJyr4A/edit?gid=293796353#gid=293796353)

其他主应用做法与上述一致：更新 `tspCreateOptions`，将例如 `resources: [TRANSLATION_RESOURCES]` 替换为 `utmCollections: [UTM_COLLECTIONS_ID]`（lazy 同理使用 `utmLazyCollections`）。

---

## 三、Merge Request 参考

| 仓库 | MR |
|------|-----|
| micro-base | [MR 254](https://git.garena.com/shopee/bg-logistics/b2c/retail-fe/micro-base/-/merge_requests/254/diffs) |
| vmi-admin-fe | [MR 3376](https://git.garena.com/shopee/bg-logistics/b2c/retail-fe/vmi-admin-fe/-/merge_requests/3376/diffs) |

---

## 四、升级后行为

- **请求路径**：由原先 TSP 相关请求（如 `/tsp/nonlive/init`）切换为通过 UTM 侧资源加载，示例 CDN 基址：`https://deo.shopeemobile.com/shopee/stm-sg-live/tsp-default/`（以实际环境为准）。

---

## 五、文案同步方案

| 方式 | 说明 |
|------|------|
| 自动同步 | 每 **2 小时**自动同步一次 |
| 手动同步 | 在 Space 项目内点击 **Sync from Tsp**，发布记录示例：`https://space.shopee.io/webfe/tm/projects/<utm_project_id>/publish-records?page=1&pageSize=20` |

### 各项目 Resource / UTM 与 Space 地址

| 项目 | Resource | utm_project_id | utm_collection_id | Space 发布记录 |
|------|----------|----------------|-------------------|----------------|
| vmi-admin-fe | 4739 | 1674 | 1797 | [打开](https://space.shopee.io/webfe/tm/projects/1674/collections/1797/publish-records?page=1&pageSize=20) |
| vmi-srm-fe | 4672 | 1800 | 1668 | [打开](https://space.shopee.io/webfe/tm/projects/1668/collections/1800/publish-records?page=1&pageSize=20) |
| pms-frontend | 926 | 1802 | 1676 | [打开](https://space.shopee.io/webfe/tm/projects/1676/collections/1802/publish-records?page=1&pageSize=20) |
| SRM-frontend | 927 | 1805 | 1680 | [打开](https://space.shopee.io/webfe/tm/projects/1680/collections/1805/publish-records?page=1&pageSize=20) |
| frs-admin-fe | 2560 | 1804 | 1677 | [打开](https://space.shopee.io/webfe/tm/projects/1677/collections/1804/publish-records?page=1&pageSize=20) |
| frs-supplier-fe | 2692 | 1801 | 1675 | [打开](https://space.shopee.io/webfe/tm/projects/1675/collections/1801/publish-records?page=1&pageSize=20) |
