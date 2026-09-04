# 黑毛 Codex Pet

钱大妈品牌 IP “黑毛”的 Codex App 自定义宠物包。

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

## 安装

本地状态基线快照为 `qa/current-state-recheck-20260903-v1.json`；它记录了历史重复条目清理后的线上传播边界，以及八条完整动作行修复后的本地门禁、三目录同步和安装器回归结果。2026-09-03 重新绑定当前 HEAD 的 v2 门禁、安装器和三目录证据分别见 `qa/current-v2-gate-recheck-20260903-v1.json`、`qa/installer-validation-recheck-20260903-v1.json` 和 `qa/three-directory-parity-recheck-20260903-v1.json`；线上删除传播和公共资源对照见 `qa/petdex-live-recheck-20260903-v2.json`。2026-09-04 五个修复角色的 PetDex edit 重提交及传播边界见 `qa/petdex-edit-resubmission-recheck-20260904-v1.json`，这是当前线上编辑队列的最新记录。

当前状态以 `qa/current-state-recheck-20260903-v1.json`、`qa/petdex-live-recheck-20260903-v2.json`、`qa/petdex-edit-resubmission-recheck-20260904-v1.json`、`qa/current-v2-gate-recheck-20260903-v1.json`、`qa/installer-validation-recheck-20260903-v1.json`、`qa/three-directory-parity-recheck-20260903-v1.json`、`qa/hatch-pet-baseline-recheck-20260903-v1.json`、`qa/visual-review-recheck-20260901-v1.json` 和 `qa/imagegen-channel-recheck-20260901-v1.json` 为准；较早的 QA 快照仅用于历史追溯。

2026-09-01 本轮通过已配置的 `mhapi-image` 图像渠道完成一次真实 smoke，并用同一渠道完成八条完整动作行的候选生成与复核。八个当前角色均通过实际色键 `#FF00FF` 的 v2 门禁（1536x2288、8x11、RGBA WebP、透明 RGB 残留 0），连续性均为 `ok=true`，仅保留已审查的 minor warning。当前仓库、`~/.codex/pets` 和 `~/.petdex/pets` 已同步一致；Bash/PowerShell 八角色隔离安装和未知 slug 拒绝均通过。2026-09-03 复核发现此前五个比例修复图集的安装器 SHA 常量仍指向旧字节，已同步修正 `install.sh` 与 `install.ps1`，并在隔离目录重新验证 8/8 支持角色安装和未知 slug 拒绝。2026-09-04 已通过 `petdex edit` 重新提交五个修复角色的 sprite 与 metadata，均处于 `queued_for_admin_review`，因此在线下载在审核生效前仍可能返回旧图集；不要把本地 parity 当成线上已发布。证据见 `qa/current-v2-gate-recheck-20260903-v1.json`、`qa/installer-validation-recheck-20260903-v1.json`、`qa/petdex-live-recheck-20260903-v2.json` 和 `qa/petdex-edit-resubmission-recheck-20260904-v1.json`。Codex App 的刷新、动画播放、多角色和跨屏气泡仍需用户在 App 内验收。

2026-09-03 用户已在 PetDex 个人页删除历史重复条目 `hei-mao-2`。随后线上传播已完成：manifest 更新为 4674 条，`petdex list`、数据库搜索和 `/pets/hei-mao-2` 均不再返回该 slug，正式 `hei-mao` 和其余 7 个角色保留。8 个当前线上图集实际均通过 v2 门禁，但 5 个比例修复图集的公共 sprite SHA 仍是旧版本。2026-09-04 已按官方 `petdex edit` 重新提交这 5 个角色的 sprite 与 metadata，均进入 `queued_for_admin_review`；审核生效前公开下载仍可能返回旧图集。不要对 `hei-mao-2` 做任何操作，也不要使用 `submit --force` 创建重复 slug。最新脱敏证据见 `qa/petdex-live-recheck-20260903-v2.json` 和 `qa/petdex-edit-resubmission-recheck-20260904-v1.json`。

### 历史复核记录（不覆盖当前状态）

下列 2026-08-31 及更早条目保留用于追溯当时的失败、修复和渠道波动；当前本地包状态以本节上方的 2026-09-03 证据为准，线上删除传播和公共资源状态以 `qa/petdex-live-recheck-20260903-v2.json` 为准。09-01 的资源下载记录 `qa/petdex-live-recheck-20260901-v1.json` 仅用于历史对照。

本节中的“最新”“当前”或“仍待处理”均是对应历史日期的快照措辞，不覆盖文档顶部的当前结论；若历史记录与顶部证据冲突，以顶部 2026-09-03/04 状态和队列复核为准。

2026-08-30 最新复核确认八个当前角色的实际 PetDex metadata 和图集均为 v2、`1536x2288 WebP RGBA`，线上 metadata 与图集 SHA 均与仓库 `8/8` 一致；八角色本地门禁、28 项测试、三目录 SHA、Bash/PowerShell 安装器和公开文件隐私扫描均通过。本机 Hook 包装器与 Desktop v0.9.1 native runner 完成五事件开闭 stdin、分片转发和显式错误码回归；上游 #689 已由合并 PR #752 关闭，#710 仍为未合并 draft；上游主线最新为 `5323e43`（PR #765，仅调整 built-with 首页内容）。采用上游 #757 的图集审计规则复核八个已发布角色，未发现空帧、边缘裁切、几何/比例离群或行级比例异常；Chef 的 failed 行有一处已审查的动作连续性提示，实图未见压扁、裁切或身份漂移。Codex App 的全量刷新、逐角色恢复、四方向、动画回环、多角色选择和跨屏气泡仍需在 App 内由用户完成，不能由静态或 Desktop 证据替代。

2026-08-31 补充视觉复核覆盖 88 行、584 帧，新增多背景小尺寸渲染、运动补偿残差、非相邻相似度图、回环/播放节奏、高对比轮廓和 alpha 边界 Hausdorff/多部位轨迹复核。结构门禁仍为 8/8，但确认八个完整动作行存在视觉硬失败，其中 `hei-mao/jumping`、`hei-mao-quality/jumping`、`hei-mao-foodie/waiting` 和 `hei-mao-delivery/failed` 为重复头部/姿态族切换，`hei-mao-quality/running-left`、`hei-mao-quality/failed`、`hei-mao-traveler/waiting` 和 `hei-mao-traveler/review` 为完整分辨率断开组件或动作结构问题；当前包不是视觉发布就绪状态，必须在生图服务恢复后按完整行重生并重跑全部门禁。证据见 `qa/visual-review-methods-recheck-20260831-v2.json`、`qa/visual-review-methods-recheck-20260831-v6.json` 和 `qa/visual-review-alternative-20260831/visual-review-alternative-20260831-v5.json`。

同日新增扫描线分段与完整分辨率断开组件复核：对每个 alpha 行统计连续横向区间、内部间隙、垂直分段变化，并用扫描线并查集识别低分辨率拓扑检查可能漏掉的断开鞋、叶菜、背包和袋子碎片。正常尺寸及 4x/5x 高对比查看确认 `hei-mao-quality/running-left`、`hei-mao-quality/failed`、`hei-mao-traveler/waiting` 和 `hei-mao-traveler/review` 四个新增完整动作行硬失败；`hei-mao-quality/idle`、`hei-mao-chef/running-left` 和 `hei-mao-traveler/idle` 另有小型断开碎片候选，需随下一次整行重生一并复核。当前包因此仍被八个完整行阻断。证据见 `qa/visual-review-alternative-20260831/scanline-segment-review-20260831-v1.json` 和 `qa/visual-review-alternative-20260831/scanline-segment-manual-review-20260831-v1.json`。

同日新增时间动力学与帧序复核：对 584 帧计算面积、重心、包围盒、基线的插值残差和局部轮廓 IoU，并以“前帧/当前/后帧”边界叠加图检查时间跳变；低分辨率 alpha 连通域仅作为候选信号。该方法未新增硬失败，但再次复现上述四个阻断项；它是静态图集和现有连续性报告之外的补充证据，不替代 Codex App 实际播放验收。证据见 `qa/visual-review-alternative-20260831/visual-review-alternative-20260831-v6.json` 和同目录 `temporal-kinematic-topology-sheet.jpg`。

同日补充左右动作成对复核：将 64 对 `running-right` 帧水平镜像后，与对应 `running-left` 帧按下半身锚点和基线对齐，检查轮廓 IoU、面积/宽高/基线差异和色彩指纹。最高差异来自福气官的侧向篮子与福袋等预期非对称道具；正常尺寸叠加未发现新的比例失衡、裁切、断裂或身份漂移。该方法仅用于证据筛选，不替代方向语义和实际 App 播放验收。证据见 `qa/visual-review-alternative-20260831/directional-pair-review-20260831-v3.json`、`qa/visual-review-alternative-20260831/directional-pair-candidates-v3.jpg` 和 `qa/visual-review-alternative-20260831/directional_pair_review.py`。

2026-08-31 线上只读刷新确认 manifest 已更新为 4672 条（生成时间 `2026-08-30T20:20:37.125Z`）；八个当前角色的实际 metadata、v2 图集和 SHA 仍与仓库 8/8 一致，但 manifest 索引仍有 5/8 个 v1 滞后字段。上游 #689 已由合并 PR #752 关闭，#710 仍为 draft；CLI 1.3.0、Desktop 0.9.1 和主线 `5323e43` 未变化。证据见 `qa/petdex-live-recheck-20260831-v2.json` 和 `qa/petdex-upstream-status-recheck-20260831-v2.json`。

同日真实生图 smoke 以新幂等键串行验证 `images-sse` 和 `images-non-stream`，两条路径均返回上游 503、没有生成 artifact；随后在渠道健康快照显示 healthy 后又以新幂等键复测一次，仍返回 503。本地 Agent 合同和路由诊断通过，但四个视觉硬失败暂不能重生。证据见 `qa/imagegen-channel-recheck-20260831-v2.json` 和 `qa/imagegen-channel-recheck-20260831-v3.json`。

随后再次分别以新幂等键验证 `images-sse` 和 `images-non-stream`，均返回 503；只读诊断确认两个失败请求均已记录、无 artifact，渠道快照虽显示 healthy 但最近失败原因为 `model_not_found`。这表明当前阻断在上游模型/渠道可用性，不是本地 Agent 合同或路由故障。证据见 `qa/imagegen-channel-recheck-20260831-v4.json`。

之后使用全新幂等键再次执行 `images-non-stream` 最小真实 smoke。客户端 60 秒门限先收到 `request_in_progress`，随后按原幂等键只读诊断确认任务已进入终态 `failed`，上游仍为 503、没有 artifact；失败键不复用，正式资产未改变。最新状态见 `qa/imagegen-channel-recheck-20260831-v5.json` 和 `qa/current-state-recheck-20260831-v3.json`。

随后本地 Docker 服务仍报告 healthy，但以两个全新幂等键分别执行官方 Agent 编排的 `images-sse` 与 Agent JSON `images-non-stream` 1K smoke；两条路径均在 `meinianda-image` 渠道返回 `upstream_unavailable / Connection error`，结构化诊断可读且 artifact 数为 0。问题仍在上游可达性，不是本地 Agent 合同或路由配置；视觉修复尚不能启动。证据见 `qa/imagegen-channel-recheck-20260831-v6.json`。

同日按各角色实际 despill 色键重新执行 v2 validator，8/8 通过（1536x2288、RGBA WebP、spriteVersionNumber 2、无错误/警告和透明 RGB 残留）；Bash/PowerShell 安装器八角色隔离安装与未知 slug 拒绝均通过，仓库、`~/.codex/pets` 和 `~/.petdex/pets` 的 16 个资产逐字节一致。轮廓集合叠加、头/下半身消融，以及新增的 alpha 边界 Hausdorff 和多部位轨迹复核再次只确认上述四个既知硬失败，没有新增硬失败。证据见 `qa/v2-contract-recheck-20260831-v1.json`、`qa/installer-validation-recheck-20260831-v1.json`、`qa/three-directory-parity-recheck-20260831-v3.json`、`qa/visual-review-alternative-20260831/visual-review-alternative-20260831-v4.json` 和 `qa/visual-review-alternative-20260831/visual-review-alternative-20260831-v5.json`。

同日又增加显示端压力复核：对 592 个非空帧执行 alpha 阈值稳定性扫描（1/16/64/128/224）、48x52/64x69/96x104 三种小尺寸和 nearest/bilinear/Lanczos 九种采样组合，并查看上半身轮廓在阈值变化下的持久性。候选图只复现两个 jumping 重复头部、foodie waiting 上下堆叠和 delivery failed 姿态族切换四项既知阻断；未发现新的透明边缘、缩放后比例或小尺寸显示硬失败。证据见 `qa/visual-review-alternative-20260831/display-alpha-lobe-review-20260831-v4.json`、`qa/visual-review-alternative-20260831/display-alpha-lobe-candidates-v4.jpg` 和 `qa/visual-review-alternative-20260831/display_alpha_lobe_review.py`。

同日新增图集边界采样与显示闪变复核：按 PetDex `.pet-sprite` 的 width-only `background-size`、`image-rendering: pixelated` 和 `zoom` 渲染约束，对完整图集和隔离 cell 在 0.67/0.83/1.00/1.17/1.33 五种缩放、nearest/bilinear/Lanczos 三种采样器和深浅/高饱和背景下做对照，共覆盖 584 帧、584 个含回环转场和 8760 组采样变体；另在 96x104 显示尺寸分离形状残差与稳定主体颜色残差。候选图人工按正常显示尺寸查看，边界差异均可归因于滤波相位、薄边缘或预期姿态/道具变化，未新增硬失败；现有四个完整动作行阻断仍然有效。该方法是 Pillow 渲染预演，不等同于浏览器 GPU 或 Codex App 实时捕获。证据见 `qa/visual-review-alternative-20260831/css-sampling-flicker-review-20260831.json`、`qa/visual-review-alternative-20260831/css-sampling-flicker-candidates.jpg` 和 `qa/visual-review-alternative-20260831/css_sampling_flicker_review.py`。

同日增加帧序扰动与压缩压力复核：对 584 个使用帧计算 96x104 的全帧、上半身和下半身插值残差，模拟丢帧/重复帧并检查回环节奏，再对时间候选和每行动作参考帧做 WebP 质量 75/50 往返，比较 alpha 保留、可见像素损失、包围盒漂移和 RGB 残差。候选图正常尺寸查看未发现新的硬失败；Quality running、两个 jumping、Foodie waiting 和 Delivery failed 的时间候选均落在已有四项阻断或正常动作变化内，压缩抽样没有可见像素损失候选。该方法是有界的 Pillow/WebP 压力预演，不等同于浏览器 GPU 或 Codex App 实时播放。证据见 `qa/visual-review-alternative-20260831/frame-cadence-compression-review-20260831-v1.json`、`qa/visual-review-alternative-20260831/frame-cadence-compression-candidates-v1.jpg` 和 `qa/visual-review-alternative-20260831/frame_cadence_compression_review.py`。

同日新增真实 Chromium CSS 合成器回放：直接用浏览器加载八个正式 WebP 图集，按 192x208 裁切、width-proportional background-size、`image-rendering: pixelated`、0/0.5px 背景相位、DPR 1/1.5/2 及 0.75x/1x/1.25x 显示尺度渲染，共覆盖 88 行、584 帧和 6 组浏览器变体；候选图、全量图和变体摘要按正常显示尺寸查看，未发现新的邻格采样、裁切、透明边缘或缩放比例硬失败，仅复现上述四个既知动作行阻断。该方法比 Pillow 预演更接近 CSS 合成器，但仍不替代真实 Codex App、GPU 和跨屏验收。证据见 `qa/visual-review-alternative-20260831/browser-css-compositor-review-20260831-v1.json`、同目录 `browser-css-compositor-candidates-v1.png`、`browser-css-compositor-full-v1.png`、`browser-css-compositor-variants-summary-v1.jpg` 和 `browser_css_compositor_review.mjs`。

同日补充稠密光流时序复核：将 584 个使用帧按 96x104 显示尺寸合成到统一背景，对每个动作的相邻帧（含回环）计算主体区域的 Farneback 光流、前后向一致性和运动幅度，并查看带箭头的候选图。该方法额外检查眼睛、头部、道具和材质纹理的实际运动，不只依赖 alpha 轮廓；未新增硬失败，仅再次保留上述四个完整动作行阻断。光流指标是候选证据，不能替代语义判断、浏览器 GPU 或 Codex App 实际播放。证据见 `qa/visual-review-alternative-20260831/dense-optical-flow-review-20260831-v1.json`、`dense-optical-flow-candidates-v1.jpg` 和 `dense_optical_flow_review.py`。

同日新增匿名时序三元组盲测：从既有正交复核候选和分层覆盖中选取 40 个 `PREV/CURRENT/NEXT` 三元组，覆盖 8 个角色、11 类动作和 9 个既知缺陷控制样本；图中隐藏角色、动作、帧号和指标分数，仅保留正常 `192x208` 显示尺寸。主代理回看重现四类既知整行动画缺陷，未发现新增明显硬失败；OMP 无法读取附件，Claude 未认证，因此该方法仍标记为待独立审查，不作为最终视觉通过。证据见 `qa/visual-review-methods-recheck-20260831-v4.json`、`qa/visual-review-alternative-20260831/blind-temporal-triplet-review-20260831-v1.json`、`blind-temporal-triplet-sheet-v1.png` 和 `blind-temporal-triplet-parent-review-20260831-v1.json`。

同日增加跨方法候选共识复核：从比例、拓扑、光流、显示尺寸、DPR、帧序和 CSS 采样七类独立证据中提取 148 个候选元组，保留 43 个至少由两个方法同时指向的交集，并对其中 36 个高优先级元组同时查看 `PREV/CURRENT/NEXT` 和当前帧二值 alpha 轮廓。该交叉层未新增硬失败，再次确认四个既有完整行动画阻断；方法数量只用于筛选，不能替代正常尺寸视觉判断或实际 Codex App 验收。证据见 `qa/visual-review-methods-recheck-20260831-v5.json`、`qa/visual-review-alternative-20260831/cross-method-consensus-review-20260831-v1.json`、`cross-method-consensus-candidates-v1.jpg` 和 `cross_method_consensus_review.py`。

同日增加完整分辨率扫描线/断开组件复核：将每帧 alpha 轮廓拆为横向连续区间，并以扫描线并查集保留缩小拓扑可能丢失的细小断开部件；结合正常尺寸、4x/5x 高对比和 alpha 阈值稳定性人工确认，新增 `hei-mao-quality/running-left`、`hei-mao-quality/failed`、`hei-mao-traveler/waiting` 和 `hei-mao-traveler/review` 四个整行动画硬失败，另记录三个小型碎片候选。证据见 `qa/visual-review-methods-recheck-20260831-v6.json` 和 `qa/visual-review-alternative-20260831/scanline-segment-manual-review-20260831-v1.json`。

同日新增循环复现图与五帧洋葱皮复核：将 584 个使用帧按每行动作的下半身锚点和基线归一化，计算全行非相邻帧的 alpha/亮度/边缘/颜色描述子复现矩阵，并对候选帧叠加前后各两帧的洋葱皮和完整循环缩略带。该方法重新筛出已知的 jumping 重复头、foodie waiting 堆叠轮廓和 delivery failed 姿态族切换；其余候选在正常宠物尺寸下未发现新的断裂、比例突变、错误方向或相位反转。它是补充证据，不替代整行重生、方向语义、连续性或 Codex App 实机验收。证据见 `qa/visual-review-alternative-20260831/cycle-recurrence-review-20260831-v1.json`、`qa/visual-review-alternative-20260831/cycle-recurrence-candidates-v1.jpg`、`qa/visual-review-alternative-20260831/cycle-recurrence-nonblock-candidates-v1.jpg` 和 `qa/visual-review-alternative-20260831/cycle_recurrence_review.py`。

同日新增状态意图与动画退化复核：以统一下半身锚点和基线归一化 584 个帧，比较 alpha/RGB 帧间变化、上/下半身运动分布、循环多样性及与 idle 的距离，筛出 36 个正常尺寸候选并逐项查看。该方法未新增硬失败；低运动量候选仍能看到细微的手部、头部、脚步或道具变化，保留为 warning，不替代动作语义、方向回环和 Codex App 实机验收。证据见 `qa/visual-review-alternative-20260831/state-semantics-review-20260831-v1.json`、`qa/visual-review-alternative-20260831/state-semantics-manual-review-20260831-v1.json`、`qa/visual-review-alternative-20260831/state-semantics-candidates-v1.jpg` 和 `qa/visual-review-alternative-20260831/state_semantics_review.py`。

同日新增跨角色核心身份与比例复核：将 584 个帧按下半身锚点及共同基线对齐，分别提取头脸 alpha 轮廓、上/下身面积比、垂直宽度剖面和固定尺度上身 alpha/RGB 指纹，再与各自 idle 参考及八角色中性队列比较。24 个正常尺寸候选逐项查看后，未发现新的身份漂移、主体压扁、裁切或断开组件；服装、帽子、背包、篮子和手持道具造成的差异均符合角色设定。该方法不清除现有八个整行动画阻断，也不替代整行重生、方向语义或 Codex App 实机验收。证据见 `qa/visual-review-methods-recheck-20260831-v12.json`、`qa/visual-review-alternative-20260831/cross-role-identity-review-20260831-v1.json`、`qa/visual-review-alternative-20260831/cross-role-identity-manual-review-20260831-v1.json`、`qa/visual-review-alternative-20260831/cross-role-identity-candidates-v1.jpg` 和 `qa/visual-review-alternative-20260831/cross_role_identity_review.py`。

### Petdex 安装

下方按日期列出的旧版本与历史 QA 结论仅用于追溯；当前版本和状态以文档顶部列出的 2026-09-03 状态快照及 2026-09-04 编辑队列证据为准。

2026-08-30 运行时复核通过 PetDex 官方 URI 逐一切换 8 个角色并恢复 `hei-mao-traveler`；Desktop 0.9.1 的健康、初始化、状态和 Codex 气泡来源探针均通过。完整 Codex App 刷新、四方向视觉、多个宠物同时显示和跨屏气泡跟随仍需用户在 App 内完成，证据见 `qa/petdex-desktop-runtime-recheck-20260830-v2.json`；Desktop 升级与 Hook 回归见 `qa/petdex-desktop-release-recheck-20260830-v2.json`。

根包已有 Petdex 公开条目；线上资源版本仍以 manifest 为准。已安装 Node.js 20 或更高版本的 macOS、Linux 或 Windows 可运行：

```bash
npx -y petdex@latest install hei-mao
npx -y petdex@latest install hei-mao-butler
npx -y petdex@latest install hei-mao-chef
npx -y petdex@latest install hei-mao-quality
npx -y petdex@latest install hei-mao-foodie
npx -y petdex@latest install hei-mao-delivery
npx -y petdex@latest install hei-mao-fortune
npx -y petdex@latest install hei-mao-traveler
```

以上命令对应八个当前角色的公开 slug；本地工作区和两个安装目录已同步到本轮修复后的图集。线上 manifest/资源状态需以单独的实时刷新证据为准，不能仅凭本地文件推断。

截至 2026-08-31 的下载结果是历史快照，不覆盖后续检查。2026-09-01 的复核记录确认 PetDex CLI 为 `1.3.0`，公开列表为 4674 个条目；该记录中的历史 `hei-mao-2` 状态已由 2026-09-03 的重复条目清理复核更新。当前八个角色的线上状态、公共 sprite SHA 和五条编辑队列以 `qa/petdex-live-recheck-20260903-v2.json` 与 `qa/petdex-edit-resubmission-recheck-20260904-v1.json` 为准；审核生效前通过 `petdex install` 获取的五个修复角色仍可能是旧图。

