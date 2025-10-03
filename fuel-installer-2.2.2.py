import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import shutil
import time

class FuelLoaderInstaller:
    def __init__(self, root):
        # 设置窗口标题
        root.title("Fuel Loader Installer")
        
        # 设置窗口图标
        self.set_window_icon(root)
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="10 10 10 10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 定义SFC版本与兼容的Loader版本映射关系
        self.version_mapping = {
            "CE3.2": ["0.0.1-build.1"],
            "CE3.1": ["0.0.1-build.1"],
            "CE3.0": [ "0.0.1-build.1"],
            "CE2.2正式版": ["本版本不兼容Fuel Loader"],
            "CE2.2": ["本版本不兼容Fuel Loader"],
            '1.9.7完结版': ["本版本不兼容Fuel Loader"],
            '2.1正式版': ["本版本不兼容Fuel Loader"],
            '2.1': ["本版本不兼容Fuel Loader"],
            '2.0.88正式版': ["本版本不兼容Fuel Loader"],
            '2.0.88': ["本版本不兼容Fuel Loader"],
            '1.2正式版': ["本版本不兼容Fuel Loader"],
            '1.2': ["本版本不兼容Fuel Loader"],
            '1.1': ["本版本不兼容Fuel Loader"],
            '1.0': ["本版本不兼容Fuel Loader"],
            '0.3': ["本版本不兼容Fuel Loader"]
        }
        
        # 所有可用的Loader版本
        self.all_loader_versions = ["0.0.1-build.1"]
        
        # 创建自定义样式
        self.style = ttk.Style()
        self.style.configure("Red.TLabel", foreground="red")
        self.style.configure("Green.TLabel", foreground="green")
        
        # SFC Version下拉框
        ttk.Label(main_frame, text="SFCVersion:").grid(row=0, column=0, padx=(5, 2), pady=10, sticky=tk.W)
        self.sfc_version = tk.StringVar()
        self.sfc_combobox = ttk.Combobox(main_frame, textvariable=self.sfc_version, state="readonly", width=15)
        self.sfc_combobox['values'] = tuple(self.version_mapping.keys())
        self.sfc_combobox.grid(row=0, column=1, padx=(2, 5), pady=10, sticky=tk.W)
        self.sfc_combobox.current(0)  # 设置默认选中第一个选项
        # 绑定SFC版本变化事件
        self.sfc_combobox.bind("<<ComboboxSelected>>", self.update_loader_display)
        
        # Loader Version显示
        ttk.Label(main_frame, text="LoaderVersion:").grid(row=1, column=0, padx=(5, 2), pady=10, sticky=tk.W)
        
        self.loader_version = tk.StringVar()
        self.loader_combobox = ttk.Combobox(
            main_frame, 
            textvariable=self.loader_version, 
            state="readonly", 
            width=15
        )
        self.loader_combobox['values'] = self.all_loader_versions
        self.loader_combobox.grid(row=1, column=1, padx=(2, 5), pady=10, sticky=tk.W)
        self.loader_combobox.current(0)
        self.loader_combobox.bind("<<ComboboxSelected>>", self.update_compatibility_label)
        
        # 兼容性标签（左移）
        self.compatibility_label = ttk.Label(main_frame, text="", style="Green.TLabel")
        self.compatibility_label.grid(row=1, column=2, padx=(5, 10), pady=10, sticky=tk.W)
        
        # 添加安装路径输入框
        ttk.Label(main_frame, text="Install at:").grid(row=2, column=0, padx=(5, 2), pady=10, sticky=tk.W)
        # 设置默认安装路径
        default_path = r"C:/ProgramsFiles/SFCCE/.sfc/versions/"
        self.install_path = tk.StringVar(value=default_path)
        install_entry = ttk.Entry(main_frame, textvariable=self.install_path, width=40)
        install_entry.grid(row=2, column=1, columnspan=2, padx=(2, 5), pady=10, sticky=tk.W)
        
        # "see"按钮
        see_button = ttk.Button(main_frame, text="see", command=self.choose_directory)
        see_button.grid(row=3, column=1, padx=(2, 5), pady=5, sticky=tk.W)
        
        # 安装按钮
        install_button = ttk.Button(main_frame, text="Install", command=self.on_install)
        install_button.grid(row=4, column=1, padx=(2, 5), pady=15, sticky=tk.W)
        
        # 调整列宽
        main_frame.columnconfigure(1, weight=1)
        
        # 保存主窗口引用
        self.main_window = root
        
        # 初始化显示
        self.update_loader_display(None)
    
    def set_window_icon(self, window):
        """设置窗口图标，使用当前文件夹下的logo.ico"""
        try:
            # 获取当前脚本所在目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(current_dir, "logo.ico")
            
            # 检查图标文件是否存在
            if os.path.exists(icon_path):
                window.iconbitmap(icon_path)
            else:
                print(f"图标文件未找到: {icon_path}")
        except Exception as e:
            print(f"设置图标时出错: {e}")
    
    def choose_directory(self):
        """打开文件夹选择对话框并更新输入框"""
        default_dir = self.install_path.get()
        if not os.path.exists(default_dir):
            default_dir = os.getcwd()
            
        selected_dir = filedialog.askdirectory(
            title="Select Installation Directory",
            initialdir=default_dir
        )
        
        if selected_dir:
            self.install_path.set(selected_dir)
    
    def update_loader_display(self, event):
        """更新Loader版本显示，标记兼容性"""
        selected_sfc = self.sfc_version.get()
        compatible_versions = self.version_mapping.get(selected_sfc, [])
        current_loader = self.loader_version.get()
        
        # 更新兼容性标签
        if current_loader in compatible_versions:
            self.compatibility_label.config(text="compatible", style="Green.TLabel")
        else:
            self.compatibility_label.config(text="incompatible", style="Red.TLabel")
    
    def update_compatibility_label(self, event):
        """当选择不同Loader版本时更新兼容性标签"""
        self.update_loader_display(event)
    
    def on_install(self):
        selected_sfc = self.sfc_version.get()
        selected_loader = self.loader_version.get()
        compatible_versions = self.version_mapping.get(selected_sfc, [])
        
        # 检查是否选择了不兼容的版本组合
        if selected_loader not in compatible_versions:
            messagebox.showwarning(
                "版本不兼容", 
                f"警告: SFC版本 {selected_sfc} 与Loader版本 {selected_loader} 不兼容！\n"
                f"兼容的版本为: {', '.join(compatible_versions)}\n"
                "只有CE3.0以上的版本兼容Fuel Loader！"
            )
            return
        
        # 构建完整安装路径（C:/ProgramsFiles/SFCCE/.sfc/versions/用户选择的SFC版本/fuel）
        install_path = os.path.join(self.install_path.get(), selected_sfc, "fuel")
        
        # 源文件目录（当前目录下的file/fuel/用户选择的loader版本）
        current_dir = os.path.dirname(os.path.abspath(__file__))
        source_dir = os.path.join(current_dir, "file", "fuel", selected_loader)
        
        # 检查源文件目录是否存在
        if not os.path.exists(source_dir):
            messagebox.showerror("源文件错误", f"未找到版本为 {selected_loader} 的Fuel Loader源文件，路径：{source_dir}")
            return
        
        # 尝试创建安装目录
        try:
            if not os.path.exists(install_path):
                os.makedirs(install_path)
        except Exception as e:
            messagebox.showerror("路径错误", f"无法创建安装目录: {str(e)}")
            return
        
        # 创建进度条窗口
        progress_window = tk.Toplevel(self.main_window)
        progress_window.title("Installing...")
        self.set_window_icon(progress_window)  # 为进度窗口设置图标
        progress_window.geometry("400x100")
        progress_window.resizable(False, False)
        progress_window.transient(self.main_window)
        progress_window.grab_set()
        
        ttk.Label(progress_window, text="Installing Fuel Loader...").pack(pady=10)
        
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(
            progress_window,
            variable=progress_var,
            length=300,
            mode='determinate'
        )
        progress_bar.pack(pady=10)
        
        def update_progress():
            # 获取源文件列表
            files = os.listdir(source_dir)
            total_files = len(files)
            copied_files = 0
            
            for file in files:
                source_file = os.path.join(source_dir, file)
                target_file = os.path.join(install_path, file)
                
                # 复制文件
                try:
                    shutil.copy2(source_file, target_file)
                    copied_files += 1
                    # 更新进度
                    progress = (copied_files / total_files) * 100
                    progress_var.set(progress)
                    progress_window.update_idletasks()
                    time.sleep(0.1)  # 模拟复制时间
                except Exception as e:
                    messagebox.showerror("安装错误", f"复制文件 {file} 时出错: {str(e)}")
                    progress_window.destroy()
                    return
            
            progress_window.destroy()
            messagebox.showinfo("Install Was Successfully!", 
                              f"Installation completed successfully!\nInstalled at: {install_path}")
        
        progress_window.after(10, update_progress)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x300")  # 恢复原来的窗口大小
    root.resizable(False, False)
    app = FuelLoaderInstaller(root)
    root.mainloop()
