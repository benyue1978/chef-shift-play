# Chef's Shift AI 自动操作开发

本项目旨在开发一个基于 AI 的自动操作系统，用于在 Chef's Shift 游戏中实现智能化操作和决策。

## 进行中任务

### 阶段一：截图与上传功能开发 ✅
- [x] 使用 pywinctl 获取游戏窗口句柄
- [x] 使用 pyautogui.screenshot(region=...) 对游戏窗口截图
- [x] 上传截图到 imgur 并获取 image_url
- [x] 手动触发截图和上传

### 阶段二：任务拆解与静态图测试 🚧
- [x] 创建任务规划器（GamePlanner）
- [x] 集成 OpenAI GPT-4 Vision
- [x] 编写基础 prompt 模板
- [ ] 优化 prompt 模板：
  - [ ] 添加更多游戏规则细节
  - [ ] 完善食物制作流程说明
  - [ ] 添加错误处理指导
- [ ] 准备测试用例：
  - [ ] 收集不同场景的游戏截图
  - [ ] 编写预期的分析结果
  - [ ] 验证 prompt 效果

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
   - ✅ 窗口控制与截图功能
   - ✅ 图片上传到 imgur
   - 🚧 静态图像分析与任务规划
   - 基本操作执行模块

2. 智能化升级：
   - 状态追踪与多任务处理
   - 异常处理机制
   - 性能优化

## 相关文件

### 核心模块
- `screenshoter.py` - 窗口控制与截图模块 ✅
- `planner.py` - 任务规划器模块 🚧
- `src/executor.py` - 执行模块，负责模拟键盘输入 🚧
- `src/image_processor.py` - 图像处理模块 🚧

### 配置文件
- `config/settings.py` - 系统配置文件 🚧
- `config/prompts.py` - Prompt 模板配置 🚧

### 测试文件
- `tests/test_screenshoter.py` - 窗口控制与截图测试 🚧
- `tests/test_planner.py` - 任务规划器测试 🚧
- `tests/test_executor.py` - 执行模块测试 🚧

## 实现细节

### 架构设计
- 采用模块化设计，各组件独立可测试
- 使用同步处理方式进行开发（后续需要时再改为异步）
- 实现基础的状态管理

### 技术栈
- Python 3.9+
- pyautogui 用于截图
- pywinctl 用于窗口控制
- imgur-python 用于图片上传
- OpenAI GPT-4 Vision 用于图像分析
- LangChain 用于 AI 工作流
- pytest 用于测试
- Ruff 用于代码格式化

### 环境配置
- 需要配置 imgur API 密钥（在 .env 文件中设置）
- 需要配置 OpenAI API 密钥（在 .env 文件中设置）
- 需要安装相关 Python 包
- 支持 Windows/MacOS 系统