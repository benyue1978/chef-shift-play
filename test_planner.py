#!/usr/bin/env python3
"""
测试任务规划器
"""

import sys

from planner import GamePlanner

def main():
    """主函数"""
    try:
        # 创建任务规划器实例
        planner = GamePlanner()
        
        # 使用已有的图片URL
        image_urls = [
            "https://i.imgur.com/znzg4hm.png"
        ]
        
        # 分析截图
        for image_url in image_urls:
            inputs = planner.analyze_screenshot(image_url)
            if not inputs:
                print("分析截图失败")
                continue

            print("\n分析结果:")
            print(inputs)
            print("-" * 80)
            print("\n")
        
    except KeyboardInterrupt:
        print("\n程序已终止")
        sys.exit(0)
    except Exception as e:
        print(f"发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 