CLI `1.3.0` 的当前命令面不包含旧版 `init`、`doctor` 或 `select`；安装使用 `petdex install <slug>`，Hook 安装与维护由 PetDex Desktop 的 Settings 管理。不要把 macOS 本机 `petdex-hook-wrapper.mjs` 配置直接复制到 Windows 或 Linux；跨平台安装器只负责角色包和固定 SHA 校验，Hook 仍需按各平台的 Desktop 设置完成。

2026-08-23 最新本机 Docker 复核再次确认生图接口可用：使用项目 `visual-journal-image-agent` 的默认服务端编排入口，显式指定或省略模型时都解析到已验证可用的 `gpt-image-2-1k`，返回一张完整的 `1024x1024 WebP`，下载、严格尺寸和视觉完整性检查通过；临时 artifact 删除后 metadata/content 均返回 404，正式 PetDex 资产未修改。最新脱敏证据见 `qa/imagegen-channel-recheck-20260823-v26.json` 和 `qa/current-state-recheck-20260823-v26.json`。

本轮真实复核确认本地 Docker 生图服务已可用于正式 PetDex 图集尺寸：上游整数取整返回的近似比例图像会在严格阈值内等比补边到 `1536x2288`，明显比例错误仍被拒绝；`gpt-image-2-1k` 实际返回 `1536x2288 WebP`，Artifact 删除后 metadata/content 均返回 404，正式 PetDex 资产未修改。证据见 `qa/imagegen-channel-recheck-20260823-v28.json` 和 `qa/current-state-recheck-20260823-v29.json`。

2026-08-22 复核确认生图服务已恢复：当前 Docker 的 Agent 编排入口和健康渠道接受自定义模型 `gpt-image-2-1k`。`1024x1024` 的中性原创吉祥物和原创猪形吉祥物源参考均经服务端编排和 `images-non-stream` 返回匹配尺寸的 WebP，严格尺寸门禁与视觉完整性通过；使用已批准角色图作为图像参考、配合中性保留指令的页面 SSE 编辑也成功。本次复核中，包含品牌或既有 IP 身份的文字提示词被上游安全审计以 403 拒绝，说明该类文字可能受上游审计限制，不是本地服务故障；客户端不会静默改写提示词，后续品牌图像任务应优先上传已批准角色图并使用中性保留指令。临时 artifact、页面图片和本地临时文件均已清理，正式资产未修改。最新脱敏复核见 `qa/imagegen-channel-recheck-20260822-v29.json` 和 `qa/current-state-recheck-20260822-v38.json`。
2026-08-23 复核确认本地 Docker 生图服务的两条实际客户端路径均可用：Agent 编排的 `images-non-stream` 和页面 SSE 的 `images-sse` 都以 `gpt-image-2-1k` 返回可读取的 `1024x1024` WebP，并通过严格尺寸和视觉完整性检查。清理后两类临时结果均返回 404；本轮没有复现生成阶段的存储读取失败，也未修改正式 PetDex 资产或图像服务源码。双路径证据见 `qa/imagegen-channel-recheck-20260823-v1.json`；本轮 Agent 编排实测见 `qa/imagegen-channel-recheck-20260823-v2.json`。

2026-08-23 最新本机 Docker 复核确认默认服务端编排已切换到实测可用的 `images-sse` 优先级：`gpt-image-2-1k` 的 `n=1`、`1024x1024` 请求返回一张完整 WebP，v26 新鲜 smoke 的显式模型和省略模型两条请求、下载、严格尺寸和视觉检查均通过；临时 artifact 删除后 metadata/content 均返回 404，正式资产未修改。此前非流式路径的提示词审计 503 仍记录为可重试上游边界，未绕过安全审计。最新脱敏证据见 `qa/imagegen-channel-recheck-20260823-v26.json` 和 `qa/current-state-recheck-20260823-v26.json`。当前仓库、`~/.codex/pets` 与 `~/.petdex/pets` 的八角色、16 个资产文件逐字节一致，最新 parity 证据见 `qa/three-directory-parity-recheck-20260830-v2.json`。

本轮再次完成本地 Docker 生图服务的真实生成和编辑复核：服务端编排生成与页面 SSE 编辑均返回 `1024x1024` WebP，下载、尺寸、视觉完整性和精确清理均通过；生成 artifact 和页面图片删除后都返回 404，正式资产未修改。最新脱敏证据见 `qa/imagegen-channel-recheck-20260823-v3.json` 和 `qa/current-state-recheck-20260823-v4.json`。

2026-08-23 最新复核再次使用本地 Docker 的 `gpt-image-2-1k` 完成一次最小真实生成：服务端编排选择 `images-non-stream`，返回 `1024x1024` WebP，下载和视觉检查通过；临时 artifact 删除后 metadata/content 均为 404，正式角色包未修改。脱敏证据见 `qa/imagegen-channel-recheck-20260823-v4.json` 和 `qa/current-state-recheck-20260823-v5.json`。

本轮继续复核确认本地 Docker 的服务端编排入口实际生成 `1024x1024` WebP，临时 artifact 下载、视觉检查、删除和删除后 404 均通过；没有修改正式角色包。五个本机 Codex Hook 事件在包装器下分别通过关闭 stdin 和保持 stdin 打开两组隔离测试；直接 native runner 的开放 stdin EOF 等待仍可复现，因此本机包装器的有界退出是必要的本地缓解，不代表上游 #689 已修复。最新脱敏证据见 `qa/imagegen-channel-recheck-20260823-v2.json`、`qa/petdex-local-hook-wrapper-recheck-20260823-v1.json` 和 `qa/current-state-recheck-20260823-v2.json`。

2026-08-23 最新复核再次用本地 Docker 的 `gpt-image-2-1k` 完成最小真实生成：服务端编排选择 `images-non-stream`，返回可读取的 `1024x1024` WebP，严格尺寸和视觉完整性检查通过；临时 artifact 删除后 metadata/content 均为 404，正式角色包未修改。最新脱敏证据见 `qa/imagegen-channel-recheck-20260823-v5.json` 和 `qa/current-state-recheck-20260823-v6.json`。

2026-08-23 随后用同一服务完成严格留白复核：新的 `gpt-image-2-1k` 请求返回 `1024x1024` WebP，主体完整、双鞋底可见、四周保留绿色色键留白，未见裁切或压扁；artifact 和本地临时文件均已清理，删除后 metadata/content 返回 404，正式角色包未修改。最新脱敏证据见 `qa/imagegen-channel-recheck-20260823-v6.json` 和 `qa/current-state-recheck-20260823-v7.json`。

本轮继续使用本地 Docker 生图服务完成一次全新 `gpt-image-2-1k` 请求：服务端编排选择 `images-non-stream`，返回可读取的 `1024x1024 WebP`，严格尺寸和视觉完整性检查通过；临时 artifact 删除后 metadata/content 均返回 404，本地临时文件已清理，正式角色包未修改。最新脱敏证据见 `qa/imagegen-channel-recheck-20260823-v12.json` 和 `qa/current-state-recheck-20260823-v12.json`。本轮八个 owned-slug 的只读刷新在官方 CLI 会话刷新后通过：8/8 HTTP 200、ID 存在、status=approved 且 display name 完整；未执行 edit、presign、upload 或 submit。

此前使用本地 Docker 的 `gpt-image-2-1k` 完成固定 `1024x1024` 的真实生成；服务端编排选择 `images-non-stream`，返回完整可读 WebP，主体比例和留白检查通过。artifact 删除后 metadata/content 均返回 404，明确的本轮临时文件已移除，正式角色包未修改。历史脱敏证据见 `qa/imagegen-channel-recheck-20260823-v15.json` 和 `qa/current-state-recheck-20260823-v15.json`；当前状态以文档顶部的 2026-09-01 最新证据为准。

2026-08-24 历史收尾复核中，八个正式角色均重新通过 v2 图集、连续性和透明度门禁，PetDex 的实际 metadata/图集均为 `8/8 HTTP 200`、v2、1536x2288 WebP，metadata 和图集 SHA 与仓库均 `8/8` 一致，未创建重复条目；manifest 索引仍有 pending/版本滞后字段，不能仅据此推断审核状态。八角色本地门禁和 `28 passed` hatch-pet 基线保持不变；正式资产与安装器逻辑未改动。当前结果以本节开头的 2026-08-30 证据为准。完整 Codex App 刷新与方向选择验收仍未完成。

本机全局 PetDex CLI 已升级并复核为 `1.3.0`；PetDex Desktop 最新公开版本为 `v0.9.1`，官方签名和公证均通过。通过官方 `petdex://<slug>` 入口逐一选择八个已安装角色后，均正确生效并恢复到 `hei-mao-traveler`；此前动画、跨屏气泡和间距证据仍有效。完整 Codex App 刷新验收仍单独保留为未完成边界。当前 release 证据见 `qa/petdex-desktop-release-recheck-20260830-v2.json`。本机 Codex 的五个 Hook 事件现直接调用带空闲/总时限的 `petdex-hook-wrapper.mjs`，关闭或保持 stdin 打开时均能在隔离测试中退出；v0.9.1 原生 runner 保持 stdin 也能有界退出，#689 已由 PR #752 修复并关闭。证据见 `qa/petdex-local-hook-wrapper-recheck-20260830-v2.json` 和 `qa/petdex-upstream-status-recheck-20260830-v4.json`。

此前通过 PetDex Desktop v0.8.0 的实际窗口捕获确认当前活动角色为 `hei-mao-traveler`；该证据属于历史版本。当前已安装 Desktop v0.9.1，未在本轮发送 UI 输入；完整 Codex App 刷新、逐角色恢复、四方向、动画回环、多角色显示和跨屏气泡仍需用户在 App 内验收。

本机 Codex Hook 已按 PetDex 的 Codex 规则启用 `hooks = true` 和五个事件；五个命令直接调用带空闲/总时限的本地包装器，原生 runner 保留为包装器目标。包装器会完整转发 131042 字节分片 payload，在短暂无输入后关闭原生 stdin，并在总时限内执行 `SIGTERM`/`SIGKILL` 双阶段收束；当前回归中原生 runner 与包装器的开闭 stdin 共 `20/20` 正常退出，分片 payload SHA 完整匹配；无响应 runner 的超时退出码为 `124`，启动错误为 `127`。v0.9.1 原生 runner 在 stdin 保持打开时也能有界退出，#689 已由合并 PR #752 关闭；本地包装器仍提供额外的本机超时边界。按 Codex 官方规范化 hook identity 算法复核，本机五个 `trusted_hash` 均为 `5/5` 匹配，不需要修改 `config.toml`；证据见 `qa/petdex-local-hook-wrapper-recheck-20260830-v2.json`、`qa/petdex-hook-trusted-hash-recheck-20260830-v1.json`、`qa/petdex-desktop-release-recheck-20260830-v2.json` 和 `qa/petdex-upstream-status-recheck-20260830-v4.json`。

Petdex CLI 会同时安装到 Petdex Desktop 与 Codex App 的宠物目录：

```text
~/.petdex/pets/hei-mao
~/.codex/pets/hei-mao
```

### 角色包状态

当前仓库中的角色包如下。每个角色都有独立的 `pet.json`、v2 图集和 QA 证据，不能用其他角色的图集替代；本轮八条完整动作行已重新生成并通过结构与视觉复核，连续性中的少量 minor warning 仍按证据保留。

| slug              | 角色   | 本地状态               | Petdex 状态                |
| ----------------- | ------ | ---------------------- | -------------------------- |
| `hei-mao`         | 黑毛   | v2 与视觉复核通过；连续性 minor warning 已记录 | 公开；sprite 更新 `queued_for_admin_review`，线上仍为旧图 |
| `hei-mao-quality` | 品控官 | v2 与视觉复核通过；连续性 minor warning 已记录 | 公开；sprite 更新 `queued_for_admin_review`，线上仍为旧图 |
| `hei-mao-butler`  | 大管家 | v2 与视觉复核通过；连续性 minor warning 已记录 | 公开；线上图集 SHA 与仓库一致 |
| `hei-mao-chef`    | 厨师   | v2 与视觉复核通过；连续性 minor warning 已记录 | 公开；线上图集 SHA 与仓库一致 |
| `hei-mao-foodie`  | 美食家 | v2 与视觉复核通过；连续性 minor warning 已记录 | 公开；sprite 更新 `queued_for_admin_review`，线上仍为旧图 |
| `hei-mao-delivery` | 配送员 | v2 与视觉复核通过；连续性 minor warning 已记录 | 公开；sprite 更新 `queued_for_admin_review`，线上仍为旧图 |
| `hei-mao-fortune` | 福气官 | v2 与视觉复核通过；连续性 minor warning 已记录 | 公开；线上图集 SHA 与仓库一致 |
| `hei-mao-traveler` | 旅行家 | v2 与视觉复核通过；连续性 minor warning 已记录 | 公开；sprite 更新 `queued_for_admin_review`，线上仍为旧图 |

2026-09-01 的 manifest 快照曾包含八个当前角色条目和历史记录 `hei-mao-2`，总数为 4674；八个当前角色均可通过 PetDex CLI 1.3.0 读取公开资源，本仓库安装器也已覆盖八个角色。该日新鲜下载确认八个线上 metadata 均为 v2 且与本地 metadata 匹配，但图集只有 `hei-mao-butler`、`hei-mao-chef`、`hei-mao-fortune` 与本地 SHA 一致；`hei-mao`、`hei-mao-quality`、`hei-mao-foodie`、`hei-mao-delivery`、`hei-mao-traveler` 的更新仍为 `queued_for_admin_review`。该段仅作历史资源对照；2026-09-03 删除重复条目后的最新 manifest、CLI 和公共资源状态以 `qa/petdex-live-recheck-20260903-v2.json` 为准。

Petdex CLI 会把成功安装的角色同时写入 Petdex Desktop 与 Codex App 的宠物目录：

```text
~/.petdex/pets/<slug>
~/.codex/pets/<slug>
```

此前的 2026-08-10、2026-08-13 和 v2-v37 复核快照仍保留在对应 `qa/` 文件中，仅用于追溯历史漂移，不代表当前线上状态。`qa/current-state-recheck-20260817-v7.json` 代表比例修复前状态；本轮角色比例修复以及 Quality 两条 look row 的连贯重生成以各自 `proportion-*.json`、`final-visual-qa.json` 和 `run-summary.json` 为准。当前 PetDex manifest、公开资源和隔离下载以 `qa/petdex-live-recheck-20260903-v2.json`、`qa/current-state-recheck-20260903-v1.json`、`qa/current-v2-gate-recheck-20260903-v1.json`、`qa/installer-validation-recheck-20260903-v1.json` 和 `qa/petdex-edit-resubmission-recheck-20260904-v1.json` 为准；Desktop、Hook 和 Codex App 的边界仍以专项证据为背景，不能替代新的线上发布结论。

本机当前保留八个角色；八个角色的 v2 结构、透明度、连续性和本轮完整动作行视觉复核均通过。连续性报告中的局部 outlier、方向中间帧 ambiguity 和设计内负空间按 minor warning 保留，没有新的比例失衡、裁切、断开组件或身份漂移。当前 HEAD 的确定性门禁证据见 `qa/current-v2-gate-recheck-20260903-v1.json`，视觉证据见 `qa/current-direction-continuity-recheck-20260901` 和 `qa/visual-review-recheck-20260901-v1.json`。

本地安装器隔离验证已通过 Bash 和 PowerShell 的八个角色，并确认未知 slug 不会写入；2026-09-03 已同步五个比例修复图集的 SHA 常量，最新证据见 `qa/installer-validation-recheck-20260903-v1.json`。三处本地目录的最新 SHA parity 见 `qa/three-directory-parity-recheck-20260903-v1.json`。PetDex Desktop、Codex App 的刷新/动画/多角色/跨屏气泡仍属于用户实机边界；本轮未停止或重启任何 Codex 进程。

### 角色安装器

无参数时安装 `hei-mao`。通过环境变量选择仓库中的任一角色包；八个角色均使用当前图集的固定 SHA 校验：

```bash
HEI_MAO_PET_ID=hei-mao-chef curl -fsSL https://raw.githubusercontent.com/MisonL/hei-mao/main/install.sh | HEI_MAO_PET_ID=hei-mao-chef bash
```

PowerShell 可使用同一个环境变量，或直接传 `-PetId`：

```powershell
$env:HEI_MAO_PET_ID="hei-mao-chef"; irm https://raw.githubusercontent.com/MisonL/hei-mao/main/install.ps1 | iex
./install.ps1 -PetId hei-mao-chef
```

安装器只接受仓库中已有完整图集和固定 SHA 的角色，未知 slug 会显式失败。Windows PowerShell 5.1 的本地 checkout 可能受 Git `core.autocrlf` 影响，安装器会对文本 manifest 显式按 UTF-8/LF 规范化后再校验固定 SHA，二进制图集保持原样。角色包默认安装到 `~/.codex/pets/<slug>`；需要 Petdex Desktop 时请使用上面的 `petdex install`，不要手动复制到未知目录。

`hei-mao-fortune` 和 `hei-mao-traveler` 均已完成本地 v2 图集、结构门禁和视觉 QA，并加入安装器白名单；二者已进入公开 manifest。最近公开资源复核显示 Fortune 线上图集已与仓库一致，Traveler 的修复版 sprite 仍在审核队列，审核生效前在线安装可能得到旧图。历史 `hei-mao-recommender` 和 `hei-mao-2` 也不属于当前发布集；三处本地目录没有这两个历史 slug 的残留。历史 slug 的最新复核见 `qa/historical-slug-recheck-20260816.json`，当前线上状态见 `qa/petdex-live-recheck-20260903-v2.json` 和 `qa/petdex-edit-resubmission-recheck-20260904-v1.json`。

`hei-mao-traveler` 是黑毛的小旅行家角色，使用红色旅行背心、绿色蔬菜纹样背包、叶菜和小福袋表达社区探访与新鲜食材探索。当前 11 行 v2 图集已完成比例归一化、单次 despill、透明度、边界、连续性和修复后方向盲测复核；horizontal-6 B 与 horizontal-7 保留 minor ambiguity warning，四个 cardinal 通过。当前可通过仓库安装器观察修复版；PetDex 线上 sprite 更新已提交，审核生效前在线安装仍可能得到旧图。

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

`hei-mao-butler` 包含完整的 v2 动画图集和 16 个观察方向的独立 QA 证据。PetDex manifest 已公开该角色；最近公开资源复核显示 metadata、v2 图集和 SHA 均与仓库一致，资源对照见 `qa/petdex-live-recheck-20260903-v2.json`。

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

`hei-mao-foodie` 是黑毛的美食家角色包。本轮 waiting 行已完整重生并通过实际色键 v2 门禁、连续性和正常显示尺寸视觉复核；方向连续性中的少量 outlier/负空间提示按 minor warning 保留。

本地安装：

```bash
HEI_MAO_PET_ID=hei-mao-foodie curl -fsSL https://raw.githubusercontent.com/MisonL/hei-mao/main/install.sh | HEI_MAO_PET_ID=hei-mao-foodie bash
```

Petdex 安装：

```bash
npx -y petdex@latest install hei-mao-foodie
```

### 配送员角色

`hei-mao-delivery` 是黑毛的社区配送角色包。本轮 failed 行已完整重生、完成单次色键去溢并通过实际色键 v2 门禁、连续性和正常显示尺寸视觉复核；配送员当前图集 SHA 已同步到两个本机安装目录。

本地安装：

```bash
HEI_MAO_PET_ID=hei-mao-delivery curl -fsSL https://raw.githubusercontent.com/MisonL/hei-mao/main/install.sh | HEI_MAO_PET_ID=hei-mao-delivery bash
```

Petdex 在线安装：

```bash
npx -y petdex@latest install hei-mao-delivery
```

配送员本地 v2 图集已通过门禁；2026-09-04 已按现有 slug 重新提交 PetDex sprite 与 metadata，当前处于 `queued_for_admin_review`，审核生效前在线安装仍可能得到旧 SHA。仓库安装器可立即获取本地已验证图集，队列证据见 `qa/petdex-edit-resubmission-recheck-20260904-v1.json`。

### 福气官角色

`hei-mao-fortune` 是黑毛的福气官角色包，使用红金服饰、爱心手套、屏幕右侧粮篮和屏幕左侧南瓜表达新鲜、丰盛和每日好彩头。当前包由通过 v2 门禁的标准动作行与 v13-final coherent 方向行重新组装，已通过单次 despill、9 个标准动作行、16 个方向、三份独立盲测和最终视觉复核；方向连续性中的局部 outlier 已记录为 minor warning，没有身份漂移、比例跳变、封闭透明洞、青色色键残留或方向反转。最新图集 SHA-256 为 `10056a01a1a85bd350f83e59e8e746540b873add65e8e360439f80a61cf197d9`，证据见 `qa/hei-mao-fortune/run-summary.json`。cardinal 生成重试的上游 502 记录仍保留在 `qa/fortune-cardinal-generation-recheck-20260816-v3.json`，失败尝试没有覆盖已验收图集。

本地安装：

```bash
HEI_MAO_PET_ID=hei-mao-fortune curl -fsSL https://raw.githubusercontent.com/MisonL/hei-mao/main/install.sh | HEI_MAO_PET_ID=hei-mao-fortune bash
```

PetDex 发布状态：条目已进入公开 manifest，`npx -y petdex@latest install hei-mao-fortune` 已在隔离环境成功；最近公开资源复核确认线上 metadata、v2 图集和 SHA 均与仓库一致。当前资源、门禁和安装结果见 `qa/petdex-live-recheck-20260903-v2.json`、`qa/current-v2-gate-recheck-20260903-v1.json` 和 `qa/installer-validation-recheck-20260903-v1.json`。

### 品控官角色

`hei-mao-quality` 是黑毛的品控官角色包。两条 coherent look row 已重新生成，结构、透明度、比例和方向语义门禁均通过；三份独立盲测的 cardinal 硬门禁通过，中间方向分歧作为 minor warning 保留。

PetDex 安装：本地仓库安装器可立即安装已验收的 Quality v2 图集；2026-09-04 重新提交的 sprite 与 metadata 当前处于 `queued_for_admin_review`，审核生效前在线安装可能得到旧图。最新资源、门禁和队列对照见 `qa/petdex-live-recheck-20260903-v2.json`、`qa/current-v2-gate-recheck-20260903-v1.json` 和 `qa/petdex-edit-resubmission-recheck-20260904-v1.json`。

本地安装：

```bash
HEI_MAO_PET_ID=hei-mao-quality curl -fsSL https://raw.githubusercontent.com/MisonL/hei-mao/main/install.sh | HEI_MAO_PET_ID=hei-mao-quality bash
```

Quality 的比例、方向盲测和透明度证据见 `qa/hei-mao-quality/recovery-v2/`；仓库安装可获取当前已验证图集，PetDex 在线安装需等待上述 sprite 审核生效后再获取同一版本。

### 旅行家角色

`hei-mao-traveler` 是黑毛的小旅行家角色，使用红色旅行背心、绿色蔬菜纹样背包、叶菜和福袋表达社区探访与新鲜食材探索。其 11 行 v2 图集已完成单次 despill、透明度验证、三份独立方向盲测、连续性复核和最终视觉 QA；中间方向的盲测分歧与连续性 outlier 均按 minor warning 记录，四个 cardinal、身份、比例、回环和透明主体检查通过。

仓库安装器已固定 Traveler 当前图集 SHA-256 `23f33c14634987575aede96567cd58a281f85ed5670bf200fb9b40586cbf519a`；Shell 和 PowerShell 的八角色隔离安装均已复核通过，方向盲测和连续性中的 minor warning 已记录。

本地安装：

```bash
HEI_MAO_PET_ID=hei-mao-traveler curl -fsSL https://raw.githubusercontent.com/MisonL/hei-mao/main/install.sh | HEI_MAO_PET_ID=hei-mao-traveler bash
```

