#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
27930功能演示脚本
演示充电桩测试功能的各种特性
"""

import tkinter as tk
from main import ModernUI
import time

def demo_27930_features():
    """演示27930功能特性"""
    print("=== 27930充电桩测试功能演示 ===")
    
    # 创建主窗口
    root = tk.Tk()
    app = ModernUI(root)
    
    # 切换到27930测试页面
    app.notebook.select(1)
    
    print("1. 界面布局演示")
    print("   - 左侧：CAN接口设置区域")
    print("   - 右侧：数据显示区域（原始数据 + 数据解析）")
    
    print("\n2. CAN接口设置演示")
    print("   - CAN设备选择：支持多种CAN设备类型")
    print("   - CAN波特率：支持标准波特率设置")
    print("   - CAN通道：支持双通道配置")
    print("   - 设备状态：实时显示连接状态")
    
    print("\n3. 27930功能设置演示")
    print("   - 消息类型：充电握手、充电参数配置、充电状态等")
    print("   - 地址设置：发送方和接收方地址配置")
    print("   - 进制选择：支持十进制和十六进制")
    
    print("\n4. 扫描功能演示")
    print("   - 定时扫描：可设置扫描间隔")
    print("   - 扫描控制：开始/停止功能")
    print("   - 状态显示：实时扫描状态")
    
    print("\n5. 数据显示演示")
    print("   - 原始数据：显示CAN数据包")
    print("   - 数据解析：显示27930协议解析结果")
    print("   - 格式选择：十六进制/十进制显示")
    
    print("\n6. 操作流程演示")
    print("   - 选择CAN设备并设置参数")
    print("   - 打开CAN设备连接")
    print("   - 选择27930消息类型")
    print("   - 设置发送方和接收方地址")
    print("   - 发送数据并查看结果")
    
    # 启动应用
    root.mainloop()

if __name__ == "__main__":
    demo_27930_features() 