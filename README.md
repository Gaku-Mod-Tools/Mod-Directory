# Gaku-Mod-Tools 模组目录

面向《学园偶像大师》（学園アイドルマスター / Gakuen IDOLM@STER）PC DMM 版的开源模组、插件、加载器及开发工具社区目录。

项目无需属于 `Gaku-Mod-Tools` 组织，也不强制依赖 `GakuLoader`，只要围绕学马仕 PC 端展开的公开生态项目均可收录。

---

## 项目索引

### 加载器与运行时

| 项目 | 定位与关系 | 详情 | 状态 |
| :--- | :--- | :--- | :--- |
| [GakuLoader](https://github.com/Gaku-Mod-Tools/GakuLoader) | 面向 PC DMM 版的原生 DLL 插件加载器（`version.dll`），提供插件发现、生命周期管理及共享宿主服务。 | [详情页](projects/gakuloader.md) | 持续维护 |
| [Gakumas Localify RE](https://github.com/chihya72/gkms-localify-dmm-RE) | 面向 PC DMM 版的插件框架（`version.dll`），提供 `Ctrl+U` 游戏内面板、插件库管理及内置字体/日志能力。 | — | 活跃维护 |
| [Gakumas Mod Runtime](https://github.com/chihya72/gakumas-mod-runtime) | 独立的本地 AssetBundle 加载与管理插件，支持服装、发型、模型及贴图等视觉资产替换。 | — | 活跃维护 |
| [GakuFSR4](https://github.com/otokuso/GakuFSR4) | 基于 GakuLoader 的 AMD FSR 4 超分与帧生成实验插件，将 DX11 渲染信息桥接至 DX12 执行缩放与插帧。（依赖 `GakuLoader`） | — | 实验性 |

### 动作与演出

| 项目 | 定位与关系 | 详情 | 状态 |
| :--- | :--- | :--- | :--- |
| [GakuMotion](https://github.com/crested-ezios/GakuMotion) | 基于 GakuLoader 的游戏原生演出扩展，支持 MMD/VMD 动作回放、面部表情、自由运镜、WAV 音频同步及自定义舞台（含多个活跃 Fork，见详情页）。 | [详情页](projects/gakumotion.md) | 开发者预览 |
| [GakuBurstBridge](https://github.com/crested-ezios/GakuBurstBridge) | GakuMotion 的可选原生物理伴生库，将外部动作姿态传递给 Unity Burst Swing 动画流以驱动官方头发和裙摆解算。 | — | 活跃维护 |
| [KineTexture](https://github.com/crested-ezios/KineTexture) | 仅头文件 C++20 运动学与动作采样核心 SDK，提供稠密姿态采样、坐标转换、骨骼重定向原语与解析两骨 IK。 | — | 实验性 |
| [Gakumas Photo Studio](https://github.com/JayAlbertZhao/gakumas-photo-studio) | 基于 Unity / Tuanjie 的角色动画与场景渲染工具库（UPM 包 `Gakumas.Toolkit`）及预览应用。 | — | 研究预览 |
| [Gakumas Player](https://github.com/a1415102876-alt/Gakumas-Player) | 运行在浏览器中的 WebGL 3D 剧情播放器，支持 Beat 脚本演出、可视化编辑及角色动作/表情驱动。 | — | 活跃维护 |

### 角色、服装与资产工具

| 项目 | 定位与关系 | 详情 | 状态 |
| :--- | :--- | :--- | :--- |
| [GakumasMI](https://github.com/chihya72/gakumas-modding) | 基于 Blender 的视觉 Mod 制作流水线，用于制作服装、发型等 AssetBundle，提供模型整理、骨骼映射与导出工具链。 | — | 活跃维护 |
| [GakuActors](https://github.com/54yq/GakuActors) | 独立的 GakuLoader 场景人物管理插件，提供人物目录、头身预设、场景名单和实验性的独立人物加载。（依赖 `GakuLoader`） | — | 实验性 |
| [GakuSMM](https://github.com/yunjiansky-a11y/GakuSMM) | 基于 GakuLoader 的场景模型管理插件，支持场景对象分类扫描、搜索、隐藏恢复与画面划选。（依赖 `GakuLoader`） | — | 活跃维护 |
| [Gakumas-PMX-Export](https://github.com/mr-quinn33/Gakumas-PMX-Export) | 用于将学马仕角色与游戏模型导出为 `.pmx` 文件的 Unity 工程。 | — | 活跃维护 |
| [GakuenMME](https://github.com/croakfang/GakuenMME) | 面向 MikuMikuDance 的《学园偶像大师》风格 HLSL 着色器。 | — | 活跃维护 |

### 解包、解密与逆向工具

| 项目 | 定位与关系 | 详情 | 状态 |
| :--- | :--- | :--- | :--- |
| [Gakuen-idolmaster-ab-decrypt](https://github.com/nijinekoyo/Gakuen-idolmaster-ab-decrypt) | 《学园偶像大师》AssetBundle 文件解密工具（Python）。 | — | 活跃维护 |
| [GkmasObjectManager](https://github.com/AllenHeartcore/GkmasObjectManager) | 基于 Python 的资源库 CLI/GUI 工具，支持清单解密导出、AssetBundle 解混淆及贴图/音视频格式转换。 | — | 活跃维护 |
| [GakumasAssetExplorer](https://github.com/shun-god/GakumasAssetExplorer) | 资源浏览、获取与角色语音/台词批量导出工具。（衍生自 `GkmasObjectManager`） | — | 活跃维护 |
| [HatsuboshiToolkit](https://github.com/DreamGallery/HatsuboshiToolkit) | 学马仕游戏资源获取与解包工具集（Python）。 | — | 活跃维护 |
| [gkmas-delta](https://github.com/Hoshisaki-Kyogiri/gkmas-delta) | 学园偶像大师资源增量更新工具（Python）。 | — | 活跃维护 |
| [gkms-meta-dec](https://github.com/chinosk6/gkms-meta-dec) | 游戏元数据解密工具。 | — | 活跃维护 |
| [campus-meta](https://github.com/vilebbit/campus-meta) | `global-metadata` 自动反混淆工具（C）。 | — | 活跃维护 |
| [Gakumas_mod](https://github.com/dhlrunner/Gakumas_mod) | PC DMM 版逆向辅助工具，支持 IL2CPP / 受保护 `GameAssembly.dll` 转储与 Unity 函数 Hook 调试。 | — | 实验中 |

### VR 与沉浸式体验

| 项目 | 定位与关系 | 详情 | 状态 |
| :--- | :--- | :--- | :--- |
| [gakumas-VRify](https://github.com/KagaminTheMirror/gakumas-VRify) | 基于 `gkms-localify-dmm` 衍生的非官方 VR 模组独立代理版（主要基于 Quest 3 + Virtual Desktop 环境验证）。（衍生自 `gkms-localify-dmm`） | — | 活跃维护 |
| [gakumas-VRify (GakuLoader Plugin Fork)](https://github.com/crested-ezios/gakumas-VRify) | `gakumas-VRify` 的 GakuLoader 插件化集成复刻，包含 Localify 相机/渲染桥接与 Motion 镜头共存桥接。（Fork 自 `gakumas-VRify`） | — | 实验性 |
| [Gakumas VR](https://github.com/deadpixel134/gakumas-vr) | 面向 PC DMM 版的 Meta Quest / OpenXR VR 模组，将支持的 3D 场景渲染为立体 VR 视图，2D 界面以空间面板呈现。 | — | 活跃维护 |

### 本地化与底层兼容

| 项目 | 定位与关系 | 详情 | 状态 |
| :--- | :--- | :--- | :--- |
| [gkms-localify-dmm](https://git.chinosk6.cn/chinosk/gkms-localify-dmm) | 上游独立版 PC DMM 本地化与功能增强模组，支持文本/贴图替换、自由视角及窗口解锁。 | — | 活跃维护 |
| [gkms-localify-dmm (hosted)](https://gitee.com/Abstergo_Ezios/gkms-localify-dmm) | 基于上游重构的 GakuLoader 插件版分支，支持多插件共存、分类目录资源管理与底层服务导出。（Fork 自 `gkms-localify-dmm`） | — | 活跃维护 |
| [GakuMas-TL](https://github.com/ImaterialC/GakuMas-TL) | 面向 PC DMM 版的贴图翻译资源仓库。 | — | 归档/静态资源 |
| [gakumas-translator](https://github.com/Samuei2000/gakumas-translator) | 面向 `gakumas.exe` 的零侵入实时日转中悬浮窗翻译工具，支持本地 Ollama、DeepSeek 与 OpenRouter。 | — | 实验性 |
| [gakumas-proton](https://github.com/0nikod/gakumas-proton) | 在 Linux / Proton 环境下运行《学园偶像大师》PC 版的兼容配置方案。 | — | 活跃维护 |
| [Gakumas_Launcher](https://github.com/a4nqi3n/Gakumas_Launcher) | 绕过 DMM 客户端直接启动《学园偶像大师》PC 版的轻量启动器。 | — | 活跃维护 |
| [gakumas-launcher](https://github.com/i0rph/gakumas-launcher) | 无需 DMM Game Player 与 VPN 即可启动 DMM 版游戏的 Windows 启动器。 | — | 活跃维护 |
| [gakumas-rich-presence](https://github.com/konattsu/gakumas-rich-presence) | Windows 端非官方 Discord Rich Presence 状态同步守护程序。 | — | 活跃维护 |

### 自动化与辅助脚本

| 项目 | 定位与关系 | 详情 | 状态 |
| :--- | :--- | :--- | :--- |
| [MaaGakumasu](https://github.com/SuperWaterGod/MaaGakumasu) | 基于 MaaFramework 的自动化助手，支持日常收菜、培育与偶像之路，适配 PC DMM 版与模拟器。 | — | 活跃维护 |
| [Gakumas_Helper](https://github.com/Kirinigh/Gakumas_Helper) | 面向 Windows DMM PC 版测试与优化的日常、培育及竞技场胜率选敌辅助脚本。（衍生自 `MaaGakumasu`） | — | 活跃维护 |
| [kotones-auto-assistant (kaa)](https://github.com/XcantloadX/kotones-auto-assistant) | 自动日常与培育脚本，支持 PC DMM 版与模拟器运行。 | — | 活跃维护 |
| [gakumas-assistant](https://github.com/skyfsj/gakumas-assistant) | 基于 YOLO 与 OCR 的自动化辅助工具，支持 Windows PC / DMM 模式及脱离 DMMPlayer 启动。 | — | 活跃维护 |
| [hiro-gakumas-hero](https://github.com/matto49/hiro-gakumas-hero) | 基于大语言模型视觉识别与决策的自动打牌/培育工程框架，支持 Windows DMM 版。 | — | 活跃维护 |

---

## 亟待探索与补充的方向

以下方向目前尚未整理出独立条目，欢迎社区提交相关工具、实验原型或研究仓库：

- **舞台与灯光**：自定义舞台加载、灯光参数控制、后处理及演出环境扩展。
- **录制与数据采集**：演出画面录制、动作/表情/相机轨迹导出及运行时诊断工具。
- **非线性演出编排**：基于受控接口的多轨时间线编排器与播放器工具。
- **格式与资产工具**：解包检查、格式转换、数据结构分析等辅助创作脚本。

---

## 提交与维护指南

### 如何新增或修正条目
欢迎直接发起 [Pull Request](https://github.com/Gaku-Mod-Tools/Mod-Directory/pulls) 修改本文件（必要时可在 `projects/` 下补充详情页），或通过 [Issues](https://github.com/Gaku-Mod-Tools/Mod-Directory/issues) 提交仓库链接。提交新项目时，请包含以下信息：

1. **项目名称与公开仓库链接**
2. **一句话定位**（简述核心功能与解决的问题）
3. **所属分类与当前状态**（如持续维护、开发者预览、实验性等）
4. **项目关系**（是否为独立上游，或 Fork / 衍生 / 移植自某个现有项目）
5. **主要前置依赖**（如需要 `GakuLoader` 或特定运行时）

### 推荐仓库标签 (GitHub Topics)
若你的项目托管在 GitHub，建议在仓库设置中添加以下标签，方便其他开发者检索：

`gakumas` · `gakumas-mod` · `gakumas-plugin` · `gaku-mod-tools`

### 提交底线
- 仓库内仅索引公开工具与代码链接，**严禁在 Issue、PR 或仓库中上传游戏本体文件、解包商业美术/音频资产，以及包含个人 Token 或账号信息的未脱敏日志**。
- 目录维护以人工审核为主，确保项目信息准确且与对应仓库实际情况一致。