PetDex 发布状态：条目已进入公开 manifest，`npx -y petdex@latest install hei-mao-traveler` 已在隔离环境成功；2026-09-04 重新提交的 sprite 与 metadata 当前处于 `queued_for_admin_review`，审核生效前在线安装可能得到旧图。当前资源、门禁和队列对照见 `qa/petdex-live-recheck-20260903-v2.json`、`qa/current-v2-gate-recheck-20260903-v1.json` 和 `qa/petdex-edit-resubmission-recheck-20260904-v1.json`。

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
- `pets/hei-mao-quality/`: 品控官角色包（v2 比例与方向门禁通过）
- `qa/hei-mao-quality/`: 品控官的结构、盲测、比例、连续性与视觉复核证据；历史阻断证据仍保留
- `pets/hei-mao-butler/`: 已验证的大管家角色包
- `qa/hei-mao-butler/`: 大管家 v2 的独立验证与视觉复核证据
- `pets/hei-mao-chef/`: 已验证的厨师角色包（Petdex manifest 可见，线上资源与仓库一致）
- `qa/hei-mao-chef/`: 厨师 v2 的独立验证与视觉复核证据
- `pets/hei-mao-foodie/`: 美食家 v2 角色包（waiting 行已完成本轮完整重生与复核）
- `qa/hei-mao-foodie/`: 美食家 v2 的结构、方向和视觉复核证据
- `pets/hei-mao-delivery/`: 配送员 v2 角色包（failed 行已完成本轮完整重生与复核）
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
- `qa/petdex-local-hook-wrapper-recheck-20260822-v1.json`: 本机 Codex Hook 的 EOF 包装器、原生 runner 对照、配置保留和隔离子进程回归；不含本机路径、地址、进程标识或凭证
- `qa/petdex-local-hook-wrapper-recheck-20260823-v2.json`: 五个本机 Codex Hook 事件的开闭 stdin 包装器新鲜回归及 native runner EOF 对照；不含本机路径、地址、进程标识或凭证
- `qa/current-state-recheck-20260830-v4.json`: 2026-08-30T08:53:25Z 汇总 Desktop 0.9.1、八角色本地门禁、PetDex 公开资源、当前版本 Hook 信任校验、上游主线和 Codex App 未覆盖边界；不含本机环境信息
- `qa/current-state-recheck-20260831-v2.json`: 2026-08-31T06:33:00+08:00 汇总最新双模式生图 503、补充视觉指纹复核、八角色确定性门禁、PetDex 资源 parity、Hook 和 Codex App 未覆盖边界；不含本机环境信息
- `qa/current-state-recheck-20260831-v3.json`: 2026-08-31T07:10:21+08:00 汇总新幂等键 `images-non-stream` 请求经终态诊断确认上游 503、无 artifact、四项视觉阻断和当前未覆盖边界；不含本机环境信息
- `qa/current-v2-gate-recheck-20260830-v2.json`: 2026-08-30T08:08:45Z 八角色 v2 图集、连续性、28 项 hatch-pet 测试、安装器、三目录 parity 和隐私门禁新鲜复核；8/8、28 passed、16/16 通过；不含本机环境信息
- `qa/current-state-recheck-20260831-v4.json`: 2026-08-31T05:11:57Z 统一 `#00FF00` 验证结果的参数敏感性复核、匿名时序盲测状态和四个视觉阻断项的当前收口边界；不含本机环境信息
- `qa/hatch-pet-baseline-recheck-20260831-v2.json`: 2026-08-31 hatch-pet 基线测试使用临时 uv 环境执行，28/28 通过；37 条为既有 Pillow 弃用警告，不含本机环境信息
- `qa/petdex-live-recheck-20260830-v3.json`: 2026-08-30T08:52:32Z 只读刷新 PetDex manifest 和八角色公开 metadata/图集；实际 v2、1536x2288 WebP RGBA、SHA parity 均为 8/8，manifest 索引仍有 5/8 版本滞后；不含本机环境信息
- `qa/petdex-local-hook-wrapper-recheck-20260830-v2.json`: 2026-08-30T08:08:45Z 针对 Desktop 0.9.1 的五个本机 Codex Hook 事件开闭 stdin、分片转发和 124/127 错误码隔离回归；20/20 有界退出；不含本机环境信息
- `qa/petdex-hook-trusted-hash-recheck-20260830-v1.json`: 2026-08-30T08:32:16Z 按 Codex 官方规范化 hook identity 算法复核本机五个 trusted_hash；5/5 匹配且未修改配置；不含本机环境信息
- `qa/codex-app-boundary-recheck-20260830-v1.json`: 2026-08-30T07:46:56Z 只读枚举 PetDex/ChatGPT 窗口元数据并记录透明高层窗口无法安全单窗采集；未发送 UI 输入，完整 Codex App 视觉验收仍由用户操作；不含本机环境信息
- `qa/petdex-upstream-status-recheck-20260830-v4.json`: 2026-08-30T08:49:43Z 只读刷新上游 issue #689、PR #752/#710、最新主线和 release；#689 已由 #752 修复关闭，#710 仍为 draft，最新提交为 5323e43（#765），CLI 1.3.0、Desktop 0.9.1；不含本机环境信息
- `qa/petdex-desktop-release-recheck-20260830-v2.json`: 2026-08-30T07:17:26Z PetDex CLI 1.3.0 与 Desktop 0.9.1 的签名、公证、安装、Hook 和运行时健康复核；不含本机环境信息
- `qa/petdex-desktop-runtime-recheck-20260830-v2.json`: 2026-08-30T07:22:58Z Desktop 0.9.1 官方 URI 八角色切换/恢复及健康、气泡来源和动画状态探针；Codex App 像素级验收仍由用户操作；不含本机环境信息
- `qa/petdex-live-recheck-20260903-v1.json`: 2026-09-03 用户删除历史重复 `hei-mao-2` 后的首次线上传播复核；个人页和数据库搜索已移除，但当时静态 manifest、CLI 列表和详情页仍待刷新；不含本机环境信息
- `qa/petdex-live-recheck-20260903-v2.json`: 2026-09-03T10:15:33Z 线上传播完成后的 manifest、CLI、搜索、详情页和 8 个当前公共资源复核；重复 slug 已消失，3/8 sprite SHA 与仓库一致，5 个修复版仍待上游资源传播；不含本机环境信息
- `qa/current-state-recheck-20260903-v1.json`: 2026-09-03T10:15:33Z 当前状态快照；八角色本地 v2 门禁、三目录 parity、安装器和 28 项基线测试通过，重复条目已完成线上清理，五个公共 sprite 更新仍待上游传播，Codex App 视觉边界单独记录；不含本机环境信息
- `qa/current-v2-gate-recheck-20260903-v1.json`: 2026-09-03T01:58:31Z 绑定当前 HEAD 的八角色 v2 图集、实际色键、完整 SHA 和无残留验证；8/8 通过；不含本机环境信息
- `qa/installer-validation-recheck-20260903-v1.json`: 2026-09-03T01:58:31Z 修正五个比例修复图集 SHA 常量后的 Bash/PowerShell 语法、8/8 隔离安装、固定 SHA 和未知 slug 拒绝；不含本机环境信息
- `qa/three-directory-parity-recheck-20260903-v1.json`: 2026-09-03T01:58:31Z 仓库、Codex 与 PetDex 三处八角色 16 个文件逐字节一致，使用当前图集 SHA；不含本机环境信息
- `qa/hatch-pet-baseline-recheck-20260903-v1.json`: 2026-09-03T01:58:31Z hatch-pet 基线测试 28/28 通过，37 条为既有 Pillow 弃用警告；不含本机环境信息
- `qa/installer-cross-platform-recheck-20260830-v2.json`: 2026-08-30T08:08:45Z Bash/PowerShell 八角色隔离安装、固定 SHA、未知 slug 拒绝和临时目标清理；不含本机环境信息
- `qa/three-directory-parity-recheck-20260830-v2.json`: 2026-08-30T08:08:45Z 仓库、Codex 和 PetDex 三处八角色包 16/16 文件逐字节一致；不含本机环境信息
- `qa/petdex-atlas-auditor-recheck-20260830-v1.json`: 2026-08-30T09:32:35Z 采用上游 #757 图集审计规则复核仓库和实际下载的八个已发布图集；结构、线上 SHA 与本地审计结果一致，Chef 的 failed 行连续性提示已结合正常尺寸实图和既有独立视觉 QA 复核为 minor warning；不含本机环境信息
- `qa/visual-review-methods-recheck-20260831-v2.json`: 2026-08-31 独立补充视觉复核；覆盖 88 行、584 帧，增加多背景小尺寸渲染、运动补偿残差、非相邻相似度图、回环/播放节奏和高对比轮廓复核；未新增硬失败，但确认四个既有动作行硬失败，生图修复因结果 URL 安全门禁暂时阻断；不含本机环境信息
- `qa/imagegen-channel-recheck-20260831-v2.json`: 2026-08-31 本地 Docker 生图服务真实 `images-sse`/`images-non-stream` smoke；两条路径均明确返回上游 503、0 个 artifact，未修改正式资产；不含本机环境信息
- `qa/imagegen-channel-recheck-20260831-v4.json`: 2026-08-31 新幂等键分别复测 `images-sse` 和 `images-non-stream`，均返回上游 503；失败请求诊断可读、无 artifact，渠道快照记录最近 `model_not_found`；不含本机环境信息
- `qa/imagegen-channel-recheck-20260831-v5.json`: 2026-08-31 新幂等键 `images-non-stream` 先在客户端门限内返回 `request_in_progress`，随后按原键只读诊断进入终态 `failed`，上游 503、无 artifact；不含本机环境信息
- `qa/imagegen-channel-recheck-20260831-v6.json`: 2026-08-31 官方脚本以新幂等键分别复测 `images-sse` 与 `images-non-stream`，均为 `upstream_unavailable / Connection error`，结构化诊断可读且无 artifact；不含本机环境信息
- `qa/imagegen-channel-recheck-20260831-v11.json`: 2026-08-31 本地 Docker 渠道健康快照为 healthy，但新幂等键的 `images-sse` 和 `images-non-stream` smoke 均为 `upstream_unavailable / Connection error`，无 artifact；不含本机环境信息
- `qa/imagegen-channel-recheck-20260831-v12.json`: 2026-08-31 再次以全新幂等键执行 1K `images-non-stream` smoke，仍为 `upstream_unavailable / Connection error`，无 artifact，未启动整行动画重生；不含本机环境信息
- `qa/v2-contract-recheck-20260831-v1.json`: 2026-08-31 按各角色实际 despill 色键重新执行八角色 v2 validator；8/8 通过，1536x2288 RGBA WebP、spriteVersionNumber 2、无错误/警告和透明 RGB 残留；不含本机环境信息
- `qa/v2-key-sensitivity-recheck-20260831-v1.json`: 2026-08-31 复核 `#00FF00` 统一色键造成的 3/8 结果；按各角色实际色键仍为 8/8，通过参数敏感性对照排除资产回归；不含本机环境信息
- `qa/installer-validation-recheck-20260831-v1.json`: 2026-08-31 Bash/PowerShell 语法、ShellCheck、八角色隔离安装和未知 slug 拒绝复核；全部通过，临时目标已清理；不含本机环境信息
- `qa/three-directory-parity-recheck-20260831-v3.json`: 2026-08-31 仓库、Codex 与 PetDex 三处八角色 16 个资产逐字节 SHA parity；8/8 通过；不含本机环境信息
- `qa/visual-review-alternative-20260831/visual-review-alternative-20260831-v4.json`: 2026-08-31 轮廓集合叠加、头/下半身消融和候选帧可视化复核；88/88 行查看，只复现四个既知硬失败，未新增硬失败；不含本机环境信息
- `qa/visual-review-alternative-20260831/visual-review-alternative-20260831-v5.json`: 2026-08-31 alpha 边界 Hausdorff 残差、多部位锚点轨迹和有限平移补偿复核；覆盖 88 行、584 帧，区分动作/道具造成的正常残差与重复头部、姿态族切换候选；只复现四个既知硬失败，未新增硬失败；不含本机环境信息
- `qa/visual-review-alternative-20260831/supplemental-invariant-review-20260831-v6.json`: 2026-08-31 锚点归一化轮廓、角色 idle 包络、多尺度边缘和材质指纹复核；覆盖 584 个动画帧及 8 个 neutral-look 复用单元，32 个候选均经正常尺寸查看，只复现四个既知硬失败；不含本机环境信息
- `qa/visual-review-alternative-20260831/supplemental-invariant-candidates-v6.jpg`: 2026-08-31 补充形状/边缘指纹候选的高对比轮廓叠加图；仅作视觉证据，不含本机环境信息
- `qa/visual-review-alternative-20260831/display-alpha-lobe-review-20260831-v4.json`: 2026-08-31 alpha 阈值稳定性、三种小尺寸与九种采样组合、上半身轮廓持久性复核；覆盖 592 个非空帧，未新增硬失败，只复现四项既知动作行阻断；不含本机环境信息
- `qa/visual-review-alternative-20260831/display-alpha-lobe-candidates-v4.jpg`: 2026-08-31 显示端压力复核候选图，左侧为多 alpha 阈值轮廓，右侧为 48x52 棋盘格渲染；仅作视觉证据，不含本机环境信息
- `qa/visual-review-alternative-20260831/display_alpha_lobe_review.py`: 显示端 alpha/采样/上轮廓复核脚本，只读生成候选证据，不修改正式资产
- `qa/visual-review-alternative-20260831/css-sampling-flicker-review-20260831.json`: 2026-08-31 按 PetDex CSS 精灵渲染约束执行完整图集边界采样、三背景压力和小尺寸形状/颜色闪变分离；覆盖 584 帧、584 个回环转场和 8760 组采样变体，未新增硬失败；不含本机环境信息
- `qa/visual-review-alternative-20260831/css-sampling-flicker-candidates.jpg`: 完整图集与隔离 cell 的采样差异、显示闪变候选的正常尺寸证据图；不含本机环境信息
- `qa/visual-review-alternative-20260831/css_sampling_flicker_review.py`: CSS 图集边界采样和显示闪变复核脚本，只读生成候选证据，不替换或修改正式图集
- `qa/visual-review-alternative-20260831/directional-pair-review-20260831-v3.json`: 2026-08-31 `running-right` 镜像与 `running-left` 成对锚点复核；64 对帧、无空配对，最高差异经正常尺寸叠加确认来自预期非对称道具，未新增硬失败；不含本机环境信息
- `qa/visual-review-alternative-20260831/directional-pair-candidates-v3.jpg`: 左侧 `running-left`、中间镜像后的 `running-right`、右侧青/洋红轮廓叠加的候选证据图；不含本机环境信息
- `qa/visual-review-alternative-20260831/directional_pair_review.py`: 左右动作成对复核脚本，只读生成候选证据，不替换或修改正式图集
- `qa/visual-review-alternative-20260831/frame-cadence-compression-review-20260831-v1.json`: 2026-08-31 帧序扰动、上/下半身时间残差和有界 WebP 质量 75/50 压力复核；覆盖 584 帧、88 行，未新增硬失败；不含本机环境信息
- `qa/visual-review-alternative-20260831/frame-cadence-compression-candidates-v1.jpg`: 帧序/压缩候选的正常尺寸证据图；不含本机环境信息
- `qa/visual-review-alternative-20260831/browser-css-compositor-review-20260831-v1.json`: 2026-08-31 Chromium CSS 合成器真实回放；覆盖 88 行、584 帧、6 组 DPR/缩放/亚像素变体，候选图正常尺寸复核未新增硬失败；不含本机环境信息
- `qa/visual-review-alternative-20260831/browser-css-compositor-candidates-v1.png`: Chromium 合成器重点候选的棋盘格/深色背景对照图；不含本机环境信息
- `qa/visual-review-alternative-20260831/browser-css-compositor-full-v1.png`: Chromium 合成器全角色全行回放图；不含本机环境信息
- `qa/visual-review-alternative-20260831/browser-css-compositor-variants-summary-v1.jpg`: 6 组 Chromium DPR/缩放/亚像素变体的紧凑对照图；不含本机环境信息
- `qa/visual-review-alternative-20260831/browser_css_compositor_review.mjs`: Chromium CSS 合成器复核脚本；只读取正式资产并写入 QA 证据，不修改资产或运行中的应用
- `qa/visual-review-alternative-20260831/frame_cadence_compression_review.py`: 帧序与压缩压力复核脚本，只读生成候选证据，不替换或修改正式图集
- `qa/visual-review-methods-recheck-20260831-v4.json`: 2026-08-31 匿名时序三元组盲测方法汇总；覆盖 8 个角色、11 类动作、40 个三元组和 9 个已知缺陷控制样本，待独立审查；不含本机环境信息
- `qa/visual-review-methods-recheck-20260831-v5.json`: 2026-08-31 跨方法候选共识复核方法汇总；148 个候选元组中 43 个由至少两个独立方法同时指向，聚焦复核 36 个元组，未新增硬失败；不含本机环境信息
- `qa/visual-review-methods-recheck-20260831-v6.json`: 2026-08-31 完整分辨率扫描线/断开组件复核方法汇总；确认四个新增整行动画硬失败并记录三个小型碎片候选；不含本机环境信息
- `qa/visual-review-alternative-20260831/cross-method-consensus-review-20260831-v1.json`: 比例、拓扑、光流、显示尺寸、DPR、帧序和 CSS 采样候选的交叉共识与邻帧/alpha 轮廓复核结果；不含本机环境信息
- `qa/visual-review-alternative-20260831/cross-method-consensus-candidates-v1.jpg`: 交叉共识候选的 `PREV/CURRENT/NEXT` 与二值 alpha 轮廓复核图；不含本机环境信息
- `qa/visual-review-alternative-20260831/cross_method_consensus_review.py`: 跨方法候选交集与聚焦视觉复核脚本，只读生成 QA 证据，不修改正式资产
- `qa/visual-review-alternative-20260831/scanline-segment-review-20260831-v1.json`: 完整分辨率扫描线分段、内部间隙和断开组件复核结果；确认四个新增整行动画阻断并记录三个小型碎片候选；不含本机环境信息
- `qa/visual-review-alternative-20260831/scanline-segment-candidates-v1.jpg`: 扫描线候选的 `PREV/CURRENT/NEXT` 与彩色分段图；仅作视觉证据，不含本机环境信息
- `qa/visual-review-alternative-20260831/scanline-segment-manual-review-20260831-v1.json`: 扫描线候选的正常尺寸/高对比人工确认和整行修复决定；不含本机环境信息
- `qa/visual-review-alternative-20260831/cycle-recurrence-review-20260831-v1.json`: 循环复现矩阵与五帧洋葱皮复核结果；覆盖 8 个角色、88 行、584 帧，未新增硬失败并保留八个既有整行动画阻断；不含本机环境信息
- `qa/visual-review-alternative-20260831/cycle-recurrence-candidates-v1.jpg`: 已知阻断控制样本和循环复现候选的正常尺寸证据图；不含本机环境信息
- `qa/visual-review-alternative-20260831/cycle-recurrence-nonblock-candidates-v1.jpg`: 排除已知阻断后的高分复现候选正常尺寸证据图；不含本机环境信息
- `qa/visual-review-alternative-20260831/cycle_recurrence_review.py`: 循环复现矩阵、锚点归一化和洋葱皮候选生成脚本，只读生成 QA 证据，不修改正式图集
- `qa/visual-review-methods-recheck-20260831-v10.json`: 2026-08-31 轮廓厚度场与局部宽度补充复核；覆盖 8 个角色、88 行、584 帧，并在 48x52 显示尺寸复核厚度持久性；未新增硬失败，八个既有整行动画阻断保持不变；不含本机环境信息
- `qa/visual-review-methods-recheck-20260831-v11.json`: 2026-08-31 小尺寸灰度/对比度压力复核方法汇总；覆盖 8 个角色、88 行、584 帧，并在三种显示尺寸和三种背景下查看 32 个候选；未新增硬失败，八个既有整行动画阻断保持不变；不含本机环境信息
- `qa/current-state-recheck-20260831-v8.json`: 2026-08-31 状态意图与上游 PetDex 状态刷新后的当前发布边界快照；记录 8/8 结构门禁、八个整行动画阻断、生图上游连接失败、#689/#752/#710 和 Codex App 待用户验收边界；不含本机环境信息
- `qa/current-state-recheck-20260831-v7.json`: 2026-08-31 状态意图与动画退化复核后的当前发布边界快照；记录 8/8 结构门禁、八个整行动画阻断、图像生成上游阻断和 Codex App 待用户验收边界；不含本机环境信息
- `qa/current-state-recheck-20260831-v6.json`: 2026-08-31 小尺寸感知压力复核后的当前发布边界快照；记录 8/8 结构门禁、八个整行动画阻断、图像生成上游阻断和 Codex App 待用户验收边界；不含本机环境信息
- `qa/readme-reference-recheck-20260831-v1.json`: 2026-08-31 README 具体 QA 引用存在性和隐私边界复核；587 个引用中无具体缺失，仅保留 15 个通用 `<slug>` 模板占位符；不含本机环境信息
- `qa/readme-reference-recheck-20260831-v2.json`: 2026-08-31 新增状态意图视觉 QA 证据后的增量引用与隐私复核；5 个新增引用均存在；不含本机环境信息
- `qa/visual-review-alternative-20260831/squint-contrast-review-20260831-v1.json`: 2026-08-31 小尺寸灰度/对比度压力复核；覆盖 8 个角色、88 行、584 帧，在 24x26、32x35、48x52 三个显示尺寸和三种背景下查看 32 个候选；未新增硬失败，八个既有整行动画阻断保持不变；不含本机环境信息
- `qa/visual-review-alternative-20260831/squint_contrast_review.py`: 小尺寸灰度、alpha 轮廓和多背景对比度复核脚本，只读生成 QA 证据，不替换或修改正式图集
- `qa/visual-review-alternative-20260831/squint-contrast-candidates-v1.jpg`: 小尺寸压力候选的深色、浅色、高饱和和灰度 alpha 对照图；仅作视觉证据，不含本机环境信息
- `qa/visual-review-alternative-20260831/thickness-field-review-20260831-v1.json`: 2026-08-31 完整分辨率和显示尺寸 alpha 距离场、局部厚度与行中值轮廓复核；32 个候选均经正常显示尺寸查看，未新增硬失败；不含本机环境信息
- `qa/visual-review-alternative-20260831/thickness-field-candidates-v1.jpg`: 轮廓厚度场候选的原帧、二值轮廓、厚度热力图和行中值轮廓对照；仅作视觉证据，不含本机环境信息
- `qa/visual-review-alternative-20260831/thickness_field_review.py`: 轮廓厚度场与局部宽度复核脚本，只读生成 QA 证据，不替换或修改正式图集
- `qa/visual-review-alternative-20260831/state-semantics-review-20260831-v1.json`: 状态意图、上/下半身运动分布、循环多样性和与 idle 距离复核结果；覆盖 8 个角色、88 行、584 帧，未新增硬失败；不含本机环境信息
- `qa/visual-review-alternative-20260831/state-semantics-manual-review-20260831-v1.json`: 状态意图候选的正常尺寸人工查看、既有阻断复现和 warning 处理；不含本机环境信息
- `qa/visual-review-alternative-20260831/state-semantics-candidates-v1.jpg`: 状态意图与动画退化候选的 `PREV/CURRENT/NEXT/DIFF` 正常尺寸证据图；仅作视觉证据，不含本机环境信息
- `qa/visual-review-alternative-20260831/state_semantics_review.py`: 状态意图和动画退化复核脚本，只读生成 QA 证据，不替换或修改正式图集
- `qa/visual-review-methods-recheck-20260831-v12.json`: 跨角色核心身份与比例复核方法汇总；覆盖 8 个角色、88 行、584 帧和 24 个候选，正常尺寸查看未新增硬失败；不含本机环境信息
- `qa/current-state-recheck-20260831-v9.json`: 跨角色身份复核后的最新状态快照；八个整行动画阻断、生图上游阻断和 Codex App 待用户验收边界均保持不变；不含本机环境信息
- `qa/current-state-recheck-20260831-v10.json`: 最新真实生图探针后的状态快照；Agent JSON 路由仍为 HTTP 502、无 artifact，八个整行动画阻断保持不变；不含本机环境信息
- `qa/current-state-recheck-20260831-v11.json`: 替代模型真实生图探针后的状态快照；模型列表可读但生成接口仍为 HTTP 502、无 artifact，八个整行动画阻断保持不变；不含本机环境信息
- `qa/current-goal-recheck-20260831-v2.json`: 直接 v2 validator、跨角色身份复核和最新生图探针合并后的 goal 快照；8/8 结构门禁通过但八个整行动画和 Codex App 实机边界仍未闭合；不含本机环境信息
- `qa/imagegen-channel-recheck-20260831-v15.json`: 新幂等键真实生图探针；本机 Docker 服务可达但上游返回 HTTP 502 `Connection error`，无图像和 artifact；不含本机环境信息
- `qa/imagegen-channel-recheck-20260831-v16.json`: 已列出替代模型的真实生图探针；模型列表 HTTP 200，但生成接口仍返回 HTTP 502 `Connection error`，无图像和 artifact；不含本机环境信息
- `qa/visual-review-alternative-20260831/cross-role-identity-review-20260831-v1.json`: 下半身锚点对齐的头脸 alpha、上/下身比例和固定尺度 alpha/RGB 指纹复核结果；未新增硬失败；不含本机环境信息
- `qa/visual-review-alternative-20260831/cross-role-identity-candidates-v1.jpg`: 跨角色身份候选的当前帧、同角色 idle 参考和差异热条正常尺寸对照图；仅作视觉证据，不含本机环境信息
- `qa/visual-review-alternative-20260831/cross-role-identity-manual-review-20260831-v1.json`: 跨角色身份候选的正常尺寸人工确认和既有阻断保留结论；不含本机环境信息
- `qa/visual-review-alternative-20260831/cross_role_identity_review.py`: 跨角色核心身份与比例复核脚本，只读生成 QA 证据，不替换或修改正式图集
- `qa/visual-review-alternative-20260831/scanline_segment_review.py`: 扫描线分段与完整分辨率断开组件复核脚本，只读生成 QA 证据，不替换或修改正式图集
- `qa/visual-review-alternative-20260831/blind-temporal-triplet-sheet-v1.png`: 匿名 `PREV/CURRENT/NEXT` 正常尺寸盲测图；不含角色、动作、帧号和指标分数
- `qa/visual-review-alternative-20260831/blind-temporal-triplet-answer-key-v1.json`: 匿名盲测隐藏答案键，仅供复核后对照；不应提供给盲审查器
- `qa/visual-review-alternative-20260831/blind-temporal-triplet-parent-review-20260831-v1.json`: 主代理正常尺寸回看结果；重现四个既知整行动画缺陷，未新增明显硬失败，但不等同于独立审查通过
- `qa/visual-review-alternative-20260831/blind-temporal-triplet-omp-review-20260831-v1.json`: OMP 图像附件通道探针；无法读取图片，未产生视觉 verdict
- `qa/visual-review-alternative-20260831/blind-temporal-triplet-claude-review-20260831-v1.json`: Claude 只读图像通道探针；未认证，未产生视觉 verdict
- `qa/petdex-live-recheck-20260831-v1.json`: 2026-08-31 最新 manifest、八角色公开 metadata/图集下载和仓库 SHA 对照；实际 v2、1536x2288 WebP RGBA、8/8 字节一致，manifest 总数 4672 且 5/8 索引版本字段滞后；不含本机环境信息
- `qa/petdex-live-recheck-20260831-v2.json`: 2026-08-31 新鲜只读 `petdex list` 与 release 刷新；gallery 4672 条、八个当前角色和历史 `hei-mao-2` 均可见，CLI 1.3.0、Desktop 0.9.1；未执行资源 mutation；不含本机环境信息
- `qa/imagegen-channel-recheck-20260831-v13.json`: 2026-08-31 新幂等本机 Docker 生图 smoke；容器健康且路由可读，但 `meinianda.top` 仍返回 HTTP 500 `Connection error`，未产出 artifact；不含本机环境信息
- `qa/imagegen-channel-recheck-20260831-v14.json`: 2026-08-31 新幂等 Agent JSON server-channel smoke；页面 JSON 与 Agent JSON 路由均能到达本机服务，但上游仍返回 `Connection error`，未产出 artifact；不含本机环境信息
- `qa/petdex-upstream-status-recheck-20260831-v2.json`: 2026-08-31 最新 issue #689、PR #752/#710、main、CLI 和 Desktop 只读状态；#689 已由 #752 合并关闭，#710 仍为 open，版本保持 CLI 1.3.0/Desktop 0.9.1；不含本机环境信息
- `qa/petdex-upstream-status-recheck-20260831-v1.json`: 2026-08-31 最新 issue #689、PR #752/#710、main、CLI 和 Desktop 只读状态；#689 已由 #752 合并关闭，#710 仍为 draft，版本保持 CLI 1.3.0/Desktop 0.9.1；不含本机环境信息
- `qa/petdex-live-recheck-20260824-v2.json`: 2026-08-24T04:22:50Z 新鲜只读 manifest、八角色 metadata/图集实际契约和仓库 SHA 对照；8/8 v2、1536x2288 WebP RGBA、SHA 一致，未执行 mutation；不含本机环境信息
- `qa/petdex-live-recheck-20260824-v3.json`: 2026-08-24T09:28:08Z 新鲜只读 manifest、八角色 metadata/图集实际契约和仓库 SHA 对照；manifest 生成于 2026-08-24T06:40:21.316Z，metadata 与图集均 8/8 字节一致，未执行 mutation；不含本机环境信息
- `qa/petdex-owned-slug-readonly-recheck-20260824-v1.json`: 2026-08-24T04:22:50Z 通过 PetDex CLI 1.2.2 认证只读解析八个 owned slug；8/8 HTTP 200、approved，未调用 edit/presign/upload/submit；不含本机环境信息
- `qa/petdex-local-hook-wrapper-recheck-20260824-v1.json`: 2026-08-24T04:22:50Z 五个本机 Hook 事件在关闭/保持打开 stdin 下隔离回归 10/10 正常退出，最大耗时 280ms；不含本机环境信息
- `qa/petdex-local-hook-wrapper-recheck-20260824-v2.json`: 2026-08-24T05:00:00Z 本机 Hook 包装器分片 payload 转发、开闭 stdin 矩阵和无响应 runner 有界退出复核；10/10 通过，最大矩阵耗时 377ms，无响应隔离 runner 在 1308ms 内退出；不含本机环境信息
- `qa/petdex-local-hook-wrapper-recheck-20260824-v3.json`: 2026-08-24T05:26:43Z 真实 native runner 五事件开闭 stdin `10/10`、分片转发 `10/10`；忽略 SIGTERM 的隔离 runner 返回 124，启动错误返回 127；不含本机环境信息
- `qa/petdex-local-hook-wrapper-recheck-20260824-v4.json`: 2026-08-24T05:26:43Z 在 v3 基础上复核五事件 Hook 配置；Shell 解析通过，包装器缺失时五个事件均明确返回 127，未回退到 EOF 易阻塞的原生 runner；不含本机环境信息
- `qa/petdex-local-hook-wrapper-recheck-20260824-v5.json`: 2026-08-24T06:02:11Z 最终真实 native runner 五事件开闭 stdin `10/10`、分片转发 `10/10`；忽略 SIGTERM 的隔离 runner返回 124，启动错误返回 127，五事件缺失包装器均显式返回 127；不含本机环境信息
- `qa/petdex-local-hook-wrapper-recheck-20260824-v6.json`: 2026-08-24T08:09:28Z 新鲜五事件开闭 stdin `10/10`、约 131115 字节分片转发 `10/10`；忽略 SIGTERM 的隔离 runner 返回 124，不可执行 runner 返回 127；不含本机环境信息
- `qa/petdex-upstream-status-recheck-20260824-v1.json`: 2026-08-24T04:07:15Z 只读刷新 #689 与 draft PR #710；#689 仍 open、#710 仍未合并且不是 EOF 修复；不含本机环境信息
- `qa/petdex-upstream-status-recheck-20260824-v2.json`: 2026-08-24T05:38:46Z 只读刷新 #689、draft PR #710 和最新 release；#689 仍 open、#710 仍未合并且不改变 EOF 语义，最新公开版为 desktop-v0.8.0；不含本机环境信息
- `qa/petdex-upstream-status-recheck-20260824-v3.json`: 2026-08-24T09:28:08Z 只读刷新 #689、draft PR #710、源码 EOF 语义和最新 release；#689 仍 open 且无评论，#710 仍未合并且不改变 EOF 语义，最新公开版为 desktop-v0.8.0；不含本机环境信息
- `qa/installer-cross-platform-recheck-20260824-v1.json`: 2026-08-24T09:28:08Z Bash 本地/远程 raw 与 PowerShell Core 八角色隔离安装、固定 SHA、历史 slug 拒绝和临时目录清理复核；不含本机环境信息
- `qa/current-v2-gate-recheck-20260824-v1.json`: 2026-08-24T04:22:50Z 八角色 v2 atlas、28 项 hatch-pet 测试、ShellCheck、PowerShell、JSON/diff、三目录 SHA 和公开隐私门禁新鲜复核；全部通过；不含本机环境信息
- `qa/current-state-recheck-20260824-v3.json`: 2026-08-24T04:22:50Z 绑定本轮八角色本地门禁、PetDex 线上资源/owned-slug、Hook 包装器和上游状态；完整 Codex App 刷新、逐角色恢复、四方向、动画、多角色和跨屏气泡仍明确未验证；不含本机环境信息
- `qa/current-state-recheck-20260824-v4.json`: 2026-08-24T05:00:00Z 绑定本轮本机 Hook 包装器加固、八角色本地门禁和 PetDex 线上边界；Hook 分片转发与有界退出通过，完整 Codex App 运行时、上游 EOF 修复、manifest 索引滞后和历史公开记录仍明确保留为边界；不含本机环境信息
- `qa/current-state-recheck-20260824-v5.json`: 2026-08-24T05:26:43Z 绑定本机 Hook 超时/错误码修补、真实 native runner 与分片转发矩阵、八角色门禁和 PetDex 线上边界；完整 Codex App 运行时、上游 EOF 修复、manifest 索引滞后和历史公开记录仍明确保留为边界；不含本机环境信息
- `qa/current-state-recheck-20260824-v6.json`: 2026-08-24T05:26:43Z 绑定本机 Hook 配置显式失败语义、包装器超时/错误码修补、真实 native runner 与分片转发矩阵、八角色门禁和 PetDex 线上边界；完整 Codex App 运行时、上游 EOF 修复、manifest 索引滞后和历史公开记录仍明确保留为边界；不含本机环境信息
- `qa/current-state-recheck-20260824-v7.json`: 2026-08-24T05:38:46Z 历史状态快照，已由 v8 收尾证据取代；仅用于追溯，不代表当前状态；不含本机环境信息
- `qa/current-state-recheck-20260824-v8.json`: 2026-08-24T06:02:11Z 绑定最终本机 Hook 配置与包装器矩阵、八角色门禁和 PetDex 线上边界；完整 Codex App 运行时、上游 EOF 修复、manifest 索引滞后和历史公开记录仍明确保留为边界；不含本机环境信息
- `qa/current-state-recheck-20260824-v9.json`: 2026-08-24T08:09:28Z 绑定最新本机 Hook 分片转发/有界终止矩阵、八角色门禁和 PetDex 线上边界；完整 Codex App 运行时、上游 EOF 修复、manifest 索引滞后和历史公开记录仍明确保留为边界；不含本机环境信息
- `qa/current-state-recheck-20260824-v10.json`: 2026-08-24T09:28:08Z 绑定当前 HEAD 的八角色 atlas/28 项测试、三目录 parity、Bash/PowerShell 安装、manifest 实际资源、上游 Hook 源码语义和 Codex App 边界；本地与公开资源门禁通过，完整 Codex App 运行时及上游 EOF 修复仍未闭合；不含本机环境信息
<details>
<summary>更早历史 QA 快照（仅追溯，不代表当前状态）</summary>

