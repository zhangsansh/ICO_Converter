import tkinter as tk
from tkinter import filedialog, ttk, messagebox, scrolledtext
from PIL import Image
import os
import sys


class BatchImageToIcoConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("批量图片转ICO工具")
        self.root.geometry("650x500")
        # 允许窗口调整大小
        self.root.resizable(True, True)

        # 设置中文字体支持
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("SimHei", 10))
        self.style.configure("TButton", font=("SimHei", 10))
        self.style.configure("TCombobox", font=("SimHei", 10))

        # 存储多个输入文件路径
        self.input_files = []
        # 输出文件夹路径
        self.output_dir = tk.StringVar()
        # ICO尺寸
        self.ico_size = tk.StringVar(value="32x32")

        self.create_widgets()

    def create_widgets(self):
        # 标题
        title_label = ttk.Label(self.root, text="批量图片转ICO转换器", font=("SimHei", 14, "bold"))
        title_label.pack(pady=10)

        # 输入文件选择
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.pack(fill=tk.X, padx=10)

        ttk.Label(input_frame, text="输入图片:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Button(input_frame, text="添加图片...", command=self.add_input_files).grid(row=0, column=1, pady=5, padx=5)
        ttk.Button(input_frame, text="清除列表", command=self.clear_input_files).grid(row=0, column=2, pady=5, padx=5)

        # 显示选中的文件列表
        list_frame = ttk.Frame(self.root, padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        ttk.Label(list_frame, text="已选择的图片文件:").pack(anchor=tk.W)
        self.file_list_text = scrolledtext.ScrolledText(list_frame, height=10, wrap=tk.WORD)
        self.file_list_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.file_list_text.config(state=tk.DISABLED)

        # 输出文件夹选择
        output_frame = ttk.Frame(self.root, padding="10")
        output_frame.pack(fill=tk.X, padx=10)

        ttk.Label(output_frame, text="输出文件夹:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(output_frame, textvariable=self.output_dir, width=50).grid(row=0, column=1, pady=5, padx=5)
        ttk.Button(output_frame, text="浏览...", command=self.browse_output_dir).grid(row=0, column=2, pady=5, padx=5)

        # ICO尺寸选择
        size_frame = ttk.Frame(self.root, padding="10")
        size_frame.pack(fill=tk.X, padx=10)

        ttk.Label(size_frame, text="ICO尺寸:").grid(row=0, column=0, sticky=tk.W, pady=5)
        size_options = ["16x16", "32x32", "48x48", "64x64", "128x128", "256x256"]
        size_combobox = ttk.Combobox(size_frame, textvariable=self.ico_size, values=size_options,
                                     state="readonly", width=10)
        size_combobox.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)

        # 转换按钮
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill=tk.X, padx=10)

        convert_btn = ttk.Button(button_frame, text="批量转换为ICO", command=self.batch_convert_to_ico)
        convert_btn.pack(pady=10)
        convert_btn.configure(width=20)

        # 状态标签
        self.status_var = tk.StringVar(value="就绪")
        status_frame = ttk.Frame(self.root, padding="10")
        status_frame.pack(fill=tk.X, padx=10, pady=10)

        status_label = ttk.Label(status_frame, textvariable=self.status_var,
                                 foreground="#2c3e50", font=("SimHei", 10, "italic"))
        status_label.pack(side=tk.LEFT)

    def add_input_files(self):
        """添加多个输入图片文件"""
        file_paths = filedialog.askopenfilenames(
            title="选择图片文件",
            filetypes=[("图片文件", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp")]
        )

        if file_paths:
            # 去重处理
            new_files = [path for path in file_paths if path not in self.input_files]
            self.input_files.extend(new_files)
            self.update_file_list_display()

            # 自动设置输出文件夹（如果尚未设置）
            if not self.output_dir.get() and self.input_files:
                first_file_dir = os.path.dirname(self.input_files[0])
                self.output_dir.set(first_file_dir)

    def clear_input_files(self):
        """清除已选择的文件列表"""
        self.input_files = []
        self.update_file_list_display()
        self.status_var.set("已清除文件列表")

    def update_file_list_display(self):
        """更新文件列表显示"""
        self.file_list_text.config(state=tk.NORMAL)
        self.file_list_text.delete(1.0, tk.END)

        for i, file_path in enumerate(self.input_files, 1):
            # 只显示文件名，而不是完整路径
            file_name = os.path.basename(file_path)
            self.file_list_text.insert(tk.END, f"{i}. {file_name}\n")

        self.file_list_text.config(state=tk.DISABLED)

    def browse_output_dir(self):
        """浏览并选择输出文件夹"""
        dir_path = filedialog.askdirectory(title="选择输出文件夹")
        if dir_path:
            self.output_dir.set(dir_path)

    def batch_convert_to_ico(self):
        """批量将图片转换为ICO格式"""
        if not self.input_files:
            messagebox.showerror("错误", "请添加至少一个图片文件")
            return

        output_dir = self.output_dir.get()
        if not output_dir:
            messagebox.showerror("错误", "请选择输出文件夹")
            return

        # 确保输出文件夹存在
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                messagebox.showerror("错误", f"无法创建输出文件夹:\n{str(e)}")
                return

        try:
            total_files = len(self.input_files)
            success_count = 0
            fail_count = 0
            fail_files = []

            # 获取尺寸
            size_str = self.ico_size.get()
            size = tuple(map(int, size_str.split('x')))

            for i, input_path in enumerate(self.input_files, 1):
                self.status_var.set(f"正在转换 {i}/{total_files}...")
                self.root.update()

                try:
                    # 获取文件名（不含扩展名）
                    file_name = os.path.splitext(os.path.basename(input_path))[0]
                    output_path = os.path.join(output_dir, f"{file_name}.ico")

                    # 打开图片并转换
                    with Image.open(input_path) as img:
                        # 转换为RGBA模式（ICO支持透明）
                        if img.mode != 'RGBA':
                            img = img.convert('RGBA')

                        # 调整大小，使用高质量缩放算法
                        img = img.resize(size, Image.Resampling.LANCZOS)

                        # 保存为ICO
                        img.save(output_path, format='ICO')

                    success_count += 1
                except Exception as e:
                    fail_count += 1
                    fail_files.append(f"{os.path.basename(input_path)}: {str(e)}")

            # 显示转换结果
            result_msg = f"转换完成！\n成功: {success_count} 个文件\n失败: {fail_count} 个文件"
            if fail_count > 0:
                result_msg += "\n\n失败的文件:\n" + "\n".join(fail_files)

            self.status_var.set(f"转换完成: 成功 {success_count} 个, 失败 {fail_count} 个")
            messagebox.showinfo("转换结果", result_msg)

        except Exception as e:
            self.status_var.set(f"处理出错: {str(e)}")
            messagebox.showerror("错误", f"处理出错:\n{str(e)}")


if __name__ == "__main__":
    # 确保中文显示正常
    root = tk.Tk()
    app = BatchImageToIcoConverter(root)
    root.mainloop()
