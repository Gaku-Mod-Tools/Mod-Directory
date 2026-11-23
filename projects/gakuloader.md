# GakuLoader

《学园偶像大师》PC DMM 版的原生 DLL 插件加载器，为社区插件提供统一的加载、生命周期管理及共享宿主服务。

**项目状态：** 持续维护，已发布 v1.0.1

**维护者：** [Gaku-Mod-Tools](https://github.com/Gaku-Mod-Tools)

**项目仓库：** [GakuLoader](https://github.com/Gaku-Mod-Tools/GakuLoader)

## 开发路线

| 开发线 | 定位 |
|---|---|
| [main](https://github.com/Gaku-Mod-Tools/GakuLoader/tree/main) | 正式发行与维护 |
| [dev](https://github.com/Gaku-Mod-Tools/GakuLoader/tree/dev) | 开发集成，目前与 main 同步 |
| feat/webview2-manager-ui | WebView2 插件内容面板实验，尚未进入正式版本 |

## 路线图

**近期方向**

- 完善插件 ABI 与共享宿主服务。
- 探索 WebView2 插件内容面板，保留 GakuLoader Manager 的原生 ImGui 外壳。
- 建立跨插件截图保护的统一协调机制。

**长期方向**

- 改进插件管理和安装诊断。
- 完善跨插件兼容性及运行时资源协调。

## 相关项目与资料

- [项目 README](https://github.com/Gaku-Mod-Tools/GakuLoader)
- [插件开发指南](https://github.com/Gaku-Mod-Tools/GakuLoader/blob/main/docs/PLUGIN_DEVELOPMENT.md)
- [插件 API 文档](https://github.com/Gaku-Mod-Tools/GakuLoader/blob/main/wiki/Plugin-API.md)
- [Issues：问题反馈与功能讨论](https://github.com/Gaku-Mod-Tools/GakuLoader/issues)
- [Pull Requests：正在进行的代码贡献](https://github.com/Gaku-Mod-Tools/GakuLoader/pulls)

**依赖此宿主的项目：** [GakuMotion](gakumotion.md)、GakuActors、GakuSMM、GakuFSR4 等。