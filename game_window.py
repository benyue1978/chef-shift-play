#!/usr/bin/env python3
"""
游戏窗口控制器
主要功能：
1. 获取和控制游戏窗口
2. 截图功能
3. 上传图片到 imgur
4. 键盘输入控制
"""

import os
import queue
import threading
import time
from pathlib import Path
from typing import Optional, Tuple, Set

import pyautogui
import pywinctl as pwc
from dotenv import load_dotenv
from imgurpython import ImgurClient


class GameWindow:
    """
    游戏窗口控制类
    
    负责管理游戏窗口的各种操作，包括：
    - 窗口查找和控制
    - 截图功能
    - 图片上传
    - 键盘输入
    """
    
    def __init__(self, window_title: str = "The Chef's Shift"):
        """
        初始化游戏窗口控制器
        
        Args:
            window_title (str): 要控制的窗口标题
        """
        # 加载环境变量
        load_dotenv()
        
        # 获取 imgur 客户端配置
        self.imgur_client_id = os.getenv('IMGUR_CLIENT_ID')
        self.imgur_client_secret = os.getenv('IMGUR_CLIENT_SECRET')
        
        if not self.imgur_client_id or not self.imgur_client_secret:
            raise ValueError("请在 .env 文件中设置 IMGUR_CLIENT_ID 和 IMGUR_CLIENT_SECRET")
        
        # 初始化 imgur 客户端
        self.imgur_client = ImgurClient(self.imgur_client_id, self.imgur_client_secret)
        
        # 游戏窗口属性
        self.window_title = window_title
        self.game_window: Optional[pwc.Window] = None
        
        # 创建 screenshots 目录
        self.screenshot_dir = Path("screenshots")
        self.screenshot_dir.mkdir(exist_ok=True)
        
        # 配置 pyautogui
        pyautogui.FAILSAFE = False
        
        # 键盘输入相关
        self.input_queue = queue.Queue()  # 输入队列
        self.current_queue_words: Set[str] = set()  # 当前队列中的单词集合
        self.keyboard_thread = None  # 键盘输入线程
        self.is_typing = False  # 键盘输入状态
        self.typing_interval = 0.05  # 字母间隔时间（秒）

    def start_keyboard_thread(self) -> None:
        """
        启动键盘输入线程
        """
        if self.keyboard_thread and self.keyboard_thread.is_alive():
            return
            
        self.is_typing = True
        self.keyboard_thread = threading.Thread(target=self._keyboard_worker, daemon=True)
        self.keyboard_thread.start()
        print("键盘输入线程已启动")

    def stop_keyboard_thread(self) -> None:
        """
        停止键盘输入线程
        """
        self.is_typing = False
        if self.keyboard_thread:
            self.keyboard_thread.join()
            print("键盘输入线程已停止")

    def _keyboard_worker(self) -> None:
        """
        键盘输入工作线程
        负责从队列中获取单词并模拟键盘输入
        """
        while self.is_typing:
            try:
                # 非阻塞方式获取队列数据
                word = self.input_queue.get_nowait()
                
                # 确保窗口处于激活状态
                window = self.get_window()
                if window:
                    window.activate()
                    time.sleep(0.1)  # 等待窗口激活
                    
                    # 逐字母输入
                    for letter in word:
                        if not self.is_typing:
                            break
                        pyautogui.write(letter)
                        time.sleep(self.typing_interval)
                    
                # 从当前队列单词集合中移除
                self.current_queue_words.remove(word)
                self.input_queue.task_done()
                print(f"完成输入单词: {word}")
                
            except queue.Empty:
                # 队列为空时短暂休眠
                time.sleep(0.1)
                continue
            except Exception as e:
                print(f"键盘输入错误: {e}")
                continue

    def add_input_words(self, words: list[str]) -> None:
        """
        添加输入单词到队列
        
        Args:
            words (list[str]): 要输入的单词列表
        """
        for word in words:
            # 只对当前队列中的单词进行去重
            if word not in self.current_queue_words:
                self.current_queue_words.add(word)
                self.input_queue.put(word)
                print(f"添加单词到输入队列: {word}")

    def clear_input_queue(self) -> None:
        """
        清空输入队列和当前队列单词集合
        """
        while not self.input_queue.empty():
            try:
                self.input_queue.get_nowait()
                self.input_queue.task_done()
            except queue.Empty:
                break
        self.current_queue_words.clear()
        print("输入队列已清空")

    def get_window(self) -> Optional[pwc.Window]:
        """
        获取游戏窗口
        
        Returns:
            Optional[pwc.Window]: 窗口对象，如果未找到则返回 None
        """
        try:
            if self.game_window:
                return self.game_window

            # 获取所有窗口
            titles = pwc.getAllTitles()
            
            # 查找游戏窗口
            for title in titles:
                if self.window_title == title:
                    print(f"找到游戏窗口: {title}")
                    windows = pwc.getWindowsWithTitle(title)
                    if windows:
                        self.game_window = windows[0]
                        return self.game_window
            
            print(f"未找到标题包含 '{self.window_title}' 的窗口")
            print("当前可用窗口:")
            for title in titles:
                print(f"- {title}")
            return None
            
        except Exception as e:
            print(f"获取窗口失败: {e}")
            return None

    def get_window_geometry(self) -> Optional[Tuple[int, int, int, int]]:
        """
        获取窗口的几何信息
        
        Returns:
            Optional[Tuple[int, int, int, int]]: (left, top, width, height) 或 None
        """
        window = self.get_window()
        if not window:
            return None
            
        left, top = window.topleft
        width, height = window.size
        
        return (int(left), int(top), int(width), int(height))

    def capture_window(self) -> Optional[str]:
        """
        截取窗口图像并保存
        
        Returns:
            Optional[str]: 截图文件路径，如果失败则返回 None
        """
        try:
            geometry = self.get_window_geometry()
            if not geometry:
                return None
                
            left, top, width, height = geometry
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
        window = self.get_window()
        if not window:
            return None
        
        # 激活窗口
        window.activate()
        
        # 截图
        screenshot_path = self.capture_window()
        if not screenshot_path:
            return None
            
        # 上传到 imgur
        return self.upload_to_imgur(screenshot_path) 