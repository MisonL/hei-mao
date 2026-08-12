# 黑毛 Codex Pet

钱大妈品牌 IP “黑毛”的 Codex App 自定义宠物包。

“黑毛”是[钱大妈官网公开发布的品牌 IP 角色](https://www.qdama.cn/brandIP)。本项目由钱大妈员工基于公开品牌形象制作，用于本地 Codex App 个性化展示，不代表钱大妈官方软件产品或技术支持承诺。

## 预览

![contact sheet](qa/hei-mao/contact-sheet.png)

## 安装

### Petdex 安装

根包已有 Petdex 公开条目；线上资源版本仍以 manifest 为准。已安装 Node.js 20 或更高版本的 macOS、Linux 或 Windows 可运行：

```bash
npx -y petdex@latest install hei-mao
npx -y petdex@latest install hei-mao-quality
npx -y petdex@latest install hei-mao-butler
npx -y petdex@latest install hei-mao-chef
npx -y petdex@latest install hei-mao-foodie
```

截至本次复核，以上命令会下载 Petdex 当前公开版本：`hei-mao`、`hei-mao-quality` 和 `hei-mao-foodie` 的线上 metadata 或 spritesheet SHA 与本仓库 v2 不一致，`hei-mao-butler` 和 `hei-mao-chef` 的字节与仓库一致。需要使用仓库 v2 图集时，请先使用下方角色安装器或手动复制到 Codex 目录；Petdex 编辑路由部署并完成已登录同步前，不要把线上下载结果当作本仓库 v2。

Petdex CLI 会同时安装到 Petdex Desktop 与 Codex App 的宠物目录：

```text
~/.petdex/pets/hei-mao
~/.codex/pets/hei-mao
```

### 角色包状态

当前仓库中的角色包如下。每个角色都有独立的 `pet.json`、v2 图集和 QA 证据，不能用其他角色的图集替代；只有没有视觉阻断的角色才会进入安装器白名单。

| slug              | 角色   | 本地状态               | Petdex 状态                |
| ----------------- | ------ | ---------------------- | -------------------------- |
| `hei-mao`         | 黑毛   | 已验证                 | manifest 可见，字段仍为 v1 |
| `hei-mao-quality` | 品控官 | 已验证                 | manifest 可见，字段仍为 v1 |
| `hei-mao-butler`  | 大管家 | 已验证                 | manifest 可见，字段仍为 v1 |
| `hei-mao-chef`    | 厨师   | 已验证                 | manifest 可见，字段仍为 v1 |
| `hei-mao-foodie`  | 美食家 | v2 已验证，可本地安装 | manifest 可见，字段仍为 v1 |
| `hei-mao-delivery` | 配送员 | v2 已验证，可本地安装 | 已提交，待审核 |

公开 manifest 当前可见五个历史角色条目以及历史重复条目 `hei-mao-2`；`hei-mao-delivery` 的仓库包已通过本地 v2 门禁，并已提交 Petdex、当前等待审核。manifest 索引仍报告 `spriteVersionNumber: 1`，虽然当前公开 pet JSON 已报告 v2，但部分 sprite 和 metadata 仍与本仓库不一致，不能据此宣称线上资源已经同步。`hei-mao-foodie` 的 waiting 行已完整重生成并通过最终视觉 QA；线上旧资源不能视为本仓库 v2。

Petdex CLI 会把成功安装的角色同时写入 Petdex Desktop 与 Codex App 的宠物目录：

```text
~/.petdex/pets/<slug>
~/.codex/pets/<slug>
```

截至 2026-08-10T04:08:08Z，Petdex 公开 manifest 的生成时间为 `2026-08-10T01:07:58.002Z`，总数为 4489，包含五个历史角色和历史重复条目 `hei-mao-2`；这些条目的 manifest 索引字段仍为 `spriteVersionNumber: 1`，但公开 pet JSON 的 `spriteVersionNumber` 已为 2。公开下载的 sprite 中，`hei-mao-butler` 和 `hei-mao-chef` 与仓库字节一致，`hei-mao`、`hei-mao-quality`、`hei-mao-foodie` 仍与仓库 v2 不一致；品控官的在线 metadata 也与仓库不一致。`petdex@1.2.0 install` 已在隔离目录成功下载五个角色并同时写入 Petdex/Codex 目录；这只证明线上安装可用，不代表线上资源已同步为仓库 v2。当前 CLI 的 `doctor` 已在 v1 移除；编辑流程仍需按正式的已登录编辑接口完成，不能把公开安装 smoke 当作 v2 发布完成。`hei-mao-2` 是历史重复条目，不属于当前发布集。完整复核证据见 `qa/petdex-live-install-recheck-20260810.json`。

本机当前保留六个通过 v2 合同和最终视觉门禁的角色，Codex 与 Petdex 两个本地目录的文件集合和 SHA-256 一致。`hei-mao-delivery` 的正式包复核见 `qa/hei-mao-delivery/run-summary.json`，最新 foodie 安装复核见 `qa/foodie-install-recheck-20260810.json`。

### 角色安装器

无参数时安装 `hei-mao`。通过环境变量选择已经通过本仓库 QA 且未被阻断的角色：

```bash
HEI_MAO_PET_ID=hei-mao-chef curl -fsSL https://raw.githubusercontent.com/MisonL/hei-mao/main/install.sh | HEI_MAO_PET_ID=hei-mao-chef bash
```

PowerShell 可使用同一个环境变量，或直接传 `-PetId`：

```powershell
$env:HEI_MAO_PET_ID="hei-mao-chef"; irm https://raw.githubusercontent.com/MisonL/hei-mao/main/install.ps1 | iex
./install.ps1 -PetId hei-mao-chef
```

安装器只接受仓库中已有完整图集和固定 SHA 的角色，未知 slug 会显式失败。Windows PowerShell 5.1 的本地 checkout 可能受 Git `core.autocrlf` 影响，安装器会对文本 manifest 显式按 UTF-8/LF 规范化后再校验固定 SHA，二进制图集保持原样。角色包默认安装到 `~/.codex/pets/<slug>`；需要 Petdex Desktop 时请使用上面的 `petdex install`，不要手动复制到未知目录。

未完成完整 v2 图集和复核的 `hei-mao-fortune`、`hei-mao-traveler` 不在安装器白名单内。历史 `hei-mao-recommender` 和 `hei-mao-2` 也不属于当前发布集。历史 slug 的当日复核见 `qa/historical-slug-recheck-20260809.json`。

`hei-mao-fortune` 和 `hei-mao-traveler` 目前没有可发布图集。2026-08-12 的本地服务合同检查通过，但新的 `images-non-stream` 和 `images-sse` 真实 smoke 均未产生 artifact，分别返回上游不可用和页面 SSE 500，因此这两个角色仍保持未开始。复核证据见 `qa/imagegen-channel-recheck-20260812.json`。

本地手动安装角色时：

```bash
mkdir -p ~/.codex/pets/hei-mao
cp pets/hei-mao/pet.json pets/hei-mao/spritesheet.webp ~/.codex/pets/hei-mao/
```

### 大管家角色

`hei-mao-butler` 包含完整的 v2 动画图集和 16 个观察方向的独立 QA 证据。该包已提交 Petdex，当前状态为待审核；审核完成前不将其视为 Petdex 已上线包。

Petdex 安装：

```bash
npx -y petdex@latest install hei-mao-butler
```

### Chef 角色

`hei-mao-chef` 是黑毛的厨师角色包，已通过结构、透明度、方向盲测、连续性和独立视觉复核。连续性报告中的四处数值告警均已记录为 minor warning，未发现可见跳帧、裁切、比例突变、身份漂移或方向反转。

Petdex 安装：

```bash
npx -y petdex@latest install hei-mao-chef
```

### 美食家角色

`hei-mao-foodie` 是黑毛的美食家角色包。waiting 行已作为完整六帧行重新生成，结构、透明度、方向盲测、连续性和独立视觉复核均通过；没有 detached effects、身份漂移或比例/基线异常。仓库安装器已纳入该角色。

本地安装：

```bash
HEI_MAO_PET_ID=hei-mao-foodie curl -fsSL https://raw.githubusercontent.com/MisonL/hei-mao/main/install.sh | HEI_MAO_PET_ID=hei-mao-foodie bash
```

Petdex 安装：

```bash
npx -y petdex@latest install hei-mao-foodie
```

### 配送员角色

`hei-mao-delivery` 是黑毛的社区配送角色包，已通过 v2 图集、透明度、方向盲测和独立视觉复核。连续性报告中的耳间开放负空间和局部数值告警均已按 minor review resolution 复核，没有封闭透明洞、裁切、身份漂移、比例跳变或方向反转。当前仓库安装器已纳入该角色；Petdex 已接受提交并标记为 `held for review`，审核通过前不能使用 Petdex 在线安装命令。

本地安装：

```bash
HEI_MAO_PET_ID=hei-mao-delivery curl -fsSL https://raw.githubusercontent.com/MisonL/hei-mao/main/install.sh | HEI_MAO_PET_ID=hei-mao-delivery bash
```

Petdex 审核通过后使用：

```bash
npx -y petdex@latest install hei-mao-delivery
```

### 品控官角色

`hei-mao-quality` 是黑毛的品控官角色包，已完成完整的 v2 图集、方向连续性、三份独立方向盲测和最终视觉复核。

Petdex 安装：

```bash
npx -y petdex@latest install hei-mao-quality
```

如需从仓库手动安装到 Codex App：

```bash
mkdir -p ~/.codex/pets/hei-mao-quality
cp pets/hei-mao-quality/pet.json pets/hei-mao-quality/spritesheet.webp ~/.codex/pets/hei-mao-quality/
```

### 一键安装

macOS / Linux:

```bash
curl -fsSL https://raw.githubusercontent.com/MisonL/hei-mao/main/install.sh | bash
```

Windows PowerShell:

```powershell
irm https://raw.githubusercontent.com/MisonL/hei-mao/main/install.ps1 | iex
```

默认安装到 Codex 自定义宠物目录：

```text
~/.codex/pets/hei-mao
```

通过 `HEI_MAO_PET_ID` 选择已验证角色，安装器会同时更换目标目录和远程资源路径；不传时安装 hei-mao。

如需指定 Codex 配置目录：

```bash
curl -fsSL https://raw.githubusercontent.com/MisonL/hei-mao/main/install.sh | CODEX_HOME=/path/to/.codex bash
```

Windows PowerShell:

```powershell
$env:CODEX_HOME="C:\Users\you\.codex"; irm https://raw.githubusercontent.com/MisonL/hei-mao/main/install.ps1 | iex
```

安装器在交互式终端中会显示黑毛小猪 ASCII 动画；日志或管道环境会自动退化为静态输出。需要手动关闭动画时，可设置 `HEI_MAO_NO_ANIMATION=1`。

### 手动安装

将本仓库复制到 Codex 自定义宠物目录，或只复制目标角色目录下这两个文件：

```text
pets/<slug>/pet.json
pets/<slug>/spritesheet.webp
```

推荐目录结构：

```bash
mkdir -p ~/.codex/pets/hei-mao
cp pets/hei-mao/pet.json pets/hei-mao/spritesheet.webp ~/.codex/pets/hei-mao/
```

然后在 Codex App 中：

1. 打开 `设置 -> 外观 -> 宠物`
2. 点击 `刷新`
3. 在自定义宠物中选择 `黑毛`

## 文件说明

- `pets/<slug>/pet.json`: Codex App 宠物清单文件
- `pets/<slug>/spritesheet.webp`: v2 11 行动画精灵图，尺寸 `1536x2288`
- `qa/<slug>/contact-sheet.png`: 动画帧总览
- `qa/<slug>/contact-sheet-extended.png`: 包含 16 个观察方向的 v2 动画帧总览
- `qa/<slug>/validation.json`: atlas 验证结果
- `qa/<slug>/review.json`: 帧提取与透明度检查结果
- `qa/<slug>/look-directions.png`: 16 个观察方向总览
- `qa/<slug>/direction-blind-pairs.png`: 随机化的无标签方向盲测图
- `qa/<slug>/direction-blind-validation.json`: 方向盲测结果
- `qa/<slug>/direction-blind-verdicts-*.json`: 三份独立盲测投票与严格多数合并结果
- `qa/<slug>/direction-blind-answer-key.json`: 盲测完成后的隐藏答案记录
- `qa/<slug>/blind-review-resolution.json`: 中间方向 warning 的审查与处理决定
- `qa/<slug>/look-continuity.json`: 方向连续性测量
- `qa/<slug>/videos/`: 每个状态的 mp4 预览
- `pets/hei-mao/`: 根角色包
- `qa/hei-mao/`: 根角色的独立验证与视觉复核证据
- `pets/hei-mao-quality/`: 已验证的品控官角色包
- `qa/hei-mao-quality/`: 品控官 v5 的独立验证、盲测投票与视觉复核证据
- `pets/hei-mao-butler/`: 已验证的大管家角色包
- `qa/hei-mao-butler/`: 大管家 v2 的独立验证与视觉复核证据
- `pets/hei-mao-chef/`: 已验证的厨师角色包（Petdex 待审核）
- `qa/hei-mao-chef/`: 厨师 v2 的独立验证与视觉复核证据
- `pets/hei-mao-foodie/`: 已通过最终视觉 QA 的美食家 v2 角色包
- `qa/hei-mao-foodie/`: 美食家 v2 的结构、方向和视觉复核证据
- `pets/hei-mao-delivery/`: 已通过最终视觉 QA 的配送员 v2 角色包
- `qa/hei-mao-delivery/`: 配送员 v2 的结构、方向、alpha 复核和视觉证据
- `qa/petdex-desktop-live-smoke-20260809.json`: Petdex Desktop 单角色实时烟测；不替代 Codex App 全量验收
- `qa/petdex-desktop-live-smoke-20260810.json`: Desktop 0.6.0 hook stdin 退出门禁与发布集复核；发现宿主保持 stdin 打开时原生 hook 仍会等待 EOF，不能据此宣称 App 验收完成
- `qa/petdex-multidisplay-recheck-20260810.json`: 双显示器实时窗口复核；Petdex 窗口可显示在另一块屏幕，但跨屏移动后气泡与宠物重叠，Codex App 多角色验收仍被阻断
- `qa/v2-contract-recheck-20260809.json`: 本轮五个角色的 v2 合同、安装一致性和技能测试复核
- `qa/v2-contract-recheck-20260810.json`: foodie 修复前的历史 v2 合同和视觉阻断快照
- `qa/current-package-install-recheck-20260810.json`: foodie 修复前的历史四角色安装一致性快照
- `qa/foodie-install-recheck-20260810.json`: foodie 修复后的 v2 合同、安装器、本机双目录一致性和公开文件卫生复核
- `qa/current-local-gate-recheck-20260810.json`: 基于当前提交重新执行的 v2 合同、hatch-pet 测试、安装器允许/拒绝路径、双目录一致性和公开文件卫生复核
- `qa/current-release-gate-recheck-20260810-v2.json`: 提交 `a8db02d` 下五个角色的 v2 合同、实际双平台安装器隔离 smoke、28 项技能测试、双目录 SHA 和公开文件复核；Codex App 实时验收仍未完成
- `qa/current-release-gate-recheck-20260810.json`: 提交 `d1a849d` 下使用专用运行时的五角色 v2 合同、28 项技能测试、安装器解析和本机双目录 SHA 复核
- `qa/local-release-hygiene-recheck-20260810.json`: 最新角色身份、历史 slug 隔离、本机双目录 SHA、一键安装器和公开文件卫生复核
- `qa/remote-install-source-recheck-20260810.json`: GitHub/GitLab main、raw 下载源和安装器拒绝路径复核
- `qa/remote-main-sync-recheck-20260810.json`: GitHub/GitLab `main` 同提交、公开 raw 文件可用性和工作树同步复核
- `qa/remote-release-source-recheck-20260810.json`: 基于 `82480ab` 的 GitHub/GitLab raw 文件、Petdex manifest/资源、PR #654 和正式路由即时复核
- `qa/imagegen-channel-recheck-20260810.json`: 本地生图 Agent 的 capabilities、runtime、契约、历史 smoke 和本轮失败生成请求复核；当前新角色生成保持阻断
- `qa/imagegen-channel-recheck-20260812.json`: 本地 Docker 生图服务的当前 capabilities、runtime、两条启用路径真实 smoke 和新角色生成阻断复核
- `qa/petdex-sync-recheck-20260809.json`: Petdex manifest、编辑接口和 PR #654 状态复核
- `qa/petdex-sync-recheck-20260810.json`: 最新 Petdex manifest、编辑接口和 PR #654 状态复核
- `qa/remote-petdex-pr-recheck-20260810.json`: 当前 Petdex manifest、公开资源 SHA、编辑路由和 PR #654 最新审查/部署状态复核
- `qa/petdex-live-install-recheck-20260810.json`: Petdex 1.2.0 当前 manifest、隔离安装、公开资源 SHA 漂移和 `doctor` 移除状态复核
- `qa/petdex-edit-route-recheck-20260810.json`: PR #654 当前检查、Vercel 授权阻断和正式编辑接口状态复核
- `qa/petdex-pr-654-merge-recheck-20260810.json`: PR #654 已合并、生产编辑路由已部署及剩余 v2 同步门禁复核
- `qa/cross-platform-installer-recheck-20260810.json`: Windows 10 PowerShell 5.1 与 Linux x86_64 隔离安装器复核及远端网络可达性结果
- `qa/active-selection-recheck-20260810.json`: 活动角色选择、双目录发布集和 Codex/Petdex Desktop 画面验收边界复核
- `prompts/`: 生成 base 和各动画行时使用的提示词
- `pet_request.json`: 本次宠物生成请求配置

## 验证结果

本包已通过 hatch-pet 校验：

- `pets/hei-mao/spritesheet.webp`: `WEBP` / `RGBA`
- `spriteVersionNumber`: `2`
- 尺寸: `1536x2288`
- 单元格: `192x208`
- `qa/hei-mao/validation.json`: `ok: true`
- `qa/hei-mao/review.json`: `ok: true`
- `qa/hei-mao/direction-blind-validation.json`: `ok: true`
- 错误: 0
- 图集透明 RGB 残留: 0
- 独立最终视觉复核: WARN（无 BLOCK）；247.5 -> 270、337.5 -> 000 为较大但可接受的方向过渡，000 的 y=12 透明行保留在连续性报告中

## 动画状态

- `idle`: 6 帧
- `running-right`: 8 帧
- `running-left`: 8 帧
- `waving`: 4 帧
- `jumping`: 5 帧
- `failed`: 8 帧
- `waiting`: 6 帧
- `running`: 6 帧
- `review`: 6 帧

## 备注

`running-left` 为单独生成，不是从 `running-right` 镜像派生，以避免破坏黑毛单肩背带裤的方向特征。

### 品控官 v5 验证结果

- `pets/hei-mao-quality/spritesheet.webp`: `WEBP` / `RGBA`，SHA-256 为 `1e22f95b918ab423d1b4bede9af93761e89ff39c5a961ee3728c671b0dd05f9f`
- 尺寸 `1536x2288`，单元格 `192x208`，`spriteVersionNumber: 2`
- quality 图集使用洋红色抠像键 `#FF00FF`；独立复核时运行 `validate_atlas.py --require-v2 --chroma-key '#FF00FF' pets/hei-mao-quality/spritesheet.webp`
- `qa/hei-mao-quality/validation.json`: `ok: true`，错误 0，透明 RGB 残留 0
- `qa/hei-mao-quality/chroma-despill.json`: `ok: true`，单次边缘色键去溢完成
- `qa/hei-mao-quality/direction-blind-validation.json`: `ok: true`，`000=up`、`180=down`、`270=screen-left` 硬门禁通过
- `qa/hei-mao-quality/final-visual-qa.json`: `visual_qa: pass`，无需要修复的行
- 连续性指标在 `157.5 -> 180` 与 `337.5 -> 000` 处有已复核的边界警告；正常尺寸下未见跳变、比例突变、身份变化或错误象限

### 大管家 v2 验证结果

- `pets/hei-mao-butler/spritesheet.webp`: `WEBP` / `RGBA`，SHA-256 为 `1e59bcd0024b4f381e740655e2457df490773e7038ea3f77f073f3ac5ca46304`
- 尺寸 `1536x2288`，单元格 `192x208`，`spriteVersionNumber: 2`
- `qa/hei-mao-butler/validation.json`: `ok: true`，错误 0，透明 RGB 残留 0
- `qa/hei-mao-butler/chroma-despill.json`: `ok: true`，单次边缘色键去溢完成
- `qa/hei-mao-butler/direction-blind-validation.json`: `ok: true`，四个 cardinal 硬门禁通过
- `qa/hei-mao-butler/final-visual-qa.json`: `pass_with_reviewed_warnings`，无需要修复的动作行
- 中间/背面方向的次轴提示较弱，且连续性报告有局部离群值；独立正常尺寸复核未见跳帧、裁切、透明洞、比例突变或方向反转

### 厨师 v2 验证结果

- `pets/hei-mao-chef/spritesheet.webp`: `WEBP` / `RGBA`，SHA-256 为 `32a4df73b3ecc58c0f1488025a841fb7be7c93127d3f0134f22d6c799580d957`
- 尺寸 `1536x2288`，单元格 `192x208`，`spriteVersionNumber: 2`
- `qa/hei-mao-chef/validation.json`: `ok: true`，错误 0，透明 RGB 残留 0
- `qa/hei-mao-chef/chroma-despill.json`: `ok: true`，单次边缘色键去溢完成
- `qa/hei-mao-chef/direction-blind-validation.json`: `ok: true`，四个 cardinal 硬门禁通过
- `qa/hei-mao-chef/final-visual-qa.json`: `pass_with_reviewed_warnings`，无需要修复的动作行
- 连续性告警集中在 `157.5 -> 180`、`225 -> 247.5`、`247.5 -> 270` 和 `337.5 -> 000`；正常尺寸下未见跳帧、裁切、比例突变、身份漂移或方向反转

### 美食家 v2 验证结果

- `pets/hei-mao-foodie/spritesheet.webp`: `WEBP` / `RGBA`，SHA-256 为 `9ceb0e1411e3036fc496d70b8283bf11483bdcf589a340f68f3e4b47983b3d23`
- `pets/hei-mao-foodie/pet.json`: SHA-256 为 `0857baacd1dbb5912ceb03a5fc4cadf121923f6d04190b9356f7588f82410a6c`
- `spriteVersionNumber: 2`，尺寸 `1536x2288`，单元格 `192x208`
- `qa/hei-mao-foodie/validation.json`: `ok: true`，错误 0，透明 RGB 残留 0
- `qa/hei-mao-foodie/chroma-despill.json`: `ok: true`，单次边缘色键去溢完成
- `qa/hei-mao-foodie/direction-blind-validation.json`: `ok: true`，四个 cardinal 硬门禁通过
- `qa/hei-mao-foodie/final-visual-qa.json`: `pass`，waiting 行完整重生成后无 detached effects；独立视觉复核记录 minor warning

### 配送员 v2 验证结果

- `pets/hei-mao-delivery/spritesheet.webp`: `WEBP` / `RGBA`，SHA-256 为 `ac742c253567d84d71541941853c4e536a77bb1686349512d14ab86e5f91aa0a`
- `pets/hei-mao-delivery/pet.json`: SHA-256 为 `16e5e9aaf0033e4676b7a298f55562607382a1a1d1fbe7ecf4377ffcd86c46a2`
- `spriteVersionNumber: 2`，尺寸 `1536x2288`，单元格 `192x208`
- `qa/hei-mao-delivery/validation.json`: `ok: true`，错误 0，透明 RGB 残留 0
- `qa/hei-mao-delivery/chroma-despill.json`: `ok: true`，单次边缘色键去溢完成
- `qa/hei-mao-delivery/direction-blind-validation.json`: `ok: true`，四个 cardinal 硬门禁通过
- `qa/hei-mao-delivery/final-visual-qa.json`: `pass_with_reviewed_warnings`；耳间开放负空间和局部连续性告警已由独立复核与 alpha 连通性证据确认，不存在封闭透明洞或方向反转
- `qa/petdex-delivery-submit-20260811.json`: Petdex 提交已接受，当前 `held_for_review`

## 许可

- 本仓库采用分离许可，详见[许可说明](LICENSE)。
- `install.sh`、`install.ps1` 及其独立功能性代码采用 [Apache License 2.0](LICENSES/Apache-2.0.txt)。
- 钱大妈、黑毛及相关角色图集、图片、视频、品牌描述和生成提示词不属于 Apache-2.0 授权范围，适用[品牌资产使用条款](ASSETS-LICENSE.md)。
- Apache-2.0 和品牌资产使用条款均不授予钱大妈或黑毛相关商标权。
