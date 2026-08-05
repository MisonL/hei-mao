# 黑毛 Codex Pet

钱大妈品牌 IP “黑毛”的 Codex App 自定义宠物包。

“黑毛”是[钱大妈官网公开发布的品牌 IP 角色](https://www.qdama.cn/brandIP)。本项目由钱大妈员工基于公开品牌形象制作，用于本地 Codex App 个性化展示，不代表钱大妈官方软件产品或技术支持承诺。

## 预览

![contact sheet](qa/contact-sheet.png)

## 安装

### Petdex 安装

当前根包已在 Petdex 上线，可在已安装 Node.js 20 或更高版本的 macOS、Linux 或 Windows 上运行：

```bash
npx -y petdex@latest install hei-mao
```

Petdex CLI 会同时安装到 Petdex Desktop 与 Codex App 的宠物目录：

```text
~/.petdex/pets/hei-mao
~/.codex/pets/hei-mao
```

### 品控官角色

`hei-mao-quality` 是黑毛的品控官角色包，已完成完整的 v2 图集、方向连续性、三份独立方向盲测和最终视觉复核。

Petdex 上已存在同名条目，但当前线上资源仍是旧版。本次使用 `petdex edit` 提交 v5 时，资源上传成功，生产编辑提交接口仍返回 HTML 404，因此不能把线上条目视为已同步。不要使用 `petdex submit` 创建重复条目；待上游编辑接口部署完成后，再对现有 slug 执行编辑。

```bash
npx -y petdex@latest install hei-mao-quality
```

如需从仓库手动安装到 Codex App：

```bash
mkdir -p ~/.codex/pets/hei-mao-quality
cp pets/hei-mao-quality/pet.json pets/hei-mao-quality/spritesheet.webp ~/.codex/pets/hei-mao-quality/
```

### 大管家角色

`hei-mao-butler` 是黑毛的大管家角色包，包含完整的 v2 动画图集和 16 个观察方向的独立 QA 证据。

```bash
npx -y petdex@latest install hei-mao-butler
```

本地验收或 Petdex 条目同步前，可手动安装仓库中的已验证包：

```bash
mkdir -p ~/.codex/pets/hei-mao-butler
cp pets/hei-mao-butler/pet.json pets/hei-mao-butler/spritesheet.webp ~/.codex/pets/hei-mao-butler/
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

将本仓库复制到 Codex 自定义宠物目录，或只复制根目录下这两个文件：

```text
pet.json
spritesheet.webp
```

推荐目录结构：

```bash
mkdir -p ~/.codex/pets/hei-mao
cp pet.json spritesheet.webp ~/.codex/pets/hei-mao/
```

然后在 Codex App 中：

1. 打开 `设置 -> 外观 -> 宠物`
2. 点击 `刷新`
3. 在自定义宠物中选择 `黑毛`

## 文件说明

- `pet.json`: Codex App 宠物清单文件
- `spritesheet.webp`: v2 11 行动画精灵图，尺寸 `1536x2288`
- `qa/contact-sheet.png`: 动画帧总览
- `qa/validation.json`: atlas 验证结果
- `qa/review.json`: 帧提取与透明度检查结果
- `qa/look-directions.png`: 16 个观察方向总览
- `qa/direction-blind-validation.json`: 方向盲测结果
- `qa/look-continuity.json`: 方向连续性测量
- `qa/videos/`: 每个状态的 mp4 预览
- `pets/hei-mao-quality/`: 已验证的品控官角色包
- `qa/quality/`: 品控官 v5 的独立验证与视觉复核证据
- `pets/hei-mao-butler/`: 已验证的大管家角色包
- `qa/butler/`: 大管家 v2 的独立验证与视觉复核证据
- `prompts/`: 生成 base 和各动画行时使用的提示词
- `pet_request.json`: 本次宠物生成请求配置

## 验证结果

本包已通过 hatch-pet 校验：

- `spritesheet.webp`: `WEBP` / `RGBA`
- `spriteVersionNumber`: `2`
- 尺寸: `1536x2288`
- 单元格: `192x208`
- `validation.json`: `ok: true`
- `review.json`: `ok: true`
- `direction-blind-validation.json`: `ok: true`
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
- `qa/quality/validation.json`: `ok: true`，错误 0，透明 RGB 残留 0
- `qa/quality/chroma-despill.json`: `ok: true`，单次边缘色键去溢完成
- `qa/quality/direction-blind-validation.json`: `ok: true`，`000=up`、`180=down`、`270=screen-left` 硬门禁通过
- `qa/quality/final-visual-qa.json`: `visual_qa: pass`，无需要修复的行
- 连续性指标在 `157.5 -> 180` 与 `337.5 -> 000` 处有已复核的边界警告；正常尺寸下未见跳变、比例突变、身份变化或错误象限

### 大管家 v2 验证结果

- `pets/hei-mao-butler/spritesheet.webp`: `WEBP` / `RGBA`，SHA-256 为 `1e59bcd0024b4f381e740655e2457df490773e7038ea3f77f073f3ac5ca46304`
- 尺寸 `1536x2288`，单元格 `192x208`，`spriteVersionNumber: 2`
- `qa/butler/validation.json`: `ok: true`，错误 0，透明 RGB 残留 0
- `qa/butler/chroma-despill.json`: `ok: true`，单次边缘色键去溢完成
- `qa/butler/direction-blind-validation.json`: `ok: true`，四个 cardinal 硬门禁通过
- `qa/butler/final-visual-qa.json`: `pass_with_reviewed_warnings`，无需要修复的动作行
- 中间/背面方向的次轴提示较弱，且连续性报告有局部离群值；独立正常尺寸复核未见跳帧、裁切、透明洞、比例突变或方向反转

## 许可

- 本仓库采用分离许可，详见[许可说明](LICENSE)。
- `install.sh`、`install.ps1` 及其独立功能性代码采用 [Apache License 2.0](LICENSES/Apache-2.0.txt)。
- 钱大妈、黑毛及相关角色图集、图片、视频、品牌描述和生成提示词不属于 Apache-2.0 授权范围，适用[品牌资产使用条款](ASSETS-LICENSE.md)。
- Apache-2.0 和品牌资产使用条款均不授予钱大妈或黑毛相关商标权。