- `qa/petdex-multidisplay-recheck-20260810.json`: 双显示器实时窗口复核；Petdex 窗口可显示在另一块屏幕，但跨屏移动后气泡与宠物重叠，Codex App 多角色验收仍被阻断
- `qa/v2-contract-recheck-20260809.json`: 本轮五个角色的 v2 合同、安装一致性和技能测试复核
- `qa/v2-contract-recheck-20260810.json`: foodie 修复前的历史 v2 合同和视觉阻断快照
- `qa/current-package-install-recheck-20260810.json`: foodie 修复前的历史四角色安装一致性快照
- `qa/foodie-install-recheck-20260810.json`: foodie 修复后的 v2 合同、安装器、本机双目录一致性和公开文件卫生复核
- `qa/current-local-gate-recheck-20260810.json`: 基于当前提交重新执行的 v2 合同、hatch-pet 测试、安装器允许/拒绝路径、双目录一致性和公开文件卫生复核
- `qa/installer-isolation-recheck-20260813.json`: Bash 与 PowerShell 隔离安装器的七角色固定 SHA、历史/阻断 slug 拒绝和临时目标写入复核
- `qa/installer-cross-platform-recheck-20260818-v1.json`: 提交 `4cda613` 下七个可发布角色的 Bash 隔离安装、PowerShell Traveler 安装、Quality/历史 slug 双平台拒绝和临时目录清理复核；不含本机环境信息
- `qa/remote-installer-recheck-20260818.json`: 提交 `8ba0124` 下 GitHub/GitLab raw Bash 安装器各自 7/7 角色安装、固定 SHA、Quality/历史 slug 拒绝和临时目标清理复核；不含本机环境信息
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
- `qa/imagegen-channel-recheck-20260818-v1.json`: 品控官 row 10 重新生成前置检查；服务通道为 `probe_pending`，最近失败为 `403 INSUFFICIENT_BALANCE`，未提交新请求或安装隔离候选
- `qa/imagegen-channel-recheck-20260818-v2.json`: 本地 Docker 生图服务的只读 Agent capabilities、契约、runtime 和渠道健康复核；capabilities/契约返回 200/预期 400，runtime 返回 500 `disk I/O error`，渠道为 `probe_pending` 且最近失败为 `403 INSUFFICIENT_BALANCE`，未发起计费请求
- `qa/imagegen-channel-recheck-20260818-v3.json`: 当前只读生图前置复核；容器健康但 runtime 仍为 500 `disk I/O error`，无健康上游通道，未发起计费请求
- `qa/imagegen-channel-recheck-20260818-v4.json`: runtime 恢复为 200 后对两个独立 Agent request mode 执行最小真实 smoke；非流式与 SSE 均返回 403 且无图像/artifact，渠道进入 `probe_pending`，Quality 未提交生成请求
- `qa/imagegen-channel-recheck-20260818-v5.json`: 冷却到期后的恢复探针仍返回 403；两个新幂等键只在本地健康门禁收到 503，未向上游重复发起请求或提交 Quality 生成
- `qa/imagegen-channel-recheck-20260818-v6.json`: 冷却后使用新幂等键重试 Quality row 9；上游仍返回 403 `INSUFFICIENT_BALANCE`，服务回到 `probe_pending`，未产生图像或替换资产
- `qa/imagegen-channel-recheck-20260818-v7.json`: 切换本地 Docker 服务后再次使用全新幂等键重试 Quality row 9；唯一渠道仍为 `probe_pending` 且无有效请求方式，请求在本地健康门禁拒绝，未向上游发送、未产生图像或替换资产
- `qa/imagegen-channel-recheck-20260818-v8.json`: 真实编排入口使用全新幂等键执行 smoke；服务仍为 `probe_pending`，`images-non-stream/images-sse` 无健康凭证，未选择渠道、未向上游发送、未产生 artifact，Quality 两条 look row 继续阻断
- `qa/imagegen-channel-recheck-20260818-v9.json`: 2026-08-18T08:11:16Z 使用全新幂等键的本地 Agent 非流式 smoke；返回 503 `configuration_error`，唯一渠道仍为 `probe_pending`，最近上游失败为 403 `INSUFFICIENT_BALANCE`，无计费、无 artifact，Quality 两条 look row 继续阻断
- `qa/imagegen-channel-recheck-20260818-v10.json`: 2026-08-18T08:31:29Z 只读恢复轮询；Agent/runtime 契约正常但有效请求方式仍为空，唯一渠道 `probe_pending`，最近探针仍为 403 `INSUFFICIENT_BALANCE`，未发送新请求，Quality 两条 look row 继续阻断
- `qa/imagegen-channel-recheck-20260818-v11.json`: 2026-08-18T14:53:21Z 更换 API 后的本地 Docker 服务恢复复核；first-run、Agent doctor、capabilities、runtime、渠道健康和合同探针通过，最小真实编排 smoke 以 `images-non-stream` 返回 1024x1024 WebP，尺寸校验和测试产物清理通过，不含本机环境信息
- `qa/imagegen-channel-recheck-20260818-v12.json`: 2026-08-18T15:35:22Z 本地 Docker API 切换后的再次真实 smoke；Agent doctor、capabilities、runtime、渠道健康和合同探针通过，编排入口以 `images-non-stream` 返回 1024x1024 WebP，尺寸校验和测试产物删除通过，不含本机环境信息
- `qa/imagegen-channel-recheck-20260819-v1.json`: 2026-08-18T16:21:05Z API 切换后的当前本地 Docker 复核；Agent capabilities、runtime、合同和渠道健康通过，`images-non-stream` 与 `images-sse` 各自真实 smoke 通过并清理产物；远程部署实例仍因上游认证 403 阻断，不含本机环境信息
- `qa/imagegen-channel-recheck-20260819-v2.json`: 2026-08-18T17:25:40Z API 切换后的延长本地 Docker 真实 smoke；统一编排 `images-non-stream` 返回 1024x1024 WebP 并清理产物，直接 Agent 路径在 75 秒门限中止，Responses 后端按当前配置禁用；不含本机环境信息
- `qa/imagegen-channel-recheck-20260819-v3.json`: 2026-08-18T17:49:15Z API 切换后的最新本地 Docker 真实 smoke；编排入口以 `images-non-stream` 返回 1024x1024 WebP，尺寸校验和单个测试 artifact 删除通过；不含本机环境信息
- `qa/imagegen-channel-recheck-20260819-v4.json`: 2026-08-19T14:16:25Z 当前本地 Docker 渠道诊断和一次新幂等键真实 smoke；容器健康但唯一渠道 `probe_pending`、有效请求方式为空，smoke 返回 `configuration_error` 且未创建 artifact；不含本机环境信息
- `qa/imagegen-channel-recheck-20260819-v5.json`: 2026-08-19T14:47:03Z 重载私有 API 配置后的 Docker 复核；运行时配置已生效，但上游 TLS 在建立前断开，两条 Images 真实 smoke 均为连接错误且未创建 artifact；不含本机环境信息
- `qa/imagegen-channel-recheck-20260819-v6.json`: 2026-08-19T15:48:42Z 当前 Docker capabilities、runtime、合同和渠道健康只读复核；容器健康但唯一渠道仍为 `probe_pending`、有效 request mode 为 0，真实请求在健康门禁前停止，未创建 artifact；不含本机环境信息
- `qa/imagegen-channel-recheck-20260819-v7.json`: 2026-08-19T16:15:22Z 私有 API 配置重载后的最新脱敏复核；容器配置与私有来源一致，服务合同通过，但上游 DNS 正常、TLS 在安全连接前断开，`/models` 返回 599，唯一渠道仍为 `probe_pending`，未创建 artifact；不含本机环境信息
- `qa/imagegen-channel-recheck-20260820-v1.json`: 2026-08-19T17:17:37Z 再次复核新 API；本地 Docker 合同和服务端编排检查通过，但主机与容器访问上游均在 TLS 建连前断开，`/models` 返回 599，未发送计费请求或创建 artifact；不含本机环境信息
- `qa/imagegen-channel-recheck-20260820-v2.json`: 2026-08-19T18:15:18Z 同时记录本地 Docker TLS 599 与正式部署最小真实 smoke 的上游 403 鉴权阻断；0 个 artifact，未修改正式资产，不含本机环境信息
- `qa/imagegen-channel-recheck-20260820-v3.json`: 2026-08-19T18:37:51Z API 配置重载后的本地 Docker 只读复核；容器、Agent 合同和运行时通过，但唯一渠道仍为 `probe_pending`，TLS 建连前断开且 `/models` 返回 599，未发起计费请求或创建 artifact，不含本机环境信息
- `qa/imagegen-channel-recheck-20260820-v4.json`: 2026-08-19T20:45:48Z 使用官方 Agent doctor 和渠道健康诊断再次复核；容器、Agent 合同、runtime 和 SQLite 状态后端通过，但 `effective_request_modes` 仍为空、渠道仍为 `probe_pending`、最近失败为 `probe_transport_error`，未发起计费请求或创建 artifact，不含本机环境信息
- `qa/imagegen-channel-recheck-20260820-v5.json`: 2026-08-19T21:07:23Z 在提交 `94d5cca` 后复核你更换的 API 配置；容器健康、Agent 契约通过，但 DNS 后 TLS 在安全连接建立前断开，`/models` 为 599，健康门禁仍阻止真实请求；不含本机环境信息
- `qa/imagegen-channel-recheck-20260820-v6.json`: 2026-08-19T21:34:45Z 使用 Skill 官方非计费探针复核当前 Docker 渠道；Agent capabilities、渠道健康和 runtime 契约通过，但有效 request mode 仍为空，DNS 通过、TLS 在安全连接前断开、`/models` 返回 599；未创建 artifact，不含本机环境信息
- `qa/imagegen-channel-recheck-20260820-v7.json`: 2026-08-19T22:11:27Z API 配置变更后的最新非计费复核；DNS/TCP 通过但 TLS 在安全连接前断开，`/models` 返回 599，渠道仍为 `probe_pending`，未创建 artifact，不含本机环境信息
- `qa/imagegen-channel-recheck-20260820-v8.json`: 2026-08-19T23:40:58Z 当前 Docker 渠道 `jisuanyun-gpt-image`、两种 Images request mode、Agent 合同和 runtime 均健康；`/models` 返回 403 `INSUFFICIENT_BALANCE`，计费 smoke 在余额门禁后未发送，未创建 artifact，不含本机环境信息
- `qa/current-v2-gate-recheck-20260819-v1.json`: 2026-08-19T14:20:22Z 八角色 v2 图集、连续性、三目录 SHA、28 项 hatch-pet 回归测试、安装器解析和双远端主线复核；本地门禁通过，PetDex、图像渠道和 Codex App 边界仍单独记录；不含本机环境信息
- `qa/current-v2-gate-recheck-20260819-v2.json`: 2026-08-19T15:48:42Z 重新执行八角色 v2 图集、方向连续性、仓库与双本地目录 parity、28 项 hatch-pet 回归测试和安装器解析；8/8 通过，外部 PetDex 审核、图像渠道和 Codex App 视觉边界仍未闭合；不含本机环境信息
- `qa/current-v2-gate-recheck-20260820-v2.json`: 2026-08-19T18:15:18Z 使用隔离 Python 3.13.7/Pillow 12.3.0 重新执行八角色 v2 合同、连续性、28 项 hatch-pet 测试、安装器解析和三目录 SHA parity；8/8、28/28 通过，外部 PetDex、图像上游和 Codex App 边界仍未闭合；不含本机环境信息
- `qa/current-v2-gate-recheck-20260820-v3.json`: 2026-08-19T19:02:24Z 在提交 `9cd8d3d` 后独立重跑八角色 v2 合同、连续性、28 项 hatch-pet 测试、Bash/PowerShell 解析和三目录 SHA parity；8/8、28/28 通过，外部 PetDex、图像上游和 Codex App 边界仍未闭合；不含本机环境信息
- `qa/current-v2-gate-recheck-20260820-v4.json`: 2026-08-19T20:55:00Z 绑定复核基线 `922b2cc` 的八角色 v2 合同、连续性、28 项 hatch-pet 测试、安装器解析、三目录 SHA parity 和检查时双远端 HEAD；8/8、28/28 通过，外部 PetDex、生图渠道和 Codex App 边界仍未闭合；不含本机环境信息
- `qa/current-v2-gate-recheck-20260820-v5.json`: 2026-08-19T21:17:51Z 绑定复核基线 `f4341b8` 的八角色 v2 合同、连续性、28 项 hatch-pet 测试、安装器解析、三目录 SHA parity 和检查时双远端 HEAD；8/8、28/28 通过，外部 PetDex、生图渠道和 Codex App 边界仍未闭合；不含本机环境信息
- `qa/current-v2-gate-recheck-20260820-v6.json`: 2026-08-19T21:34:45Z 绑定提交 `1348bb9` 的八角色 v2 合同、连续性、28 项 hatch-pet 测试、安装器解析和三目录 SHA parity；8/8、28/28 通过，PetDex 六个 owned-slug、生图通道和 Codex App 边界仍未闭合；不含本机环境信息
- `qa/current-v2-gate-recheck-20260820-v7.json`: 2026-08-19T23:51:49Z 绑定提交 `39a59b2` 的八角色 v2 合同、连续性、28 项 hatch-pet 测试、安装器语法/ShellCheck/PowerShell 解析和三目录 SHA parity；8/8、28/28 通过，PetDex 六个 owned-slug、生图余额和 Codex App 边界仍未闭合；不含本机环境信息
- `qa/current-v2-gate-recheck-20260820-v8.json`: 2026-08-20T00:40:07Z 绑定正式资产基线 `39a59b2`、QA 提交 `df8c216` 的八角色 fresh v2 合同、连续性、28 项 hatch-pet 测试、安装器语法/ShellCheck/PowerShell 解析和三目录 SHA parity；8/8、28/28 通过，连续性 warning 仅为已审查证据；不含本机环境信息
- `qa/current-v2-gate-recheck-20260820-v9.json`: 2026-08-20T01:18:28Z 绑定已推送提交 `9543baf` 的 post-sync 八角色 v2 合同、连续性、28 项 hatch-pet 测试、安装器与 JSON/diff 检查和三目录 SHA parity；8/8、28/28 通过，连续性 warning 仅为已审查证据；不含本机环境信息
- `qa/current-v2-gate-recheck-20260820-v10.json`: 2026-08-20T04:47:21Z 绑定当前提交 `856b33d` 的八角色 v2、连续性、透明度、28 项测试、安装器解析和三目录 SHA parity 新鲜复核；8/8、28/28 通过，连续性 warning 仍为已审查 minor 证据；不含本机环境信息
- `qa/current-v2-gate-recheck-20260820-v11.json`: 2026-08-20T07:02:29Z 绑定提交 `242cd938` 的八角色 v2、连续性、透明度、28 项测试、安装器解析和三目录 SHA parity 新鲜复核；8/8、28/28 通过，透明 RGB 残留 0；不含本机环境信息
- `qa/current-v2-alpha-review-20260820-v2.json`: 2026-08-20T07:02:29Z 绑定提交 `242cd938` 的 11 个 alpha-hole 候选高对比复核；全部是与外部相连的合法开放负空间，封闭主体透明洞 0；不含本机环境信息
- `qa/remote-main-sync-recheck-20260820-v1.json`: 2026-08-20T05:19:14Z 复核当前提交 `6968f63` 的本地、GitHub 和 GitLab `main` 一致，GitHub raw README 可读取；保留用户原有未跟踪目录，不含本机环境信息
- `qa/remote-main-sync-recheck-20260820-v2.json`: 2026-08-20T06:11:10Z 复核当前提交 `942359b` 的本地、GitHub 和 GitLab `main` 一致，GitHub raw README 可读取并包含 PetDex v8 证据；保留用户原有未跟踪目录，不含本机环境信息
- `qa/remote-main-sync-recheck-20260820-v3.json`: 2026-08-20T07:21:33Z 绑定提交 `3e953fe` 的最终本地、GitHub 和 GitLab `main` 一致性、GitHub raw README 可达性和工作树边界复核；保留用户原有未跟踪目录，不含本机环境信息
- `qa/current-head-recheck-20260820-v1.json`: 2026-08-20T02:10:59Z 基于正式资产提交 `9876004` 的八角色 v2 合同、连续性、28 项 hatch-pet 测试、安装器检查、三目录 SHA parity、双远端主线和 PetDex 公开资源复核；本地门禁与远端同步通过，六个 owned-slug 更新和 Codex App 视觉验收仍未闭合；不含本机环境信息
- `qa/petdex-desktop-multidisplay-recheck-20260820-v1.json`: 2026-08-20T02:38:00Z PetDex Desktop v0.8.0 只读多显示器探针；旅行家在第二块显示器完整显示，3 次采样有动画变化，未见裁切或明显比例失衡；多角色切换、气泡跟随和长时回环仍未验收；不含本机环境信息
- `qa/petdex-desktop-multidisplay-recheck-20260820-v2.json`: 2026-08-20T04:47:21Z PetDex Desktop v0.8.0 跨屏气泡跟随复核；两个显示器均保持宠物与气泡清晰分离，原显示器已恢复；不含本机环境信息
- `qa/petdex-desktop-live-recheck-20260820-v3.json`: 2026-08-20T04:47:21Z PetDex Desktop v0.8.0 八角色 URI 切换/恢复、40 秒动画采样和 Codex 气泡显示复核；8/8 选择通过，34/39 相邻采样发生变化；不含本机环境信息
- `qa/current-state-recheck-20260820-v8.json`: 2026-08-19T22:11:27Z 绑定提交 `ad382c7` 的八角色本地门禁、PetDex 资源、图像通道 TLS、#689/#710 和 Codex App 边界汇总；本地门禁通过，外部边界仍未闭合；不含本机环境信息
- `qa/current-state-recheck-20260820-v10.json`: 2026-08-19T23:51:49Z 绑定提交 `39a59b2` 的八角色本地发布门禁、PetDex 4569 条目/2 个线上图集同步/6 个 owned-slug 待审核、生图渠道健康但上游余额门禁和 Codex App 未验证边界汇总；不含本机环境信息
- `qa/current-state-recheck-20260820-v11.json`: 2026-08-20T00:40:07Z 绑定提交 `df8c216`、正式资产基线 `39a59b2` 的本地发布、PetDex 公开资源、图像服务合同、上游 issue/PR 和 Codex App 边界汇总；本地 fixture 协议门禁通过，六个 owned-slug、生图余额和 Codex App 视觉验收仍未闭合；不含本机环境信息
- `qa/current-state-recheck-20260820-v12.json`: 2026-08-20T01:19:32Z 绑定已推送提交 `9543baf` 的本地发布、刷新后的 PetDex manifest、图像服务合同、上游 issue/PR 和 Codex App 边界汇总；本地 fixture 协议门禁通过，六个 owned-slug、真实上游生图和 Codex App 视觉验收仍未闭合；不含本机环境信息
- `qa/petdex-hook-eof-recheck-20260820.json`: CLI 1.2.2 隔离 Hook stdin 生命周期复现；有效 payload 在写端保持打开时超时，关闭 stdin 后正常退出；未触碰现有 Codex/ChatGPT 进程，不含本机环境信息
- `qa/petdex-hook-eof-recheck-20260820-v2.json`: CLI 1.2.2 当前版本 Hook EOF 边界复核；关闭 stdin 在 244ms 内正常退出，写端保持打开仍等待 EOF，#689 仍是上游未解决边界；不含本机环境信息
- `qa/petdex-hook-eof-recheck-20260820-v3.json`: CLI 1.2.2 在当前 HEAD 上的隔离 Hook EOF 重测；关闭 stdin 正常退出，写端保持打开 1.2 秒仍等待 EOF，仅终止隔离测试子进程；不含本机环境信息
- `qa/petdex-hook-eof-recheck-20260821-v1.json`: CLI 1.2.2 新鲜隔离 Hook EOF 重测；关闭 stdin 约 226ms 正常退出，写端保持打开 1.5 秒仍等待 EOF，仅终止隔离测试子进程；不含本机环境信息
- `qa/petdex-hook-eof-recheck-20260822-v3.json`: CLI 1.2.2 新鲜隔离 Hook EOF 重测；关闭 stdin 144ms 正常退出，写端保持打开 1.6 秒仍等待 EOF，仅终止隔离测试子进程；不含本机环境信息
- `qa/current-state-recheck-20260820-v14.json`: 2026-08-20T04:47:21Z 绑定当前提交的八角色本地门禁、PetDex Desktop 交互、跨屏气泡、Hook EOF、PetDex 线上待审核项和生图/上游边界综合状态；不含本机环境信息
- `qa/current-state-recheck-20260820-v15.json`: 2026-08-20T07:02:29Z 绑定提交 `242cd938` 的八角色本地门禁、alpha-hole 复核、PetDex Desktop 交互、跨屏气泡、Hook EOF、PetDex 线上待审核项和生图/上游边界综合状态；不含本机环境信息
- `qa/current-state-recheck-20260820-v16.json`: 2026-08-20T07:46:20Z 绑定提交 `6ae54de` 的八角色本地门禁、alpha-hole 复核、最新 PetDex manifest/metadata/SHA、Desktop 交互、Hook EOF 和外部边界综合状态；不含本机环境信息
- `qa/current-state-recheck-20260820-v17.json`: 2026-08-20T08:49:44Z 绑定当前主线的八角色新鲜门禁、PetDex 公开资源哈希、上游 Hook 状态和授权边界；不含本机环境信息
- `qa/current-state-recheck-20260820-v18.json`: 2026-08-20T09:22:19Z 绑定提交 `5b286e5` 的八角色门禁、当前 PetDex metadata/SHA、Hook EOF 实测和安全 Codex App 边界；不含本机环境信息
- `qa/current-state-recheck-20260820-v19.json`: 2026-08-20T09:58:27Z 绑定提交 `b4fd541` 的继续复核、PetDex 认证边界、Hook EOF 重测和本地回归；不含本机环境信息
- `qa/current-state-recheck-20260820-v20.json`: 2026-08-20T10:27:35Z 绑定提交 `75c85d0` 的八角色本地门禁、PetDex 公开资源、Hook EOF、Desktop/Codex App 边界和授权边界汇总；不含本机环境信息
- `qa/current-state-recheck-20260820-v21.json`: 2026-08-20T10:35:00Z 绑定 post-sync 提交 `42e5601`；确认三方主线一致，且资产树与安装器逻辑继承 v12 审计结果未变化；不含本机环境信息
- `qa/current-state-recheck-20260820-v22.json`: 2026-08-20T12:05:00Z 绑定提交 `90786c6` 的授权生图 smoke 结果；本地资产和门禁未变，真实上游两条协议均因余额不足失败；不含本机环境信息
- `qa/current-state-recheck-20260820-v23.json`: 2026-08-20T14:47:34Z 绑定提交 `679b093` 的本地 Docker 与部署服务双端生图复核、最新 PetDex manifest；本地健康门禁未通过，部署服务两次 502 后最终 403，未产生 artifact；不含本机环境信息
- `qa/current-state-recheck-20260821-v2.json`: 2026-08-21T04:30:22Z 绑定提交 `679b093` 的生图服务恢复后真实重试、最新 PetDex manifest 和八角色本地基线；编辑/生成均未产生 artifact，六个 owned-slug 更新仍待审核；不含本机环境信息
- `qa/current-state-recheck-20260821-v3.json`: 2026-08-21T10:28:25Z 汇总最新八角色本地基线、PetDex 线上图集 SHA、Hook EOF、上游 #689/#710 和两次本地生图失败；不含本机环境信息
- `qa/current-state-recheck-20260821-v4.json`: 2026-08-21T11:10:37Z 绑定当前 HEAD 的 PetDex v3 线上资源、Hook、上游状态、生图对账和最新 Codex App 窗口捕获边界；本地资产/安装门禁等待本轮新鲜 validator/test 结果，其余未闭合边界明确记录；不含本机环境信息
- `qa/current-state-recheck-20260821-v5.json`: 2026-08-21T11:35:47Z 绑定当前 HEAD 的新鲜八角色本地门禁、PetDex v3 线上资源、Hook、上游状态、生图对账和 Codex App 窗口捕获边界；本地资产/安装门禁通过，六个 owned-slug、生图和完整 Codex App 验收仍未闭合；不含本机环境信息
- `qa/current-state-recheck-20260821-v6.json`: 2026-08-21T11:58:32Z 绑定当前提交的最新本地生图请求对账、八角色门禁、PetDex 线上资源、Hook 和 Codex App 边界；本地请求无产物，正式资产未变；不含本机环境信息
- `qa/current-state-recheck-20260821-v7.json`: 2026-08-21T12:30:32Z 绑定当前提交的最新本地生图请求对账、八角色门禁、PetDex 线上资源、Hook 和 Codex App 边界；本地请求无产物，正式资产未变；不含本机环境信息
- `qa/current-state-recheck-20260821-v9.json`: 2026-08-21T14:04:26Z 绑定当前提交的最新 PetDex manifest 及本地/部署双端生图请求对账；本地 503、部署 403，均无 artifact，正式资产未变；不含本机环境信息
- `qa/current-state-recheck-20260821-v10.json`: 2026-08-21T15:30:12Z 绑定当前提交的自定义模型恢复 smoke；`gpt-image-2-1k` Agent 编排成功返回 2 个 1254x1254 WebP 临时 artifact，已删除并验证不存在；默认模型映射和固定尺寸契约仍单独保留边界；不含本机环境信息
- `qa/current-state-recheck-20260821-v11.json`: 2026-08-21T16:06:40Z 绑定当前提交的本机 Docker 自定义模型固定尺寸 smoke；`gpt-image-2-1k` 真实生成返回 1254x1254，1024x1024 尺寸门禁拒绝，临时 artifact 已确认不存在；部署服务仍拒绝自定义模型；不含本机环境信息
- `qa/current-state-recheck-20260822-v13.json`: 2026-08-21T20:45:51Z 绑定提交 `679b093` 的本机 Docker 自定义模型真实 smoke、PetDex 线上资源、Hook EOF 和 Codex App 边界；自定义模型生成成功但 1254x1254 未通过固定尺寸门禁，临时 artifact 已清理；不含本机环境信息
- `qa/current-state-recheck-20260822-v14.json`: 2026-08-21T21:01:08Z 绑定提交 `679b093` 的最新本机 Docker 自定义模型真实 smoke、PetDex 线上资源、Hook EOF 和 Codex App 边界；自定义模型生成成功但 1254x1254 未通过固定尺寸门禁，临时 artifact 已清理；不含本机环境信息
- `qa/current-state-recheck-20260822-v15.json`: 2026-08-21T21:14:32Z 绑定提交 `679b093` 的最新 PetDex 公开资源、Hook EOF、上游状态和本机生图证据；线上图集仍 2/8 与仓库一致，六个 owned-slug 更新未上线；不含本机环境信息
- `qa/current-state-recheck-20260822-v17.json`: 2026-08-21T21:48:25Z 绑定提交 `679b093` 的最新 PetDex 线上资源、本地八角色门禁、自定义模型非计费契约、Hook EOF 和 Codex App 边界；线上图集仍 2/8 与仓库一致，六个 owned-slug 更新未上线；不含本机环境信息
- `qa/current-state-recheck-20260822-v18.json`: 2026-08-21T22:21:33Z 绑定提交 `679b093` 的最新本机自定义模型真实 smoke、PetDex 线上资源、Hook EOF 和 Codex App 边界；源参考请求成功，固定 1024x1024 请求返回 1254x1254 并被门禁拒绝；临时产物已清理；不含本机环境信息
- `qa/current-state-recheck-20260822-v19.json`: 2026-08-21T22:41:15Z 绑定提交 `679b093` 的最新 PetDex manifest、恢复后的自定义模型非计费能力检查、Hook 上游状态和 Codex App 边界；六个 owned-slug 更新仍未上线，完整 Codex App 视觉验收仍未验证；不含本机环境信息
- `qa/current-state-recheck-20260822-v20.json`: 2026-08-21T23:01:17Z 绑定提交 `679b093` 的自定义模型成功真实 smoke、最新 PetDex 资源、Hook 上游状态和 Codex App 边界；自定义模型返回尺寸匹配的 1024x1536 WebP，六个 owned-slug 更新仍未上线，完整 Codex App 视觉验收仍未验证；不含本机环境信息
- `qa/current-state-recheck-20260822-v21.json`: 2026-08-21T23:28:23Z 绑定提交 `679b093` 的自定义模型固定尺寸 smoke、八角色新鲜门禁、PetDex 资源、Hook 上游状态和 Codex App 边界；固定 1024x1024 请求仍返回 1254x1254，六个 owned-slug 更新仍未上线，完整 Codex App 视觉验收仍未验证；不含本机环境信息
- `qa/imagegen-channel-recheck-20260823-v1.json`: 2026-08-22T16:20:30Z 本机 Docker 自定义模型 Agent 编排和页面 SSE 双路径真实复核；两条路径均返回可读取的 1024x1024 WebP，严格尺寸、视觉完整性和清理后 404 通过；未复现生成阶段存储读取失败，正式资产未变；不含本机环境信息
- `qa/imagegen-channel-recheck-20260823-v2.json`: 本机 Docker 自定义模型 Agent 编排 1024x1024 实际 smoke；下载、尺寸、视觉、artifact 删除和删除后 404 均通过；正式资产未变；不含本机环境信息
- `qa/imagegen-channel-recheck-20260823-v3.json`: 本机 Docker 自定义模型真实生成和页面 SSE 编辑均返回 1024x1024 WebP；下载、尺寸、视觉和各自清理/404 复核通过；正式资产未变；不含本机环境信息
- `qa/imagegen-channel-recheck-20260823-v21.json`: 2026-08-23T00:55:01Z 本机 Docker 自定义模型生成与页面 SSE 编辑双路径真实复核；两条路径均返回 1024x1024 WebP，尺寸、视觉和删除后 404 通过；正式资产未变；不含本机环境信息
- `qa/imagegen-channel-recheck-20260823-v22.json`: 2026-08-23T01:06:49Z 本机 Docker 自定义模型 `n=1`、1024x1024 真实生成；上游返回两张完整 WebP，二者尺寸、下载和视觉检查通过，artifact 删除后 metadata/content 均为 404；记录为上游数量契约边界，未静默截取，正式资产未变；不含本机环境信息
- `qa/imagegen-channel-recheck-20260823-v23.json`: 2026-08-23T01:53:00Z 本机 Docker 默认服务端编排恢复复核；非流式提示词审计 503 后，私有渠道优先级切换到已实测成功的 `images-sse`，`gpt-image-2-1k` 返回一张 1024x1024 WebP，尺寸/视觉通过，artifact 删除后 metadata/content 均为 404；不含本机环境信息
- `qa/imagegen-channel-recheck-20260823-v24.json`: 2026-08-23T02:07:12Z 本机 Docker 默认服务端编排新鲜 smoke；`images-sse` 返回一张 1024x1024 WebP，严格尺寸门禁通过，artifact 删除后 metadata/content 均为 404；本次未重复视觉检查，沿用既有视觉证据；不含本机环境信息
- `qa/imagegen-channel-recheck-20260823-v25.json`: 2026-08-23T02:32:10Z 本机 Docker 默认 Agent 编排新鲜 smoke；`images-sse` 返回一张完整 1024x1024 WebP，下载、严格尺寸和视觉检查通过，artifact 删除后 metadata/content 均为 404；正式资产未变；不含本机环境信息
- `qa/current-state-recheck-20260823-v1.json`: 2026-08-22T16:20:30Z 绑定提交 `679b093` 的本机生图双路径复核、八角色本地门禁、PetDex 线上资源、Hook EOF 和 Codex App 边界；生图服务可用，完整 Codex App 视觉验收仍未验证；不含本机环境信息
- `qa/petdex-live-recheck-20260823-v1.json`: 2026-08-22T16:50:51Z 只读刷新 PetDex manifest、八个公开角色 metadata/spritesheet、v2 尺寸格式和 SHA parity；8/8 通过，未执行 mutation；不含本机环境信息
- `qa/petdex-live-recheck-20260823-v2.json`: 2026-08-22T19:11:00Z 只读刷新 manifest 并实际下载八个当前角色；metadata/图集 HTTP 200、实际 v2/1536x2288/WebP 和仓库 SHA 为 8/8，但 manifest 索引有 6/8 pending URL 与版本滞后字段；未执行 mutation；不含本机环境信息
- `qa/petdex-live-recheck-20260823-v5.json`: 2026-08-23T00:55:01Z 跟随 manifest 307 重定向后重新读取八个当前角色；metadata/图集 HTTP 200、实际 v2/1536x2288/RGBA WebP 和仓库 SHA 为 8/8；未执行 mutation；不含本机环境信息
- `qa/petdex-live-recheck-20260823-v6.json`: 2026-08-23T02:01:00Z 按最新 manifest `2026-08-23T00:51:54.165Z` 重新下载八个当前角色及历史 `hei-mao-2`；当前角色 metadata/图集契约和 SHA 为 8/8，历史条目标记为 metadata ID 不匹配且仅记录；未执行 mutation；不含本机环境信息
- `qa/current-state-recheck-20260823-v3.json`: 2026-08-22T16:50:51Z 绑定八角色本地基线、生图服务、Hook 包装器和 PetDex 线上资源复核；完整 Codex App 视觉验收及上游 #689 EOF 修复仍明确未完成；不含本机环境信息
- `qa/current-state-recheck-20260823-v4.json`: 2026-08-22T17:23:29Z 绑定八角色本地基线、真实生图/编辑双路径、PetDex 线上资源和 Hook 包装器复核；生图与编辑均可用且临时结果已清理，完整 Codex App 视觉验收及上游 #689 EOF 修复仍明确未完成；不含本机环境信息
- `qa/current-state-recheck-20260823-v21.json`: 2026-08-23T00:55:01Z 绑定八角色本地门禁、生成/编辑双路径可用性、PetDex 线上资源、Hook 上游状态和 Codex App 边界；生图与编辑均可用且临时结果已清理，完整 Codex App 视觉验收及上游 #689 EOF 修复仍明确未完成；不含本机环境信息
- `qa/current-state-recheck-20260823-v22.json`: 2026-08-23T01:06:49Z 绑定本轮 `n=1` 生成返回两张图的数量契约边界、八角色本地门禁、PetDex 线上资源、Hook 上游状态和 Codex App 边界；正式资产未变，完整 Codex App 视觉验收及上游 #689 EOF 修复仍明确未完成；不含本机环境信息
- `qa/current-state-recheck-20260823-v23.json`: 2026-08-23T01:53:00Z 绑定本轮默认服务端编排恢复、八角色本地门禁、PetDex 线上资源、Hook 上游状态和 Codex App 边界；生图默认路径已通过，正式资产未变，完整 Codex App 视觉验收及上游 #689 EOF 修复仍明确未完成；不含本机环境信息
- `qa/current-state-recheck-20260823-v24.json`: 2026-08-23T02:10:26Z 绑定本轮本机 Docker `images-sse` 新鲜 smoke、八角色本地门禁、PetDex 线上资源、Hook 上游状态和 Codex App 边界；固定 1024x1024 通过且临时产物已清理，完整 Codex App 视觉验收及上游 #689 EOF 修复仍明确未完成；不含本机环境信息
- `qa/current-state-recheck-20260823-v25.json`: 2026-08-23T02:35:59Z 绑定本轮本机 Docker `images-sse` Agent 编排 smoke、八角色本地门禁、PetDex 线上资源、Hook 上游状态和 Codex App 边界；生成、下载、尺寸/视觉检查和临时产物清理均通过，完整 Codex App 视觉验收及上游 #689 EOF 修复仍明确未完成；不含本机环境信息
- `qa/current-state-recheck-20260823-v6.json`: 2026-08-22T19:02:52Z 绑定当前八角色、本地生图最小真实 smoke、PetDex 线上资源、Hook 包装器和上游状态；生图服务可用、正式资产未变，完整 Codex App 视觉验收及上游 #689 EOF 修复仍明确未完成；不含本机环境信息
- `qa/imagegen-channel-recheck-20260823-v5.json`: 本机 Docker 自定义模型最小真实生成复核；服务端编排选择 `images-non-stream`，1024x1024 WebP 下载、尺寸、视觉、artifact 删除和删除后 404 均通过；正式资产未变；不含本机环境信息
- `qa/imagegen-channel-recheck-20260823-v7.json`: 2026-08-22T20:18:13Z 本机 Docker 自定义模型全新真实生图复核；服务端编排选择 `images-non-stream`，1024x1024 WebP 下载、尺寸、视觉和 artifact 删除/404 均通过；正式资产未变；不含本机环境信息
- `qa/current-state-recheck-20260823-v8.json`: 2026-08-22T20:18:13Z 绑定八角色、本轮本机生图可用性 smoke、PetDex 线上资源、Hook 和 Codex App 边界；生图服务可用且临时产物已清理，完整 Codex App 视觉验收及上游 #689 EOF 修复仍明确未完成；不含本机环境信息
- `qa/petdex-upstream-status-recheck-20260823-v9.json`: 只读刷新 PetDex #689、draft PR #710、最新主线和 release；#689 仍 open、#710 仍为 draft/未合并，最新 release 仍为 Desktop v0.8.0；不含本机环境信息
- `qa/current-v2-gate-recheck-20260823-v7.json`: 2026-08-22T19:07:00Z 重新执行八角色实际色键 v2 图集门禁、28 项 hatch-pet 测试、三目录 SHA、ShellCheck、PowerShell、JSON 和公开隐私扫描；8/8、28 passed、16/16 通过；不含本机环境信息
- `qa/imagegen-channel-recheck-20260823-v9.json`: 2026-08-22T21:09:48Z 本机 Docker `gpt-image-2-1k` 固定尺寸真实生成复核；服务端编排选择 `images-non-stream`，返回 1024x1024 WebP，下载、尺寸和视觉检查通过，artifact 删除后 metadata/content 均为 404；正式资产未变；不含本机环境信息
- `qa/current-state-recheck-20260823-v10.json`: 2026-08-22T21:11:35Z 绑定本轮固定尺寸生图成功结果、八角色本地门禁、PetDex 线上资源、Hook 和 Codex App 边界；生图链路已可用，完整 Codex App 视觉验收及上游 #689 EOF 修复仍明确未完成；不含本机环境信息
- `qa/imagegen-channel-recheck-20260823-v12.json`: 2026-08-22T21:54:14Z 本机 Docker `gpt-image-2-1k` 固定尺寸真实生成复核；服务端编排选择 `images-non-stream`，返回 1024x1024 WebP，下载、尺寸、视觉检查和 artifact 删除/404 均通过；正式资产未变；不含本机环境信息
- `qa/current-state-recheck-20260823-v12.json`: 2026-08-22T22:12:36Z 绑定本轮固定尺寸生图成功结果、八角色本地门禁、PetDex 线上资源、Hook 和 Codex App 边界；生图链路可用，刷新官方 CLI 会话后 owned-slug 只读查询 8/8 HTTP 200 且均为 approved，未发生任何远端 mutation；完整 Codex App 视觉验收及上游 #689 EOF 修复仍明确未完成；不含本机环境信息
- `qa/imagegen-channel-recheck-20260823-v16.json`: 2026-08-22T23:21:47Z 本机 Docker `gpt-image-2-1k` 固定尺寸真实生成复核；服务端编排选择 `images-non-stream`，返回 1024x1024 WebP，下载、尺寸、视觉检查和 artifact 删除/404 均通过；正式资产未变；不含本机环境信息
- `qa/current-state-recheck-20260823-v16.json`: 2026-08-22T23:21:47Z 绑定本轮固定尺寸生图成功结果、八角色本地门禁、PetDex 线上资源、Hook 和 Codex App 边界；生图链路可用，完整 Codex App 视觉验收及上游 #689 EOF 修复仍明确未完成；不含本机环境信息
- `qa/imagegen-channel-recheck-20260823-v18.json`: 2026-08-22T23:44:36Z 本机 Docker `gpt-image-2-1k` 固定尺寸真实生成复核；服务端编排选择 `images-non-stream`，返回两张 1024x1024 WebP，下载、尺寸和视觉检查通过，两个临时 artifact 清理后 metadata/content 均为 404；正式资产未变；不含本机环境信息
- `qa/current-state-recheck-20260823-v18.json`: 2026-08-22T23:44:36Z 绑定本轮固定尺寸生图成功结果、八角色本地门禁、PetDex 线上资源、Hook 和 Codex App 边界；生图链路可用，完整 Codex App 视觉验收及上游 #689 EOF 修复仍明确未完成；不含本机环境信息
- `qa/imagegen-channel-recheck-20260822-v29.json`: 2026-08-22T15:49:17Z 本机 Docker 自定义模型批准参考图编辑真实复核；已批准角色图作为图像参考、配合中性保留指令成功返回匹配的 1024x1024 WebP，身份、服装和全身比例保持，页面图片删除后确认 404，本地临时文件已清理；正式资产未变；不含本机环境信息
- `qa/imagegen-channel-recheck-20260822-v26.json`: 2026-08-22T14:36:46Z 本机 Docker 自定义模型源参考 smoke；`gpt-image-2-1k` 经服务端编排返回匹配的 1024x1024 WebP，合同、严格尺寸、视觉、请求后健康检查和 artifact 清理通过；正式资产未变；不含本机环境信息
- `qa/imagegen-channel-recheck-20260822-v25.json`: 2026-08-22T14:05:18Z 本机 Docker 自定义模型真实源参考 smoke；`gpt-image-2-1k` 经服务端编排返回匹配的 1024x1024 RGB WebP，严格尺寸门禁、请求后健康检查、视觉完整性和 artifact 清理/404 复核通过；正式资产未变；不含本机环境信息
- `qa/imagegen-channel-recheck-20260822-v24.json`: 2026-08-22T12:12:08Z 本机 Docker 自定义模型真实源参考 smoke；`gpt-image-2-1k` 经服务端编排返回匹配的 1024x1024 RGBA WebP，严格尺寸门禁、请求后健康检查、视觉完整性和 artifact 删除/404 复核通过；正式资产未变；不含本机环境信息
- `qa/current-state-recheck-20260822-v38.json`: 2026-08-22T15:49:17Z 绑定提交 `679b093` 的自定义模型批准参考图编辑、八角色门禁、PetDex 线上资源、Hook EOF 和 Codex App 边界；已批准角色图参考编辑通过，品牌或既有 IP 文字提示词的上游审计边界已记录，完整 Codex App 视觉验收仍未验证；不含本机环境信息
- `qa/current-state-recheck-20260822-v35.json`: 2026-08-22T14:40:00Z 绑定提交 `679b093` 的本机 Docker 自定义模型、Hook fallback 和八角色发布状态；本地生图服务与 Hook 包装器可用，完整 Codex App 视觉验收仍未验证；不含本机环境信息
- `qa/current-state-recheck-20260822-v34.json`: 2026-08-22T14:05:18Z 绑定提交 `679b093` 的最新自定义模型真实生图源参考 smoke、八角色门禁、PetDex 线上资源、Hook 上游状态和 Codex App 边界；最新 `1024x1024` RGB WebP 通过视觉/尺寸门禁并完成 artifact 清理，完整 Codex App 视觉验收仍未验证；不含本机环境信息
- `qa/current-state-recheck-20260822-v33.json`: 2026-08-22T12:12:08Z 绑定提交 `679b093` 的真实生图源参考 smoke、八角色门禁、PetDex 线上资源、Hook 上游状态和 Codex App 边界；生图通道可用于后续 hatch-pet 源参考，完整 Codex App 视觉验收仍未验证；不含本机环境信息
- `qa/imagegen-channel-recheck-20260822-v23.json`: 2026-08-22T11:36:02Z 本机 Docker 自定义模型固定尺寸真实 smoke；`gpt-image-2-1k` 经服务端编排返回匹配的 1024x1024 WebP，严格尺寸门禁、请求后健康检查和 artifact 删除/404 复核通过；正式资产未变；不含本机环境信息
- `qa/imagegen-channel-recheck-20260822-v20.json`: 2026-08-22T00:06:15Z 本机 Docker 自定义模型固定尺寸真实 smoke；`gpt-image-2-1k` 接受 1024x1024 请求但返回 1254x1254，尺寸门禁非重试失败；artifact 删除后 metadata/content 均为 404，正式资产未变；不含本机环境信息
- `qa/current-state-recheck-20260822-v23.json`: 2026-08-22T00:06:15Z 绑定提交 `679b093` 的自定义模型固定尺寸 smoke、八角色门禁、PetDex 资源、Hook 上游状态和 Codex App 边界；固定尺寸契约仍未解决，六个 owned-slug 更新仍未上线，完整 Codex App 视觉验收仍未验证；不含本机环境信息
- `qa/current-state-recheck-20260822-v24.json`: 2026-08-22T00:23:40Z 绑定提交 `679b093` 的新鲜 PetDex manifest/资源、上游 Hook 状态、八角色本地门禁、隔离安装器和生图固定尺寸边界；本地门禁与安装通过，线上图集仍 2/8 与仓库一致，六个 owned-slug 更新待审核，完整 Codex App 验收仍未验证；不含本机环境信息
- `qa/current-state-recheck-20260822-v25.json`: 2026-08-22T00:46:03Z 绑定提交 `679b093` 的新鲜 PetDex 资源、隔离 Hook EOF 和 Codex App 窗口边界复核；本地门禁与线上 v2 资源契约保持通过，线上图集仍 2/8 与仓库一致，六个 owned-slug 更新待审核，Hook EOF 仍为上游 open，完整 Codex App 验收仍未验证；不含本机环境信息
- `qa/petdex-live-recheck-20260822-v12.json`: 2026-08-22T01:12:03Z 在内存中重新读取当前 manifest 并下载八个角色资源；8/8 metadata/图集 HTTP 200，实际 v2/1536x2288/RGBA WebP 通过，线上图集仍 2/8 与仓库一致，六个 owned-slug 更新未上线；不含本机环境信息
- `qa/current-state-recheck-20260822-v26.json`: 2026-08-22T01:12:36Z 绑定提交 `679b093` 的新鲜线上资源和 Hook EOF 复核；本地门禁与线上 v2 资源契约保持通过，线上图集仍 2/8 与仓库一致，Hook EOF 仍为上游 open，完整 Codex App 验收仍未验证；不含本机环境信息
- `qa/current-state-recheck-20260822-v27.json`: 2026-08-22T01:18:42Z 绑定提交 `679b093` 的新鲜线上资源、Hook EOF 和上游状态复核；本地门禁与线上 v2 资源契约保持通过，线上图集仍 2/8 与仓库一致，Hook EOF 仍为上游 open，完整 Codex App 验收仍未验证；不含本机环境信息
- `qa/current-state-recheck-20260822-v28.json`: 2026-08-22T01:54:14Z 绑定提交 `679b093` 的新鲜线上资源、Hook EOF、上游状态和 PetDex Desktop 8 角色 URI 切换复核；桌面端角色切换 8/8 通过，线上图集仍 2/8 与仓库一致，Hook EOF 仍为上游 open，完整 Codex App 验收仍未验证；不含本机环境信息
- `qa/petdex-desktop-role-switch-recheck-20260822-v1.json`: 2026-08-22T01:54:14Z PetDex Desktop v0.8.0 官方 URI 逐一切换八个角色均通过，恢复到 hei-mao-traveler 和原窗口位置；不含本机环境信息
- `qa/codex-app-boundary-recheck-20260822-v3.json`: 2026-08-22T01:27:00Z 只读复核 ChatGPT/PetDex 原生窗口边界；ChatGPT 窗口可捕获，PetDex 位于当前不存在的历史第二屏坐标且透明窗口捕获失败，未发送 UI 输入、未改设置、未停止或重启进程；完整 Codex App 宠物验收仍未验证，不含本机环境信息
- `qa/petdex-desktop-window-boundary-recheck-20260824-v1.json`: 2026-08-24T02:31:28Z 只读捕获 PetDex Desktop 当前旅行家和活动气泡；未发送 UI 输入、未移动窗口或切换角色，Codex App 全量宠物验收仍未验证；不含本机路径、地址、窗口坐标、进程标识或凭证
- `qa/current-state-recheck-20260824-v2.json`: 2026-08-24T02:40:19Z 汇总本轮 8/8 本地 v2 门禁、28 项 hatch-pet 测试、8/8 实时 PetDex metadata/图集和 SHA parity、Hook 上游状态及 Desktop/Codex App 边界；完整 Codex App 运行时验收仍未验证；不含本机路径、地址、进程标识或凭证
- `qa/current-v2-gate-recheck-20260822-v6.json`: 2026-08-22T00:52:00Z 绑定提交 `679b093` 的实际色键重跑八角色 atlas、28 项 hatch-pet 测试、隔离安装器、三目录 SHA parity、ShellCheck、PowerShell、JSON/diff 和隐私检查；8/8、28/28、16/16 通过；不含本机环境信息
- `qa/petdex-owned-slug-readonly-recheck-20260822-v1.json`: 2026-08-21T23:09:00Z 按官方 CLI edit 解析规则只读查询八个 owned-slug；8/8 HTTP 200、ID 存在且 status=approved，未调用 edit/presign/upload/submit；六个已提交 sprite 更新仍未上线；不含本机环境信息
- `qa/petdex-owned-slug-readonly-recheck-20260823-v2.json`: 2026-08-22T22:12:36Z 刷新官方 CLI 会话后按官方 edit 解析规则只读查询八个 owned-slug；8/8 HTTP 200、ID 存在且 status=approved，未调用 edit/presign/upload/submit；不含本机环境信息
- `qa/current-v2-gate-recheck-20260822-v3.json`: 2026-08-21T21:48:25Z 重新执行八角色 v2 图集、连续性、三目录 SHA、28 项 hatch-pet 回归测试、安装器解析和隐私检查；8/8、28/28 通过；不含本机环境信息
- `qa/current-v2-gate-recheck-20260822-v4.json`: 2026-08-21T23:28:23Z 使用专用 Python 3.13.7/Pillow 12.3.0 重新执行八角色 v2 图集、连续性和 28 项 hatch-pet 测试；8/8、28/28 通过，未修改正式资产；不含本机环境信息
- `qa/current-v2-gate-recheck-20260822-v5.json`: 2026-08-22T00:23:40Z 重新执行八角色 v2 图集、连续性、28 项 hatch-pet 测试、八角色隔离安装、未知 slug 拒绝、ShellCheck、PowerShell 解析和 diff 检查；全部通过；不含本机环境信息
- `qa/petdex-live-recheck-20260822-v7.json`: 2026-08-21T21:48:25Z 跟随 manifest 307 重定向后重新下载八个公开角色 metadata/图集；8/8 HTTP 200、实际 metadata v2、1536x2288/RGBA WebP 通过，线上图集仍 2/8 与仓库一致，六个 owned-slug 更新未上线；不含本机环境信息
- `qa/petdex-live-recheck-20260822-v8.json`: 2026-08-21T22:39:23Z 重新下载当前 manifest 指向的八个公开角色 metadata/图集并校验 SHA；8/8 metadata id/v2/1536x2288/RGBA WebP 通过，线上图集仍 2/8 与仓库一致，六个 owned-slug 更新未上线；不含本机环境信息
- `qa/petdex-live-recheck-20260822-v10.json`: 2026-08-22T00:23:40Z 重新读取 manifest 并下载八个当前角色 metadata/图集；8/8 metadata id/v2/1536x2288/RGBA WebP 通过，线上图集仍 2/8 与仓库一致，六个 owned-slug 更新未上线；不含本机环境信息
- `qa/petdex-live-recheck-20260822-v11.json`: 2026-08-22T00:46:03Z 重新读取 manifest 并下载八个当前角色 metadata/图集；8/8 metadata id/v2/1536x2288/RGBA WebP 通过，线上图集仍 2/8 与仓库一致，六个 owned-slug 更新未上线；不含本机环境信息
- `qa/petdex-hook-eof-recheck-20260822-v5.json`: 2026-08-21T21:14:32Z CLI 1.2.2 新鲜隔离 Hook EOF 复现；关闭 stdin 的测试子进程退出码 0，写端保持打开 1.6 秒仍等待 EOF；仅终止隔离测试子进程，不含本机环境信息
- `qa/petdex-hook-eof-recheck-20260822-v6.json`: 2026-08-22T00:32:00Z CLI 1.2.2 再次隔离复现 Hook EOF；关闭 stdin 正常退出，写端保持打开 1.6 秒未自然退出；仅终止隔离测试子进程，不含本机环境信息
- `qa/petdex-hook-eof-recheck-20260822-v7.json`: 2026-08-22T00:46:03Z CLI 1.2.2 隔离复现 Hook EOF；关闭 stdin 约 178ms 正常退出，写端保持打开 1.6 秒未自然退出；仅终止隔离测试子进程，不含本机环境信息
- `qa/petdex-hook-eof-recheck-20260822-v8.json`: 2026-08-22T01:12:36Z CLI 1.2.2 再次隔离复现 Hook EOF；关闭 stdin 正常退出，写端保持打开 1.6 秒未自然退出；仅终止隔离测试子进程，不含本机环境信息
- `qa/petdex-upstream-status-recheck-20260822-v2.json`: 2026-08-21T21:14:32Z 只读复核 issue #689、draft PR #710 和最新 release；#689 仍 open、#710 仍为 draft 且未合并、最新 release 仍为 Desktop v0.8.0；不含本机环境信息
- `qa/petdex-upstream-status-recheck-20260822-v3.json`: 2026-08-21T22:41:15Z 再次只读复核 issue #689、draft PR #710 和最新 release；状态未变，未发现改变 stdin EOF 语义的上游动作；不含本机环境信息
- `qa/petdex-upstream-status-recheck-20260822-v5.json`: 2026-08-22T00:23:40Z 通过 GitHub CLI 只读复核 issue #689、draft PR #710、最新主线和 release；#689 仍 open、#710 仍 draft/未合并，最新 release 仍为 Desktop v0.8.0；不含本机环境信息
- `qa/petdex-upstream-status-recheck-20260822-v6.json`: 2026-08-22T00:46:03Z 通过 GitHub CLI 只读复核 issue #689、draft PR #710、最新主线和 release；#689 仍 open、#710 仍 draft/未合并，最新 release 仍为 Desktop v0.8.0；不含本机环境信息
- `qa/petdex-upstream-status-recheck-20260822-v7.json`: 2026-08-22T01:18:42Z 通过 GitHub CLI 只读复核 issue #689、draft PR #710、最新主线和 release；#689 仍 open、#710 仍 draft/未合并，最新 release 仍为 Desktop v0.8.0；不含本机环境信息
- `qa/codex-app-boundary-recheck-20260822-v2.json`: 2026-08-22T00:46:03Z 只读复核 ChatGPT/Codex App 窗口和 Computer Use 边界；WindowServer 可发现窗口但原生/全屏捕获均失败，未执行设置或宠物操作，未停止或重启进程；完整 Codex App 宠物验收仍未验证，不含本机环境信息
- `qa/current-state-recheck-20260822-v1.json`: 2026-08-21T16:27:07Z 绑定当前提交的本机 Docker 自定义模型真实复核和最新 PetDex 线上资源；自定义模型生成可达但 1254x1254 输出未通过 1024 固定尺寸门禁，正式资产未变；不含本机环境信息
- `qa/current-state-recheck-20260822-v2.json`: 2026-08-21T16:51:11Z 绑定当前提交的本机 Docker 自定义模型探针与真实 Agent 编排复核；自定义模型已列出并可生成，但 1254x1254 输出未通过 1024 固定尺寸门禁，artifact 删除及 404 复核通过，正式资产未变；不含本机环境信息
- `qa/current-state-recheck-20260822-v3.json`: 2026-08-21T17:15:39Z 绑定当前提交的本机 Docker 自定义模型恢复 smoke；`gpt-image-2-1k` 的 1024x1024 与 auto 请求均返回 1254x1254 WebP，固定尺寸门禁未通过，两个 artifact 删除及 404 复核通过，正式资产未变；不含本机环境信息
- `qa/current-state-recheck-20260822-v4.json`: 2026-08-21T18:04:32Z 绑定当前提交的新鲜本机 Docker 自定义模型 smoke；`gpt-image-2-1k` 的 1024x1024 请求返回 1254x1254 WebP，固定尺寸门禁未通过，artifact 删除及 404 复核通过，正式资产未变；不含本机环境信息
- `qa/current-state-recheck-20260822-v5.json`: 2026-08-21T18:26:18Z 绑定当前提交的最新本机 Docker 自定义模型 smoke；`gpt-image-2-1k` 的 1024x1024 请求实际返回 1254x1254 WebP，固定尺寸门禁未通过，artifact 删除及 404 复核通过，正式资产未变；不含本机环境信息
- `qa/current-state-recheck-20260822-v6.json`: 2026-08-21T18:54:13Z 绑定当前提交的最新本机 Docker 自定义模型 smoke；`gpt-image-2-1k` 的 1024x1024 请求实际返回 1254x1254 WebP，固定尺寸门禁未通过，artifact 删除及 404 复核通过，正式资产未变；不含本机环境信息
- `qa/current-state-recheck-20260822-v11.json`: 2026-08-21T19:59:40Z 绑定当前提交的最新本机 Docker 自定义模型 smoke；`gpt-image-2-1k` 的 1024x1024 请求实际返回 1254x1254 WebP，固定尺寸门禁未通过，artifact 删除及 404 复核通过，正式资产未变；不含本机环境信息
- `qa/petdex-live-recheck-20260820-v2.json`: 最新 manifest 与八个公开资源的 metadata/图集 SHA 对照；八个 metadata 为 v2，六个 owned-slug 更新仍未切换；不含本机环境信息
- `qa/petdex-live-recheck-20260820-v3.json`: 2026-08-19T21:30:28Z 重新读取官方 manifest 并下载八个当前角色资源；8/8 metadata 为 v2、1536x2288、RGBA WEBP，仓库图集 SHA 仍仅 2/8 一致，六个 owned-slug 更新仍待审核，历史 `hei-mao-2` 仍存在；不含本机环境信息
- `qa/petdex-live-recheck-20260820-v4.json`: 2026-08-19T22:11:27Z 严格按八个当前 slug 重新下载 PetDex metadata/图集并做 SHA 对照；8/8 metadata id/v2 通过，2/8 图集与仓库一致，六个 owned-slug 更新仍待审核；不含本机环境信息
- `qa/petdex-live-recheck-20260820-v5.json`: 2026-08-19T23:40:24Z 重新下载八个公开 metadata/图集；8/8 HTTP 200、v2、1536x2288、RGBA，metadata SHA 7/8 与仓库一致，图集 SHA 2/8 与仓库一致，六个 owned-slug 更新仍待审核；不含本机环境信息
- `qa/petdex-live-recheck-20260820-v6.json`: 2026-08-20T00:29:44Z 重新下载八个公开 metadata/图集；8/8 HTTP 200、v2、1536x2288、RGBA WEBP，metadata SHA 7/8 与仓库一致，图集 SHA 2/8 与仓库一致，六个 owned-slug 更新仍待审核；不含本机环境信息
- `qa/petdex-live-recheck-20260820-v7.json`: 2026-08-20T01:17:00Z manifest 刷新至 2026-08-20T00:46:43.668Z 后重新下载八个公开 metadata/图集；8/8 HTTP 200、实际 metadata v2、1536x2288、RGBA WEBP，metadata SHA 7/8 与仓库一致，图集 SHA 2/8 与仓库一致，六个 owned-slug 更新仍待审核；不含本机环境信息
- `qa/petdex-live-recheck-20260820-v8.json`: 2026-08-20T05:57:59Z 重新读取官方 manifest 并实际下载八个公开图集；8/8 metadata HTTP 200 且实际为 v2，图集 SHA 仍为 2/8 与仓库一致，六个 owned-slug 更新仍待审核；不含本机环境信息
- `qa/petdex-live-recheck-20260820-v9.json`: 2026-08-20T07:31:00Z 重新读取官方 manifest（生成于 2026-08-20T06:31:51.943Z）并实际下载八个公开图集与 metadata；8/8 metadata id 和实际 spriteVersionNumber=2，图集 SHA 仍为 2/8 与仓库一致，六个 owned-slug 更新仍待审核；不含本机环境信息
- `qa/petdex-live-recheck-20260820-v10.json`: 2026-08-20T09:22:19Z 刷新官方 manifest、八个公开 metadata 和图集 SHA；8/8 metadata 为 v2，线上图集仍 2/8 与仓库一致，六个 owned-slug 更新仍待审核；不含本机环境信息
- `qa/petdex-live-recheck-20260820-v11.json`: 2026-08-20T10:25:45Z 重新下载官方 manifest、八个公开 metadata 和图集；8/8 HTTP 200、ID/v2/1536x2288/RGBA WebP 通过，线上图集仍 2/8 与仓库一致，六个 owned-slug 更新仍待审核；不含本机环境信息
- `qa/petdex-live-recheck-20260820-v12.json`: 2026-08-20T14:47:34Z 刷新官方 manifest 并重新读取八个公开 metadata/图集；8/8 HTTP 200、实际 metadata v2、1536x2288、RGBA WebP 通过，线上图集仍 2/8 与仓库一致，六个 owned-slug 更新仍待审核；不含本机环境信息
- `qa/petdex-live-recheck-20260821-v1.json`: 2026-08-21T00:51:37.079Z 刷新官方 manifest 并重新读取八个公开 metadata/图集；8/8 HTTP 200、实际 metadata v2、1536x2288、RGBA WebP 通过，线上图集仍 2/8 与仓库一致，六个 owned-slug 更新仍待审核，历史 `hei-mao-2` 仅作记录；不含本机环境信息
- `qa/petdex-live-recheck-20260821-v2.json`: 2026-08-21T10:14:47Z 刷新官方 manifest 并重新下载八个公开 metadata/图集；8/8 HTTP 200、实际 metadata v2、1536x2288、RGBA WebP 通过，线上图集仍 2/8 与仓库一致，六个 owned-slug 更新仍待审核，未重复提交；不含本机环境信息
- `qa/petdex-live-recheck-20260821-v3.json`: 2026-08-21T10:57:51Z 独立重新读取 manifest 并下载八个公开 metadata/图集；8/8 HTTP 200、ID/v2/1536x2288/RGBA WebP 通过，线上图集仍 2/8 与仓库一致，六个 owned-slug 更新仍待审核，未重复提交；不含本机环境信息
- `qa/petdex-live-recheck-20260821-v5.json`: 2026-08-21T14:04:26Z 刷新官方 manifest，确认生成时间 `2026-08-21T12:30:23.084Z`、4568 条目和八个当前 slug；沿用最新完整资源下载的 8/8 metadata/图集契约，线上图集仍 2/8 与仓库一致；不含本机环境信息
- `qa/petdex-live-recheck-20260822-v1.json`: 2026-08-21T16:27:07Z 重新读取官方 manifest 并实际下载八个当前角色 metadata/图集；8/8 HTTP 200、实际 metadata v2、1536x2288、RGBA WEBP，线上图集仍 2/8 与仓库一致，六个 owned-slug 更新仍待审核；不含本机环境信息
- `qa/petdex-live-recheck-20260822-v2.json`: 2026-08-22T01:02:00+08:00 重新读取官方 manifest 并实际下载八个当前角色 metadata/图集；8/8 HTTP 200、实际 metadata v2、1536x2288、RGBA WEBP，线上图集仍 2/8 与仓库一致，六个 owned-slug 更新仍未上线；不含本机环境信息
- `qa/petdex-live-recheck-20260822-v3.json`: 2026-08-21T18:36:44Z 重新读取官方 manifest 并实际下载八个当前角色 metadata/图集；8/8 HTTP 200、实际 metadata v2、1536x2288、RGBA WEBP，线上图集仍 2/8 与仓库一致，六个 owned-slug 更新仍未上线；不含本机环境信息
- `qa/petdex-upstream-status-recheck-20260820-v6.json`: 2026-08-20T10:25:45Z 只读复核 issue #689、draft PR #710 和最新 release；状态未变，未发现改变 stdin EOF 语义的上游动作；不含本机环境信息
- `qa/petdex-upstream-status-recheck-20260821-v1.json`: 2026-08-21T10:28:25Z 新鲜只读复核 issue #689、draft PR #710 和最新 release；#689 仍 open、#710 仍为 draft 且未合并、最新 release 仍为 Desktop v0.8.0；不含本机环境信息
- `qa/codex-app-boundary-recheck-20260821-v1.json`: 2026-08-21T11:02:00Z 只读复核 ChatGPT/Codex App 窗口和屏幕捕获边界；WindowServer 可见 ChatGPT 窗口，但窗口/全屏捕获均失败，未发送输入、未改设置、未停止或重启进程；完整 Codex App 宠物验收仍未验证，不含本机环境信息
- `qa/current-v2-gate-recheck-20260820-v12.json`: 2026-08-20T10:27:35Z 绑定当前 HEAD `75c85d0` 的八角色 atlas、连续性、透明度、28 项 hatch-pet 测试、安装器、三目录 parity 和隐私复核；8/8、28/28 通过；不含本机环境信息
- `qa/current-v2-gate-recheck-20260821-v1.json`: 2026-08-21T11:35:47Z 绑定当前 HEAD `679b093`，按每个角色真实 chroma key 新鲜重跑八角色 atlas、连续性、透明度、28 项 hatch-pet 测试、安装器、三目录 parity、JSON/diff 和隐私复核；8/8、28/28 通过；不含本机环境信息
- `qa/current-v2-gate-recheck-20260822-v1.json`: 2026-08-21T16:27:07Z 绑定当前 HEAD `679b093`，专用 Python 3.13.7/Pillow 12.3.0 新鲜重跑八角色 atlas 与连续性，8/8 无 validator error、8/8 连续性无 error，28/28 hatch-pet 测试通过；不含本机环境信息
- `qa/remote-main-sync-recheck-20260820-v4.json`: 2026-08-20T07:46:20Z 绑定提交 `6ae54de` 的本地、GitHub 和 GitLab `main` 一致性、GitHub raw README 可达性和工作树边界复核；不含本机环境信息
- `qa/remote-main-sync-recheck-20260820-v5.json`: 2026-08-20T10:35:00Z 绑定提交 `42e5601` 的本地、GitHub 和 GitLab `main` 一致性，确认本轮仅同步 QA/README；不含本机环境信息
- `qa/current-state-recheck-20260820-v4.json`: 2026-08-19T20:55:00Z 绑定复核基线 `922b2cc` 的本地发布门禁、PetDex 4569 条目/6 个 owned-slug 待审核、生图渠道 `probe_pending` 和 Codex App 未验证边界汇总；不含本机环境信息
- `qa/current-state-recheck-20260820-v5.json`: 2026-08-19T21:07:23Z 绑定提交 `94d5cca` 的八角色本地发布门禁、最新生图 TLS 阻断、PetDex 六个 owned-slug 待审核和 Codex App 未验证边界汇总；不含本机环境信息
- `qa/current-state-recheck-20260820-v6.json`: 2026-08-19T21:17:51Z 绑定提交 `f4341b8` 的八角色本地发布门禁、最新生图 TLS 阻断、PetDex 六个 owned-slug 待审核和 Codex App 未验证边界汇总；不含本机环境信息
- `qa/current-state-recheck-20260820-v7.json`: 2026-08-19T21:34:45Z 绑定提交 `1348bb9` 的八角色本地发布门禁、最新 PetDex manifest/下载、图像通道 TLS 阻断、#689/#710 状态和 Codex App 未验证边界汇总；不含本机环境信息
- `qa/petdex-upstream-status-recheck-20260820-v3.json`: 2026-08-19T22:11:27Z 再次核对 #689、#603、#654、#710、最新 release 和近期主线；#689/#710 状态未变，#603/#654 已关闭，未发现改变 stdin EOF 语义的动作；不含本机环境信息
- `qa/petdex-upstream-status-recheck-20260820-v4.json`: 2026-08-20T00:37:00Z 再次核对 #689、#603、#654、#710、最新 release 和近期主线；#689/#710 状态未变，#603/#654 已关闭，最新 release 仍为 Desktop v0.8.0；不含本机环境信息
- `qa/petdex-upstream-status-recheck-20260820-v5.json`: 2026-08-20T01:17:00Z 使用已认证只读接口再次核对 #689、#603、#654、#710、最新 release 和近期主线；#689/#710 状态未变，#603/#654 已关闭，最新 release 仍为 Desktop v0.8.0；不含本机环境信息
- `qa/imagegen-channel-recheck-20260820-v9.json`: 2026-08-20T00:32:15Z 当前 Docker 渠道、Agent doctor、运行时合同和本地六协议 fixture 门禁复核；本地合同通过，真实上游余额证据仍为 403 `INSUFFICIENT_BALANCE`，未发送新计费请求或创建 artifact；不含本机环境信息
- `qa/imagegen-channel-recheck-20260820-v10.json`: 2026-08-20T01:19:32Z API 配置更新后的本地 Docker 渠道、Agent doctor、运行时合同和六协议 fixture final gate 复核；本地服务/合同/fixture 通过，真实计费 smoke 未发送，最新已知余额证据仍为 403 `INSUFFICIENT_BALANCE`；不含本机环境信息
- `qa/imagegen-channel-recheck-20260820-v13.json`: 2026-08-20T12:04:00Z 获得授权后的两条真实 smoke 均到达上游并返回 403 `INSUFFICIENT_BALANCE`；0 个 artifact，正式资产未变，失败后渠道进入 `probe_pending`；不含本机环境信息
- `qa/imagegen-channel-recheck-20260820-v14.json`: 2026-08-20T12:35:26Z 用户确认后的本地 Docker/部署服务双端复核；本地请求被无健康渠道门禁拒绝，部署服务两次新幂等键请求均返回不可重试 403；0 个 artifact，正式资产未变；不含本机环境信息
- `qa/imagegen-channel-recheck-20260820-v17.json`: 2026-08-20T14:43:15Z 用户确认后的 Quality row-9 最小生成复核；本地两次请求在健康门禁拒绝，部署服务两次 502 后最后一次 403 授权失败；0 个 artifact，正式资产未变；不含本机环境信息
- `qa/imagegen-channel-recheck-20260820-v18.json`: 2026-08-20T15:15:00Z 用户确认后的 Quality row-9 继续复核；本地 Agent 请求因无健康渠道返回 503，部署 Agent 请求返回 401、页面 SSE 返回 403；0 个 artifact，正式资产未变；不含本机环境信息
- `qa/imagegen-channel-recheck-20260821-v1.json`: 2026-08-21T03:45:50Z 生图服务恢复后的 Quality row-9 真实复核；本地渠道健康但生成/编辑 smoke 返回上游 400/502，部署渠道返回上游 403 授权失败；0 个 artifact，正式资产未变；不含本机环境信息
- `qa/current-state-recheck-20260821-v1.json`: 2026-08-21T03:45:50Z 绑定提交 `679b093` 的生图服务恢复后综合状态；八角色本地门禁保持通过，Quality 正式图集未变，PetDex 六个 owned-slug 更新和 Codex App 全量验收仍待完成；不含本机环境信息
- `qa/imagegen-channel-recheck-20260821-v2.json`: 2026-08-21T04:25:07Z 生图服务恢复后的 Quality row-9 多参考图、单参考图、页面 SSE 和 1K 文生图真实重试；本地编辑返回上游 400、生成返回上游 502，部署编辑返回上游 403，0 个 artifact，正式资产未变；不含本机环境信息
- `qa/imagegen-channel-recheck-20260821-v6.json`: 2026-08-21T09:57:32Z 生图服务调整后的本地 Docker 编排 smoke；合同和渠道健康门禁通过，但 `gpt-image-2` 上游返回不可重试 503，提示模型与上游可用模型不一致；0 个 artifact，正式资产未变；不含本机环境信息
- `qa/imagegen-channel-recheck-20260821-v7.json`: 2026-08-21T10:09:48Z 生图服务调整后的第二次本地 Docker 编排 smoke；请求到达 `meinianda-image` 但 `gpt-image-2` 仍返回不可重试 503，0 个 artifact；外部成功消费截图未与本地请求关联，不含本机环境信息
- `qa/imagegen-channel-recheck-20260821-v8.json`: 2026-08-21T10:47:17Z 最新本地 Docker 编排 smoke 与 Agent 状态只读对账；真实请求返回 503、Agent 状态为 failed、0 个 artifact；后台成功记录未与本机请求关联，并记录即时响应与存储状态的 retryable 字段不一致；不含本机环境信息
- `qa/imagegen-channel-recheck-20260821-v9.json`: 2026-08-21T11:35:47Z 用户提供后台成功记录后的新幂等键本地真实 smoke 与 Agent 状态只读对账；渠道健康和合同通过，但真实请求仍返回 503、Agent 状态为 failed、0 个 artifact；后台成功记录未与本机请求关联；不含本机环境信息
- `qa/imagegen-channel-recheck-20260821-v11.json`: 2026-08-21T12:30:32Z 用户提供后台成功记录后的新幂等键本地真实 smoke 与 Agent 状态只读对账；渠道健康和合同通过，但真实请求仍返回 503、Agent 状态为 failed、0 个 artifact；后台成功记录未与本机请求关联；不含本机环境信息
- `qa/imagegen-channel-recheck-20260821-v12.json`: 2026-08-21T14:04:26Z 用户提供后台成功记录后的本地与部署双端真实 smoke 及 Agent 状态对账；本地返回 503、部署返回 403，均为 failed 且 0 个 artifact，后台成功记录未与测试请求关联；不含本机环境信息
- `qa/imagegen-channel-recheck-20260821-v14.json`: 2026-08-21T15:30:12Z 生图服务恢复并开放自定义模型后的真实 Agent 编排 smoke；`gpt-image-2-1k` 成功返回 2 个 1254x1254 WebP artifact，删除后查询为 404；渠道和两种 Images request mode 健康，默认模型与固定 1024 尺寸契约仍保留边界；不含本机环境信息
- `qa/imagegen-channel-recheck-20260821-v15.json`: 2026-08-21T16:06:40Z 本机 Docker 自定义模型固定尺寸真实 smoke；`gpt-image-2-1k` 生成 1254x1254，1024x1024 尺寸校验失败并确认临时 artifact 不存在；部署旧 Agent 合同拒绝自定义模型；不含本机环境信息
- `qa/imagegen-channel-recheck-20260822-v1.json`: 2026-08-21T16:27:07Z 本机 Docker 自定义模型真实 smoke；`gpt-image-2-1k` 请求被接受并生成 1254x1254 WebP，1024x1024 尺寸校验按预期失败，删除和 404 清理验证通过；本次未重新测试部署服务；不含本机环境信息
- `qa/imagegen-channel-recheck-20260822-v2.json`: 2026-08-21T16:51:11Z 本机 Docker 自定义模型探针与真实 Agent 编排 smoke；`gpt-image-2-1k` 已列出并被接受，生成 1254x1254 WebP，1024x1024 尺寸校验按预期失败，artifact 删除及内容/metadata 404 清理验证通过；本次未重新测试部署服务；不含本机环境信息
- `qa/imagegen-channel-recheck-20260822-v3.json`: 2026-08-21T17:15:39Z 本机 Docker 自定义模型恢复 smoke；`gpt-image-2-1k` 已列出并被接受，1024x1024 与 auto 请求均生成 1254x1254 WebP，固定尺寸门禁按预期失败，两个 artifact 删除及内容/metadata 404 清理验证通过；本次未重新测试部署服务；不含本机环境信息
- `qa/imagegen-channel-recheck-20260822-v4.json`: 2026-08-21T18:04:32Z 本机 Docker 自定义模型恢复 smoke；`gpt-image-2-1k` 已列出并被接受，1024x1024 请求生成 1254x1254 WebP，固定尺寸门禁按预期失败，artifact 删除及内容/metadata 404 清理验证通过；本次未重新测试部署服务；不含本机环境信息
- `qa/imagegen-channel-recheck-20260822-v5.json`: 2026-08-21T18:26:18Z 本机 Docker 自定义模型真实 smoke；`gpt-image-2-1k` 已列出并被接受，1024x1024 请求实际生成 1254x1254 WebP，固定尺寸门禁按预期失败，artifact 删除及内容/metadata 404 清理验证通过；本次未重新测试部署服务；不含本机环境信息
- `qa/imagegen-channel-recheck-20260822-v7.json`: 2026-08-21T19:21:33Z 本机 Docker 自定义模型真实 smoke；`gpt-image-2-1k` 已列出并被接受，1024x1024 请求实际生成 1254x1254 WebP，固定尺寸门禁未通过，artifact 删除及内容/metadata 404 清理验证通过；本次未重新测试部署服务；不含本机环境信息
- `qa/imagegen-channel-recheck-20260822-v9.json`: 2026-08-21T19:59:40Z 本机 Docker 自定义模型真实 smoke；`gpt-image-2-1k` 已列出并被接受，1024x1024 请求实际生成 1254x1254 WebP，固定尺寸门禁未通过，artifact 删除及内容/metadata 404 清理验证通过；本次未重新测试部署服务；不含本机环境信息
- `qa/imagegen-channel-recheck-20260822-v11.json`: 2026-08-21T20:45:51Z 本机 Docker 自定义模型真实 smoke；`gpt-image-2-1k` 被默认 Agent 编排入口接受并生成 1254x1254 WebP，1024x1024 固定尺寸门禁未通过，artifact 删除及内容/metadata 404 清理验证通过；本次未测试部署服务；不含本机环境信息
- `qa/imagegen-channel-recheck-20260822-v12.json`: 2026-08-21T21:01:08Z 本机 Docker 自定义模型真实 smoke；`gpt-image-2-1k` 被默认 Agent 编排入口接受并生成 1254x1254 WebP，1024x1024 固定尺寸门禁未通过，artifact 删除及内容/metadata 404 清理验证通过；本次未测试部署服务；不含本机环境信息
- `qa/imagegen-channel-recheck-20260822-v13.json`: 2026-08-21T21:29:39Z 本机 Docker 自定义模型实时目录探测和真实 smoke；五个自定义模型可探测，`gpt-image-2-1k` 生成 1254x1254 WebP，1024x1024 固定尺寸门禁未通过，artifact 和本地生成文件已清理并确认不存在；本次未测试部署服务；不含本机环境信息
- `qa/imagegen-channel-recheck-20260822-v14.json`: 2026-08-21T21:48:25Z 本机 Docker 自定义模型健康渠道与非计费契约复核；`gpt-image-2-1k` 自定义模型意图被接受，上一轮真实 smoke 的 1254x1254 输出仍未通过固定尺寸门禁，本轮未重复计费请求；不含本机环境信息
- `qa/imagegen-channel-recheck-20260822-v15.json`: 2026-08-21T22:21:33Z 本机 Docker 自定义模型真实 smoke；`gpt-image-2-1k` 的 auto 请求生成 1024x1536 源参考图，固定 1024x1024 请求返回 1254x1254 并被尺寸门禁拒绝，两次产物均删除并验证 metadata/content 为 404；不含本机环境信息
- `qa/imagegen-channel-recheck-20260822-v16.json`: 2026-08-21T22:39:23Z 本机 Docker 自定义模型恢复后的非计费 Agent 能力/运行时契约复核；自定义模型请求构造被接受，实际有效模式为 images-non-stream/images-sse，Responses 后端仍未启用；不含本机环境信息
- `qa/imagegen-channel-recheck-20260822-v17.json`: 2026-08-21T23:01:17Z 本机 Docker 自定义模型真实 smoke；`gpt-image-2-1k` 通过 images-non-stream Agent JSON 返回尺寸匹配的 1024x1536 WebP，临时 artifact 删除并确认 metadata/content 为 404；不含本机环境信息
- `qa/imagegen-channel-recheck-20260822-v18.json`: 2026-08-21T23:28:23Z 本机 Docker 自定义模型固定尺寸真实 smoke；`gpt-image-2-1k` 被接受但 1024x1024 请求返回 1254x1254，尺寸门禁非重试失败；artifact 删除并确认 metadata/content 为 404，正式资产未变；不含本机环境信息
- `qa/imagegen-channel-recheck-20260823-v29.json`: 2026-08-23T07:18:41Z 本机 Docker 自定义模型 `1536x2288` 真实 smoke；上游 `1024x1536` 竖版结果按动态有界比例门禁补边归一化为 `1536x2288` WebP，尺寸和视觉检查通过，artifact 删除及 metadata/content 404 清理验证通过；不含本机环境信息
- `qa/imagegen-channel-recheck-20260824-v1.json`: 2026-08-24T00:40:24Z 本机 Docker 自定义模型 `1536x2288`、n=1 最新路由 smoke；服务端编排 HTTP 200 返回 1 个临时 artifact，删除后 metadata/content 404，正式资产未变；尺寸/视觉合同沿用 v29；不含本机环境信息
- `qa/current-state-recheck-20260821-v2.json`: 2026-08-21T04:30:22Z 绑定提交 `679b093` 的生图重试与最新 PetDex 线上快照；八角色本地门禁保持通过，Quality 正式图集未变，PetDex 六个 owned-slug 更新和 Codex App 全量验收仍待完成；不含本机环境信息
- `qa/current-state-recheck-20260820-v2.json`: 2026-08-19T18:15:18Z 汇总本轮本地门禁、正式服务 403 smoke、PetDex 4569 条目/6 个 owned-slug 待审核和 Codex App 未验证边界；不含本机环境信息
- `qa/current-local-recheck-20260818-v1.json`: 生图重试后的八角色 v2 结构、方向连续性和 28 项 hatch-pet 回归测试复核；这是 Quality recovery-v2 之前的历史快照，比例阻断已由 `qa/hei-mao-quality/recovery-v2/` 解决
- `qa/hei-mao-quality/proportion-repair-20260818.json`: 品控官 row 10 八个方向的历史中间等比归一化记录；最终两条 look row 以 `qa/hei-mao-quality/recovery-v2/` 为准
- `qa/hei-mao-quality/proportion-recheck-20260818.json`: Quality recovery-v2 之前的历史 alpha 高度对照；曾确认两个 cardinal 偏矮，后续已由 recovery-v2 的完整 row 9/10 重生成解决
- `qa/hei-mao-quality/chroma-despill-recheck-20260818.json`: 品控官等比修复后的透明度与既有单次去溢继承边界
- `qa/petdex-live-recheck-20260818-v2.json`: 2026-08-17T18:26:47.414Z manifest、八角色公开资源 SHA/metadata、GitHub/GitLab `a6d7a71` 主线提交对照；六个本地修复图集仍待 PetDex 审核，不含本机环境信息
- `qa/petdex-live-recheck-20260818-v3.json`: 2026-08-18T00:46:18.062Z manifest 和八角色公开 `petjson`/图集实际下载复核；八个 metadata 均为 v2、1536x2288、RGBA，只有大管家和厨师线上 SHA 与仓库一致，其余六个 owned-slug 更新仍待审核，不含本机环境信息
- `qa/petdex-live-recheck-20260818-v4.json`: 2026-08-18T06:29:10.591Z manifest 逐角色解析和公开资源复核；八个 metadata/下载图集均为 v2、1536x2288、RGBA，两个图集与仓库一致，六个 owned-slug 图集仍待审核，并记录 manifest 索引版本滞后，不含本机环境信息
- `qa/petdex-live-recheck-20260818-v5.json`: 2026-08-18T08:27:27Z 重新下载八个公开图集并校验 v2、1536x2288、RGBA 与 SHA；Butler/Chef 与仓库一致，其余六个 owned-slug 更新仍待审核，不含本机环境信息
- `qa/petdex-live-recheck-20260818-v6.json`: 2026-08-18T12:29:32Z 最新 manifest 与八个公开图集实际下载复核；manifest 共 4568 条且仍含历史重复 `hei-mao-2`，远端资源全部为 v2、1536x2288、RGBA，Butler/Chef 与仓库一致，其余六个 owned-slug 更新仍待审核，不含本机环境信息
- `qa/petdex-live-recheck-20260818-v7.json`: 2026-08-18T15:54:16Z 实时读取 PetDex manifest 并在内存下载八个公开 `pet.json`/图集复核；八个资源均返回 200，实际 metadata/图集均为 v2、1536x2288、RGBA，Butler/Chef 与仓库一致，其余六个 owned-slug 更新仍待审核，不含本机环境信息
- `qa/petdex-live-recheck-20260819-v1.json`: 2026-08-18T16:37:19Z 刷新官方 manifest、八个公开资源和隔离 CLI 安装；历史快照，实际资源仍为 v2、1536x2288、RGBA，Butler/Chef 与仓库一致，其余六个 owned-slug 更新仍待审核，未知旧 slug 被拒绝，不含本机环境信息
- `qa/petdex-live-recheck-20260819-v2.json`: 2026-08-18T17:04:59Z 刷新官方 manifest、八个公开资源和隔离 CLI 安装；实际资源仍为 v2、1536x2288、RGBA，Butler/Chef 与仓库一致，其余六个 owned-slug 更新仍待审核，未知旧 slug 被拒绝，不含本机环境信息
- `qa/petdex-live-recheck-20260819-v3.json`: 2026-08-19T14:20:22Z 最新 manifest 和八个公开资源实际下载；4569 条目、八个 metadata v2/1536x2288/RGBA、Butler/Chef 与仓库一致，其余六个 owned-slug 更新仍待审核，历史重复 `hei-mao-2` 仍存在；不含本机环境信息
- `qa/petdex-live-recheck-20260819-v4.json`: 2026-08-19T15:57:23Z 重新读取 manifest 并实际下载八个公开 metadata/图集；8/8 为 v2、1536x2288、RGBA WEBP，Butler/Chef 与仓库一致，其余六个 owned-slug 更新仍待审核，历史重复 `hei-mao-2` 仍存在；不含本机环境信息
- `qa/petdex-live-recheck-20260820-v1.json`: 2026-08-19T18:40:59Z 无查询参数重新读取 manifest 并实际下载八个公开 metadata/图集；8/8 为 v2、1536x2288、RGBA WEBP，Butler/Chef 与仓库一致，其余六个 owned-slug 更新仍待审核，历史重复 `hei-mao-2` 仍存在；不含本机环境信息
- `qa/petdex-live-status-recheck-20260819-v1.json`: 2026-08-18T18:32:29Z 重新用 PetDex CLI 下载八个公开角色并与本地 SHA 对照；8/8 下载和尺寸/模式/v2 检查通过，2 个角色同步，6 个 owned-slug 更新仍待审核，不含本机环境信息
- `qa/current-state-recheck-20260819-v1.json`: 提交 `8565738` 后的历史八角色门禁、三目录 SHA、生图通道、PetDex manifest 和 App 可见性边界快照；本轮最新 API smoke 见 `qa/imagegen-channel-recheck-20260819-v2.json`，最新 PetDex 资源复核见 `qa/petdex-live-recheck-20260819-v2.json`，但 Codex App 视觉验收无窗口证据，六个 PetDex owned-slug 更新仍待审核，不含本机环境信息
- `qa/current-state-recheck-20260819-v2.json`: 提交 `38923ba` 的当前最终状态；Quality 两条 look row 比例阻断已由 recovery-v2 解决，8/8 本地 v2 门禁和 28 项测试通过，API smoke 通过；Codex App 视觉验收仍未取得窗口证据，六个 PetDex owned-slug 更新仍待审核，不含本机环境信息
- `qa/current-state-recheck-20260820-v1.json`: 提交 `a94aca0` 后的八角色最终复核；8/8 v2 图集门禁、28 项测试、双平台安装器隔离验证、本机三目录 SHA parity 和双远端一致性通过，11 个 alpha-hole 候选均确认为开放负空间；生图上游 TLS 阻断、Codex App 视觉验收和六个 PetDex owned-slug 更新仍未闭合，不含本机环境信息
- `qa/current-state-recheck-20260820-v3.json`: 2026-08-19T18:40:59Z 本地生图通道和 PetDex 公开资源最新复核；本地八角色门禁及安装 parity 保持通过，生图上游 TLS、六个 owned-slug 更新和 Codex App 视觉验收仍未闭合，不含本机环境信息
- `qa/petdex-quality-edit-recheck-20260818.json`: Quality owned-slug 编辑提交成功、公开资源仍为旧 SHA、manifest 索引与实际 metadata 漂移复核；不含本机环境信息
- `qa/petdex-upstream-status-recheck-20260818.json`: 2026-08-18T08:41:31Z 只读核对 PetDex #603/#596/#654/#662/#667 等已关闭项，以及仍开放的 #689 Hook EOF 阻塞和不改变该语义的 #710 WIP；不含本机环境信息
- `qa/petdex-upstream-status-recheck-20260820-v1.json`: 2026-08-19T17:18:20Z 公开核对 #689、#710 和 PetDex 最近主线提交；#689 仍 open、#710 仍未合并，未发现改变 stdin EOF 语义的上游动作；不含本机环境信息
- `qa/petdex-upstream-status-recheck-20260820-v2.json`: 2026-08-19T20:45:48Z 公开刷新 #689、#603、#710、#654 和最新 release；#689 仍 open 且无评论，#710 仍未合并，#603 已关闭，#654 已合并，最新 Desktop release 仍为 v0.8.0；不含本机环境信息
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
- `qa/current-state-recheck-20260817-v3.json`: 提交 `577712c` 上的方向语义字段统一、QA 摘要索引、预览帧数、请求标识脱敏和八角色最终本地复核，不含本机环境信息
- `qa/current-state-recheck-20260817-v4.json`: 提交 `1c59260` 上按各角色实际色键重跑的八角色 v2 门禁、连续性、方向/盲测、三目录 parity、最新 PetDex manifest、#689 和 Codex App 边界，不含本机环境信息
- `qa/current-state-recheck-20260817-v5.json`: 证据提交 `9a7a975`（八角色门禁基线 `b86da01`）上的实时 atlas/连续性/方向门禁、隔离安装器、公开资源 CDN、#689 与开放 PR #710 边界；记录 Skill 测试在隔离 uv runtime 中 28 项通过、配置的 GitLab 镜像项目为 public 且已同步，不含本机环境信息
- `qa/current-state-recheck-20260817-v6.json`: 提交 `f0ce45f` 上使用 bundled Python 3.12.13 fresh 重跑八角色 v2/连续性/方向门禁、视觉 QA 资产基线、三目录 parity、PetDex 八角色公开安装、#689/PR #710 和 Codex App 边界，不含本机环境信息
- `qa/current-state-recheck-20260817-v7.json`: 提交 `9221c80` 上重新执行八角色 v2/连续性门禁、QA 产物完整性、安装器静态检查、三目录 SHA parity、八角色临时 HOME 在线安装、实时 manifest、上游 Hook 源码与本机 stdin stall 复现、Desktop release 和 Codex App 边界，不含本机环境信息
- `qa/current-state-recheck-20260817-v8.json`: 本轮五个角色比例归一化、八角色 fresh v2/连续性门禁、Traveler 修复后三份独立方向盲测、Shell/PowerShell 安装器和三目录 SHA parity；PetDex/Codex App 外部边界明确分开，不含本机环境信息
- `qa/current-v2-gate-recheck-20260818-v2.json`: 八角色色键 v2/连续性门禁、28 项 hatch-pet 测试、安装器解析与隔离安装、三目录 SHA parity 和 Quality look-row 比例阻断；不含本机环境信息
- `qa/current-v2-gate-recheck-20260818-v3.json`: 2026-08-18T07:50:43Z 新鲜八角色 v2/连续性门禁、28 项测试、QA 资产完整性、三目录 SHA parity、旧 slug 清理、安装器解析和双远端同步；唯一视觉阻断为 Quality 两条 look row 的完整重生成，不含本机环境信息
- `qa/current-v2-gate-recheck-20260818-v4.json`: Quality 重生成前的八角色 v2 validator/连续性历史快照；当时 Quality 两条 look row 仍需完整重生成，不含本机环境信息
- `qa/current-v2-gate-recheck-20260818-v5.json`: 提交 `fa9b7c3` 后八角色 v2 atlas、连续性、Quality 视觉门禁、安装器、双目录 SHA、GitHub/GitLab 同步和公开文件卫生复核，不含本机环境信息
- `qa/remote-quality-install-recheck-20260818.json`: GitHub/GitLab raw 安装器的 Quality 下载、固定 SHA、未知 slug 拒绝和临时目录清理复核，不含本机环境信息
- `qa/current-state-recheck-20260818-v1.json`: 基于提交 `f80b910` 的八角色新鲜门禁、28 项测试、三目录 parity、安装器、PetDex 公开资源、生图服务和 Codex App 边界复核；不含本机环境信息
- `qa/codex-app-boundary-recheck-20260817.json`: ChatGPT/Codex App 进程、菜单栏和设置菜单可见性复核；窗口数为 0，宠物视图仍不可访问，未停止或重启 Codex 进程，不含本机环境信息
- `qa/petdex-live-install-recheck-20260817.json`: 2026-08-16 早期 PetDex CLI `1.2.2` 隔离安装六个公开角色的历史快照，仅用于追溯，不含本机环境信息
- `qa/petdex-live-recheck-20260817.json`: 最新 manifest 中八个黑毛角色均已公开、八个线上资源的 v2/尺寸/SHA 对照、Fortune/Traveler 当前 owned-slug 编辑队列和无重复提交边界，不含本机环境信息
- `qa/petdex-live-recheck-20260818-v2.json`: 2026-08-17T18:26:47.414Z manifest、八角色公开资源 SHA/metadata、GitHub/GitLab `a6d7a71` 主线提交对照；六个本地修复图集仍待 PetDex 审核，不含本机环境信息
- `qa/petdex-live-install-recheck-20260817-v2.json`: PetDex CLI `1.2.2` 隔离安装八个公开角色到两个目标根目录的真实结果、ID/v2/文件 parity 和公开资源编辑审核边界，不含本机环境信息
- `qa/petdex-live-install-recheck-20260818-v1.json`: PetDex CLI `1.2.2` 新鲜隔离安装八个公开角色、两个目录各 16 个文件及 SHA parity；六个本地修复图集仍待线上审核，不含本机环境信息
- `qa/petdex-live-install-recheck-20260818-v2.json`: PetDex CLI `1.2.2` 新鲜隔离安装七个可发布角色到两个临时目标，14+14 个文件 SHA parity 通过，Quality 与历史 `hei-mao-2` 按规则拒绝，临时目标已清理，不含本机环境信息
- `qa/petdex-live-install-recheck-20260819-v1.json`: PetDex CLI `1.2.2` 最新隔离安装八个当前角色到两个临时目标，16+16 个文件存在、metadata id 和双目录 SHA parity 通过，临时目标已清理，不含本机环境信息
- `qa/petdex-live-install-recheck-20260819-v2.json`: PetDex CLI `1.2.2` 重新核对八个当前角色的 metadata、v2、1536x2288、RGBA、双目录 SHA parity 和临时目录清理；8/8 通过，六个 owned-slug 线上资源仍待审核切换；不含本机环境信息
- `qa/codex-app-boundary-recheck-20260818.json`: ChatGPT/Codex App 当前只读进程和窗口探针；进程可见但窗口数为 0，未执行设置或进程控制，不含本机环境信息
- `qa/codex-app-boundary-recheck-20260818-v2.json`: 2026-08-18T08:37:49Z ChatGPT/Codex App 只读进程探针；窗口查询在安全 8 秒边界超时，未执行设置或进程控制，视觉验收仍未完成，不含本机环境信息
- `qa/codex-app-boundary-recheck-20260819.json`: 2026-08-18T19:13:29Z WindowServer 可见两个 ChatGPT 窗口，屏幕录制/辅助功能预检均为 true，ScreenCaptureKit 已找到窗口但以 `SCStreamErrorDomain Code -3811` 失败；未发送输入、未改设置、未停止或重启 Codex 进程，视觉验收仍未完成，不含本机环境信息
- `qa/petdex-desktop-live-recheck-20260819.json`: 2026-08-19T00:41:17Z Petdex Desktop v0.8.0 实际窗口捕获；Traveler 活动角色、全身比例和连续帧变化通过，bubble 跟随和多角色切换仍未验证，不含本机环境信息
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
- `qa/current-v2-alpha-review-20260819.json`: 提交 `51288a4` 的八角色 v2 门禁、连续性重算和 11 个 alpha-hole 候选高对比度复核；候选均为耳间或下半身开放负空间，未发现封闭主体透明洞
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
- `qa/petdex-fortune-submit-recheck-20260813.json`: Fortune 进入公开 manifest 前的提交/审核历史快照，仅用于追溯
- `qa/petdex-traveler-submit-recheck-20260814.json`: Traveler 进入公开 manifest 前的提交/审核历史快照，仅用于追溯
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

