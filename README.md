# Gaku-Mod-Tools 模组目录

面向《学园偶像大师》（学園アイドルマスター / Gakuen IDOLM@STER）PC DMM 版的开源模组、插件、加载器及开发工具索引。

项目无需属于 `Gaku-Mod-Tools` 组织，也不强制依赖 `GakuLoader`，只要围绕学马仕 PC 端展开的公开生态项目均可收录。

---

## 项目索引

### 加载器与运行时

| 项目 | 定位与说明 |
| :--- | :--- |
| [GakuLoader](https://github.com/Gaku-Mod-Tools/GakuLoader) | 面向 PC DMM 版的原生 DLL 插件加载器，提供插件发现、生命周期管理及共享宿主服务。 |
| [Gakumas Mod Runtime](https://github.com/chihya72/gakumas-mod-runtime) | 独立的本地 AssetBundle 加载与管理插件，支持服装、发型、模型及贴图等视觉资产替换。 |

### 动作与演出

| 项目 | 定位与说明 |
| :--- | :--- |
| [GakuMotion](https://github.com/crested-ezios/GakuMotion) | 基于 GakuLoader 的游戏原生演出扩展，支持 MMD/VMD 动作回放、面部表情、自由运镜、WAV 音频同步及自定义舞台（目前处于 Technical Preview 阶段）。 |

### 角色、服装与资产工具

| 项目 | 定位与说明 |
| :--- | :--- |
| [GakumasMI](https://github.com/chihya72/gakumas-modding) | 基于 Blender 的视觉 Mod 制作流水线，用于制作服装、发型等 AssetBundle，提供模型整理、骨骼映射与导出工具链。 |
| [GakuActors](https://github.com/54yq/GakuActors) | 独立的 GakuLoader 场景人物管理插件，提供人物目录、头身预设、场景名单和实验性的独立人物加载。 |

### VR 与沉浸式体验

| 项目 | 定位与说明 |
| :--- | :--- |
| [gakumas-VRify](https://github.com/KagaminTheMirror/gakumas-VRify) | 基于 `gkms-localify-dmm` 的非官方 VR 模组（当前主要基于 Quest 3 + Virtual Desktop 环境验证）。 |
| [Gakumas VR](https://github.com/deadpixel134/gakumas-vr) | 面向 PC DMM 版的 Meta Quest / OpenXR VR 模组，将支持的 3D 场景渲染为立体 VR 视图，2D 界面以空间面板呈现。 |

### 本地化与底层兼容

| 项目 | 定位与说明 |
| :--- | :--- |
| [gkms-localify-dmm](https://git.chinosk6.cn/chinosk/gkms-localify-dmm) | 上游独立版 PC DMM 本地化与功能增强模组，支持文本/贴图替换、自由视角及窗口解锁。 |
| [Gakumas Localify DMM (Hosted)](https://github.com/crested-ezios/gkms-localify-dmm) | 基于上游重构的 GakuLoader 插件版分支，支持多插件共存、分类目录资源管理与底层服务导出。 |

---

## 亟待探索与补充的方向

以下方向目前尚未整理出独立条目，欢迎社区提交相关工具、实验原型或研究仓库：

- **舞台与灯光**：自定义舞台加载、灯光参数控制、后处理及演出环境扩展。
- **录制与数据采集**：演出画面录制、动作/表情/相机轨迹导出及运行时诊断工具。
- **格式与资产工具**：解包检查、格式转换、数据结构分析等辅助创作脚本。

---

## 提交与维护指南

### 如何新增或修正条目
欢迎直接发起 [Pull Request](https://github.com/Gaku-Mod-Tools/Mod-Directory/pulls) 修改本文件，或通过 [Issues](https://github.com/Gaku-Mod-Tools/Mod-Directory/issues) 提交仓库链接。提交新项目时，请包含以下信息：

1. **项目名称与公开仓库链接**
2. **一句话定位**（简述核心功能与解决的问题）
3. **所属分类与当前状态**（如开发中、已发布、开发库等）
4. **主要前置依赖**（如需要 GakuLoader 或特定运行时）

### 推荐仓库标签 (GitHub Topics)
若你的项目托管在 GitHub，建议在仓库设置中添加以下标签，方便其他开发者检索以及后续的自动化索引：

`gakumas` · `gakumas-mod` · `gakumas-plugin` · `gaku-mod-tools`

### 提交底线
- 仓库内仅索引公开工具与代码链接，**严禁在 Issue、PR 或仓库中上传游戏本体文件、解包商业美术/音频资产，以及包含个人 Token 或账号信息的未脱敏日志**。
- 目录维护前期以人工审核为主，后续将结合 GitHub Topics 进行定期扫描检索，并在人工核对后合入索引。
