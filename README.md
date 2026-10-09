# 硅晶之梦 MV · v25

本仓库保存原制作工作流、剧本、核验记录与制作 Skill。素材和成片以 Release 附件保存；原项目文件未重构。

- [下载完整工程和素材归档（230 文件）](https://github.com/NakanoIchirou/-MV-/releases/tag/v25-archive)：`silicon-dream-mv-v25-complete.zip`，包含全部关键帧、逐镜视频、音频、成片及 FFmpeg 工具。
- [下载 v25 完整成片](https://github.com/NakanoIchirou/-MV-/releases/tag/v25-archive)：`硅晶之梦-成片-v25.mp4`，1920 × 1080，60fps，108.866667 秒。
- [原制作与审片 Skill](project/skills/silicon-dream-mv/SKILL.md)
- [现行工程定义](project/06_工程与核验/工程.json)
- [重导出工具](project/06_工程与核验/reexport.py)
- [原项目总览](project/README.md)

## 恢复完整项目

仓库中的 `project/` 仅包含可浏览的工作流和文档。下载完整 ZIP 并解压到 `project/`，使 `project/01_剧本`、`project/02_关键帧` 等目录直接位于其中；所有原件都在压缩包内，仓库文件与压缩包同路径文件一致。然后打开 `project/03_审片/硅晶之梦-逐M审片.html` 查看审片页面。

在 Windows 中运行 `project/06_工程与核验/校验归档.ps1` 可核验归档；也可用已安装的 Python 运行 `verify_archive.py`。重导出使用归档内的 Windows FFmpeg；修改定格关键帧后重建指定镜头还需 Pillow。M13–M25 连续运动保存在原逐镜视频中，请保留。原 PowerShell 启动脚本含制作机器的 Python 路径，换机器时可直接用本机 Python 运行对应脚本。

所有工作目录、缓存及新增依赖按用户要求放在 D 盘。

## 校验与状态

v25 已通过现有技术核验，仍为用户审阅版本，尚未投稿。上传归档不代表审片意见已全部通过。完整 ZIP 在上传前已逐文件与原件比对。

成片 SHA-256：`5aac433236d3e54bcc8028ed9983b2eaa75057f2e89e802539875026317c1b7e`。

完整 ZIP SHA-256：`83e98cb25ecf954e88f513c4a6e8e95e8f910c172bc8268192a62c95a2701af6`。Release 中提供 `SHA256SUMS.txt`。