</details>

## 验证结果

本包的结构、格式、确定性门禁和本轮完整动作行视觉复核均已通过；连续性中的局部 outlier、方向中间帧 ambiguity 和设计内负空间作为 minor warning 保留：

- `pets/hei-mao/spritesheet.webp`: `WEBP` / `RGBA`
- `spriteVersionNumber`: `2`
- 尺寸: `1536x2288`
- 单元格: `192x208`
- `qa/hei-mao/validation.json`: `ok: true`
- `qa/hei-mao/review.json`: `ok: true`
- `qa/hei-mao/direction-blind-validation.json`: `ok: true`
- 错误: 0
- 图集透明 RGB 残留: 0
- 补充视觉复核: `pass_with_reviewed_minor_warnings`；上述八条完整动作行已完成重生、装配和正常显示尺寸复核，未发现新的比例失衡、裁切、断开组件或身份漂移。证据见 `qa/visual-review-recheck-20260901-v1.json`。
- 另一路补充复核已完成：使用下半身锚点归一化轮廓、角色 idle 包络、多尺度边缘指纹和材质指纹，并对 32 个候选图逐一做正常显示尺寸确认；共检查 584 个动画帧及 8 个 v2 neutral-look 复用单元，未新增硬失败，四个原有阻断保持不变。证据见 `qa/visual-review-alternative-20260831/supplemental-invariant-review-20260831-v6.json` 和 `qa/visual-review-alternative-20260831/supplemental-invariant-candidates-v6.jpg`。
- 显示端压力复核也已完成：对 592 个非空帧进行 alpha 阈值稳定性、三种小尺寸/三种采样和上半身轮廓持久性复核，候选图只复现四个原有阻断，未新增透明边缘、缩放比例或小尺寸可读性硬失败。证据见 `qa/visual-review-alternative-20260831/display-alpha-lobe-review-20260831-v4.json` 和 `qa/visual-review-alternative-20260831/display-alpha-lobe-candidates-v4.jpg`。
- 轮廓厚度场补充复核也已完成：对 584 个动画帧同时计算完整分辨率与 48x52 显示尺寸的 alpha 距离场，32 个候选经正常显示尺寸查看，只复现既有阻断，未新增主体压扁、变薄或局部厚度突变硬失败。证据见 `qa/visual-review-methods-recheck-20260831-v10.json` 和 `qa/visual-review-alternative-20260831/thickness-field-review-20260831-v1.json`。
- 小尺寸感知压力复核也已完成：把 584 个动画帧在 24x26、32x35、48x52 三个显示尺寸下分别叠加深色、浅色和高饱和背景，并检查灰度 alpha 轮廓、视觉质量和边缘能量；32 个候选逐项查看后未新增硬失败，八个既有完整动作行阻断保持不变。证据见 `qa/visual-review-alternative-20260831/squint-contrast-review-20260831-v1.json` 和 `qa/visual-review-alternative-20260831/squint-contrast-candidates-v1.jpg`。
- 状态意图与动画退化复核也已完成：用下半身锚点和基线归一化 584 个帧，检查帧间 alpha/RGB 变化、上/下半身运动分布、循环多样性和与 idle 的距离；36 个候选经正常尺寸查看，低运动量候选仍有可见手部、头部、脚步或道具变化，未新增硬失败。证据见 `qa/visual-review-alternative-20260831/state-semantics-review-20260831-v1.json` 和 `qa/visual-review-alternative-20260831/state-semantics-manual-review-20260831-v1.json`。

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

