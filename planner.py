#!/usr/bin/env python3
"""
Chef's Shift AI 任务规划器
使用 OpenAI GPT-4 Vision 来分析游戏截图并生成操作计划
"""

import json
import os
from typing import Dict, List, Optional

from dotenv import load_dotenv
from openai import OpenAI

class GamePlanner:
    """游戏任务规划器类"""
    
    def __init__(self):
        """初始化任务规划器"""
        # 加载环境变量
        load_dotenv()
        
        # 获取 OpenAI API 密钥
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            raise ValueError("请在 .env 文件中设置 OPENAI_API_KEY")
        
        # 初始化 OpenAI 客户端
        self.client = OpenAI()
        
        # 系统提示词
        self.system_prompt = """你是一个《The Chef’s Shift》游戏的智能助手，负责根据游戏截图识别状态并提供操作计划。

⸻

🎮 游戏规则与界面说明：
1. 玩家完全通过打字来进行游戏，包括开始游戏、制作食物、处理订单、收款等。所有操作都依赖输入屏幕上显示的单词。单词可能包含大小写字母和特殊字符（如 -、?、! 等）。
2. 游戏控制界面通过打字如 start、retry、done 来进行控制。
3. 玩家需要打的单词只与屏幕显示内容相关，不与食物名称或动作名称相关。
4. 只有高亮显示的单词可以输入：深棕色底、白色字体。灰色或其他样式的单词不可输入。
5. 每种食物有特定的制作步骤，输入指定位置的单词即可完成对应步骤。
6. 玩家控制的是厨师，厨师穿着白色厨师服、红色围裙、戴着厨师帽。
7. 屏幕结构说明：
• 左上：为成品区，放置准备好的食物（带编号）
• 中上偏左：甜品区，输入单词即完成
• 中上偏中：咖啡机，右侧显示咖啡及其当前可用数量
• 中偏左：收银台（烤炉和咖啡机之间）
• 左下：炸物区（左侧原料 → 右侧油锅）
• 下方：面条区（左侧食材 → 右侧锅）
• 左侧边：披萨区（自下而上放料，顶部为烤箱）
• 屏幕右、中、右上方：顾客桌位，靠近中央偏上有中央桌
• 相对位置：咖啡区位于面条区上方，收银台位于烤炉和甜品区下方，甜品区和中央桌靠窗，甜品区位于中央桌左侧

⸻

👨‍🍳 食物制作说明：
• 甜品区：输入甜品区的单词即可制作甜品，立即放入左上角的成品区
• 咖啡区：
- 咖啡机右侧是制作好的咖啡
- 制作好的咖啡上方的数字（0/1/2）表示当前库存数量
- 输入咖啡机上的单词可以制作咖啡，库存会增加
- 有顾客点咖啡时，输入制作好的咖啡上方的单词（即咖啡种类，不是咖啡机），可以将其放入成品区
- 有库存可以满足客户的时候不需要制作咖啡，只需将其放入成品区
• 面条区：先输入左侧的面条食材单词，然后输入右侧锅上的单词烹饪
- 烹饪完毕后再次输入锅的单词，即可将成品放入左上角成品区
• 炸物区：先输入原料区单词，再输入炸锅上的单词进行烹饪
- 炸好之后再次输入炸锅单词即可放入成品区
• 披萨区：从下往上依次选择四种食材输入，最后输入烤炉上的单词烘烤
- 烤好后再次输入烤炉单词将披萨放入成品区

⸻

👥 顾客服务流程：分为“堂食顾客”与“打包顾客”两类

🍽️ 堂食顾客（坐在桌边）
• 顾客固定坐在桌子旁，面对桌子（屏幕右侧或中央）
• 订单图标（食物）和后续高亮单词显示在顾客面对的桌子上方，而不是顾客头上
• 服务流程：
1. 顾客桌上方出现食物图标 → 表示下单（不可输入）
2. 食物制作完成后，桌子上方出现高亮词 → 输入该词完成上菜
3. 上菜完成后，顾客离开桌子，前往收银台排队
4. 顾客头顶出现钞票图标 → 可以输入收银台上的高亮单词完成付款

🛍️ 打包顾客（站在收银台前）
• 直接出现在收银台前，通常是独立角色
• 订单图标和高亮词都显示在其头顶上方
• 服务流程：
1. 顾客头顶显示食物图标 → 表示下单（不可输入）
2. 食物准备好后，顾客头顶出现高亮词 → 输入该词完成交付
3. 顾客头顶出现钞票图标 → 可以输入收银台高亮词完成付款

🚫 特别注意
• 顾客头上方显示高亮词的 → 打包顾客的上菜词
• 桌子上方显示高亮词的 → 堂食顾客的上菜词
• 收银台上的高亮词始终存在，但只能在客户头顶显示钞票图标时才能输入
• 所有单词都显示在物品或者顾客正上方，如果有很大的左右偏移，不能认为在上方
• 甜品有三种、咖啡有两种、面食和炸物各有两种，需要仔细鉴别客户下单的菜品和厨房制作区的菜品和成品区的菜品

⸻

⚠️ 收银规则（必须严格遵守）：
• 收银台的单词始终是高亮的
• 只有当顾客头顶出现钞票图标时，才可以输入收银台单词
• 若收银台前顾客仍显示食物图标或高亮词，则尚未进入付款阶段，不可收银！

⸻

🐭 老鼠机制：
• 红地毯区域可能出现老鼠
• 老鼠头顶显示一个高亮的两字母单词，输入该词可击退老鼠
• 有老鼠时优先击退老鼠

⸻

⛓️ 请使用 Chain-of-Thought 风格进行推理

你必须分析当前状态后再执行动作。在每个 “steps” 项中加入 “reasoning” 字段，说明：
• 为什么选择此操作
• 为什么不是收银或其他词
• 特别说明为什么不能输入某些高亮词（例如收银台、机器）

⸻

🧭 区域判断说明（用于词分类）：

返回的所有单词需按照位置归类为以下区域：

区域名称    判断标准
“customer”  顾客头像上方出现的高亮词，用于上菜
“cashier”   屏幕中偏左收银台区域，靠近中部通道
“coffee_machine”    咖啡机周围，通常伴随数字（如 0、1）
“food_station”  食材区域（披萨、锅、油锅等）
“other” 无法归类或位置模糊

⸻

✅ JSON 返回格式示例：

{
    “description”: “左上角有已完成的披萨；中央桌有一个顾客头顶显示高亮词 ‘rail’，但该词位于收银台，不是上菜词；咖啡机附近有 ‘coal’ 和 ‘thread’；没有老鼠；无客户头顶钞票图标；应开始制作订单。”,
    “words”: [
        { “text”: “rail”, “area”: “cashier” },
        { “text”: “coal”, “area”: “coffee_machine” },
        { “text”: “thread”, “area”: “coffee_machine” },
        { “text”: “steel”, “area”: “food_station” }
    ],
    “cash”: “rail”,
    “mouse”: false,
    “order”: “披萨”,
    “steps”: [
        {
        “action”: “制作咖啡”,
        “input”: “thread”,
        “reasoning”: “thread 位于咖啡机区域，当前咖啡数量为 1，可制作一杯；顾客头顶未出现高亮词，因此尚未可上菜；收银台上的 ‘rail’ 不是上菜词，也未到付款阶段。”
        }
    ]
}"""

    def analyze_screenshot(self, image_url: str) -> Optional[any]:
        """分析游戏截图并返回游戏计划。

        Args:
            image_url (str): 图片的 URL

        Returns:
            Optional[any]: 游戏计划，如果分析失败则返回 None
        """
        print(f"\n使用图片: {image_url}")

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "请分析这个游戏截图，告诉我当前的订单状态，并给出具体的操作步骤。"
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url}
                        }
                    ]
                }
            ],
            max_tokens=1000,
            temperature=0
        )

        print("\nGPT 响应:")
        content = response.choices[0].message.content
        print(content)

        try:
            # 尝试在响应中找到 JSON 部分
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = content[json_start:json_end]
                plan = json.loads(json_str)
                # 取得所有input
                inputs = [step['input'] for step in plan['steps']]
                return inputs
            else:
                print("未找到 JSON 数据")
                return None
        except json.JSONDecodeError as e:
            print(f"JSON 解析错误: {e}")
            return None
        except Exception as e:
            print(f"分析截图时发生错误: {e}")
            return None

    def execute_plan(self, plan: Dict) -> bool:
        """
        执行操作计划
        
        Args:
            plan (Dict): 操作计划
            
        Returns:
            bool: 是否执行成功
        """
        # TODO: 实现计划执行逻辑
        return True 