import tkinter as tk
from tkinter import ttk, messagebox
import os

class ModernUI:
    def __init__(self, root):
        self.root = root
        self.root.title("测试应用")
        
        # 设置窗口默认大小为显示器窗口的一半
        self.setup_window_size()
        
        # 创建菜单栏
        self.create_menu()
        
        # 创建主界面
        self.create_main_interface()
        
        # 绑定窗口大小改变事件
        self.root.bind('<Configure>', self.on_window_resize)
        
    def setup_window_size(self):
        """设置窗口默认大小为显示器窗口的一半"""
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
        self.root.minsize(400, 300)
        
    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 第一个菜单：测试
        test_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="测试", menu=test_menu)
        test_menu.add_command(label="modbus测试", command=self.modbus_test)
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
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
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
        self.com_port_var = tk.StringVar(value="COM1")
        com_port_combo = ttk.Combobox(settings_frame, textvariable=self.com_port_var, 
                                     values=["COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8"], 
                                     width=10, state="readonly")
        com_port_combo.grid(row=0, column=1, sticky=tk.W, pady=2)
        
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
        ttk.Label(settings_frame, text="停止位:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.stop_bits_var = tk.StringVar(value="1")
        stop_bits_combo = ttk.Combobox(settings_frame, textvariable=self.stop_bits_var,
                                      values=["1", "1.5", "2"], width=10, state="readonly")
        stop_bits_combo.grid(row=3, column=1, sticky=tk.W, pady=2)
        
        # 校验位设置
        ttk.Label(settings_frame, text="校验位:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.parity_var = tk.StringVar(value="无")
        parity_combo = ttk.Combobox(settings_frame, textvariable=self.parity_var,
                                   values=["无", "奇校验", "偶校验"], width=10, state="readonly")
        parity_combo.grid(row=4, column=1, sticky=tk.W, pady=2)
        
        # 分隔线
        separator1 = ttk.Separator(settings_frame, orient='horizontal')
        separator1.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Modbus功能设置
        ttk.Label(settings_frame, text="Modbus功能:", font=("Arial", 10, "bold")).grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        # 功能码选择
        ttk.Label(settings_frame, text="功能码:").grid(row=7, column=0, sticky=tk.W, pady=2)
        self.function_code_var = tk.StringVar(value="03 - 读保持寄存器")
        function_code_combo = ttk.Combobox(settings_frame, textvariable=self.function_code_var,
                                          values=["01 - 读线圈状态", "02 - 读离散输入", "03 - 读保持寄存器", 
                                                 "04 - 读输入寄存器", "05 - 写单个线圈", "06 - 写单个寄存器",
                                                 "15 - 写多个线圈", "16 - 写多个寄存器"], 
                                          width=15, state="readonly")
        function_code_combo.grid(row=7, column=1, sticky=tk.W, pady=2)
        
        # 从站地址
        ttk.Label(settings_frame, text="从站地址:").grid(row=8, column=0, sticky=tk.W, pady=2)
        self.slave_address_var = tk.StringVar(value="1")
        slave_address_entry = ttk.Entry(settings_frame, textvariable=self.slave_address_var, width=10)
        slave_address_entry.grid(row=8, column=1, sticky=tk.W, pady=2)
        
        # 寄存器地址
        ttk.Label(settings_frame, text="寄存器地址:").grid(row=9, column=0, sticky=tk.W, pady=2)
        self.register_address_var = tk.StringVar(value="0")
        register_address_entry = ttk.Entry(settings_frame, textvariable=self.register_address_var, width=10)
        register_address_entry.grid(row=9, column=1, sticky=tk.W, pady=2)
        
        # 寄存器数量
        ttk.Label(settings_frame, text="寄存器数量:").grid(row=10, column=0, sticky=tk.W, pady=2)
        self.register_count_var = tk.StringVar(value="1")
        register_count_entry = ttk.Entry(settings_frame, textvariable=self.register_count_var, width=10)
        register_count_entry.grid(row=10, column=1, sticky=tk.W, pady=2)
        
        # 分隔线
        separator2 = ttk.Separator(settings_frame, orient='horizontal')
        separator2.grid(row=11, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # 数据显示设置
        ttk.Label(settings_frame, text="显示设置:", font=("Arial", 10, "bold")).grid(row=12, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        # 数据显示格式
        self.data_format_var = tk.StringVar(value="HEX")
        ttk.Radiobutton(settings_frame, text="十六进制", variable=self.data_format_var, value="HEX").grid(row=13, column=0, columnspan=2, sticky=tk.W, pady=1)
        ttk.Radiobutton(settings_frame, text="十进制", variable=self.data_format_var, value="DEC").grid(row=14, column=0, columnspan=2, sticky=tk.W, pady=1)
        
        # 控制按钮
        button_frame = ttk.Frame(settings_frame)
        button_frame.grid(row=15, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="打开串口", command=self.open_serial, style="Accent.TButton").grid(row=0, column=0, padx=2)
        ttk.Button(button_frame, text="关闭串口", command=self.close_serial).grid(row=0, column=1, padx=2)
        
        ttk.Button(button_frame, text="发送", command=self.send_modbus, style="Accent.TButton").grid(row=1, column=0, padx=2, pady=5)
        ttk.Button(button_frame, text="清空", command=self.clear_data).grid(row=1, column=1, padx=2, pady=5)
        
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
        self.status_var.set("已切换到Modbus测试页面")
        
    def test_27930(self):
        """27930测试功能"""
        # 选中27930测试Tab页面
        self.notebook.select(1)  # 选择第二个Tab（27930测试）
        self.status_var.set("已切换到27930测试页面")
        
    # Modbus相关方法
    def open_serial(self):
        """打开串口"""
        try:
            # 这里应该实现实际的串口打开逻辑
            # 目前只是模拟
            port = self.com_port_var.get()
            baud = int(self.baud_rate_var.get())
            self.status_var.set(f"串口 {port} 已打开，波特率: {baud}")
            self.add_raw_data(f"[{self.get_timestamp()}] 串口 {port} 已打开，波特率: {baud}")
        except Exception as e:
            messagebox.showerror("错误", f"打开串口失败: {str(e)}")
            
    def close_serial(self):
        """关闭串口"""
        try:
            # 这里应该实现实际的串口关闭逻辑
            self.status_var.set("串口已关闭")
            self.add_raw_data(f"[{self.get_timestamp()}] 串口已关闭")
        except Exception as e:
            messagebox.showerror("错误", f"关闭串口失败: {str(e)}")
            
    def send_modbus(self):
        """发送Modbus数据"""
        try:
            # 获取设置参数
            function_code = self.function_code_var.get().split(" - ")[0]
            slave_addr = int(self.slave_address_var.get())
            reg_addr = int(self.register_address_var.get())
            reg_count = int(self.register_count_var.get())
            
            # 构建Modbus请求帧（简化版）
            if function_code in ["01", "02", "03", "04"]:
                # 读操作
                request = f"{slave_addr:02X} {function_code} {reg_addr:04X} {reg_count:04X}"
                crc = self.calculate_crc(request.replace(" ", ""))
                full_request = f"{request} {crc:04X}"
                
                self.add_raw_data(f"[{self.get_timestamp()}] 发送: {full_request}")
                self.add_decode_data(f"[{self.get_timestamp()}] 发送Modbus请求: 从站{slave_addr}, 功能码{function_code}, 地址{reg_addr}, 数量{reg_count}")
                
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
            data = " ".join([f"{random.randint(0, 1):02X}" for _ in range(reg_count)])
        else:
            # 寄存器
            data_bytes = reg_count * 2
            data = " ".join([f"{random.randint(0, 65535):04X}" for _ in range(reg_count)])
            
        response = f"{slave_addr:02X} {function_code} {data_bytes:02X} {data}"
        crc = self.calculate_crc(response.replace(" ", ""))
        full_response = f"{response} {crc:04X}"
        
        self.add_raw_data(f"[{self.get_timestamp()}] 接收: {full_response}")
        self.add_decode_data(f"[{self.get_timestamp()}] 接收Modbus响应: 从站{slave_addr}, 功能码{function_code}, 数据长度{data_bytes}字节")
        
    def calculate_crc(self, data):
        """计算CRC校验码（简化版）"""
        # 这里实现CRC16计算，目前返回模拟值
        return 0x1234
        
    def clear_data(self):
        """清空数据显示"""
        self.raw_data_text.delete(1.0, tk.END)
        self.decode_data_text.delete(1.0, tk.END)
        self.status_var.set("数据已清空")
        
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
        about_text = """测试应用 v1.0

功能特性：
• 可调整大小的现代化界面
• Modbus测试功能
• 27930测试功能
• 响应式设计

开发者：AI助手
创建时间：2024年"""
        
        messagebox.showinfo("关于本软件", about_text)
        self.status_var.set("显示关于信息")
        
    def on_window_resize(self, event):
        """窗口大小改变事件处理"""
        if event.widget == self.root:
            self.status_var.set(f"窗口大小: {event.width} x {event.height}")

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