#!/usr/bin/env python3
"""
游戏窗口截图器
主要功能：
1. 获取游戏窗口
2. 截图
3. 上传到 imgur
"""

import os
import time
from pathlib import Path
from typing import Optional

import pyautogui
import pywinctl as pwc
from dotenv import load_dotenv
from imgurpython import ImgurClient

class GameScreenshoter:
    """游戏窗口截图类"""
    
    def __init__(self, window_title: str = "The Chef's Shift"):
        """
        初始化截图器
        
        Args:
            window_title (str): 要截图的窗口标题
        """
        # 加载环境变量
        load_dotenv()
        
        # 获取 imgur 客户端 ID 和密钥
        self.imgur_client_id = os.getenv('IMGUR_CLIENT_ID')
        self.imgur_client_secret = os.getenv('IMGUR_CLIENT_SECRET')
        
        if not self.imgur_client_id or not self.imgur_client_secret:
            raise ValueError("请在 .env 文件中设置 IMGUR_CLIENT_ID 和 IMGUR_CLIENT_SECRET")
        
        # 初始化 imgur 客户端
        self.imgur_client = ImgurClient(self.imgur_client_id, self.imgur_client_secret)
        
        # 游戏窗口标题
        self.window_title = window_title
        
        # 创建 screenshots 目录
        self.screenshot_dir = Path("screenshots")
        self.screenshot_dir.mkdir(exist_ok=True)
        
        # 禁用 pyautogui 的暂停功能
        pyautogui.FAILSAFE = False

    def get_game_window(self) -> Optional[pwc.Window]:
        """
        获取游戏窗口
        
        Returns:
            Optional[pwc.Window]: 窗口对象，如果未找到则返回 None
        """
        try:
            # 获取所有窗口
            titles = pwc.getAllTitles()
            
            # 查找游戏窗口
            for title in titles:
                if self.window_title == title:
                    print(f"找到游戏窗口: {title}")
                    windows = pwc.getWindowsWithTitle(title)
                    if windows:  # 确保找到了窗口
                        return windows[0]  # 返回第一个匹配的窗口
            
            print(f"未找到标题包含 '{self.window_title}' 的窗口")
            print("当前可用窗口:")
            for title in titles:
                print(f"- {title}")
            return None
            
        except Exception as e:
            print(f"获取窗口失败: {e}")
            return None

    def capture_window(self, window: pwc.Window) -> Optional[str]:
        """
        截取窗口图像并保存
        
        Args:
            window (pwc.Window): 窗口对象
            
        Returns:
            Optional[str]: 截图文件路径，如果失败则返回 None
        """
        try:
            # 获取窗口几何信息
            left, top = window.topleft
            width, height = window.size
            
            # 转换为整数坐标
            left, top = int(left), int(top)
            width, height = int(width), int(height)
            region = (left, top, width, height)
            
            print(f"窗口位置: left={left}, top={top}, width={width}, height={height}")
            
            # 生成截图文件名
            timestamp = int(time.time())
            screenshot_path = self.screenshot_dir / f"game_{timestamp}.png"
            
            # 截图并保存
            screenshot = pyautogui.screenshot(region=region)
            screenshot.save(str(screenshot_path))
            
            print(f"截图已保存至: {screenshot_path}")
            return str(screenshot_path)
            
        except Exception as e:
            print(f"截图失败: {e}")
            return None

    def upload_to_imgur(self, image_path: str) -> Optional[str]:
        """
        将图片上传到 imgur
        
        Args:
            image_path (str): 图片文件路径
            
        Returns:
            Optional[str]: 图片URL，如果上传失败则返回 None
        """
        try:
            # 上传图片
            response = self.imgur_client.upload_from_path(image_path)
            image_url = response['link']
            
            print(f"图片已上传: {image_url}")
            return image_url
            
        except Exception as e:
            print(f"上传失败: {e}")
            return None

    def take_screenshot(self) -> Optional[str]:
        """
        执行截图操作并上传
        
        Returns:
            Optional[str]: 上传后的图片URL，如果失败则返回 None
        """
        # 获取游戏窗口
        window = self.get_game_window()
        if not window:
            return None
        
        # 激活窗口
        window.activate()
        time.sleep(0.5)
        
        # 截图
        screenshot_path = self.capture_window(window)
        if not screenshot_path:
            return None
            
        # 上传到 imgur
        return self.upload_to_imgur(screenshot_path) 