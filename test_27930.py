#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
27930测试功能验证脚本
"""

import tkinter as tk
from main import ModernUI

def test_27930_functionality():
    """测试27930功能"""
    print("启动27930测试...")
    
    # 创建主窗口
    root = tk.Tk()
    app = ModernUI(root)
    
    # 切换到27930测试页面
    app.notebook.select(1)  # 选择27930测试页面
    
    print("27930测试页面已创建")
    print("功能包括:")
    print("- CAN接口设置")
    print("- 27930功能设置")
    print("- 原始数据显示")
    print("- 数据解析显示")
    
    # 启动应用
    root.mainloop()

if __name__ == "__main__":
    test_27930_functionality() 