# 黑毛 Codex Pet

钱大妈品牌 IP“黑毛”的 Codex App 自定义宠物包。

“黑毛”是[钱大妈官网公开发布的品牌 IP 角色](https://www.qdama.cn/brandIP)。本项目由钱大妈员工基于公开品牌形象制作，用于本地 Codex App 个性化展示，不代表钱大妈官方软件产品或技术支持承诺。

## 预览

![黑毛全部动作总览](qa/hei-mao/contact-sheet.png)

以下为当前发布集中的八个角色预览。动画预览取各角色已验证的 `idle` 循环；完整动作和方向复核图见对应的 `qa/<slug>/` 目录。

<table>
  <tr>
    <td align="center">黑毛<br><img src="qa/hei-mao/previews/idle.gif" alt="黑毛" width="144"></td>
    <td align="center">品控官<br><img src="qa/hei-mao-quality/previews/idle.gif" alt="黑毛·品控官" width="144"></td>
    <td align="center">大管家<br><img src="qa/hei-mao-butler/previews/idle.gif" alt="黑毛·大管家" width="144"></td>
    <td align="center">厨师<br><img src="qa/hei-mao-chef/previews/idle.gif" alt="黑毛·厨师" width="144"></td>
  </tr>
  <tr>
    <td align="center">美食家<br><img src="qa/hei-mao-foodie/previews/idle.gif" alt="黑毛·美食家" width="144"></td>
    <td align="center">配送员<br><img src="qa/hei-mao-delivery/previews/idle.gif" alt="黑毛·配送员" width="144"></td>
    <td align="center">福气官<br><img src="qa/hei-mao-fortune/previews/idle.gif" alt="黑毛·福气官" width="144"></td>
    <td align="center">旅行家<br><img src="qa/hei-mao-traveler/previews/idle.gif" alt="黑毛·旅行家" width="144"></td>
  </tr>
</table>

## 快速安装

### PetDex

安装 [PetDex CLI](https://petdex.dev/) 后，使用已有角色 slug 安装：

```bash
npx -y petdex@latest install <slug>
```

可用 slug 和角色名称见下表。不要使用历史 slug `hei-mao-2`，也不要使用 `submit --force` 创建重复条目。

### 安装器

macOS / Linux：

```bash
curl -fsSL https://raw.githubusercontent.com/MisonL/hei-mao/main/install.sh | bash
```

Windows PowerShell：

```powershell
irm https://raw.githubusercontent.com/MisonL/hei-mao/main/install.ps1 | iex
```

不传参数时安装根角色 `hei-mao`。通过 `HEI_MAO_PET_ID` 选择其他已验证角色；安装器会校验固定 SHA，并拒绝未知 slug。例如：

```bash
HEI_MAO_PET_ID=hei-mao-chef curl -fsSL https://raw.githubusercontent.com/MisonL/hei-mao/main/install.sh | HEI_MAO_PET_ID=hei-mao-chef bash
```

安装器默认写入 `~/.codex/pets/<slug>`。需要 PetDex Desktop 时，请使用 `petdex install <slug>`，不要手动复制到未知目录。

### 手动安装

只复制目标角色目录中的两个文件，然后在 Codex App 的“设置 -> 外观 -> 宠物”中刷新并选择角色：

```text
pets/<slug>/pet.json
pets/<slug>/spritesheet.webp
```

## 角色

| slug | 角色 | 定位 |
| --- | --- | --- |
| `hei-mao` | 黑毛 | 根角色，小猪形象 |
| `hei-mao-quality` | 品控官 | 品质检查与稳定性 |
| `hei-mao-butler` | 大管家 | 日常事务与整理 |
| `hei-mao-chef` | 厨师 | 食材与烹饪主题 |
| `hei-mao-foodie` | 美食家 | 美食探索与品尝 |
| `hei-mao-delivery` | 配送员 | 社区食材配送 |
| `hei-mao-fortune` | 福气官 | 新鲜、丰盛与好彩头 |
| `hei-mao-traveler` | 旅行家 | 社区连接与食材探索 |

每个角色均包含独立的 `pet.json` 和 v2 精灵图。标准动作包括 `idle`、`running-right`、`running-left`、`waving`、`jumping`、`failed`、`waiting`、`running` 和 `review`，另有 16 个观察方向。

## 当前验证状态

截至 2026-09-04：

- 本地八个角色均通过 v2 合同：`1536x2288`、`8x11`、RGBA WebP、`spriteVersionNumber: 2`，透明 RGB 残留为 0。
- hatch-pet 基线测试为 `28 passed`；现有 Pillow 弃用警告已记录在 QA 证据中。
- Bash / PowerShell 安装器语法、ShellCheck、八个支持 slug 的隔离安装、固定 SHA 校验和未知 slug 拒绝均通过。
- 仓库、`~/.codex/pets` 和 `~/.petdex/pets` 的八个角色包逐字节一致。
- PetDex 历史重复条目 `hei-mao-2` 已从公开列表、搜索和详情路由移除。五个修复角色的 sprite 更新已进入 `queued_for_admin_review`；审核传播前，线上安装可能仍获取旧图集。
- 静态 QA 不替代 Codex App 的实时刷新、动画播放、多角色显示和跨屏气泡跟随验收。

最新证据和历史过程记录见[QA 与过程记录索引](qa/README.md)。

## 开发与验证

本项目是资产包，没有传统的应用构建步骤。修改安装器后至少运行：

```bash
bash -n install.sh
shellcheck -S warning install.sh
```

修改精灵图时，使用仓库约定的 hatch-pet 运行时和 `validate_atlas.py --require-v2`，并记录对应 QA 证据。不要用裸系统 Python 替代 bundled runtime。

## 文件结构

- `pets/<slug>/`：可分发的 `pet.json` 和 `spritesheet.webp`
- `prompts/`：基础形象和动画行提示词
- `qa/`：验证结果、视觉复核、发布快照和过程记录索引
- `install.sh`、`install.ps1`：macOS / Linux / Windows 安装器
- `ASSETS-LICENSE.md`、`NOTICE`、`LICENSES/`：资产条款、版权声明和代码许可证

## 许可证

- 仓库采用[分离许可](LICENSE)。
- `install.sh`、`install.ps1` 及其独立功能性代码采用 [Apache License 2.0](LICENSES/Apache-2.0.txt)。
- 钱大妈、黑毛及相关角色图集、图片、视频、品牌描述和生成提示词不属于 Apache-2.0 授权范围，适用[品牌资产使用条款](ASSETS-LICENSE.md)。
- Apache-2.0 不授予钱大妈或黑毛相关商标权。
