import tkinter as tk
from tkinter import ttk, messagebox
import os
import serial.tools.list_ports
from modbus_parser import ModbusParserWindow

class ModernUI:
    def __init__(self, root):
        self.root = root
        self.root.title("工控测试软件")
        
        # 设置窗口默认大小为显示器窗口的一半
        self.setup_window_size()
        
        # 创建菜单栏
        self.create_menu()
        
        # 创建主界面
        self.create_main_interface()
        
        # 绑定窗口大小改变事件
        self.root.bind('<Configure>', self.on_window_resize)
        
    def setup_window_size(self):
        """设置窗口默认大小为适合显示完整内容"""
        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 计算窗口大小为屏幕的一半
        window_width = screen_width // 2
        window_height = screen_height // 2
        
        # 计算窗口位置（居中）
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # 设置窗口大小和位置
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 设置最小窗口大小
        self.root.minsize(850, 600)
        
    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 第一个菜单：测试
        test_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="测试", menu=test_menu)
        test_menu.add_command(label="modbus测试", command=self.modbus_test)
        test_menu.add_command(label="modbus解析对码", command=self.open_modbus_parser)
        test_menu.add_command(label="27930测试", command=self.test_27930)
        test_menu.add_separator()
        test_menu.add_command(label="退出", command=self.root.quit)
        
        # 第二个菜单：关于
        about_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="关于", menu=about_menu)
        about_menu.add_command(label="本软件", command=self.show_about)
        
    def create_main_interface(self):
        """创建主界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重，使界面可以随窗口调整大小
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
                # 创建Tab控件
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Modbus测试页面
        self.modbus_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.modbus_frame, text="Modbus测试")
        
        # 创建Modbus页面内容
        self.create_modbus_interface()
        
        # 27930测试页面
        self.test_27930_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.test_27930_frame, text="27930测试")
        
        # 创建27930页面内容
        self.create_27930_interface()
        
        # 删除状态栏，不再显示窗口大小信息
        
        # 应用现代化样式
        self.apply_modern_style()
        
    def create_modbus_interface(self):
        """创建Modbus测试界面"""
        # 配置Modbus页面的网格权重
        self.modbus_frame.columnconfigure(1, weight=1)
        self.modbus_frame.rowconfigure(0, weight=1)
        
        # 左侧设置区域
        self.create_modbus_settings()
        
        # 右侧数据显示区域
        self.create_modbus_data_area()
        
    def create_modbus_settings(self):
        """创建左侧设置区域"""
        # 设置区域框架
        settings_frame = ttk.LabelFrame(self.modbus_frame, text="串口设置", padding="10")
        settings_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # 串口号设置
        ttk.Label(settings_frame, text="串口号:").grid(row=0, column=0, sticky=tk.W, pady=2)
        com_port_frame = ttk.Frame(settings_frame)
        com_port_frame.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        self.com_port_var = tk.StringVar()
        self.com_port_combo = ttk.Combobox(com_port_frame, textvariable=self.com_port_var, 
                                          width=10, state="readonly")
        self.com_port_combo.grid(row=0, column=0, padx=(0, 2))
        
        ttk.Button(com_port_frame, text="刷新", command=self.refresh_com_ports, width=6).grid(row=0, column=1, padx=(2, 0))
        
        # 串口状态图标
        self.com_status_label = tk.Label(com_port_frame, text="ℹ", font=("Arial", 12), fg="black", cursor="hand2")
        self.com_status_label.grid(row=0, column=2, padx=(5, 0))
        self.com_status_label.bind("<Enter>", self.show_com_info_tooltip)
        self.com_status_label.bind("<Leave>", self.hide_com_info_tooltip)
        
        # 初始化串口列表
        self.refresh_com_ports()
        
        # 波特率设置
        ttk.Label(settings_frame, text="波特率:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.baud_rate_var = tk.StringVar(value="9600")
        baud_rate_combo = ttk.Combobox(settings_frame, textvariable=self.baud_rate_var,
                                      values=["1200", "2400", "4800", "9600", "19200", "38400", "57600", "115200"],
                                      width=10, state="readonly")
        baud_rate_combo.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        # 数据位设置
        ttk.Label(settings_frame, text="数据位:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.data_bits_var = tk.StringVar(value="8")
        data_bits_combo = ttk.Combobox(settings_frame, textvariable=self.data_bits_var,
                                      values=["5", "6", "7", "8"], width=10, state="readonly")
        data_bits_combo.grid(row=2, column=1, sticky=tk.W, pady=2)
        
        # 停止位设置
        ttk.Label(settings_frame, text="停止位:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.stop_bits_var = tk.StringVar(value="1")
        stop_bits_combo = ttk.Combobox(settings_frame, textvariable=self.stop_bits_var,
                                      values=["1", "1.5", "2"], width=10, state="readonly")
        stop_bits_combo.grid(row=4, column=1, sticky=tk.W, pady=2)
        
        # 校验位设置
        ttk.Label(settings_frame, text="校验位:").grid(row=5, column=0, sticky=tk.W, pady=2)
        parity_frame = ttk.Frame(settings_frame)
        parity_frame.grid(row=5, column=1, sticky=tk.W, pady=2)
        
        self.parity_var = tk.StringVar(value="无")
        parity_combo = ttk.Combobox(parity_frame, textvariable=self.parity_var,
                                   values=["无", "奇校验", "偶校验"], width=10, state="readonly")
        parity_combo.grid(row=0, column=0, padx=(0, 15))
        
        # 串口开关按钮
        self.serial_status = False  # 串口状态：False=关闭，True=打开
        self.serial_button = ttk.Button(parity_frame, text="打开", command=self.toggle_serial, style="Accent.TButton", width=6)
        self.serial_button.grid(row=0, column=1)
        
        # 分隔线
        separator1 = ttk.Separator(settings_frame, orient='horizontal')
        separator1.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Modbus功能设置
        ttk.Label(settings_frame, text="Modbus功能:", font=("Arial", 10, "bold")).grid(row=7, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))
        
        # 从站地址
        ttk.Label(settings_frame, text="从站地址:").grid(row=8, column=0, sticky=tk.W, pady=2)
        slave_address_frame = ttk.Frame(settings_frame)
        slave_address_frame.grid(row=8, column=1, sticky=tk.W, pady=2)
        
        # 功能码选择
        ttk.Label(settings_frame, text="功能码:").grid(row=9, column=0, sticky=tk.W, pady=2)
        self.function_code_var = tk.StringVar(value="03 - 读保持寄存器")
        function_code_combo = ttk.Combobox(settings_frame, textvariable=self.function_code_var,
                                          values=["01 - 读线圈状态", "02 - 读离散输入", "03 - 读保持寄存器", 
                                                 "04 - 读输入寄存器", "05 - 写单个线圈", "06 - 写单个寄存器",
                                                 "15 - 写多个线圈", "16 - 写多个寄存器"], 
                                          width=15, state="readonly")
        function_code_combo.grid(row=9, column=1, sticky=tk.W, pady=2)
        
        self.slave_address_var = tk.StringVar(value="1")
        slave_address_entry = ttk.Entry(slave_address_frame, textvariable=self.slave_address_var, width=8)
        slave_address_entry.grid(row=0, column=0, padx=(0, 2))
        
        self.slave_address_base_var = tk.StringVar(value="DEC")
        slave_address_base_combo = ttk.Combobox(slave_address_frame, textvariable=self.slave_address_base_var,
                                               values=["DEC", "HEX"], width=4, state="readonly")
        slave_address_base_combo.grid(row=0, column=1)
        slave_address_base_combo.bind('<<ComboboxSelected>>', self.on_slave_address_base_change)
        
        # 寄存器地址
        ttk.Label(settings_frame, text="寄存器地址:").grid(row=10, column=0, sticky=tk.W, pady=2)
        register_address_frame = ttk.Frame(settings_frame)
        register_address_frame.grid(row=10, column=1, sticky=tk.W, pady=2)
        
        self.register_address_var = tk.StringVar(value="0")
        register_address_entry = ttk.Entry(register_address_frame, textvariable=self.register_address_var, width=8)
        register_address_entry.grid(row=0, column=0, padx=(0, 2))
        
        self.register_address_base_var = tk.StringVar(value="DEC")
        register_address_base_combo = ttk.Combobox(register_address_frame, textvariable=self.register_address_base_var,
                                                  values=["DEC", "HEX"], width=4, state="readonly")
        register_address_base_combo.grid(row=0, column=1)
        register_address_base_combo.bind('<<ComboboxSelected>>', self.on_register_address_base_change)
        
        # 寄存器数量
        ttk.Label(settings_frame, text="寄存器数量:").grid(row=11, column=0, sticky=tk.W, pady=2)
        register_count_frame = ttk.Frame(settings_frame)
        register_count_frame.grid(row=11, column=1, sticky=tk.W, pady=2)
        
        self.register_count_var = tk.StringVar(value="1")
        register_count_entry = ttk.Entry(register_count_frame, textvariable=self.register_count_var, width=8)
        register_count_entry.grid(row=0, column=0, padx=(0, 2))
        
        self.register_count_base_var = tk.StringVar(value="DEC")
        register_count_base_combo = ttk.Combobox(register_count_frame, textvariable=self.register_count_base_var,
                                                values=["DEC", "HEX"], width=4, state="readonly")
        register_count_base_combo.grid(row=0, column=1)
        register_count_base_combo.bind('<<ComboboxSelected>>', self.on_register_count_base_change)
        
        # 扫描设置
        ttk.Label(settings_frame, text="扫描:").grid(row=12, column=0, sticky=tk.W, pady=2)
        scan_rate_frame = ttk.Frame(settings_frame)
        scan_rate_frame.grid(row=12, column=1, sticky=tk.W, pady=2)
        
        self.scan_rate_var = tk.StringVar(value="1000")
        scan_rate_entry = ttk.Entry(scan_rate_frame, textvariable=self.scan_rate_var, width=8)
        scan_rate_entry.grid(row=0, column=0, padx=(0, 5))
        
        ttk.Label(scan_rate_frame, text="ms").grid(row=0, column=1)
        
        # 扫描按钮
        self.scan_button = ttk.Button(scan_rate_frame, text="开始", command=self.toggle_scan, style="Accent.TButton", width=6)
        self.scan_button.grid(row=0, column=2, padx=(10, 0))
        
        # 定时器状态
        self.scan_timer = None
        self.scanning = False
        
        # 分隔线
        separator2 = ttk.Separator(settings_frame, orient='horizontal')
        separator2.grid(row=13, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # 数据显示设置
        ttk.Label(settings_frame, text="显示设置:", font=("Arial", 10, "bold")).grid(row=14, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))
        
        # 数据显示格式
        self.data_format_var = tk.StringVar(value="HEX")
        format_frame = ttk.Frame(settings_frame)
        format_frame.grid(row=15, column=0, columnspan=3, sticky=tk.W, pady=1)
        ttk.Radiobutton(format_frame, text="十六进制", variable=self.data_format_var, value="HEX").grid(row=0, column=0, padx=(0, 20))
        ttk.Radiobutton(format_frame, text="十进制", variable=self.data_format_var, value="DEC").grid(row=0, column=1)
        
        # 控制按钮
        button_frame = ttk.Frame(settings_frame)
        button_frame.grid(row=16, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="发送", command=self.send_modbus, style="Accent.TButton").grid(row=0, column=0, padx=2)
        ttk.Button(button_frame, text="清空", command=self.clear_data).grid(row=0, column=1, padx=2)
        

        
    def create_modbus_data_area(self):
        """创建右侧数据显示区域"""
        # 数据区域框架
        data_frame = ttk.Frame(self.modbus_frame)
        data_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        data_frame.columnconfigure(0, weight=1)
        data_frame.rowconfigure(0, weight=1)
        data_frame.rowconfigure(1, weight=1)
        
        # 原始数据区域
        raw_data_frame = ttk.LabelFrame(data_frame, text="原始数据", padding="5")
        raw_data_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 5))
        raw_data_frame.columnconfigure(0, weight=1)
        raw_data_frame.rowconfigure(0, weight=1)
        
        # 原始数据文本框
        self.raw_data_text = tk.Text(raw_data_frame, height=15, width=50, font=("Consolas", 9))
        raw_data_scrollbar = ttk.Scrollbar(raw_data_frame, orient="vertical", command=self.raw_data_text.yview)
        self.raw_data_text.configure(yscrollcommand=raw_data_scrollbar.set)
        
        self.raw_data_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        raw_data_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 解码数据区域
        decode_data_frame = ttk.LabelFrame(data_frame, text="解码数据", padding="5")
        decode_data_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        decode_data_frame.columnconfigure(0, weight=1)
        decode_data_frame.rowconfigure(0, weight=1)
        
        # 解码数据文本框
        self.decode_data_text = tk.Text(decode_data_frame, height=10, width=50, font=("Consolas", 9))
        decode_data_scrollbar = ttk.Scrollbar(decode_data_frame, orient="vertical", command=self.decode_data_text.yview)
        self.decode_data_text.configure(yscrollcommand=decode_data_scrollbar.set)
        
        self.decode_data_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        decode_data_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
    def create_27930_interface(self):
        """创建27930测试界面"""
        # 配置27930页面的网格权重
        self.test_27930_frame.columnconfigure(1, weight=1)
        self.test_27930_frame.rowconfigure(0, weight=1)
        
        # 左侧设置区域
        self.create_27930_settings()
        
        # 右侧数据显示区域
        self.create_27930_data_area()
        
    def create_27930_settings(self):
        """创建左侧27930设置区域"""
        # 设置区域框架
        settings_frame = ttk.LabelFrame(self.test_27930_frame, text="CAN接口设置", padding="10")
        settings_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # CAN设备选择
        ttk.Label(settings_frame, text="CAN设备:").grid(row=0, column=0, sticky=tk.W, pady=2)
        can_device_frame = ttk.Frame(settings_frame)
        can_device_frame.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        self.can_device_var = tk.StringVar()
        self.can_device_combo = ttk.Combobox(can_device_frame, textvariable=self.can_device_var, 
                                            width=15, state="readonly")
        self.can_device_combo.grid(row=0, column=0, padx=(0, 2))
        
        ttk.Button(can_device_frame, text="刷新", command=self.refresh_can_devices, width=6).grid(row=0, column=1, padx=(2, 0))
        
        # CAN设备状态图标
        self.can_status_label = tk.Label(can_device_frame, text="ℹ", font=("Arial", 12), fg="black", cursor="hand2")
        self.can_status_label.grid(row=0, column=2, padx=(5, 0))
        self.can_status_label.bind("<Enter>", self.show_can_info_tooltip)
        self.can_status_label.bind("<Leave>", self.hide_can_info_tooltip)
        
        # 初始化CAN设备列表
        self.refresh_can_devices()
        
        # CAN波特率设置
        ttk.Label(settings_frame, text="CAN波特率:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.can_baud_rate_var = tk.StringVar(value="500000")
        can_baud_rate_combo = ttk.Combobox(settings_frame, textvariable=self.can_baud_rate_var,
                                          values=["125000", "250000", "500000", "1000000"],
                                          width=15, state="readonly")
        can_baud_rate_combo.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        # CAN通道设置
        ttk.Label(settings_frame, text="CAN通道:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.can_channel_var = tk.StringVar(value="0")
        can_channel_combo = ttk.Combobox(settings_frame, textvariable=self.can_channel_var,
                                        values=["0", "1"], width=15, state="readonly")
        can_channel_combo.grid(row=2, column=1, sticky=tk.W, pady=2)
        
        # CAN开关按钮
        self.can_status = False  # CAN状态：False=关闭，True=打开
        self.can_button = ttk.Button(settings_frame, text="打开", command=self.toggle_can, style="Accent.TButton", width=8)
        self.can_button.grid(row=3, column=0, columnspan=2, pady=5)
        
        # 分隔线
        separator1 = ttk.Separator(settings_frame, orient='horizontal')
        separator1.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # 27930功能设置
        ttk.Label(settings_frame, text="27930功能:", font=("Arial", 10, "bold")).grid(row=5, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))
        
        # 消息类型选择
        ttk.Label(settings_frame, text="消息类型:").grid(row=6, column=0, sticky=tk.W, pady=2)
        self.message_type_var = tk.StringVar(value="充电握手")
        message_type_combo = ttk.Combobox(settings_frame, textvariable=self.message_type_var,
                                         values=["充电握手", "充电参数配置", "充电状态", "充电统计", "充电停止", "自定义消息"],
                                         width=15, state="readonly")
        message_type_combo.grid(row=6, column=1, sticky=tk.W, pady=2)
        
        # 发送方地址
        ttk.Label(settings_frame, text="发送方地址:").grid(row=7, column=0, sticky=tk.W, pady=2)
        sender_address_frame = ttk.Frame(settings_frame)
        sender_address_frame.grid(row=7, column=1, sticky=tk.W, pady=2)
        
        self.sender_address_var = tk.StringVar(value="01")
        sender_address_entry = ttk.Entry(sender_address_frame, textvariable=self.sender_address_var, width=8)
        sender_address_entry.grid(row=0, column=0, padx=(0, 2))
        
        self.sender_address_base_var = tk.StringVar(value="HEX")
        sender_address_base_combo = ttk.Combobox(sender_address_frame, textvariable=self.sender_address_base_var,
                                                values=["DEC", "HEX"], width=4, state="readonly")
        sender_address_base_combo.grid(row=0, column=1)
        
        # 接收方地址
        ttk.Label(settings_frame, text="接收方地址:").grid(row=8, column=0, sticky=tk.W, pady=2)
        receiver_address_frame = ttk.Frame(settings_frame)
        receiver_address_frame.grid(row=8, column=1, sticky=tk.W, pady=2)
        
        self.receiver_address_var = tk.StringVar(value="02")
        receiver_address_entry = ttk.Entry(receiver_address_frame, textvariable=self.receiver_address_var, width=8)
        receiver_address_entry.grid(row=0, column=0, padx=(0, 2))
        
        self.receiver_address_base_var = tk.StringVar(value="HEX")
        receiver_address_base_combo = ttk.Combobox(receiver_address_frame, textvariable=self.receiver_address_base_var,
                                                  values=["DEC", "HEX"], width=4, state="readonly")
        receiver_address_base_combo.grid(row=0, column=1)
        
        # 扫描设置
        ttk.Label(settings_frame, text="扫描:").grid(row=9, column=0, sticky=tk.W, pady=2)
        scan_rate_frame = ttk.Frame(settings_frame)
        scan_rate_frame.grid(row=9, column=1, sticky=tk.W, pady=2)
        
        self.can_scan_rate_var = tk.StringVar(value="1000")
        can_scan_rate_entry = ttk.Entry(scan_rate_frame, textvariable=self.can_scan_rate_var, width=8)
        can_scan_rate_entry.grid(row=0, column=0, padx=(0, 5))
        
        ttk.Label(scan_rate_frame, text="ms").grid(row=0, column=1)
        
        # 扫描按钮
        self.can_scan_button = ttk.Button(scan_rate_frame, text="开始", command=self.toggle_can_scan, style="Accent.TButton", width=6)
        self.can_scan_button.grid(row=0, column=2, padx=(10, 0))
        
        # 定时器状态
        self.can_scan_timer = None
        self.can_scanning = False
        
        # 分隔线
        separator2 = ttk.Separator(settings_frame, orient='horizontal')
        separator2.grid(row=10, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # 数据显示设置
        ttk.Label(settings_frame, text="显示设置:", font=("Arial", 10, "bold")).grid(row=11, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))
        
        # 数据显示格式
        self.can_data_format_var = tk.StringVar(value="HEX")
        can_format_frame = ttk.Frame(settings_frame)
        can_format_frame.grid(row=12, column=0, columnspan=3, sticky=tk.W, pady=1)
        ttk.Radiobutton(can_format_frame, text="十六进制", variable=self.can_data_format_var, value="HEX").grid(row=0, column=0, padx=(0, 20))
        ttk.Radiobutton(can_format_frame, text="十进制", variable=self.can_data_format_var, value="DEC").grid(row=0, column=1)
        
        # 控制按钮
        button_frame = ttk.Frame(settings_frame)
        button_frame.grid(row=13, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="发送", command=self.send_27930, style="Accent.TButton").grid(row=0, column=0, padx=2)
        ttk.Button(button_frame, text="清空", command=self.clear_27930_data).grid(row=0, column=1, padx=2)
        
    def create_27930_data_area(self):
        """创建右侧27930数据显示区域"""
        # 数据区域框架
        data_frame = ttk.Frame(self.test_27930_frame)
        data_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        data_frame.columnconfigure(0, weight=1)
        data_frame.rowconfigure(0, weight=1)
        data_frame.rowconfigure(1, weight=1)
        
        # 原始数据区域
        raw_data_frame = ttk.LabelFrame(data_frame, text="原始数据", padding="5")
        raw_data_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 5))
        raw_data_frame.columnconfigure(0, weight=1)
        raw_data_frame.rowconfigure(0, weight=1)
        
        # 原始数据文本框
        self.can_raw_data_text = tk.Text(raw_data_frame, height=15, width=50, font=("Consolas", 9))
        can_raw_data_scrollbar = ttk.Scrollbar(raw_data_frame, orient="vertical", command=self.can_raw_data_text.yview)
        self.can_raw_data_text.configure(yscrollcommand=can_raw_data_scrollbar.set)
        
        self.can_raw_data_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        can_raw_data_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 数据解析区域
        parse_data_frame = ttk.LabelFrame(data_frame, text="数据解析", padding="5")
        parse_data_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        parse_data_frame.columnconfigure(0, weight=1)
        parse_data_frame.rowconfigure(0, weight=1)
        
        # 数据解析文本框
        self.can_parse_data_text = tk.Text(parse_data_frame, height=10, width=50, font=("Consolas", 9))
        can_parse_data_scrollbar = ttk.Scrollbar(parse_data_frame, orient="vertical", command=self.can_parse_data_text.yview)
        self.can_parse_data_text.configure(yscrollcommand=can_parse_data_scrollbar.set)
        
        self.can_parse_data_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        can_parse_data_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
    def apply_modern_style(self):
        """应用现代化样式"""
        style = ttk.Style()
        
        # 配置主题
        style.theme_use('clam')
        
        # 自定义按钮样式
        style.configure("Accent.TButton", 
                       background="#0078d4", 
                       foreground="white",
                       font=("Arial", 10, "bold"))
        
        # 配置标签框样式
        style.configure("TLabelframe", 
                       background="#f0f0f0",
                       relief="solid",
                       borderwidth=1)
        
        # 配置标签样式
        style.configure("TLabel", 
                       background="#ffffff",
                       font=("Arial", 10))
        
    def modbus_test(self):
        """Modbus测试功能"""
        # 选中Modbus测试Tab页面
        self.notebook.select(0)  # 选择第一个Tab（Modbus测试）
        
    def test_27930(self):
        """27930测试功能"""
        # 选中27930测试Tab页面
        self.notebook.select(1)  # 选择第二个Tab（27930测试）
        
    # Modbus相关方法
    def open_serial(self):
        """打开串口"""
        try:
            # 这里应该实现实际的串口打开逻辑
            # 目前只是模拟
            port = self.com_port_var.get()
            baud = int(self.baud_rate_var.get())
            self.add_raw_data(f"[{self.get_timestamp()}] 串口 {port} 已打开，波特率: {baud}")
            # 更新串口状态和按钮文本
            self.serial_status = True
            self.serial_button.config(text="关闭", style="TButton")
        except Exception as e:
            messagebox.showerror("错误", f"打开串口失败: {str(e)}")
            
    def toggle_serial(self):
        """串口开关切换"""
        if not self.serial_status:
            # 当前串口关闭，执行打开操作
            self.open_serial()
        else:
            # 当前串口打开，执行关闭操作
            self.close_serial()
            
    def toggle_scan(self):
        """扫描开关切换"""
        if not self.scanning:
            # 当前扫描停止，执行开始扫描操作
            self.start_scan()
        else:
            # 当前扫描进行中，执行停止扫描操作
            self.stop_scan()
            
    def start_scan(self):
        """开始定时扫描"""
        if not self.serial_status:
            messagebox.showwarning("警告", "请先打开串口")
            return
            
        try:
            scan_rate = int(self.scan_rate_var.get())
            if scan_rate < 100:
                messagebox.showwarning("警告", "扫描间隔不能小于100ms")
                return
                
            self.scanning = True
            self.scan_timer = self.root.after(scan_rate, self.scan_modbus)
            self.scan_button.config(text="停止", style="TButton")
            self.add_raw_data(f"[{self.get_timestamp()}] 开始定时扫描，间隔: {scan_rate}ms")
        except ValueError:
            messagebox.showerror("错误", "请输入有效的扫描间隔")
            
    def stop_scan(self):
        """停止定时扫描"""
        if self.scan_timer:
            self.root.after_cancel(self.scan_timer)
            self.scan_timer = None
        self.scanning = False
        self.scan_button.config(text="开始", style="Accent.TButton")
        self.add_raw_data(f"[{self.get_timestamp()}] 停止定时扫描")
        
    def scan_modbus(self):
        """执行一次Modbus扫描"""
        if self.scanning and self.serial_status:
            # 执行一次Modbus通讯
            self.send_modbus()
            
            # 设置下一次扫描
            try:
                scan_rate = int(self.scan_rate_var.get())
                self.scan_timer = self.root.after(scan_rate, self.scan_modbus)
            except ValueError:
                self.stop_scan()
                messagebox.showerror("错误", "扫描间隔设置无效，已停止扫描")
            
    def close_serial(self):
        """关闭串口"""
        try:
            # 这里应该实现实际的串口关闭逻辑
            self.add_raw_data(f"[{self.get_timestamp()}] 串口已关闭")
            # 更新串口状态和按钮文本
            self.serial_status = False
            self.serial_button.config(text="打开", style="Accent.TButton")
        except Exception as e:
            messagebox.showerror("错误", f"关闭串口失败: {str(e)}")
            
    def send_modbus(self):
        """发送Modbus数据"""
        try:
            # 获取设置参数
            function_code = self.function_code_var.get().split(" - ")[0]
            
            # 解析从站地址（支持十进制和十六进制）
            slave_addr_str = self.slave_address_var.get().strip()
            if self.slave_address_base_var.get() == "HEX":
                if slave_addr_str.upper().startswith('0X'):
                    slave_addr = int(slave_addr_str, 16)
                else:
                    slave_addr = int(slave_addr_str, 16)
            else:
                slave_addr = int(slave_addr_str)
                
            # 解析寄存器地址（支持十进制和十六进制）
            reg_addr_str = self.register_address_var.get().strip()
            if self.register_address_base_var.get() == "HEX":
                if reg_addr_str.upper().startswith('0X'):
                    reg_addr = int(reg_addr_str, 16)
                else:
                    reg_addr = int(reg_addr_str, 16)
            else:
                reg_addr = int(reg_addr_str)
                
            # 解析寄存器数量（支持十进制和十六进制）
            reg_count_str = self.register_count_var.get().strip()
            if self.register_count_base_var.get() == "HEX":
                if reg_count_str.upper().startswith('0X'):
                    reg_count = int(reg_count_str, 16)
                else:
                    reg_count = int(reg_count_str, 16)
            else:
                reg_count = int(reg_count_str)
            
            # 构建Modbus请求帧
            if function_code in ["01", "02", "03", "04"]:
                # 读操作
                # 构建数据包（不包含CRC）
                request_data = [slave_addr, int(function_code), reg_addr >> 8, reg_addr & 0xFF, reg_count >> 8, reg_count & 0xFF]
                
                # 计算CRC
                crc = self.calculate_crc16(request_data)
                crc_low = crc & 0xFF
                crc_high = (crc >> 8) & 0xFF
                
                # 添加CRC到数据包
                request_data.extend([crc_low, crc_high])
                
                # 转换为十六进制字符串显示
                request_hex = " ".join([f"{b:02X}" for b in request_data])
                
                self.add_raw_data(f"[{self.get_timestamp()}] 发送: {request_hex}")
                self.add_decode_data(f"[{self.get_timestamp()}] 发送: 从站{slave_addr}, 功能码{function_code}, 地址{reg_addr}, 数量{reg_count} - CRC:低{crc_low:02X},高{crc_high:02X}")
                
                # 模拟接收响应
                self.simulate_response(slave_addr, function_code, reg_count)
                
            else:
                # 写操作（简化处理）
                self.add_raw_data(f"[{self.get_timestamp()}] 发送写命令: 功能码{function_code}")
                self.add_decode_data(f"[{self.get_timestamp()}] 发送Modbus写命令: 从站{slave_addr}, 功能码{function_code}")
                
        except ValueError as e:
            messagebox.showerror("错误", f"参数错误: {str(e)}")
        except Exception as e:
            messagebox.showerror("错误", f"发送失败: {str(e)}")
            
    def simulate_response(self, slave_addr, function_code, reg_count):
        """模拟Modbus响应"""
        import random
        import time
        
        # 模拟延迟
        time.sleep(0.1)
        
        # 生成模拟数据
        if function_code in ["01", "02"]:
            # 线圈/离散输入
            data_bytes = reg_count
            # 生成随机线圈状态数据
            coil_data = []
            for _ in range(reg_count):
                coil_data.append(random.randint(0, 1))
            
            # 构建响应数据包（不包含CRC）
            response_data = [slave_addr, int(function_code), data_bytes]
            
            # 添加线圈数据
            for coil in coil_data:
                response_data.append(coil)
                
        else:
            # 寄存器
            data_bytes = reg_count * 2
            # 生成随机寄存器数据
            register_data = []
            for _ in range(reg_count):
                register_value = random.randint(0, 65535)
                register_data.append(register_value >> 8)  # 高字节
                register_data.append(register_value & 0xFF)  # 低字节
            
            # 构建响应数据包（不包含CRC）
            response_data = [slave_addr, int(function_code), data_bytes]
            
            # 添加寄存器数据
            response_data.extend(register_data)
        
        # 计算CRC
        crc = self.calculate_crc16(response_data)
        crc_low = crc & 0xFF
        crc_high = (crc >> 8) & 0xFF
        
        # 添加CRC到响应数据包
        response_data.extend([crc_low, crc_high])
        
        # 转换为十六进制字符串显示
        response_hex = " ".join([f"{b:02X}" for b in response_data])
        
        self.add_raw_data(f"[{self.get_timestamp()}] 接收: {response_hex}")
        
        # 验证CRC并合并显示
        crc_result = self.verify_crc_silent(response_data)
        if crc_result:
            self.add_decode_data(f"[{self.get_timestamp()}] 响应: 从站{slave_addr}, 功能码{function_code}, 数据{data_bytes}字节 - CRC:低{crc_low:02X},高{crc_high:02X} - 成功")
        else:
            # 获取接收到的CRC值用于错误显示
            received_crc_low = response_data[-2]
            received_crc_high = response_data[-1]
            received_crc = (received_crc_high << 8) | received_crc_low
            self.add_decode_data(f"[{self.get_timestamp()}] 响应: 从站{slave_addr}, 功能码{function_code}, 数据{data_bytes}字节 - CRC:低{crc_low:02X},高{crc_high:02X} - CRC错误({received_crc:04X})")
        

        
    def on_slave_address_base_change(self, event=None):
        """从站地址进制改变事件"""
        try:
            current_value = self.slave_address_var.get().strip()
            if not current_value:
                return
                
            current_base = self.slave_address_base_var.get()
            
            if current_base == "DEC":
                # 当前是十进制，转换为十进制显示
                try:
                    # 尝试解析为十六进制
                    if current_value.upper().startswith('0X'):
                        value = int(current_value, 16)
                    else:
                        value = int(current_value, 16)
                    self.slave_address_var.set(str(value))
                except ValueError:
                    pass
            else:
                # 当前是十六进制，转换为十六进制显示
                try:
                    value = int(current_value)
                    self.slave_address_var.set(f"{value:02X}")
                except ValueError:
                    pass
        except Exception as e:
            pass
            
    def on_register_address_base_change(self, event=None):
        """寄存器地址进制改变事件"""
        try:
            current_value = self.register_address_var.get().strip()
            if not current_value:
                return
                
            current_base = self.register_address_base_var.get()
            
            if current_base == "DEC":
                # 当前是十进制，转换为十进制显示
                try:
                    # 尝试解析为十六进制
                    if current_value.upper().startswith('0X'):
                        value = int(current_value, 16)
                    else:
                        value = int(current_value, 16)
                    self.register_address_var.set(str(value))
                except ValueError:
                    pass
            else:
                # 当前是十六进制，转换为十六进制显示
                try:
                    value = int(current_value)
                    self.register_address_var.set(f"{value:04X}")
                except ValueError:
                    pass
        except Exception as e:
            pass
            
    def on_register_count_base_change(self, event=None):
        """寄存器数量进制改变事件"""
        try:
            current_value = self.register_count_var.get().strip()
            if not current_value:
                return
                
            current_base = self.register_count_base_var.get()
            
            if current_base == "DEC":
                # 当前是十进制，转换为十进制显示
                try:
                    # 尝试解析为十六进制
                    if current_value.upper().startswith('0X'):
                        value = int(current_value, 16)
                    else:
                        value = int(current_value, 16)
                    self.register_count_var.set(str(value))
                except ValueError:
                    pass
            else:
                # 当前是十六进制，转换为十六进制显示
                try:
                    value = int(current_value)
                    self.register_count_var.set(f"{value:04X}")
                except ValueError:
                    pass
        except Exception as e:
            pass
        
    def show_com_info_tooltip(self, event=None):
        """显示串口信息工具提示"""
        if hasattr(self, 'com_ports_info') and self.com_ports_info:
            # 创建工具提示窗口
            tooltip = tk.Toplevel(self.root)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            # 设置工具提示样式
            tooltip.configure(bg='lightyellow', relief='solid', borderwidth=1)
            
            # 创建标签显示信息
            label = tk.Label(tooltip, text=self.com_ports_info, 
                           bg='lightyellow', fg='black', 
                           font=("Arial", 9), justify=tk.LEFT)
            label.pack(padx=5, pady=5)
            
            # 保存工具提示引用
            self.tooltip = tooltip
            
            # 绑定鼠标离开事件
            self.com_status_label.bind("<Leave>", self.hide_com_info_tooltip)
            
    def hide_com_info_tooltip(self, event=None):
        """隐藏串口信息工具提示"""
        if hasattr(self, 'tooltip'):
            self.tooltip.destroy()
            delattr(self, 'tooltip')
        
    def refresh_com_ports(self):
        """刷新串口列表"""
        try:
            # 获取所有可用串口
            ports = list(serial.tools.list_ports.comports())
            
            if not ports:
                # 如果没有检测到串口，显示默认列表
                port_list = ["COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8"]
                self.com_port_combo['values'] = port_list
                if not self.com_port_var.get():
                    self.com_port_var.set("COM1")
                
                # 更新图标状态 - 红色表示没有可用串口
                self.com_status_label.config(fg="red")
                self.com_ports_info = "未检测到可用串口\n请检查串口设备连接\n或手动选择串口号"
            else:
                # 更新串口列表
                port_list = [port.device for port in ports]
                self.com_port_combo['values'] = port_list
                
                # 如果当前选择的串口不在列表中，选择第一个
                if self.com_port_var.get() not in port_list:
                    self.com_port_var.set(port_list[0] if port_list else "")
                
                # 更新图标状态 - 黑色表示有可用串口
                self.com_status_label.config(fg="black")
                self.com_ports_info = ""
                    
        except Exception as e:
            # 如果pyserial不可用，使用默认列表
            port_list = ["COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8"]
            self.com_port_combo['values'] = port_list
            if not self.com_port_var.get():
                self.com_port_var.set("COM1")
            
            # 更新图标状态 - 红色表示检测功能不可用
            self.com_status_label.config(fg="red")
            self.com_ports_info = f"串口检测功能不可用\n请手动选择串口号\n错误: {str(e)}"
        
    def verify_crc_silent(self, data):
        """验证CRC校验码（静默模式，只返回结果）"""
        if len(data) < 3:  # 至少需要从站地址、功能码和CRC（2字节）
            return False
            
        # 提取数据部分（不包括CRC）
        data_without_crc = data[:-2]
        received_crc_low = data[-2]
        received_crc_high = data[-1]
        received_crc = (received_crc_high << 8) | received_crc_low
        
        # 计算数据部分的CRC
        calculated_crc = self.calculate_crc16(data_without_crc)
        
        return calculated_crc == received_crc
        
    def verify_crc(self, data):
        """验证CRC校验码"""
        if len(data) < 3:  # 至少需要从站地址、功能码和CRC（2字节）
            self.add_decode_data(f"[{self.get_timestamp()}] CRC验证失败: 数据长度不足")
            return False
            
        # 提取数据部分（不包括CRC）
        data_without_crc = data[:-2]
        received_crc_low = data[-2]
        received_crc_high = data[-1]
        received_crc = (received_crc_high << 8) | received_crc_low
        
        # 计算数据部分的CRC
        calculated_crc = self.calculate_crc16(data_without_crc)
        
        if calculated_crc == received_crc:
            self.add_decode_data(f"[{self.get_timestamp()}] CRC验证成功: 接收CRC {received_crc:04X} = 计算CRC {calculated_crc:04X}")
            return True
        else:
            self.add_decode_data(f"[{self.get_timestamp()}] CRC验证失败: 接收CRC {received_crc:04X} ≠ 计算CRC {calculated_crc:04X}")
            return False
        
    def calculate_crc16(self, data):
        """计算CRC16校验码（Modbus标准）"""
        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x0001:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc = crc >> 1
        return crc
    
    def calculate_crc(self, data):
        """计算CRC校验码（兼容旧接口）"""
        # 将十六进制字符串转换为字节列表
        data_bytes = []
        for i in range(0, len(data), 2):
            if i + 1 < len(data):
                data_bytes.append(int(data[i:i+2], 16))
        
        return self.calculate_crc16(data_bytes)
        
    def clear_data(self):
        """清空数据显示"""
        self.raw_data_text.delete(1.0, tk.END)
        self.decode_data_text.delete(1.0, tk.END)
        
    def add_raw_data(self, data):
        """添加原始数据"""
        self.raw_data_text.insert(tk.END, data + "\n")
        self.raw_data_text.see(tk.END)
        
    def add_decode_data(self, data):
        """添加解码数据"""
        self.decode_data_text.insert(tk.END, data + "\n")
        self.decode_data_text.see(tk.END)
        
    def get_timestamp(self):
        """获取时间戳"""
        import datetime
        return datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
    def show_about(self):
        """显示关于信息"""
        about_text = """工控测试软件 v1.0

