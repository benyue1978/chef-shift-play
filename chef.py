#!/usr/bin/env python3
"""
Chef's Shift AI 自动操作程序
"""

import sys
import time

from game_window import GameWindow
from planner import GamePlanner

def main():
    """主函数"""
    try:
        # 创建游戏窗口实例
        game_window = GameWindow("The Chef's Shift")
        
        # 启动键盘输入线程
        game_window.start_keyboard_thread()
        
        try:
            while True:
                # 获取截图URL
                image_url = game_window.take_screenshot()
                if not image_url:
                    print("获取截图失败")
                    continue
                    
                print(f"获取截图成功: {image_url}")
                
                # 创建任务规划器实例
                planner = GamePlanner()
                
                # 分析截图
                inputs = planner.analyze_screenshot(image_url)
                if not inputs:
                    print("分析截图失败")
                    continue
                
                # 添加输入到队列
                print(f"添加输入队列: {inputs}")
                game_window.add_input_words(inputs)
                
                # 等待一段时间再进行下一次截图
                time.sleep(2)
                
        except KeyboardInterrupt:
            print("\n停止自动操作")
        finally:
            # 停止键盘输入线程
            game_window.stop_keyboard_thread()
            
    except Exception as e:
        print(f"发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 