### 品控官 recovery-v2 验证结果

- `pets/hei-mao-quality/spritesheet.webp`: `WEBP` / `RGBA`，SHA-256 为 `a74c7e3ef8ed5b23f94c7f926494291d061494d3d0ba718041349bb27eca09f2`
- 尺寸 `1536x2288`，单元格 `192x208`，`spriteVersionNumber: 2`
- quality 图集使用洋红色抠像键 `#FF00FF`；独立复核时运行 `validate_atlas.py --require-v2 --chroma-key '#FF00FF' pets/hei-mao-quality/spritesheet.webp`
- `qa/hei-mao-quality/validation.json`: `ok: true`，错误 0，透明 RGB 残留 0
- `qa/hei-mao-quality/recovery-v2/validation-final-webp.json`: `ok: true`，错误和警告均为 0，透明 RGB 残留为 0
- `qa/hei-mao-quality/recovery-v2/chroma-despill.json`: `ok: true`，完成单次边缘色键去溢
- `qa/hei-mao-quality/recovery-v2/direction-blind-validation.json`: `ok: true`，三份独立盲测严格多数汇总；`000=up`、`180=down`、`270=screen-left` cardinal 硬门禁通过，中间方向 warning 保留
- `qa/hei-mao-quality/recovery-v2/proportion.json`: row 9 为 `179-194px`、row 10 为 `189-196px`，中性帧为 `198px`，共同基线底部为 `201px`
- `qa/hei-mao-quality/recovery-v2/look-continuity-final.json`: 数值 outlier 作为已复核 minor warning 保留；正常尺寸下未见身份变化、错误象限、方向反转或透明内部洞

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

