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
npx -y petdex@latest install hei-mao-delivery
```

2026-08-17（北京时间）复核中 PetDex CLI 为 `1.2.2`。本次 manifest 生成时间为 `2026-08-16T12:22:49.975Z`，共 4523 个条目；当前六个黑毛角色可见，`hei-mao-2` 仍是历史重复条目。今天逐个重试下载的六个公开 `petjson.json` 和图集均为 v2、1536x2288；但 `hei-mao`、`hei-mao-quality` 和 `hei-mao-foodie` 的线上图集 SHA 仍与仓库不同，`hei-mao-quality` 的线上 metadata 也不同，`hei-mao-butler`、`hei-mao-chef` 和 `hei-mao-delivery` 的 metadata/图集均与仓库一致。首次批量探针曾出现 CDN 20 秒传输超时，逐项重试后六个资源均成功；manifest 索引对前五个旧条目仍报告 v1，不能只依据索引版本判断实际资源。`hei-mao-fortune` 与 `hei-mao-traveler` 尚未进入公开 manifest，不能运行对应的 PetDex 在线安装命令。Fortune 的 cardinal 生成重试和上游 502 证据仍保留在历史 QA 中；当前本地包使用通过门禁的 v2 标准行与 row10 v29 候选重新组装，WebP SHA-256 为 `b896e039599c9b9e9aec240cfddcdb38eb1bab463416139465818126d91c35a1`。需要使用仓库 v2 图集时，请使用下方角色安装器；公开资源、重试结果和发布边界见 `qa/current-state-recheck-20260817-v3.json`，历史编辑队列见 `qa/petdex-edit-sync-recheck-20260814.json`。

本机全局 PetDex CLI 已升级并复核为 `1.2.2`；PetDex Desktop 最新公开版本为 `v0.8.0`，官方签名 DMG 已校验并安装到标准 Applications 目录，但本轮没有启动应用，也没有停止或重启任何 Codex 进程。安装与签名证据见 `qa/petdex-desktop-install-recheck-20260814.json`。`petdex bubble` 在 stdin 已收到 payload 但写端保持打开时仍会等待 EOF，#689 仍未修复；本地复现和版本边界见 `qa/petdex-local-cli-recheck-20260814.json`。

Petdex CLI 会同时安装到 Petdex Desktop 与 Codex App 的宠物目录：

```text
~/.petdex/pets/hei-mao
~/.codex/pets/hei-mao
```

### 角色包状态

当前仓库中的角色包如下。每个角色都有独立的 `pet.json`、v2 图集和 QA 证据，不能用其他角色的图集替代；只有没有视觉阻断的角色才会进入安装器白名单。

| slug              | 角色   | 本地状态               | Petdex 状态                |
| ----------------- | ------ | ---------------------- | -------------------------- |
| `hei-mao`         | 黑毛   | 已验证                 | manifest 可见，图集编辑待审核，线上仍为旧资源 |
| `hei-mao-quality` | 品控官 | 已验证                 | manifest 可见，metadata 与图集编辑待审核 |
| `hei-mao-butler`  | 大管家 | 已验证                 | manifest index 为 v1，资源一致 |
| `hei-mao-chef`    | 厨师   | 已验证                 | manifest index 为 v1，资源一致 |
| `hei-mao-foodie`  | 美食家 | v2 已验证，可本地安装 | manifest 可见，图集编辑待审核，线上仍为旧资源 |
| `hei-mao-delivery` | 配送员 | v2 已验证，可本地安装 | manifest 可见，线上 v2 资源已与仓库一致 |
| `hei-mao-fortune` | 福气官 | v2 已验证，可本地安装 | 已提交，等待审核 |
| `hei-mao-traveler` | 旅行家 | v2 已验证，可本地安装 | 已提交，审核中，不在公开 manifest |

公开 manifest 当前包含六个当前角色条目和历史重复条目 `hei-mao-2`，总数为 4523；公开资源下载和 v2 结构验证见 `qa/petdex-live-recheck-20260816-v5.json`。`hei-mao-delivery`、`hei-mao-butler` 和 `hei-mao-chef` 的线上图集与仓库 SHA 一致，`hei-mao`、`hei-mao-quality` 和 `hei-mao-foodie` 的线上图集仍未切换到仓库版本。`hei-mao-fortune` 与 `hei-mao-traveler` 尚未出现在公开 manifest。提交状态和历史编辑记录见 `qa/petdex-fortune-submit-recheck-20260813.json`、`qa/petdex-traveler-submit-recheck-20260814.json` 与 `qa/petdex-edit-sync-recheck-20260814.json`；历史快照只用于追溯。

Petdex CLI 会把成功安装的角色同时写入 Petdex Desktop 与 Codex App 的宠物目录：

```text
~/.petdex/pets/<slug>
~/.codex/pets/<slug>
```

此前的 2026-08-10、2026-08-13 和 v2-v35 复核快照仍保留在对应 `qa/` 文件中，仅用于追溯历史漂移，不代表当前线上状态。安装器和本地主线状态以最新的 `qa/current-state-recheck-20260817-v3.json` 为准，PetDex manifest、公开资源和发布边界以该快照及 `qa/petdex-live-recheck-20260816-v5.json` 为准；Desktop、Hook 和 Codex App 的边界仍以专项证据为背景，不能替代新的线上发布结论。

本机当前保留八个通过 v2 合同和最终视觉门禁的角色，仓库、Codex 与 PetDex 三个本地目录的文件集合和 SHA-256 一致。2026-08-17（北京时间）按各角色实际色键使用 hatch-pet 精确 runtime 重新执行的八包结构门禁、连续性、28 项测试、安装器静态检查和 parity，以及双远端一致性见 `qa/current-state-recheck-20260817-v3.json`；视觉 warning 和 App 边界仍按专项证据标注，未把不可见的 App 设置视图误报为完成。此前 2026-08-14 的详细证据仍用于追溯。Traveler 的独立门禁和双目录复核见 `qa/hei-mao-traveler/run-summary.json`。`hei-mao-delivery` 的正式包复核见 `qa/hei-mao-delivery/run-summary.json`，`hei-mao-fortune` 的最新图集与双目录复核见 `qa/hei-mao-fortune/run-summary.json`，其余角色的历史门禁复核见 `qa/current-v2-gate-recheck-20260813.json` 和 `qa/all-roles-v2-keyed-recheck-20260813.json`。

本轮本地安装器隔离验证已通过 Shell 和 PowerShell 的八个角色，并确认未知 slug 不会写入；最新安装器和本地主线证据见 `qa/current-state-recheck-20260817-v3.json`，当前 manifest、公开资源和发布边界见同一快照及 `qa/petdex-live-recheck-20260816-v5.json`。Traveler 独立图集证据见 `qa/hei-mao-traveler/run-summary.json`。Petdex Desktop `v0.8.0` 已完成官方签名校验、标准目录安装、Pets 设置可见性、动画帧变化、角色切换和双屏气泡跟随复测；已验证旅行家切换到厨师后恢复旅行家，宠物从副屏移动到主屏时气泡同步移动且保持间距，运行证据见 `qa/petdex-desktop-live-recheck-20260814-v3.json` 和 `qa/petdex-desktop-multidisplay-recheck-20260814-v1.json`。本机 Codex App 当前只读边界见 `qa/codex-app-boundary-recheck-20260816.json`，尚未暴露宠物设置视图。PetDex PR #662（跨屏气泡锚定）和 #667（气泡与宠物间距）已合并；PR #583 已修复大输入排空和 EPIPE，但 #689 的宿主不关闭 stdin、持续等待 EOF 是不同问题，目前仍待上游修复。

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

`hei-mao-fortune` 和 `hei-mao-traveler` 均已完成本地 v2 图集、结构门禁和视觉 QA，并加入安装器白名单；二者均已提交 PetDex，当前处于审核队列，公开 manifest 尚未出现，因此不能使用 PetDex 在线安装命令。历史 `hei-mao-recommender` 和 `hei-mao-2` 也不属于当前发布集；三处本地目录没有这两个历史 slug 的残留。历史 slug 的最新复核见 `qa/historical-slug-recheck-20260816.json`。

`hei-mao-traveler` 是黑毛的小旅行家角色，使用红色旅行背心、绿色蔬菜纹样背包、叶菜和小福袋表达社区探访与新鲜食材探索。其 11 行 v2 图集已完成单次 despill、透明度验证、三份独立方向盲测、连续性复核和最终视觉 QA；中间方向的盲测分歧与连续性 outlier 均按 minor warning 记录，四个 cardinal、身份、比例、回环和透明主体检查通过。当前仅可通过仓库安装器安装；PetDex 条目已提交并在审核队列中，公开 manifest 尚未出现。

本地手动安装角色时：

```bash
mkdir -p ~/.codex/pets/hei-mao
cp pets/hei-mao/pet.json pets/hei-mao/spritesheet.webp ~/.codex/pets/hei-mao/
```

Fortune 角色的本地安装：

```bash
HEI_MAO_PET_ID=hei-mao-fortune curl -fsSL https://raw.githubusercontent.com/MisonL/hei-mao/main/install.sh | HEI_MAO_PET_ID=hei-mao-fortune bash
```

Traveler 角色的本地安装：

```bash
HEI_MAO_PET_ID=hei-mao-traveler curl -fsSL https://raw.githubusercontent.com/MisonL/hei-mao/main/install.sh | HEI_MAO_PET_ID=hei-mao-traveler bash
```

### 大管家角色

`hei-mao-butler` 包含完整的 v2 动画图集和 16 个观察方向的独立 QA 证据。Petdex manifest 已公开该角色，线上 metadata 和精灵图与仓库一致；manifest 索引仍标为 v1，需要仓库 v2 图集时使用仓库安装器。

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

`hei-mao-delivery` 是黑毛的社区配送角色包，已通过 v2 图集、透明度、方向盲测和独立视觉复核。连续性报告中的耳间开放负空间和局部数值告警均已按 minor review resolution 复核，没有封闭透明洞、裁切、身份漂移、比例跳变或方向反转。当前仓库安装器已纳入该角色；Petdex manifest 已公开其 v2 metadata，线上 metadata 和精灵图均已与仓库 SHA 一致。

本地安装：

```bash
HEI_MAO_PET_ID=hei-mao-delivery curl -fsSL https://raw.githubusercontent.com/MisonL/hei-mao/main/install.sh | HEI_MAO_PET_ID=hei-mao-delivery bash
```

Petdex 在线安装：

```bash
npx -y petdex@latest install hei-mao-delivery
```

当前线上资源已与仓库 v2 SHA 一致；需要固定 SHA 的已验证图集时仍可使用上面的仓库安装器。

### 福气官角色

`hei-mao-fortune` 是黑毛的福气官角色包，使用红金服饰、爱心手套、屏幕右侧粮篮和屏幕左侧南瓜表达新鲜、丰盛和每日好彩头。当前包由通过 v2 门禁的标准动作行与 row10 v29 coherent 候选重新组装，已通过单次 despill、9 个标准动作行、16 个方向、三份独立盲测和最终视觉复核；方向连续性中的局部 outlier 已记录为 minor warning，没有身份漂移、比例跳变、封闭透明洞、青色色键残留或方向反转。最新图集 SHA-256 为 `b896e039599c9b9e9aec240cfddcdb38eb1bab463416139465818126d91c35a1`，证据见 `qa/hei-mao-fortune/run-summary.json`。cardinal 生成重试的上游 502 记录仍保留在 `qa/fortune-cardinal-generation-recheck-20260816-v3.json`，失败尝试没有覆盖已验收图集。

本地安装：

```bash
HEI_MAO_PET_ID=hei-mao-fortune curl -fsSL https://raw.githubusercontent.com/MisonL/hei-mao/main/install.sh | HEI_MAO_PET_ID=hei-mao-fortune bash
```

Petdex 发布状态：已提交，当前审核中。提交结果为 `1 submitted, 0 failed`，审核状态为 `held_for_review`，审核备注为 `possible policy issue`；2026-08-16 按 owned-slug 规则尝试更新时返回 `409 pet_not_editable` 且状态为 `pending`，未替换线上资源，也没有重复 submit。当前公开 manifest 尚未出现该条目，因此仍不能运行 `npx -y petdex@latest install hei-mao-fortune`。提交和编辑状态分别见 `qa/petdex-fortune-submit-recheck-20260813.json` 与 `qa/petdex-fortune-edit-recheck-20260816.json`；此前未登录时在上传前阻断的历史记录见 `qa/petdex-fortune-submit-blocked-20260813.json`。

### 品控官角色

`hei-mao-quality` 是黑毛的品控官角色包，已完成完整的 v2 图集、方向连续性、三份独立方向盲测和最终视觉复核。

Petdex 安装：

```bash
npx -y petdex@latest install hei-mao-quality
```

### 旅行家角色

`hei-mao-traveler` 是黑毛的小旅行家角色，使用红色旅行背心、绿色蔬菜纹样背包、叶菜和福袋表达社区探访与新鲜食材探索。其 11 行 v2 图集已完成单次 despill、透明度验证、三份独立方向盲测、连续性复核和最终视觉 QA；中间方向的盲测分歧与连续性 outlier 均按 minor warning 记录，四个 cardinal、身份、比例、回环和透明主体检查通过。

仓库安装器已固定 Traveler 图集 SHA-256 `68ca886f057a6d9ef931c2f3095d9d1f412c5cd8921ed9dd7618f9845a068592`，Shell 和 PowerShell 的隔离安装均已复核通过。

本地安装：

```bash
HEI_MAO_PET_ID=hei-mao-traveler curl -fsSL https://raw.githubusercontent.com/MisonL/hei-mao/main/install.sh | HEI_MAO_PET_ID=hei-mao-traveler bash
```

Petdex 发布状态：已提交，当前审核中。提交结果为 `1 submitted, 0 failed`，审核状态为 `held_for_review`，审核备注为 `possible policy issue`；当前公开 manifest 尚未出现该条目，因此仍不能运行 `npx -y petdex@latest install hei-mao-traveler`。提交状态见 `qa/petdex-traveler-submit-recheck-20260814.json`。

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
- `qa/<slug>/previews/*.gif`: 标准状态动画预览
- `qa/<slug>/preview-generation.json`（存在时）: 标准状态预览的相对路径、帧数和来源 SHA
- `qa/<slug>/look-mechanics.md`: 角色专属的 16 方向视线、锚点和道具跟随规则
- `qa/<slug>/run-summary.json`: 当前图集、结构门禁、视觉复核、方向 QA 和预览证据索引
- `qa/<slug>/validation.json`: atlas 验证结果
- `qa/<slug>/review.json`: 帧提取与透明度检查结果
- `qa/<slug>/look-directions.png`: 16 个观察方向总览
- `qa/<slug>/direction-blind-pairs.png`: 随机化的无标签方向盲测图
- `qa/<slug>/direction-blind-validation.json`: 方向盲测结果
- `qa/<slug>/direction-blind-verdicts-*.json`: 三份独立盲测投票与严格多数合并结果
- `qa/<slug>/direction-blind-answer-key.json`: 盲测完成后的隐藏答案记录
- `qa/<slug>/blind-review-resolution.json`: 中间方向 warning 的审查与处理决定
- `qa/<slug>/look-continuity.json`: 方向连续性测量
- `pets/hei-mao/`: 根角色包
- `qa/hei-mao/`: 根角色的独立验证与视觉复核证据
- `pets/hei-mao-quality/`: 已验证的品控官角色包
- `qa/hei-mao-quality/`: 品控官 v5 的独立验证、盲测投票与视觉复核证据
- `pets/hei-mao-butler/`: 已验证的大管家角色包
- `qa/hei-mao-butler/`: 大管家 v2 的独立验证与视觉复核证据
- `pets/hei-mao-chef/`: 已验证的厨师角色包（Petdex manifest 可见，线上资源与仓库一致）
- `qa/hei-mao-chef/`: 厨师 v2 的独立验证与视觉复核证据
- `pets/hei-mao-foodie/`: 已通过最终视觉 QA 的美食家 v2 角色包
- `qa/hei-mao-foodie/`: 美食家 v2 的结构、方向和视觉复核证据
- `pets/hei-mao-delivery/`: 已通过最终视觉 QA 的配送员 v2 角色包
- `qa/hei-mao-delivery/`: 配送员 v2 的结构、方向、alpha 复核和视觉证据
- `pets/hei-mao-fortune/`: 已通过最终视觉 QA 的福气官 v2 角色包
- `qa/hei-mao-fortune/`: 福气官 v2 的结构、方向、盲测、连续性和视觉证据
- `pets/hei-mao-traveler/`: 已通过最终视觉 QA 的旅行家 v2 角色包
- `qa/hei-mao-traveler/`: 旅行家 v2 的结构、方向、盲测、连续性和视觉证据
- `qa/petdex-desktop-live-smoke-20260809.json`: Petdex Desktop 单角色实时烟测；不替代 Codex App 全量验收
- `qa/petdex-desktop-live-smoke-20260810.json`: Desktop 0.6.0 hook stdin 退出门禁与发布集复核；发现宿主保持 stdin 打开时原生 hook 仍会等待 EOF，不能据此宣称 App 验收完成
- `qa/petdex-local-cli-recheck-20260814.json`: 全局 CLI 1.2.2、Desktop v0.8.0 发布边界和 #689 Hook EOF 阻塞复现；不含本机路径或进程标识
- `qa/petdex-desktop-install-recheck-20260814.json`: 官方 Desktop v0.8.0 DMG SHA、签名、公证、标准目录安装和未启动 Codex 边界；不含本机路径或进程标识
- `qa/petdex-desktop-live-recheck-20260814.json`: Desktop v0.8.0 运行烟测、Pets 设置视图、活动角色和未修改 Codex 边界；不含本机路径或进程标识
- `qa/petdex-desktop-live-recheck-20260814-v2.json`: Desktop v0.8.0 动画帧变化、实际活动角色和未修改 Codex 边界；不含本机路径或进程标识
- `qa/petdex-desktop-live-recheck-20260814-v3.json`: Desktop v0.8.0 动画帧变化、旅行家与厨师之间的角色切换和恢复原角色证据；不含本机路径或进程标识
- `qa/petdex-multidisplay-recheck-20260810.json`: 双显示器实时窗口复核；Petdex 窗口可显示在另一块屏幕，但跨屏移动后气泡与宠物重叠，Codex App 多角色验收仍被阻断
- `qa/v2-contract-recheck-20260809.json`: 本轮五个角色的 v2 合同、安装一致性和技能测试复核
- `qa/v2-contract-recheck-20260810.json`: foodie 修复前的历史 v2 合同和视觉阻断快照
- `qa/current-package-install-recheck-20260810.json`: foodie 修复前的历史四角色安装一致性快照
- `qa/foodie-install-recheck-20260810.json`: foodie 修复后的 v2 合同、安装器、本机双目录一致性和公开文件卫生复核
- `qa/current-local-gate-recheck-20260810.json`: 基于当前提交重新执行的 v2 合同、hatch-pet 测试、安装器允许/拒绝路径、双目录一致性和公开文件卫生复核
- `qa/installer-isolation-recheck-20260813.json`: Bash 与 PowerShell 隔离安装器的七角色固定 SHA、历史/阻断 slug 拒绝和临时目标写入复核
- `qa/current-v2-gate-recheck-20260813.json`: 七个当前角色的 v2 atlas、单次 despill、标准动作、方向盲测、连续性和最终视觉 QA 门禁复核
- `qa/current-v2-gate-recheck-20260814-v2.json`: 当前八个角色按实际色键执行的 v2 atlas 结构门禁，全部通过且无透明 RGB 残留、错误或警告
- `qa/three-directory-parity-recheck-20260814-v1.json`: 仓库、Codex 和 PetDex 三个本地目录的八角色文件集合、metadata 和 SHA-256 一致性复核
- `qa/all-roles-v2-keyed-recheck-20260813.json`: 使用各角色实际抠像键重新执行的七角色 v2 结构、透明度和双目录 SHA 一致性复核
- `qa/current-release-gate-recheck-20260810-v2.json`: 提交 `a8db02d` 下五个角色的 v2 合同、实际双平台安装器隔离 smoke、28 项技能测试、双目录 SHA 和公开文件复核；Codex App 实时验收仍未完成
- `qa/current-release-gate-recheck-20260810.json`: 提交 `d1a849d` 下使用专用运行时的五角色 v2 合同、28 项技能测试、安装器解析和本机双目录 SHA 复核
- `qa/local-release-hygiene-recheck-20260810.json`: 最新角色身份、历史 slug 隔离、本机双目录 SHA、一键安装器和公开文件卫生复核
- `qa/remote-install-source-recheck-20260810.json`: GitHub/GitLab main、raw 下载源和安装器拒绝路径复核
- `qa/remote-main-sync-recheck-20260810.json`: GitHub/GitLab `main` 同提交、公开 raw 文件可用性和工作树同步复核
- `qa/remote-main-sync-recheck-20260813.json`: GitHub/GitLab `main` 远端分支、非强制同步和同步后同提交复核
- `qa/remote-main-sync-recheck-20260813-v2.json`: 本次文档与安装器更新后的 GitHub/GitLab `main` 提交、公开 README raw 内容和工作树一致性复核
- `qa/remote-release-source-recheck-20260810.json`: 基于 `82480ab` 的 GitHub/GitLab raw 文件、Petdex manifest/资源、PR #654 和正式路由即时复核
- `qa/imagegen-channel-recheck-20260810.json`: 本地生图 Agent 的 capabilities、runtime、契约、历史 smoke 和本轮失败生成请求复核；当前新角色生成保持阻断
- `qa/imagegen-channel-recheck-20260812.json`: 本地 Docker 生图服务的当前 capabilities、runtime、两条启用路径真实 smoke 和新角色生成阻断复核
- `qa/traveler-generation-blocked-20260813.json`: Traveler 生成前置服务连接拒绝时的历史安全阻断记录，不含本机环境信息
- `qa/traveler-generation-recheck-20260813.json`: Traveler 生成服务可达但上游图像路径被 429 限流的历史阻断记录，不含本机环境信息
- `qa/traveler-generation-recheck-20260813-v3.json`: Traveler 使用全新幂等键的历史生成阻断记录；上游返回 429，未产生图像，不含本机环境信息
- `qa/traveler-generation-recheck-20260814.json`: Traveler 当前生成阻断记录；两次页面 SSE 和一次显式 Agent JSON 请求均返回 429，未产生图像，不含本机环境信息
- `qa/traveler-generation-recheck-20260814-v2.json`: Traveler 早期 Agent API 真实编辑阻断记录，仅用于追溯
- `qa/traveler-generation-recheck-20260814-v3.json`: Traveler 页面 SSE 和 Agent JSON 对照阻断记录；两条路径均被上游限流，未产生图像，不含本机环境信息
- `qa/traveler-generation-recheck-20260814-v4.json`: Traveler 最新 Agent JSON 与页面 SSE 对照阻断记录；两条路径均返回 429，未产生 artifact，不含本机环境信息
- `qa/traveler-generation-recheck-20260814-v5.json`: Traveler 默认 Agent JSON、页面 SSE 和显式 Agent SSE 三路径阻断记录；均返回 429，未产生 artifact，不含本机环境信息
- `qa/traveler-generation-recheck-20260814-v6.json`: Traveler 服务编排入口最新真实 smoke 阻断记录；上游返回 429，未产生 artifact，不含本机环境信息
- `qa/current-state-recheck-20260814-v2.json`: 2026-08-14 早期状态快照，仅用于追溯
- `qa/current-state-recheck-20260814-v3.json`: 早期七角色显式色键 v2 门禁快照，仅用于追溯
- `qa/current-state-recheck-20260814-v4.json`: 当前七角色 v2 门禁、28 项测试、三处目录 parity、Petdex manifest、Traveler/App 未完成边界和远端一致性复核，不含本机环境信息
- `qa/current-state-recheck-20260814-v5.json`: 当前七角色 v2 门禁、28 项测试、三处目录 parity、跨平台安装器、Petdex manifest、Traveler/App 未完成边界和远端一致性复核，不含本机环境信息
- `qa/current-state-recheck-20260814-v6.json`: 当前七角色发布门禁、Petdex manifest、跨平台安装器、Traveler 双路径阻断、Codex App 未完成边界和远端一致性复核，不含本机环境信息
- `qa/current-state-recheck-20260814-v7.json`: 最新七角色发布门禁、Petdex manifest v3、本机三目录 parity、跨平台安装器、Traveler 双路径阻断、Codex App 未完成边界和远端一致性复核，不含本机环境信息
- `qa/current-state-recheck-20260814-v8.json`: 最新七角色发布门禁、Petdex manifest v3、本机三目录 parity、跨平台安装器、Traveler 新一轮双路径阻断、Codex App 未完成边界和远端一致性复核，不含本机环境信息
- `qa/current-state-recheck-20260814-v9.json`: 最新七角色发布门禁、Petdex manifest v3、本机三目录 parity、跨平台安装器、Traveler 三路径阻断、Codex App 未完成边界和远端一致性复核，不含本机环境信息
- `qa/current-state-recheck-20260814-v10.json`: post-commit 最新七角色发布门禁、Petdex manifest v3、本机三目录 parity、跨平台安装器、Traveler 三路径阻断、Codex App 未完成边界和远端一致性复核，不含本机环境信息
- `qa/current-state-recheck-20260814-v11.json`: 最新七角色逐包 v2 门禁、28 项测试、Petdex manifest v4、Traveler 服务编排阻断、Codex App 未完成边界和远端一致性复核，不含本机环境信息
- `qa/current-state-recheck-20260814-v12.json`: 最终七角色逐包 v2 门禁、28 项测试、Petdex CLI 登录与 telemetry 状态、三目录 parity、Traveler 阻断、Codex App 窗口边界和远端一致性复核，不含本机环境信息
- `qa/current-state-recheck-20260814-v13.json`: 八角色早期状态快照，仅用于追溯
- `qa/current-state-recheck-20260814-v15.json`: 当前八角色本地发布门禁、PetDex 编辑审核边界、三处目录 parity、远端一致性和 Codex App 视觉验收边界，不含本机环境信息
- `qa/current-state-recheck-20260814-v16.json`: 以当前远端同步提交为基线的八角色发布门禁、PetDex 资源/编辑边界、三处目录 parity、远端一致性和 Codex App 视觉验收边界，不含本机环境信息
- `qa/current-state-recheck-20260814-v17.json`: 2026-08-14 早期八角色发布门禁和 PetDex 边界快照，仅用于追溯，不含本机环境信息
- `qa/current-state-recheck-20260814-v18.json`: 2026-08-14 早期八角色发布门禁、PetDex 资源/编辑边界和上游 issue/PR 状态快照，仅用于追溯，不含本机环境信息
- `qa/current-state-recheck-20260814-v19.json`: 当前八角色发布门禁、QA 媒体完整性、PetDex 资源/编辑边界、上游 issue/PR 状态、CLI/Hook 边界、三处目录 parity、远端一致性和 Codex App 视觉验收边界，不含本机环境信息
- `qa/current-state-recheck-20260814-v20.json`: 官方 Desktop v0.8.0 安装后的八角色发布门禁、PetDex 资源/编辑边界、上游 issue/PR 状态、CLI/Hook 边界、三处目录 parity、远端一致性和 Codex App 视觉验收边界，不含本机环境信息
- `qa/current-state-recheck-20260814-v21.json`: Desktop v0.8.0 运行烟测后的八角色发布门禁、PetDex 资源/编辑边界、上游 issue/PR 状态、CLI/Hook 边界、三处目录 parity、远端一致性和 Codex App 视觉验收边界，不含本机环境信息
- `qa/current-state-recheck-20260814-v22.json`: Desktop v0.8.0 动画烟测后的八角色发布门禁、PetDex 资源/编辑边界、上游 issue/PR 状态、CLI/Hook 边界、三处目录 parity、远端一致性和 Codex App 视觉验收边界，不含本机环境信息
- `qa/current-state-recheck-20260814-v24.json`: Desktop v0.8.0 动画、角色切换和双屏气泡复测后的历史状态快照，仅用于追溯
- `qa/current-state-recheck-20260814-v25.json`: 基于提交 `e843623` 的历史八角色发布门禁和 PetDex 边界快照，仅用于追溯
- `qa/current-state-recheck-20260814-v26.json`: 基于提交 `44e85a9` 的历史八角色门禁、alpha-hole 复核、三处目录 parity、PetDex 公开状态、#583/#689 Hook 边界、远端同步和 Codex App 可访问性边界，不含本机环境信息
- `qa/current-state-recheck-20260814-v27.json`: 基于提交 `ab63934` 的当前八角色门禁、三处目录 parity、实时 PetDex manifest/资源/审核状态、#583/#689 Hook 边界、远端同步和 Codex App 可访问性边界，不含本机环境信息
- `qa/current-state-recheck-20260814-v28.json`: post-push 提交 `30f734a` 的远端一致性、资产基线不变、实时 PetDex 状态、#583/#689 Hook 边界和只读 Codex App 可访问性边界，不含本机环境信息
- `qa/current-state-recheck-20260814-v29.json`: 提交 `9c6be8c` 上的本地八角色安装、实时 PetDex manifest、上游 `main` SHA、#689 stdin 代码证据和 Desktop 边界复核，不含本机环境信息
- `qa/current-state-recheck-20260814-v30.json`: 提交 `ce2b7dc` 上新增跨平台安装器 smoke 后的本地八角色、实时 PetDex、上游 Hook 和 Desktop 边界复核，不含本机环境信息
- `qa/current-state-recheck-20260814-v31.json`: 提交 `4d5fcfd` 上的最新 manifest、本人提交的 GitHub issue/PR、上游 Hook 和本地发布边界复核，不含本机环境信息
- `qa/current-state-recheck-20260814-v32.json`: 提交 `10d426c` 后重启主机的只读 Codex App 边界复核，不含本机环境信息
- `qa/current-state-recheck-20260814-v33.json`: 提交 `d251c42` 上八角色本地包契约、安装器和外部阻断汇总，不含本机环境信息
- `qa/current-state-recheck-20260814-v34.json`: 提交 `b77a134` 上使用精确 hatch-pet runtime 的八角色 v2 门禁和剩余阻断汇总，不含本机环境信息
- `qa/current-state-recheck-20260814-v35.json`: 提交 `d8f9320` 上 hatch-pet 28 项测试、八角色 v2 门禁和剩余阻断汇总，不含本机环境信息
- `qa/current-state-recheck-20260816-v2.json`: 以提交 `cceca66` 为检查基线并记录发布提交 `56ead92`，包含八角色 v2 门禁、hatch-pet 测试、三目录 SHA parity、GitHub/GitLab main 同步和剩余发布阻断，不含本机环境信息
- `qa/current-state-recheck-20260816-v3.json`: 以提交 `9699e72` 为检查基线，记录八角色按实际色键 v2 门禁、28 项测试、安装器、三目录 SHA parity、双远端一致性和剩余发布边界，不含本机环境信息
- `qa/current-state-recheck-20260816-v4.json`: Fortune v2 基础图集纠错后的全角色门禁、盲测、安装器、三目录 parity 和剩余 PetDex/Codex App 边界，不含本机环境信息
- `qa/current-state-recheck-20260816-v5.json`: 八角色当前门禁、Fortune 盲测平票边界、PetDex manifest、Codex App 可访问性和双远端状态汇总，不含本机环境信息
- `qa/current-state-recheck-20260816-v6.json`: 当前提交上的八角色结构/连续性复核、28 项测试、三目录 parity、Shell/PowerShell 隔离安装器和公开发布边界，不含本机环境信息
- `qa/current-state-recheck-20260817-v1.json`: 提交 `a18c063` 上重新执行的八角色 v2 结构/连续性门禁、28 项测试、三目录 parity、双远端一致性、PetDex 公开资源和上游 issue/PR 复探、Codex App 未完成边界，不含本机环境信息
- `qa/current-state-recheck-20260817-v2.json`: 提交 `88d1120` 上重新执行的八角色 v2 结构/连续性门禁、28 项测试、安装器静态检查、三目录 parity、PetDex 资源重试结果、上游 issue/PR 和 Codex App 未完成边界，不含本机环境信息
- `qa/fortune-cardinal-generation-recheck-20260816-v1.json`: Fortune cardinal 两种有效 request mode 的真实失败证据和未产出 artifact 边界，不含本机环境信息
- `qa/fortune-cardinal-generation-recheck-20260816-v2.json`: Fortune cardinal 第五次真实 502 失败、一次未发送的本地预检和只读诊断结果，不含本机环境信息
- `qa/fortune-cardinal-generation-recheck-20260816-v3.json`: Fortune cardinal 新增三次真实 502 失败和未替换正式图集的脱敏边界，不含本机环境信息
- `qa/petdex-fortune-edit-recheck-20260816.json`: Fortune owned-slug 编辑被 PetDex 以 409 `pet_not_editable`/`pending` 拒绝的脱敏结果，不含本机环境信息
- `qa/current-v2-gate-recheck-20260816-v1.json`: 提交 `e9c29e9` 前按每个角色记录的实际色键重新执行八角色 `validate_atlas.py --require-v2`，全部通过且无透明 RGB 残留、错误或警告
- `qa/petdex-live-recheck-20260816-v2.json`: 实时 PetDex manifest、公开资源 HTTP 状态与 SHA 对照、历史重复条目和 Fortune/Traveler 公开边界，不含本机环境信息
- `qa/petdex-live-recheck-20260816-v3.json`: 2026-08-16 06:25 manifest、公开资源 SHA 对照、历史重复条目和 Fortune/Traveler 公开边界，不含本机环境信息
- `qa/petdex-live-recheck-20260816-v4.json`: 2026-08-16 14:24 manifest 刷新、Fortune/Traveler 仍待审核边界和公开资源探针 TLS 超时记录，不含本机环境信息
- `qa/petdex-live-recheck-20260816-v5.json`: 2026-08-16 15:53 manifest、六个公开资源下载/哈希、v2 门禁和 Fortune/Traveler 发布边界，不含本机环境信息
- `qa/installer-cross-platform-recheck-20260814-v4.json`: 提交 `ce2b7dc` 上 Bash/PowerShell 八角色隔离安装、未知 slug 拒绝、ShellCheck 和临时目标清理证据，不含本机环境信息
- `qa/petdex-desktop-multidisplay-recheck-20260814-v1.json`: Desktop v0.8.0 宠物窗口跨屏移动时的气泡跟随、间距和位置恢复证据，不含屏幕截图或本机敏感信息
- `qa/qa-media-completeness-recheck-20260814.json`: 八个角色的标准接触表、根包和大管家标准状态预览、来源 SHA 与公开路径完整性证据
- `qa/current-v2-alpha-review-20260814.json`: 当前提交八个角色的 v2 门禁、look-continuity alpha-hole 候选高对比度复核和透明连通性结论；未发现封闭主体透明洞
- `qa/current-v2-gate-recheck-20260814-v3.json`: 提交 `ab63934` 上使用各角色实际色键重新执行的八角色 `validate_atlas.py --require-v2` 结果，全部通过且无透明 RGB 残留、错误或警告
- `qa/current-v2-gate-recheck-20260814-v4.json`: 提交 `b77a134` 上使用精确 hatch-pet Python runtime 重新执行的八角色 `validate_atlas.py --require-v2` 结果，全部通过且无透明 RGB 残留、错误或警告
- `qa/hatch-pet-runtime-test-recheck-20260814-v1.json`: 提交 `d8f9320` 上使用精确 hatch-pet runtime 运行的 28 项标准测试结果
- `qa/three-directory-parity-recheck-20260814-v2.json`: 提交 `ab63934` 上仓库、Codex 和 PetDex 三个本地目录的八角色文件集合和 SHA-256 一致性复核
- `qa/codex-app-boundary-recheck-20260814-v2.json`: 脱敏的只读 App 可见性检查；目标宠物界面未出现，不代表视觉验收通过
- `qa/codex-app-boundary-recheck-20260814-v3.json`: macOS System Events 只读窗口/菜单栏计数检查；目标宠物界面仍未暴露，不代表视觉验收通过
- `qa/installer-cross-platform-recheck-20260814-v2.json`: Shell 和 PowerShell 七角色隔离安装、SHA 校验、Traveler 拒绝和临时目标清理复核，不含本机环境信息
- `qa/current-local-gate-live-recheck-20260813.json`: 七个角色实时 v2 结构门禁、双目录 SHA 一致性和安装器隔离复核，不含本机环境信息
- `qa/petdex-current-recheck-20260813.json`: 2026-08-13 的 Petdex CLI、manifest、线上资源 SHA、编辑路由、上游合并和相关条目历史复核
- `qa/petdex-current-recheck-20260814.json`: 2026-08-14 早期 Petdex 状态快照，仅用于追溯
- `qa/petdex-current-recheck-20260814-v2.json`: 当前 Petdex manifest、六个公开角色线上 SHA、本机三目录 parity、Fortune/Traveler 发布边界复核
- `qa/petdex-current-recheck-20260814-v3.json`: 最新 Petdex manifest、六个公开角色线上 SHA、本机三目录 parity、Fortune/Traveler 发布边界复核；当前 Petdex 证据
- `qa/petdex-current-recheck-20260814-v4.json`: 最新 Petdex manifest、六个公开角色线上 SHA、本机 v2 SHA 对照、Fortune/Traveler 发布边界复核；当前 Petdex 证据
- `qa/petdex-current-recheck-20260814-v5.json`: 2026-08-14 的历史 Petdex CLI、manifest 和线上资源快照，仅用于追溯
- `qa/petdex-current-recheck-20260814-v7.json`: 实时 `petdex list`、manifest、已有编辑队列、Fortune/Traveler 审核状态和 #689 状态复核
- `qa/petdex-public-resource-recheck-20260814.json`: 2026-08-14 早期公开资源快照，仅用于追溯审核前资源未切换的边界
- `qa/petdex-public-resource-recheck-20260814-v2.json`: 历史公开 manifest 和六个公开角色资源 SHA 快照，仅用于追溯
- `qa/petdex-public-resource-recheck-20260814-v3.json`: 2026-08-14 早期公开 manifest、六个公开角色实际下载资源的 SHA/尺寸和 metadata 字节/语义对照，仅用于追溯
- `qa/petdex-public-resource-recheck-20260814-v4.json`: 历史公开 manifest、六个公开角色实际下载资源的 SHA/尺寸和 metadata 字节/语义对照
- `qa/petdex-public-resource-recheck-20260814-v5.json`: 最新实时公开 manifest、七个 `hei-mao*` 条目和本地角色 CDN SHA 对照
- `qa/codex-app-boundary-recheck-20260814-v4.json`: 重启主机后的只读 Codex App 可访问性边界，不含本机环境信息
- `qa/codex-app-boundary-recheck-20260816.json`: 当前主机只读 System Events 查询；目标 Codex App 宠物设置仍未暴露，不含本机环境信息
- `qa/local-package-contract-recheck-20260814-v5.json`: 八角色 pet.json 契约、三目录 SHA、Bash/PowerShell 安装器和 QA JSON 复核，不含本机环境信息
- `qa/petdex-edit-sync-recheck-20260814.json`: `hei-mao`、`hei-mao-quality` 和 `hei-mao-foodie` 的已有 slug 编辑队列及提交后 manifest 状态
- `qa/petdex-edit-submit-recheck-20260813.json`: `hei-mao`、`hei-mao-quality` 和 `hei-mao-foodie` 的已有 slug 编辑提交、审核队列和提交后 manifest 状态复核
- `qa/petdex-fortune-submit-blocked-20260813.json`: Fortune 提交在未登录状态下于上传前安全阻断的历史记录
- `qa/petdex-fortune-submit-recheck-20260813.json`: Fortune 已提交、等待审核且尚未进入公开 manifest 的当前状态记录
- `qa/petdex-traveler-submit-recheck-20260814.json`: Traveler 已提交、等待审核且尚未进入公开 manifest 的当前状态记录
- `qa/current-local-app-boundary-recheck-20260813.json`: 七角色本地门禁、安装器隔离和 Codex App 实时验收边界复核
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
- `qa/petdex-delivery-submit-20260811.json`: 配送员首次提交的历史记录；当前线上 metadata 和精灵图已与仓库 v2 SHA 一致

## 许可

- 本仓库采用分离许可，详见[许可说明](LICENSE)。
- `install.sh`、`install.ps1` 及其独立功能性代码采用 [Apache License 2.0](LICENSES/Apache-2.0.txt)。
- 钱大妈、黑毛及相关角色图集、图片、视频、品牌描述和生成提示词不属于 Apache-2.0 授权范围，适用[品牌资产使用条款](ASSETS-LICENSE.md)。
- Apache-2.0 和品牌资产使用条款均不授予钱大妈或黑毛相关商标权。
