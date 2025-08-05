import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import datetime

class ModbusParserWindow:
    """Modbus解析对码窗口"""
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Modbus解析对码")
        self.window.geometry("850x600")  # 减少高度从700到600
        self.window.minsize(800, 500)     # 减少最小高度从600到500
        
        # 注释数据存储
        self.annotations = {}
        self.annotation_file = "modbus_annotations.json"
        
        # 创建界面
        self.create_interface()
        
        # 加载注释（在界面创建之后）
        self.load_annotations()
        
        # 设置窗口关闭事件
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def create_interface(self):
        """创建解析界面"""
        # 状态栏变量初始化
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        
        # 主框架 - 进一步减少padding
        main_frame = ttk.Frame(self.window, padding="2")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)  # 让tab控件占据更多空间
        main_frame.rowconfigure(1, weight=0)  # 状态栏不扩展
        
        # 创建Tab控件 - 最小间距，让状态栏更贴近
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=2, pady=(2, 0))
        
        # 功能码解析页面
        self.function_code_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.function_code_frame, text="功能码解析")
        self.create_function_code_parser()
        
        # 状态栏 - 紧贴notebook下部，无间距
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 0))
        
    def create_function_code_parser(self):
        """创建功能码解析界面"""
        # 配置网格权重 - 让左右两个区域大小均衡
        self.function_code_frame.columnconfigure(0, weight=1)  # 左侧区域权重
        self.function_code_frame.columnconfigure(1, weight=1)  # 右侧区域权重
        self.function_code_frame.rowconfigure(0, weight=1)
        
        # 左侧输入区域 - 设置固定宽度，让右侧区域有更多空间
        input_frame = ttk.LabelFrame(self.function_code_frame, text="数据输入", padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # 配置输入框架的网格权重，让内容垂直分布
        input_frame.columnconfigure(1, weight=1)
        input_frame.rowconfigure(11, weight=1)  # 让最后一个按钮区域扩展
        
        # 功能码选择
        ttk.Label(input_frame, text="功能码:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.function_code_var = tk.StringVar(value="01 - 读线圈状态")
        function_code_combo = ttk.Combobox(input_frame, textvariable=self.function_code_var,
                                          values=["01 - 读线圈状态", "02 - 读离散输入", "03 - 读保持寄存器", 
                                                 "04 - 读输入寄存器", "05 - 写单个线圈", "06 - 写单个寄存器",
                                                 "15 - 写多个线圈", "16 - 写多个寄存器"], 
                                          width=25, state="readonly")
        function_code_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        function_code_combo.bind('<<ComboboxSelected>>', self.on_function_code_change)
        
        # 数据输入
        ttk.Label(input_frame, text="数据(HEX):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.data_input_var = tk.StringVar(value="01 01 00 00 00 04 3D CC")
        data_entry = ttk.Entry(input_frame, textvariable=self.data_input_var, width=35)
        data_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # 解析按钮
        ttk.Button(input_frame, text="解析数据", command=self.parse_data, 
                  style="Accent.TButton").grid(row=2, column=0, columnspan=2, pady=10)
        
        # 分隔线
        separator = ttk.Separator(input_frame, orient='horizontal')
        separator.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # 注释管理
        ttk.Label(input_frame, text="注释管理:", font=("Arial", 10, "bold")).grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        ttk.Button(input_frame, text="保存注释", command=self.save_annotations).grid(row=5, column=0, pady=2)
        ttk.Button(input_frame, text="加载注释", command=self.load_annotations).grid(row=5, column=1, pady=2)
        ttk.Button(input_frame, text="导出注释", command=self.export_annotations).grid(row=6, column=0, pady=2)
        ttk.Button(input_frame, text="清空注释", command=self.clear_annotations).grid(row=6, column=1, pady=2)
        
        # 注释编辑区域
        ttk.Label(input_frame, text="注释编辑:", font=("Arial", 10, "bold")).grid(row=7, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        ttk.Label(input_frame, text="键值:").grid(row=8, column=0, sticky=tk.W, pady=2)
        self.annotation_key_var = tk.StringVar()
        annotation_key_entry = ttk.Entry(input_frame, textvariable=self.annotation_key_var, width=25)
        annotation_key_entry.grid(row=8, column=1, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(input_frame, text="注释:").grid(row=9, column=0, sticky=tk.W, pady=2)
        self.annotation_value_var = tk.StringVar()
        annotation_value_entry = ttk.Entry(input_frame, textvariable=self.annotation_value_var, width=25)
        annotation_value_entry.grid(row=9, column=1, sticky=(tk.W, tk.E), pady=2)
        
        annotation_button_frame = ttk.Frame(input_frame)
        annotation_button_frame.grid(row=10, column=0, columnspan=2, pady=5)
        
        ttk.Button(annotation_button_frame, text="添加/更新", command=self.add_annotation).grid(row=0, column=0, padx=2)
        ttk.Button(annotation_button_frame, text="删除", command=self.delete_annotation).grid(row=0, column=1, padx=2)
        ttk.Button(annotation_button_frame, text="查找", command=self.find_annotation).grid(row=0, column=2, padx=2)
        
        # 注释格式帮助按钮 - 放在底部，让它填满剩余空间
        help_button = ttk.Button(input_frame, text="注释格式帮助", command=self.show_annotation_help)
        help_button.grid(row=11, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 右侧解析结果显示区域 - 确保填满整个右侧区域
        result_frame = ttk.Frame(self.function_code_frame)
        result_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
        # 解析结果文本框 - 确保填满整个框架
        result_label_frame = ttk.LabelFrame(result_frame, text="解析结果", padding="5")
        result_label_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        result_label_frame.columnconfigure(0, weight=1)
        result_label_frame.rowconfigure(0, weight=1)
        
        self.result_text = tk.Text(result_label_frame, font=("Consolas", 10), wrap=tk.WORD)
        result_scrollbar = ttk.Scrollbar(result_label_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=result_scrollbar.set)
        
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        result_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 初始化显示
        self.on_function_code_change()
        
    def on_function_code_change(self, event=None):
        """功能码改变事件"""
        function_code_full = self.function_code_var.get()
        # 提取功能码的数字部分
        function_code = function_code_full.split(" - ")[0] if " - " in function_code_full else function_code_full
        self.status_var.set(f"当前功能码: {function_code_full}")
        
        # 根据功能码设置默认数据（实际应用场景的示例数据）
        default_data = {
            "01": "01 01 00 00 00 04 3D CC",  # 读线圈状态 - 主机请求报文
            "02": "01 02 00 00 00 08 3D 8C",  # 读离散输入 - 主机请求报文
            "03": "01 03 00 00 00 02 25 CA",  # 读保持寄存器 - 主机请求报文
            "04": "01 04 00 00 00 02 71 CB",  # 读输入寄存器 - 主机请求报文
            "05": "01 05 00 01 FF 00 8C 3A",  # 写单个线圈 - 主机请求报文
            "06": "01 06 00 01 00 0A 9D 9B",  # 写单个寄存器 - 主机请求报文
            "15": "01 0F 00 00 00 08 01 FF FF FF FF FF FF FF 8C 3A",  # 写多个线圈 - 主机请求报文
            "16": "01 10 00 00 00 02 04 00 0A 00 0B 8C 3A"  # 写多个寄存器 - 主机请求报文
        }
        
        if function_code in default_data:
            self.data_input_var.set(default_data[function_code])
            
    def parse_data(self):
        """解析数据"""
        try:
            function_code_full = self.function_code_var.get()
            # 提取功能码的数字部分
            function_code = function_code_full.split(" - ")[0] if " - " in function_code_full else function_code_full
            data_str = self.data_input_var.get().strip()
            
            # 清理数据字符串
            data_str = data_str.replace(" ", "").replace(",", "").replace(";", "")
            
            # 验证数据格式
            if not all(c in '0123456789ABCDEFabcdef' for c in data_str):
                raise ValueError("数据格式错误，请输入有效的十六进制数据")
            
            # 解析数据
            result = self.parse_modbus_data(function_code, data_str)
            
            # 显示结果
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
            
            self.status_var.set(f"数据解析完成 - 功能码: {function_code_full}")
            
        except Exception as e:
            messagebox.showerror("解析错误", str(e))
            self.status_var.set("数据解析失败")
            
    def parse_modbus_data(self, function_code, data_str):
        """解析Modbus数据"""
        result = []
        
        # 添加功能码说明
        function_descriptions = {
            "01": "读线圈状态（功能码01）\n用途：读取设备的开关量输出（DO），如继电器状态。",
            "02": "读离散输入（功能码02）\n用途：读取设备的开关量输入（DI），如传感器状态。",
            "03": "读保持寄存器（功能码03）\n用途：读取设备的保持寄存器，如设备参数、设定值等。",
            "04": "读输入寄存器（功能码04）\n用途：读取设备的输入寄存器，如传感器数据、测量值等。",
            "05": "写单个线圈（功能码05）\n用途：控制单个开关量输出，如继电器开关。",
            "06": "写单个寄存器（功能码06）\n用途：写入单个保持寄存器，如设定参数值。",
            "15": "写多个线圈（功能码15）\n用途：同时控制多个开关量输出。",
            "16": "写多个寄存器（功能码16）\n用途：同时写入多个保持寄存器。"
        }
        
        result.append(f"=== {function_descriptions.get(function_code, f'功能码{function_code}')} ===\n")
        
        # 将十六进制字符串转换为字节列表
        data_bytes = []
        for i in range(0, len(data_str), 2):
            if i + 1 < len(data_str):
                data_bytes.append(int(data_str[i:i+2], 16))
        
        result.append(f"原始数据: {' '.join([f'{b:02X}' for b in data_bytes])}\n")
        result.append(f"数据长度: {len(data_bytes)} 字节\n")
        
        # 根据功能码进行不同解析
        if function_code in ["01", "02"]:
            result.extend(self.parse_coil_data(data_bytes, function_code))
        elif function_code in ["03", "04"]:
            result.extend(self.parse_register_data(data_bytes, function_code))
        elif function_code in ["05", "06"]:
            result.extend(self.parse_single_write_data(data_bytes, function_code))
        elif function_code in ["15", "16"]:
            result.extend(self.parse_multiple_write_data(data_bytes, function_code))
        else:
            result.append("未知功能码，无法解析")
            
        return "".join(result)
        
    def parse_coil_data(self, data_bytes, function_code):
        """解析线圈/离散输入数据"""
        result = []
        
        if len(data_bytes) < 1:
            return ["数据长度不足"]
        
        # 判断是请求报文还是响应报文
        # 请求报文：从机地址 + 功能码 + 起始地址(2字节) + 数量(2字节) + CRC(2字节) = 8字节
        # 响应报文：字节数 + 数据字节 + CRC(2字节)
        if len(data_bytes) >= 6 and data_bytes[1] in [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x0F, 0x10]:
            # 这是请求报文
            result.append("=== 主机请求报文解析 ===\n")
            result.append(f"{data_bytes[0]:02X}：从机地址 ({data_bytes[0]})\n")
            result.append(f"{data_bytes[1]:02X}：功能码 ({data_bytes[1]:02d})\n")
            result.append(f"{data_bytes[2]:02X} {data_bytes[3]:02X}：起始地址 ({data_bytes[2] * 256 + data_bytes[3]})\n")
            result.append(f"{data_bytes[4]:02X} {data_bytes[5]:02X}：读取数量 ({data_bytes[4] * 256 + data_bytes[5]})\n")
            if len(data_bytes) >= 8:
                result.append(f"{data_bytes[6]:02X} {data_bytes[7]:02X}：CRC校验\n")
        else:
            # 这是响应报文
            result.append("=== 从机响应报文解析 ===\n")
            result.append(f"{data_bytes[0]:02X}：字节数 ({data_bytes[0]} 字节)\n")
            
            # 解析每个字节的位
            for i in range(1, min(len(data_bytes), data_bytes[0] + 1)):
                byte_value = data_bytes[i]
                result.append(f"字节 {i}: {byte_value:02X} (二进制: {byte_value:08b})\n")
                
                # 解析每个位
                for bit_pos in range(8):
                    bit_value = (byte_value >> bit_pos) & 1
                    bit_status = "ON" if bit_value == 1 else "OFF"
                    
                    # 计算全局位位置
                    global_bit_pos = (i - 1) * 8 + bit_pos
                    
                    # 获取注释
                    annotation_key = f"{function_code}_{global_bit_pos}"
                    annotation = self.annotations.get(annotation_key, "")
                    
                    # 根据功能码显示不同的文本
                    if function_code == "01":
                        result.append(f"  线圈 {global_bit_pos}: {bit_value} ({bit_status})")
                    else:  # function_code == "02"
                        result.append(f"  离散输入 {global_bit_pos}: {bit_value} ({bit_status})")
                    if annotation:
                        result.append(f" - {annotation}")
                    result.append("\n")
                
        return result
        
    def parse_register_data(self, data_bytes, function_code):
        """解析寄存器数据"""
        result = []
        
        if len(data_bytes) < 1:
            return ["数据长度不足"]
        
        # 判断是请求报文还是响应报文
        # 请求报文：从机地址 + 功能码 + 起始地址(2字节) + 数量(2字节) + CRC(2字节) = 8字节
        # 响应报文：字节数 + 数据字节 + CRC(2字节)
        if len(data_bytes) >= 6 and data_bytes[1] in [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x0F, 0x10]:
            # 这是请求报文
            result.append("=== 主机请求报文解析 ===\n")
            result.append(f"{data_bytes[0]:02X}：从机地址 ({data_bytes[0]})\n")
            result.append(f"{data_bytes[1]:02X}：功能码 ({data_bytes[1]:02d})\n")
            result.append(f"{data_bytes[2]:02X} {data_bytes[3]:02X}：起始地址 ({data_bytes[2] * 256 + data_bytes[3]})\n")
            result.append(f"{data_bytes[4]:02X} {data_bytes[5]:02X}：读取数量 ({data_bytes[4] * 256 + data_bytes[5]})\n")
            if len(data_bytes) >= 8:
                result.append(f"{data_bytes[6]:02X} {data_bytes[7]:02X}：CRC校验\n")
        else:
            # 这是响应报文
            result.append("=== 从机响应报文解析 ===\n")
            result.append(f"{data_bytes[0]:02X}：字节数 ({data_bytes[0]} 字节)\n")
            
            # 解析寄存器值（每个寄存器2字节）
            register_count = data_bytes[0] // 2
            result.append(f"寄存器数量: {register_count}\n")
            
            for i in range(register_count):
                if 1 + i * 2 + 1 < len(data_bytes):
                    high_byte = data_bytes[1 + i * 2]
                    low_byte = data_bytes[1 + i * 2 + 1]
                    register_value = (high_byte << 8) | low_byte
                    
                    result.append(f"寄存器 {i}: {register_value:04X} ({register_value})")
                    
                    # 获取注释
                    annotation_key = f"{function_code}_reg_{i}"
                    annotation = self.annotations.get(annotation_key, "")
                    if annotation:
                        result.append(f" - {annotation}")
                    result.append("\n")
                
        return result
        
    def parse_single_write_data(self, data_bytes, function_code):
        """解析单个写操作数据"""
        result = []
        
        if len(data_bytes) < 4:
            return ["数据长度不足"]
        
        # 判断是请求报文还是响应报文
        # 请求报文：从机地址 + 功能码 + 起始地址(2字节) + 数量(2字节) + CRC(2字节) = 8字节
        # 响应报文：字节数 + 数据字节 + CRC(2字节)
        if len(data_bytes) >= 6 and data_bytes[1] in [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x0F, 0x10]:
            # 这是请求报文
            result.append("=== 主机请求报文解析 ===\n")
            result.append(f"{data_bytes[0]:02X}：从机地址 ({data_bytes[0]})\n")
            result.append(f"{data_bytes[1]:02X}：功能码 ({data_bytes[1]:02d})\n")
            result.append(f"{data_bytes[2]:02X} {data_bytes[3]:02X}：地址 ({data_bytes[2] * 256 + data_bytes[3]})\n")
            result.append(f"{data_bytes[4]:02X} {data_bytes[5]:02X}：写入值 ({data_bytes[4] * 256 + data_bytes[5]})\n")
            if len(data_bytes) >= 8:
                result.append(f"{data_bytes[6]:02X} {data_bytes[7]:02X}：CRC校验\n")
        else:
            # 这是响应报文
            result.append("=== 从机响应报文解析 ===\n")
            result.append(f"{data_bytes[0]:02X}：从机地址 ({data_bytes[0]})\n")
            result.append(f"{data_bytes[1]:02X}：功能码 ({data_bytes[1]:02d})\n")
            result.append(f"{data_bytes[2]:02X} {data_bytes[3]:02X}：地址 ({data_bytes[2] * 256 + data_bytes[3]})\n")
            result.append(f"{data_bytes[4]:02X} {data_bytes[5]:02X}：写入值 ({data_bytes[4] * 256 + data_bytes[5]})\n")
            if len(data_bytes) >= 8:
                result.append(f"{data_bytes[6]:02X} {data_bytes[7]:02X}：CRC校验\n")
            
        return result
        
    def parse_multiple_write_data(self, data_bytes, function_code):
        """解析多个写操作数据"""
        result = []
        
        if len(data_bytes) < 5:
            return ["数据长度不足"]
        
        # 判断是请求报文还是响应报文
        # 请求报文：从机地址 + 功能码 + 起始地址(2字节) + 数量(2字节) + CRC(2字节) = 8字节
        # 响应报文：字节数 + 数据字节 + CRC(2字节)
        if len(data_bytes) >= 6 and data_bytes[1] in [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x0F, 0x10]:
            # 这是请求报文
            result.append("=== 主机请求报文解析 ===\n")
            result.append(f"{data_bytes[0]:02X}：从机地址 ({data_bytes[0]})\n")
            result.append(f"{data_bytes[1]:02X}：功能码 ({data_bytes[1]:02d})\n")
            result.append(f"{data_bytes[2]:02X} {data_bytes[3]:02X}：起始地址 ({data_bytes[2] * 256 + data_bytes[3]})\n")
            result.append(f"{data_bytes[4]:02X} {data_bytes[5]:02X}：数量 ({data_bytes[4] * 256 + data_bytes[5]})\n")
            result.append(f"{data_bytes[6]:02X}：字节数 ({data_bytes[6]} 字节)\n")
            
            # 解析数据部分
            data_start = 7
            data_end = len(data_bytes) - 2  # 减去CRC校验的2字节
            if function_code == "15":  # 写多个线圈
                result.extend(self.parse_multiple_coil_data(data_bytes[data_start:data_end], data_bytes[2] * 256 + data_bytes[3], data_bytes[4] * 256 + data_bytes[5]))
            else:  # 写多个寄存器
                result.extend(self.parse_multiple_register_data(data_bytes[data_start:data_end], data_bytes[2] * 256 + data_bytes[3], data_bytes[4] * 256 + data_bytes[5]))
            
            # 添加CRC校验
            if len(data_bytes) >= 8:
                result.append(f"{data_bytes[-2]:02X} {data_bytes[-1]:02X}：CRC校验\n")
        else:
            # 这是响应报文
            result.append("=== 从机响应报文解析 ===\n")
            result.append(f"{data_bytes[0]:02X}：从机地址 ({data_bytes[0]})\n")
            result.append(f"{data_bytes[1]:02X}：功能码 ({data_bytes[1]:02d})\n")
            result.append(f"{data_bytes[2]:02X} {data_bytes[3]:02X}：起始地址 ({data_bytes[2] * 256 + data_bytes[3]})\n")
            result.append(f"{data_bytes[4]:02X} {data_bytes[5]:02X}：数量 ({data_bytes[4] * 256 + data_bytes[5]})\n")
            if len(data_bytes) >= 8:
                result.append(f"{data_bytes[6]:02X} {data_bytes[7]:02X}：CRC校验\n")
            else:
                result.append("响应报文格式错误，数据长度不足\n")
            
        return result
        
    def parse_multiple_coil_data(self, data_bytes, start_address, count):
        """解析多个线圈数据"""
        result = []
        
        for i in range(count):
            byte_index = i // 8
            bit_index = i % 8
            
            if byte_index < len(data_bytes):
                byte_value = data_bytes[byte_index]
                bit_value = (byte_value >> bit_index) & 1
                coil_status = "开" if bit_value == 1 else "闭"
                
                result.append(f"线圈 {start_address + i}: {bit_value} ({coil_status})")
                
                # 获取注释
                annotation_key = f"15_coil_{start_address + i}"
                annotation = self.annotations.get(annotation_key, "")
                if annotation:
                    result.append(f" - {annotation}")
                result.append("\n")
                
        return result
        
    def parse_multiple_register_data(self, data_bytes, start_address, count):
        """解析多个寄存器数据"""
        result = []
        
        for i in range(count):
            if i * 2 + 1 < len(data_bytes):
                high_byte = data_bytes[i * 2]
                low_byte = data_bytes[i * 2 + 1]
                register_value = (high_byte << 8) | low_byte
                
                result.append(f"寄存器 {start_address + i}: {register_value:04X} ({register_value})")
                
                # 获取注释
                annotation_key = f"16_reg_{start_address + i}"
                annotation = self.annotations.get(annotation_key, "")
                if annotation:
                    result.append(f" - {annotation}")
                result.append("\n")
                
        return result
        
    def save_annotations(self):
        """保存注释到文件"""
        try:
            with open(self.annotation_file, 'w', encoding='utf-8') as f:
                json.dump(self.annotations, f, ensure_ascii=False, indent=2)
            self.status_var.set("注释已保存")
            messagebox.showinfo("成功", "注释已保存到文件")
        except Exception as e:
            messagebox.showerror("错误", f"保存注释失败: {str(e)}")
            
    def load_annotations(self):
        """从文件加载注释"""
        try:
            if os.path.exists(self.annotation_file):
                with open(self.annotation_file, 'r', encoding='utf-8') as f:
                    self.annotations = json.load(f)
                if hasattr(self, 'status_var'):
                    self.status_var.set("注释已加载")
            else:
                self.annotations = {}
                if hasattr(self, 'status_var'):
                    self.status_var.set("注释文件不存在，已创建新的注释字典")
        except Exception as e:
            self.annotations = {}
            if hasattr(self, 'status_var'):
                messagebox.showerror("错误", f"加载注释失败: {str(e)}")
            
    def export_annotations(self):
        """导出注释为文本文件"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"modbus_annotations_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("Modbus注释导出文件\n")
                f.write("=" * 50 + "\n")
                f.write(f"导出时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for key, value in self.annotations.items():
                    f.write(f"{key}: {value}\n")
                    
            self.status_var.set(f"注释已导出到 {filename}")
            messagebox.showinfo("成功", f"注释已导出到文件: {filename}")
        except Exception as e:
            messagebox.showerror("错误", f"导出注释失败: {str(e)}")
            
    def clear_annotations(self):
        """清空注释"""
        if messagebox.askyesno("确认", "确定要清空所有注释吗？"):
            self.annotations = {}
            self.status_var.set("注释已清空")
            
    def add_annotation(self):
        """添加或更新注释"""
        key = self.annotation_key_var.get().strip()
        value = self.annotation_value_var.get().strip()
        
        if not key or not value:
            messagebox.showwarning("警告", "键和注释不能为空")
            return
            
        self.annotations[key] = value
        self.status_var.set(f"注释已添加/更新: {key}")
        
        # 清空输入框
        self.annotation_key_var.set("")
        self.annotation_value_var.set("")
        
    def delete_annotation(self):
        """删除注释"""
        key = self.annotation_key_var.get().strip()
        if key in self.annotations:
            if messagebox.askyesno("确认", f"确定要删除注释 '{key}' 吗？"):
                del self.annotations[key]
                self.status_var.set(f"注释已删除: {key}")
                # 清空输入框
                self.annotation_key_var.set("")
                self.annotation_value_var.set("")
        else:
            messagebox.showwarning("警告", f"注释 '{key}' 不存在")
            
    def find_annotation(self):
        """查找注释"""
        key = self.annotation_key_var.get().strip()
        if key in self.annotations:
            self.annotation_value_var.set(self.annotations[key])
            self.status_var.set(f"找到注释: {key}")
        else:
            messagebox.showwarning("警告", f"注释 '{key}' 不存在")
            
    def show_annotation_help(self):
        """显示注释键值格式帮助"""
        help_text = """注释键值格式说明：

1. 线圈/离散输入位注释：
   - 格式: 功能码_位位置
   - 示例: 01_0, 01_1, 02_15
   - 说明: 用于标识具体的开关量点位

2. 寄存器注释：
   - 格式: 功能码_reg_寄存器索引
   - 示例: 03_reg_0, 04_reg_1
   - 说明: 用于标识具体的寄存器地址

3. 单个写操作注释：
   - 格式: 功能码_addr_地址
   - 示例: 05_addr_1, 06_addr_100
   - 说明: 用于标识写入操作的地址

4. 多个写操作注释：
   - 格式: 功能码_coil_地址 或 功能码_reg_地址
   - 示例: 15_coil_1, 16_reg_100
   - 说明: 用于标识批量写入的地址

功能码说明：
- 01: 读线圈状态 - 读取开关量输出（DO）
- 02: 读离散输入 - 读取开关量输入（DI）
- 03: 读保持寄存器 - 读取设备参数、设定值
- 04: 读输入寄存器 - 读取传感器数据、测量值
- 05: 写单个线圈 - 控制单个开关量输出
- 06: 写单个寄存器 - 写入单个参数值
- 15: 写多个线圈 - 同时控制多个开关量输出
- 16: 写多个寄存器 - 同时写入多个参数值

实际应用示例：
- 01_0: 继电器1状态
- 02_15: 传感器15状态
- 03_reg_100: 温度设定值
- 04_reg_200: 压力测量值
- 05_addr_1: 继电器1控制
- 06_addr_100: 温度设定写入"""
        
        messagebox.showinfo("注释格式帮助", help_text)
            
    def on_closing(self):
        """窗口关闭事件"""
        self.window.destroy()


# 如果直接运行此文件，创建测试窗口
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    parser_window = ModbusParserWindow(root)
    root.mainloop()
       