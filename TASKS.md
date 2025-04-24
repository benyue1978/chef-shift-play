# Chef's Shift AI 自动操作开发

本项目旨在开发一个基于 AI 的自动操作系统，用于在 Chef's Shift 游戏中实现智能化操作和决策。

## 进行中任务

### 阶段一：截图与上传功能开发
- [ ] 使用 pygetwindow 或 pywinauto 获取游戏窗口句柄
- [ ] 使用 pyautogui.screenshot(region=...) 对游戏窗口截图
- [ ] 上传截图到 imgur 并获取 image_url
- [ ] 手动触发截图和上传

### 阶段二：任务拆解与静态图测试
- [ ] 准备并上传数张游戏截图（PNG）
- [ ] 编写 prompt 模板，包含：
  - [ ] 游戏背景规则（食物制作流程）
  - [ ] 如何识别顾客订单与打字指令
  - [ ] "sold"、"edge" 等 UI 元素含义
- [ ] 使用 GPT-4o API 测试 prompt，有效返回多步骤操作计划
- [ ] 保存示例对话结果，用于后续验证

### 阶段三：实现 executor 执行模块
- [ ] 使用 pyautogui.write() 模拟逐字输入
- [ ] 封装 execute_action(action: str) 函数，解析 LLM 输出并执行
- [ ] 支持多步指令的顺序输入

### 阶段四：接入自动截图与窗口控制（后续启用）
- [ ] 实现定时轮询截图 + 上传 + 调用 GPT-4o
- [ ] 整合为循环：截图 → 上传 → 推理 → 执行

### 阶段五：优化与智能化
- [ ] 对 LLM 输出进行结构化解析（JSON）
- [ ] 加入异常处理（如识别失败 / GPT超时）
- [ ] 多角色状态判断：同时处理多个顾客订单

## 未来任务

### 阶段六：高级功能增强
- [ ] 图像增强处理：对特定区域（如炉子）进行图像增强提取"sold"标识
- [ ] 性能优化：减少 API 调用延迟
- [ ] 添加实时监控界面

## 实现计划

系统将通过以下步骤实现：

1. 基础功能实现：
   - 窗口控制与截图功能
   - 图片上传到 imgur
   - 静态图像分析与任务规划
   - 基本操作执行模块

2. 智能化升级：
   - 状态追踪与多任务处理
   - 异常处理机制
   - 性能优化

## 相关文件

### 核心模块
- `src/window_controller.py` - 窗口控制与截图模块 🚧
- `src/uploader.py` - 图像上传（imgur）模块 🚧
- `src/executor.py` - 执行模块，负责模拟键盘输入 🚧
- `src/llm_interface.py` - GPT-4o API 接口模块 🚧
- `src/image_processor.py` - 图像处理模块 🚧

### 配置文件
- `config/settings.py` - 系统配置文件 🚧
- `config/prompts.py` - Prompt 模板配置 🚧

### 测试文件
- `tests/test_window_controller.py` - 窗口控制测试 🚧
- `tests/test_uploader.py` - 图片上传测试 🚧
- `tests/test_executor.py` - 执行模块测试 ��

## 实现细节

### 架构设计
- 采用模块化设计，各组件独立可测试
- 使用同步处理方式进行开发（后续需要时再改为异步）
- 实现基础的状态管理

### 技术栈
- Python 3.9+
- pyautogui 用于截图
- pygetwindow 或 pywinauto 获取窗口信息
- imgur-python 用于图片上传
- pytest 用于测试
- Ruff 用于代码格式化

### 环境配置
- 需要配置 imgur API 密钥
- 需要安装相关 Python 包
- 支持 Windows/MacOS 系统