- `pets/hei-mao-foodie/spritesheet.webp`: `WEBP` / `RGBA`，SHA-256 为 `3eccffe95a7ea7d419a43ff325ac4324b67d82f0a7e1be7a3d2b7cdca8fce6c9`
- `pets/hei-mao-foodie/pet.json`: SHA-256 为 `0857baacd1dbb5912ceb03a5fc4cadf121923f6d04190b9356f7588f82410a6c`
- `spriteVersionNumber: 2`，尺寸 `1536x2288`，单元格 `192x208`
- `qa/hei-mao-foodie/validation.json`: `ok: true`，错误 0，透明 RGB 残留 0
- `qa/hei-mao-foodie/chroma-despill.json`: `ok: true`，单次边缘色键去溢完成
- `qa/hei-mao-foodie/direction-blind-validation.json`: `ok: true`，四个 cardinal 硬门禁通过
- `qa/hei-mao-foodie/final-visual-qa.json`: 历史结果为 `pass`；waiting 行已完成完整重生、装配和当前正常显示尺寸复核，未发现新的硬失败

### 配送员 v2 验证结果

- `pets/hei-mao-delivery/spritesheet.webp`: `WEBP` / `RGBA`，SHA-256 为 `6abe515e3b51357f2dbb44fbed46339fdf1234eb2ab8edd53cde9f553acdd5a4`
- `pets/hei-mao-delivery/pet.json`: SHA-256 为 `16e5e9aaf0033e4676b7a298f55562607382a1a1d1fbe7ecf4377ffcd86c46a2`
- `spriteVersionNumber: 2`，尺寸 `1536x2288`，单元格 `192x208`
- `qa/hei-mao-delivery/validation.json`: `ok: true`，错误 0，透明 RGB 残留 0
- `qa/hei-mao-delivery/chroma-despill.json`: `ok: true`，单次边缘色键去溢完成
- `qa/hei-mao-delivery/direction-blind-validation.json`: `ok: true`，四个 cardinal 硬门禁通过
- `qa/hei-mao-delivery/final-visual-qa.json`: 历史结果为 `pass_with_reviewed_warnings`；failed 行已完成完整重生、单次去溢和当前正常显示尺寸复核，未发现新的硬失败
- `qa/petdex-delivery-submit-20260811.json`: 配送员首次提交的历史记录；当前线上状态以 `qa/petdex-live-recheck-20260903-v2.json` 和 `qa/petdex-edit-resubmission-recheck-20260904-v1.json` 为准

