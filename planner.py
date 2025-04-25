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
        self.system_prompt = """你是一个《The Chef's Shift》游戏的AI助手。
游戏规则：
1. 玩家完全通过打字来进行游戏，包括开始游戏，制作食物的所有动作，处理订单，收款等。单词包括字母和特殊字符。
2. 游戏控制界面上通过start，retry，done等词来进行控制。
3. 在游戏进行中，玩家需要通过打字来制作食物，需要打的单词跟食物的名称或采取的动作无关，只跟屏幕显示有关。
4. 只有高亮显示的单词才是可以输入的单词，灰色显示的单词不能输入。高亮的单词是深棕色底色白色字体。
5. 每个食物都有特定的制作步骤。
6. 玩家控制的是厨师，厨师穿着白色厨师服，戴着厨师帽，穿着红色围裙。
7. 关于屏幕区域：
   * 屏幕左上方显示当前准备好的食物，食物下方有数字序号显示
   * 屏幕右侧有两张桌子，屏幕正中有一张桌子
   * 屏幕上方偏左窗户下面是三种甜品，输入单词直接制作完成
   * 屏幕中间靠下一点是咖啡机，咖啡机旁边是制作好的咖啡。咖啡机可以制作两种咖啡，边上显示两种咖啡的数量
   * 屏幕中间偏左是收银台，收银台在烤炉和咖啡机之间
   * 屏幕下方是面条制作区，食材在左边，煮锅在右边；先拿起面条食材，再放到锅里煮熟
   * 屏幕左下角是炸物区，可以制作两种炸物；原料在左边，炸锅在右边；拿起原料放入边上炸锅，炸好后拿出
   * 屏幕左侧边上是披萨制作区，从下到上依次准备好食材，放入上边烤箱，烤好之后拿出
8. 坐在桌边的客户服务流程如下：
   * 客户所在的桌子上方会显示食物图片，此时桌子上方没有单词高亮显示，需要按照客户订单，制作食物
   * 食物准备好后，桌子上方会显示高亮单词，此时输入这个单词即可完成订单
   * 订单完成后，客户会来到收银台前，此时客户头顶会显示钞票图案，此时没有单词显示，需要输入收银台上的单词完成付款
9. 来到收银台前的客户服务流程如下：
   * 客户头顶会显示食物图片，此时客户头顶没有单词高亮显示，需要按照客户订单，制作食物
   * 食物准备好后，客户头顶会显示高亮单词，此时输入客户头顶的单词即可完成订单
   * 订单完成后，客户头顶会显示钞票图案，此时没有单词显示，需要输入收银台上的单词完成付款
10. 收银台上的单词一直是高亮的，但只有客户头上有钞票图案时，才需要输入收银台上的单词完成付款
11. 如果红色地毯上有老鼠，输入老鼠头顶的两个字母的单词可以消灭老鼠
12. 如果屏幕上没有老鼠，则优先处理已经准备好食物的订单，然后处理其他订单。
13. 如果屏幕上有老鼠，优先消灭老鼠。
14. 异常情况，如果屏幕上高亮的单词前面几个字符是黄色的，代表单词没有输入完，需要用退格键删除已经输入的单词，或者将单词输入完整。


你的任务是：
1. 分析游戏截图，识别当前图片上的内容和状态
2. 识别当前需要处理的订单和步骤
3. 生成具体的操作步骤，也就是需要输入的单词和动作
4. 返回结构化的 JSON 格式响应

请确保你的响应以json格式返回，包含以下信息：
1. 详细描述当前图片上的所有信息
2. 当前图片上所有高亮的可以输入的单词
3. 当前图片收银台上的单词
4. 当前图片上是否有老鼠
5. 当前需要处理的订单
6. 详细的制作步骤
7. 制作步骤中input的单词必须在words列表里

响应格式示例：
{
    "description": "左上角显示已经做好咖啡和披萨；收银台上有use，收银台前有两个客户，一个准备付款，一个需要咖啡；面条已经煮好；炸锅是空的；咖啡机旁显示咖啡还有两杯；桌子上有两组客户，一组的食物已经准备好，另一组需要两个汉堡；红色地毯上没有老鼠。厨师的位置在收银台附近。两个客户头顶显示的订单没有准备好，需要先制作食物；一个客户头顶显示钞票，需要收款；一个客户头顶显示高亮单词，需要上菜。",
    "words": ['toe', 'body', 'page', 'week', 'use', 'cow'],
    "cash": 'use',
    "mouse": 'false',
    "order": "披萨",
    "steps": [
        {
            "action": "拿起pizza面饼",
            "input": "week",
            "note": "制作pizza需要先拿起pizza面饼"
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