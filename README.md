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
```

截至本次复核，以上命令会下载 Petdex 当前公开版本：`hei-mao` 和 `hei-mao-quality` 的线上 metadata 或 spritesheet SHA 与本仓库 v2 不一致，`hei-mao-butler` 和 `hei-mao-chef` 的字节与仓库一致。需要使用仓库 v2 图集时，请先使用下方角色安装器或手动复制到 Codex 目录；Petdex 编辑路由部署并完成已登录同步前，不要把线上下载结果当作本仓库 v2。

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
| `hei-mao-foodie`  | 美食家 | 视觉 QA 阻断，暂缓安装 | manifest 可见，字段仍为 v1 |

公开 manifest 当前可见五个角色条目以及历史重复条目 `hei-mao-2`。manifest 中的公开资源仍报告 `spriteVersionNumber: 1`，不能据此宣称本仓库的 v2 版本已经同步。`hei-mao-foodie` 的本地最终视觉 QA 已发现 waiting 行的三个 detached effects，已从安装器白名单和本机 active 安装中移除；生图渠道恢复并完成整行重生成前不得安装或发布。

Petdex CLI 会把成功安装的角色同时写入 Petdex Desktop 与 Codex App 的宠物目录：

```text
~/.petdex/pets/<slug>
~/.codex/pets/<slug>
```

截至 2026-08-09T17:17:39Z，Petdex 公开 manifest 的生成时间为 `2026-08-09T12:33:27.214Z`，总数为 4489，包含 `hei-mao`、`hei-mao-quality`、`hei-mao-butler`、`hei-mao-chef`、`hei-mao-foodie` 和历史重复条目 `hei-mao-2`，这些条目的 manifest 字段均为 `spriteVersionNumber: 1`。公开下载的 sprite SHA-256 依次为 `ee9394b4f794943dd0d364fe2fdd7a4cc1c82dda5765cdbf656357417341997c`、`254402bcebc7eba068f39cc8c2c5f8f511bc5d120c49db7ffb13c9855c4fcb92`、`1e59bcd0024b4f381e740655e2457df490773e7038ea3f77f073f3ac5ca46304`、`32a4df73b3ecc58c0f1488025a841fb7be7c93127d3f0134f22d6c799580d957`、`fd2173bc21c5ca563cadfb1935bb037f08812559fd3d6717c1add7a40d79dc49`；根包和品控官的线上 sprite 与本仓库当前版本不同，其他三个 sprite 字节相同但 manifest 版本字段仍为 v1。最新 CLI 为 `petdex@1.2.0`，其编辑流程使用 `/api/pets/<slug>`、`POST /api/cli/edit-presign` 和 `PATCH /api/my-pets/<id>/edit`；本 PR 提议的 `PATCH /api/cli/edit` 在正式服务仍返回 HTML 404，说明 PR #654 尚未部署。未登录调用 `edit-presign` 返回 JSON 401 属于认证门禁，不能替代已登录端到端验证；本轮未进行外部写入，因此不能将线上 v2 同步标记为完成。`hei-mao-2` 是历史重复条目，不属于当前发布集。完整复核证据见 `qa/petdex-sync-recheck-20260810.json`。

本机当前只保留四个通过 v2 合同和最终视觉门禁的角色，Codex 与 Petdex 两个本地目录的文件集合和 SHA-256 一致；`hei-mao-foodie` 已从两处 active 安装中移除。当前安装复核见 `qa/current-package-install-recheck-20260810.json`。

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

未完成完整 v2 图集和复核的 `hei-mao-delivery`、`hei-mao-fortune`、`hei-mao-traveler` 不在安装器白名单内。`hei-mao-foodie` 虽有图集文件，但最终视觉 QA 因 waiting 行 detached effects 阻断，同样不在安装器白名单内。历史 `hei-mao-recommender` 和 `hei-mao-2` 也不属于当前发布集。历史 slug 的当日复核见 `qa/historical-slug-recheck-20260809.json`。

这三个角色目前没有可发布图集。2026-08-09 的本地生图渠道复核显示能力与契约正常，但没有任何 effective request mode，因此未发送可交付图集，也未把缺图角色加入安装器；复核证据见 `qa/imagegen-channel-recheck-20260809.json`。同一渠道不可用期间，`hei-mao-foodie` 的 waiting 行也不能合法重生成。

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

`hei-mao-foodie` 是黑毛的美食家角色包。结构、透明度、方向盲测和连续性检查已通过，但最终视觉复核发现 waiting 行第 1 帧的悬浮感叹号、第 3 帧的悬浮爱心和第 5 帧的悬浮星光，属于 Hatch Pet 禁止的 detached effects。该包当前为 `fail`，在完整重生成 waiting 行并重新通过最终视觉复核前不得安装或发布。

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
- `pets/hei-mao-foodie/`: 美食家角色包（最终视觉 QA 阻断，待修复）
- `qa/hei-mao-foodie/`: 美食家 v2 的结构验证和视觉阻断证据
- `qa/petdex-desktop-live-smoke-20260809.json`: Petdex Desktop 单角色实时烟测；不替代 Codex App 全量验收
- `qa/petdex-desktop-live-smoke-20260810.json`: Desktop 0.6.0 hook stdin 退出门禁与发布集复核；发现宿主保持 stdin 打开时原生 hook 仍会等待 EOF，不能据此宣称 App 验收完成
- `qa/v2-contract-recheck-20260809.json`: 本轮五个角色的 v2 合同、安装一致性和技能测试复核
- `qa/current-package-install-recheck-20260810.json`: 最新四个发布角色的 v2 合同、安装器、本机双目录一致性和 Petdex 隔离下载安装复核；其中根包与品控官线上资源仍与仓库 SHA 不同
- `qa/petdex-sync-recheck-20260809.json`: Petdex manifest、编辑接口和 PR #654 状态复核
- `qa/petdex-sync-recheck-20260810.json`: 最新 Petdex manifest、编辑接口和 PR #654 状态复核
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

- `pets/hei-mao-foodie/spritesheet.webp`: `WEBP` / `RGBA`，SHA-256 为 `fd2173bc21c5ca563cadfb1935bb037f08812559fd3d6717c1add7a40d79dc49`（当前包仅保留为待修复输入）
- `pets/hei-mao-foodie/pet.json`: SHA-256 为 `0857baacd1dbb5912ceb03a5fc4cadf121923f6d04190b9356f7588f82410a6c`
- `spriteVersionNumber: 2`，尺寸 `1536x2288`，单元格 `192x208`
- `qa/hei-mao-foodie/validation.json`: `ok: true`，错误 0，透明 RGB 残留 0
- `qa/hei-mao-foodie/chroma-despill.json`: `ok: true`，单次边缘色键去溢完成
- `qa/hei-mao-foodie/direction-blind-validation.json`: `ok: true`，四个 cardinal 硬门禁通过
- `qa/hei-mao-foodie/final-visual-qa.json`: `fail`，waiting 行有 3 个 detached effects，阻止安装和发布

## 许可

- 本仓库采用分离许可，详见[许可说明](LICENSE)。
- `install.sh`、`install.ps1` 及其独立功能性代码采用 [Apache License 2.0](LICENSES/Apache-2.0.txt)。
- 钱大妈、黑毛及相关角色图集、图片、视频、品牌描述和生成提示词不属于 Apache-2.0 授权范围，适用[品牌资产使用条款](ASSETS-LICENSE.md)。
- Apache-2.0 和品牌资产使用条款均不授予钱大妈或黑毛相关商标权。
