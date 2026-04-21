# 🏁 2021 F1 Abu Dhabi Grand Prix: Tactical Replay Visualization

[![D3.js](https://img.shields.io/badge/Visualization-D3.js_v7-F9A03C?logo=d3.js)](https://d3js.org/)
[![Python](https://img.shields.io/badge/Data_Pipeline-FastF1-blue?logo=python)](https://github.com/theOehrly/FastF1)

本项目是一个关于 **2021年F1阿布扎比大奖赛** 的交互式数据可视化平台。它不仅展示了比赛中 20 位车手的排位变化，还通过深度整合战术数据（进站、轮胎、安全车），复盘了整场比赛的动态演变。

## 🔗 在线预览
**[点击这里访问 GitHub Pages 演示页面](https://p-park-jpg.github.io/F1-vis/)**

---

## 🚀 项目亮点

### 1. 深度交互体验
*   **实时回放系统**：支持点击播放按钮自动回放比赛进程，或通过进度条手动控制圈数。
*   **平滑补间动画**：利用 D3.js 的 `transition` 机制，实现线条与标签的平滑过渡，消除了数据更新时的顿挫感。
*   **动态聚焦高亮**：鼠标悬停在特定车手轨迹上时，该线条会自动置顶并加粗，同时弱化其他干扰线条。
*   **战术事件图层**：集成了安全车（SC/VSC）背景标识、进站标记以及轮胎配方指示器，可通过开关自由切换显示。

### 2. 硬核数据驱动
*   **官方遥测接口**：数据直接来源于 F1 官方 Live Timing，通过 Python 库 `FastF1` 进行自动化抓取。
*   **自动化流水线**：项目包含一个完整的 Python 数据清洗脚本，能够自动识别进站耗时、轮胎种类以及赛道状态变化。

### 3. 底层渲染实现
*   **纯 D3.js 开发**：未调用任何高层封装库（如 Plot 或 ECharts），完全基于 SVG 坐标映射、路径生成器（Line Generator）及数据绑定（Data Join）实现。

---

## 🛠️ 技术架构

### 文件夹结构
*   `index.html`: 核心前端页面，包含所有 D3.js 可视化逻辑与 CSS 样式。
*   `XX_data.json`: 经过清洗后的比赛数据文件。
*   `get_f1_data.py`: 后端数据处理脚本，用于从 FastF1 API 提取数据。

### 数据流向
1.  **Extract**: `get_f1_data.py` 连接 F1 官方接口下载原始 Telemetry。
2.  **Transform**: Python 脚本进行特征提取，生成包含 `raceData`, `pitStops`, `stints`, `safetyCars` 的 JSON。
3.  **Load**: `index.html` 通过 D3.js 异步读取 JSON 并进行动态渲染。

---

## 📖 如何运行

### 方式一：直接查看（推荐）
直接访问 [GitHub Pages 链接](https://p-park-jpg.github.io/F1-vis/)。

### 方式二：本地运行
1.  克隆仓库：
    ```bash
    git clone https://github.com/P-Park-jpg/F1-vis.git
    ```
2.  在文件夹中启动一个本地服务器（例如使用 VS Code 的 Live Server 插件，或使用 Python）：
    ```bash
    python -m http.server 8000
    ```
3.  在浏览器访问 `http://localhost:8000`。

---

## 🎓 课程说明
本项目为 **北京航空航天大学-软件学院** - **数据可视化** 课程作业（Assignment II）。

*   **作业要求**：实现现有可视化设计的拆解与再现，重点考察 D3.js 的运用能力、交互设计以及数据处理流。
*   **参考项目**：RaceFans Strategy Analysis, Flourish F1 Examples.

---

## 📜 开源协议
本项目采用 [MIT License](LICENSE) 许可协议。

---

**🏁 Keep Racing!** 如果你觉得这个可视化项目有意思，欢迎点一个 Star! ⭐