### 最新生图请求复核

2026-09-01 已使用更新后的私有图像渠道完成一次真实 smoke：服务端编排选择 `mhapi-image` / `mhapi.net` 的 `images-non-stream`，返回经尺寸校验的 `1024x1024 WebP`，请求成功且未记录凭证或私有端点。脱敏证据见 `qa/imagegen-channel-recheck-20260901-v1.json`；本轮八条动作行的生成与复核也基于该渠道完成。

2026-08-24 专项本机 Docker 复核确认当时生图接口可实际使用：`gpt-image-2-1k` 的 `1536x2288`、`n=1` 请求通过服务端编排返回一个临时 artifact，metadata/content 删除后均为 404；正式 PetDex 资产未修改。尺寸、比例和视觉完整性沿用上一轮 `1536x2288` 合同证据 `qa/imagegen-channel-recheck-20260823-v29.json`，本轮最新路由/清理证据见 `qa/imagegen-channel-recheck-20260824-v1.json`；当前总体状态以文档顶部的 2026-09-03/04 证据为准。当前仓库、`~/.codex/pets` 与 `~/.petdex/pets` 的八角色、16 个资产文件逐字节一致，最新 parity 证据见 `qa/three-directory-parity-recheck-20260903-v1.json`。

2026-08-31 新幂等请求曾通过本机 Docker 服务端 `images-non-stream` 路由探针，但上游 `meinianda.top` 返回 `Connection error`（HTTP 500），没有产生可用于修复动作行的图像；这是已结束的历史渠道阻断，证据见 `qa/imagegen-channel-recheck-20260831-v13.json`。2026-09-01 渠道恢复后，八条完整动作行已完成重生、装配和复核，当前状态以文档顶部证据为准。

随后使用新的幂等键复测官方 Agent JSON server-channel 路由，返回 HTTP 502 `Connection error`，同样没有 artifact；页面 JSON 与 Agent JSON 两条本机路径均已排除为本地路由故障。证据见 `qa/imagegen-channel-recheck-20260831-v14.json`。

## 许可

- 本仓库采用分离许可，详见[许可说明](LICENSE)。
- `install.sh`、`install.ps1` 及其独立功能性代码采用 [Apache License 2.0](LICENSES/Apache-2.0.txt)。
- 钱大妈、黑毛及相关角色图集、图片、视频、品牌描述和生成提示词不属于 Apache-2.0 授权范围，适用[品牌资产使用条款](ASSETS-LICENSE.md)。
- Apache-2.0 和品牌资产使用条款均不授予钱大妈或黑毛相关商标权。
