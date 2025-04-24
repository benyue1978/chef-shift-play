#!/usr/bin/env python3
"""
Chef's Shift AI 自动操作程序
"""

import sys

from screenshoter import GameScreenshoter

def main():
    """主函数"""
    try:
        # 创建截图器实例
        screenshoter = GameScreenshoter("The Chef's Shift")
        
        # 获取截图URL
        image_url = screenshoter.take_screenshot()
        if not image_url:
            sys.exit(1)
            
        print("处理完成！")
        print(f"图片URL: {image_url}")
        
    except KeyboardInterrupt:
        print("\n程序已终止")
        sys.exit(0)
    except Exception as e:
        print(f"发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 