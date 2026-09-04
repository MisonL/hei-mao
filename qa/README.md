# QA 与过程记录索引

本目录保存黑毛宠物包的结构门禁、视觉复核、安装器验证和 PetDex 发布证据。根目录 README 只保留当前状态和使用入口；详细过程不再重复粘贴到 README。

## 当前基线

以下文件是当前状态的主要依据，日期较早的快照仅用于追溯：

| 文件 | 用途 | 当前结论 |
| --- | --- | --- |
| [`current-state-recheck-20260903-v1.json`](current-state-recheck-20260903-v1.json) | 汇总本地包、线上传播和剩余边界 | 本地八角色与安装器就绪；五个线上 sprite 更新待传播；App 实机验收仍需用户完成 |
| [`current-v2-gate-recheck-20260903-v1.json`](current-v2-gate-recheck-20260903-v1.json) | 八角色 v2 结构、尺寸、透明度和 SHA | 8/8 通过，`1536x2288`、`8x11`、RGBA WebP、无透明 RGB 残留 |
| [`installer-validation-recheck-20260903-v1.json`](installer-validation-recheck-20260903-v1.json) | Bash / PowerShell 语法和隔离安装 | 8/8 支持角色通过，未知 slug 拒绝 |
| [`three-directory-parity-recheck-20260903-v1.json`](three-directory-parity-recheck-20260903-v1.json) | 仓库、Codex 和 PetDex 本地目录对照 | 八个角色的 16 个文件逐字节一致 |
| [`hatch-pet-baseline-recheck-20260903-v1.json`](hatch-pet-baseline-recheck-20260903-v1.json) | hatch-pet 基线测试 | `28 passed`；保留既有 Pillow 弃用警告 |
| [`visual-review-recheck-20260901-v1.json`](visual-review-recheck-20260901-v1.json) | 八角色动作和比例视觉复核 | `pass_with_reviewed_minor_warnings`；minor warning 已记录，不替代 App 播放验收 |
| [`petdex-live-recheck-20260903-v2.json`](petdex-live-recheck-20260903-v2.json) | PetDex manifest、搜索、详情和公共资源 | 历史重复条目已消失；八个当前条目保留；五个 sprite SHA 待上游传播 |
| [`petdex-edit-resubmission-recheck-20260904-v1.json`](petdex-edit-resubmission-recheck-20260904-v1.json) | 五个已有 slug 的 sprite / metadata 编辑 | 五次编辑均进入 `queued_for_admin_review` |
| [`imagegen-channel-recheck-20260901-v1.json`](imagegen-channel-recheck-20260901-v1.json) | 最近一次真实图像渠道 smoke | 请求成功并已记录脱敏结果；不代表需要重新生成正式资产 |

## 精简过程记录

- **2026-09-01**：八个角色完成完整动作行生成、装配和视觉复核；本地 v2 门禁、安装器和目录一致性保持通过。
- **2026-09-03**：用户删除历史重复条目 `hei-mao-2`；公开列表、搜索和详情路由完成传播；同时刷新五个修复图集的安装器 SHA 常量。
- **2026-09-04**：使用已有 slug 的 `petdex edit` 重新提交五个修复角色，全部进入管理员审核队列；审核完成前公共 CDN 可能仍提供旧图集。

更早的探针、重试和中间候选仍按日期保留在 `qa/`，但不再作为当前状态摘要。阅读旧文件时，应优先查看其 `checked_at`、`scope`、`result` 或 `decision` 字段，并与当前基线对照。

## 证据边界

- `queued_for_admin_review` 表示提交已接收，不等于公共 sprite 已完成审核和传播。
- 结构门禁、静态图像和浏览器合成器复核不能替代 Codex App 实时播放、窗口刷新、多角色和跨屏气泡验收。
- QA 文件只记录脱敏后的结果；不得写入凭证、请求令牌、本机绝对路径、私网地址或进程标识。

## 目录约定

每个角色的 `qa/<slug>/` 通常包含：

- `validation*.json`：图集格式、尺寸、透明度和 v2 合同
- `review*.json`：帧提取、透明度和静态视觉检查
- `contact-sheet*.png`：动作帧总览
- `previews/*.gif`：标准状态动画预览
- `look-directions.png`、`direction-blind-*.json`：16 方向和盲测证据
- `run-summary.json`、`look-continuity*.json`：当前运行与连续性摘要（存在时）

## 新增记录

新增 QA 文件使用 `<topic>-<YYYYMMDD>-vN.json` 命名，至少包含检查时间、范围、命令或方法、结果和未覆盖边界。过程记录应引用证据文件，不复制整段日志；完成后运行 `git diff --check`，并确认内容不含本机环境信息。