功能特性：
• 可调整大小的现代化界面
• Modbus测试功能
• 27930测试功能
• Modbus解析对码功能
• 响应式设计

开发者：lyxer123
创建时间：2025年"""
        
        messagebox.showinfo("关于本软件", about_text)
        
    def on_window_resize(self, event):
        """窗口大小改变事件处理"""
        # 窗口大小改变时不做任何处理，因为已删除状态栏
        pass
    
    # 27930相关方法
    def refresh_can_devices(self):
        """刷新CAN设备列表"""
        try:
            # 模拟CAN设备列表（实际应用中应该检测真实的CAN设备）
            can_devices = ["CAN1", "CAN2", "USB-CAN", "PCI-CAN"]
            self.can_device_combo['values'] = can_devices
            if not self.can_device_var.get():
                self.can_device_var.set("CAN1")
            
            # 更新图标状态 - 黑色表示有可用设备
            self.can_status_label.config(fg="black")
            self.can_devices_info = "检测到CAN设备\n请选择设备并设置参数"
        except Exception as e:
            # 如果检测失败，使用默认列表
            can_devices = ["CAN1", "CAN2", "USB-CAN", "PCI-CAN"]
            self.can_device_combo['values'] = can_devices
            if not self.can_device_var.get():
                self.can_device_var.set("CAN1")
            
            # 更新图标状态 - 红色表示检测功能不可用
            self.can_status_label.config(fg="red")
            self.can_devices_info = f"CAN设备检测功能不可用\n请手动选择设备\n错误: {str(e)}"
    
    def show_can_info_tooltip(self, event=None):
        """显示CAN设备信息工具提示"""
        if hasattr(self, 'can_devices_info') and self.can_devices_info:
            # 创建工具提示窗口
            tooltip = tk.Toplevel(self.root)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            # 设置工具提示样式
            tooltip.configure(bg='lightyellow', relief='solid', borderwidth=1)
            
            # 创建标签显示信息
            label = tk.Label(tooltip, text=self.can_devices_info, 
                           bg='lightyellow', fg='black', 
                           font=("Arial", 9), justify=tk.LEFT)
            label.pack(padx=5, pady=5)
            
            # 保存工具提示引用
            self.can_tooltip = tooltip
            
            # 绑定鼠标离开事件
            self.can_status_label.bind("<Leave>", self.hide_can_info_tooltip)
    
    def hide_can_info_tooltip(self, event=None):
        """隐藏CAN设备信息工具提示"""
        if hasattr(self, 'can_tooltip'):
            self.can_tooltip.destroy()
            delattr(self, 'can_tooltip')
    
    def toggle_can(self):
        """CAN开关切换"""
        if not self.can_status:
            # 当前CAN关闭，执行打开操作
            self.open_can()
        else:
            # 当前CAN打开，执行关闭操作
            self.close_can()
    
    def open_can(self):
        """打开CAN设备"""
        try:
            # 这里应该实现实际的CAN打开逻辑
            # 目前只是模拟
            device = self.can_device_var.get()
            baud = int(self.can_baud_rate_var.get())
            channel = int(self.can_channel_var.get())
            self.add_can_raw_data(f"[{self.get_timestamp()}] CAN设备 {device} 已打开，波特率: {baud}, 通道: {channel}")
            # 更新CAN状态和按钮文本
            self.can_status = True
            self.can_button.config(text="关闭", style="TButton")
        except Exception as e:
            messagebox.showerror("错误", f"打开CAN设备失败: {str(e)}")
    
    def close_can(self):
        """关闭CAN设备"""
        try:
            # 这里应该实现实际的CAN关闭逻辑
            self.add_can_raw_data(f"[{self.get_timestamp()}] CAN设备已关闭")
            # 更新CAN状态和按钮文本
            self.can_status = False
            self.can_button.config(text="打开", style="Accent.TButton")
        except Exception as e:
            messagebox.showerror("错误", f"关闭CAN设备失败: {str(e)}")
    
    def toggle_can_scan(self):
        """CAN扫描开关切换"""
        if not self.can_scanning:
            # 当前扫描停止，执行开始扫描操作
            self.start_can_scan()
        else:
            # 当前扫描进行中，执行停止扫描操作
            self.stop_can_scan()
    
    def start_can_scan(self):
        """开始定时CAN扫描"""
        if not self.can_status:
            messagebox.showwarning("警告", "请先打开CAN设备")
            return
        
        try:
            scan_rate = int(self.can_scan_rate_var.get())
            if scan_rate < 100:
                messagebox.showwarning("警告", "扫描间隔不能小于100ms")
                return
            
            self.can_scanning = True
            self.can_scan_timer = self.root.after(scan_rate, self.scan_27930)
            self.can_scan_button.config(text="停止", style="TButton")
            self.add_can_raw_data(f"[{self.get_timestamp()}] 开始定时CAN扫描，间隔: {scan_rate}ms")
        except ValueError:
            messagebox.showerror("错误", "请输入有效的扫描间隔")
    
    def stop_can_scan(self):
        """停止定时CAN扫描"""
        if self.can_scan_timer:
            self.root.after_cancel(self.can_scan_timer)
            self.can_scan_timer = None
        self.can_scanning = False
        self.can_scan_button.config(text="开始", style="Accent.TButton")
        self.add_can_raw_data(f"[{self.get_timestamp()}] 停止定时CAN扫描")
    
    def scan_27930(self):
        """执行一次27930扫描"""
        if self.can_scanning and self.can_status:
            # 执行一次27930通讯
            self.send_27930()
            
            # 设置下一次扫描
            try:
                scan_rate = int(self.can_scan_rate_var.get())
                self.can_scan_timer = self.root.after(scan_rate, self.scan_27930)
            except ValueError:
                self.stop_can_scan()
                messagebox.showerror("错误", "扫描间隔设置无效，已停止扫描")
    
    def send_27930(self):
        """发送27930数据"""
        try:
            # 获取设置参数
            message_type = self.message_type_var.get()
            
            # 解析发送方地址
            sender_addr_str = self.sender_address_var.get().strip()
            if self.sender_address_base_var.get() == "HEX":
                if sender_addr_str.upper().startswith('0X'):
                    sender_addr = int(sender_addr_str, 16)
                else:
                    sender_addr = int(sender_addr_str, 16)
            else:
                sender_addr = int(sender_addr_str)
            
            # 解析接收方地址
            receiver_addr_str = self.receiver_address_var.get().strip()
            if self.receiver_address_base_var.get() == "HEX":
                if receiver_addr_str.upper().startswith('0X'):
                    receiver_addr = int(receiver_addr_str, 16)
                else:
                    receiver_addr = int(receiver_addr_str, 16)
            else:
                receiver_addr = int(receiver_addr_str)
            
            # 根据消息类型构建27930数据包
            if message_type == "充电握手":
                # 充电握手消息
                can_id = 0x1801F456  # 示例CAN ID
                data = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]
                message_info = f"充电握手 - 发送方:{sender_addr:02X}, 接收方:{receiver_addr:02X}"
                
            elif message_type == "充电参数配置":
                # 充电参数配置消息
                can_id = 0x1802F456
                data = [0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80]
                message_info = f"充电参数配置 - 发送方:{sender_addr:02X}, 接收方:{receiver_addr:02X}"
                
            elif message_type == "充电状态":
                # 充电状态消息
                can_id = 0x1803F456
                data = [0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0x11, 0x22]
                message_info = f"充电状态 - 发送方:{sender_addr:02X}, 接收方:{receiver_addr:02X}"
                
            elif message_type == "充电统计":
                # 充电统计消息
                can_id = 0x1804F456
                data = [0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0xAA]
                message_info = f"充电统计 - 发送方:{sender_addr:02X}, 接收方:{receiver_addr:02X}"
                
            elif message_type == "充电停止":
                # 充电停止消息
                can_id = 0x1805F456
                data = [0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0x00, 0x11, 0x22]
                message_info = f"充电停止 - 发送方:{sender_addr:02X}, 接收方:{receiver_addr:02X}"
                
            else:
                # 自定义消息
                can_id = 0x1800F456
                data = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
                message_info = f"自定义消息 - 发送方:{sender_addr:02X}, 接收方:{receiver_addr:02X}"
            
            # 构建CAN数据包
            can_data = [can_id >> 24, (can_id >> 16) & 0xFF, (can_id >> 8) & 0xFF, can_id & 0xFF] + data
            
            # 转换为十六进制字符串显示
            can_hex = " ".join([f"{b:02X}" for b in can_data])
            
            self.add_can_raw_data(f"[{self.get_timestamp()}] 发送: {can_hex}")
            self.add_can_parse_data(f"[{self.get_timestamp()}] {message_info}")
            self.add_can_parse_data(f"  CAN ID: {can_id:08X}")
            self.add_can_parse_data(f"  数据: {' '.join([f'{d:02X}' for d in data])}")
            
            # 模拟接收响应
            self.simulate_27930_response(can_id, data, message_type)
            
        except ValueError as e:
            messagebox.showerror("错误", f"参数错误: {str(e)}")
        except Exception as e:
            messagebox.showerror("错误", f"发送失败: {str(e)}")
    
    def simulate_27930_response(self, can_id, data, message_type):
        """模拟27930响应"""
        import random
        import time
        
        # 模拟延迟
        time.sleep(0.1)
        
        # 生成响应数据
        response_data = []
        for _ in range(8):
            response_data.append(random.randint(0, 255))
        
        # 构建响应CAN数据包
        response_can_data = [can_id >> 24, (can_id >> 16) & 0xFF, (can_id >> 8) & 0xFF, can_id & 0xFF] + response_data
        
        # 转换为十六进制字符串显示
        response_hex = " ".join([f"{b:02X}" for b in response_can_data])
        
        self.add_can_raw_data(f"[{self.get_timestamp()}] 接收: {response_hex}")
        
        # 解析响应数据
        self.add_can_parse_data(f"[{self.get_timestamp()}] 响应: {message_type}")
        self.add_can_parse_data(f"  CAN ID: {can_id:08X}")
        self.add_can_parse_data(f"  响应数据: {' '.join([f'{d:02X}' for d in response_data])}")
    
    def clear_27930_data(self):
        """清空27930数据显示"""
        self.can_raw_data_text.delete(1.0, tk.END)
        self.can_parse_data_text.delete(1.0, tk.END)
    
    def add_can_raw_data(self, data):
        """添加CAN原始数据"""
        self.can_raw_data_text.insert(tk.END, data + "\n")
        self.can_raw_data_text.see(tk.END)
    
    def add_can_parse_data(self, data):
        """添加CAN解析数据"""
        self.can_parse_data_text.insert(tk.END, data + "\n")
        self.can_parse_data_text.see(tk.END)
    
    def open_modbus_parser(self):
        """打开Modbus解析对码窗口"""
        parser_window = ModbusParserWindow(self.root)


def main():
    """主函数"""
    root = tk.Tk()
    app = ModernUI(root)
    
    # 设置窗口图标（可选）
    try:
        # 设置测试图标
        root.iconbitmap('test_icon.ico')
    except:
        # 如果没有图标文件，使用默认图标
        pass
    
    # 启动应用
    root.mainloop()

if __name__ == "__main__":
    main() 