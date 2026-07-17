"""
FPS-fasta — FASTA / Excel 格式互转工具
=========================================
支持 Excel↔FASTA、FASTA ID 标记、SEQ→FASTA 四种功能。
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sv_ttk
import time
import traceback
import threading

from ExcelToFasta import excel_to_fasta
from FastaToExcel import fasta_to_excel
from LabelFastaEnd import add_string_to_fasta
from SeqToFasta import convert_seq_to_fasta


# ============================================================
# FastaProcessorApp — GUI 应用
# ============================================================

class FastaProcessorApp:
    """FPS-fasta 图形界面。

    使用 ttk + sv_ttk 暗色主题，提供文件选择、参数配置、
    执行控制和彩色日志输出。
    """

    FONT_FAMILY = "Microsoft YaHei UI"

    def __init__(self, root):
        self.root = root
        self.root.title("FPS-fasta")
        self.root.geometry("680x620")
        self.root.minsize(580, 500)

        # 样式
        self.style = ttk.Style()
        self._setup_theme()

        # 用 StringVar 存放各选项卡的路径和参数
        self.ef_input = tk.StringVar()       # Excel→FASTA 输入
        self.ef_output = tk.StringVar()      # Excel→FASTA 输出
        self.ef_id_col = tk.StringVar()      # ID 列名
        self.ef_seq_col = tk.StringVar()     # 序列列名

        self.fe_input = tk.StringVar()       # FASTA→Excel 输入
        self.fe_output = tk.StringVar()      # FASTA→Excel 输出

        self.lf_input = tk.StringVar()       # LabelFastaEnd 输入
        self.lf_output = tk.StringVar()      # LabelFastaEnd 输出
        self.lf_custom = tk.StringVar()      # 自定义字符串

        self.sf_input = tk.StringVar()       # Seq→FASTA 输入
        self.sf_output = tk.StringVar()      # Seq→FASTA 输出
        self.sf_count = tk.StringVar(value="1")  # 每个文件序列数

        # 构建界面
        self._build_ui()

    # ---- 主题设置 ----

    def _setup_theme(self):
        """配置 sv_ttk 暗色主题与全局字体。"""
        sv_ttk.set_theme("dark")

        default_font = (self.FONT_FAMILY, 9)
        heading_font = (self.FONT_FAMILY, 10, "bold")

        self.style.configure('.', font=default_font)
        self.style.configure('TButton', font=default_font)
        self.style.configure('TLabel', font=default_font)
        self.style.configure('TEntry', font=default_font)
        self.style.configure('TLabelframe.Label', font=heading_font)

        # GO 按钮样式
        self.style.configure('Go.TButton', font=(self.FONT_FAMILY, 11, "bold"))

    # ---- UI 构建 ----

    def _build_ui(self):
        """构建完整 GUI 布局。"""
        # 主容器
        main = ttk.Frame(self.root, padding="10")
        main.pack(fill=tk.BOTH, expand=True)

        # Notebook（选项卡）
        self.notebook = ttk.Notebook(main)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        # 创建各选项卡
        self._create_excel_to_fasta_tab()
        self._create_fasta_to_excel_tab()
        self._create_label_fasta_end_tab()
        self._create_seq_to_fasta_tab()

        # ---- 日志区域 ----
        log_frame = ttk.Labelframe(main, text="运行日志", padding="4")
        log_frame.pack(fill=tk.BOTH, expand=True)

        self.log_text = tk.Text(
            log_frame, height=8, wrap=tk.WORD,
            font=(self.FONT_FAMILY, 9),
            bg="#1c1c1c", fg="#d4d4d4",
            insertbackground="#ffffff",
            relief=tk.FLAT, borderwidth=0,
        )
        log_scroll = ttk.Scrollbar(log_frame, orient=tk.VERTICAL,
                                   command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scroll.set)

        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # 日志颜色标签
        self.log_text.tag_configure("success", foreground="#4ec9b0")
        self.log_text.tag_configure("error", foreground="#f44747")
        self.log_text.tag_configure("warn", foreground="#cca700")
        self.log_text.tag_configure("info", foreground="#569cd6")

        self.log_text.configure(state=tk.DISABLED)
        self._log_line_count = 0
        self._max_log_lines = 500

        # 版权署名
        ttk.Label(main, text="© 0x4c4d59",
                  font=(self.FONT_FAMILY, 8)).pack(anchor=tk.E, pady=(2, 0))

    # ---- 各选项卡 ----

    def _create_excel_to_fasta_tab(self):
        """Excel → FASTA 选项卡。"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Excel → fasta")

        # 文件路径
        file_frame = ttk.Labelframe(tab, text="文件路径", padding="8")
        file_frame.pack(fill=tk.X, padx=8, pady=(8, 4))

        ttk.Label(file_frame, text="输入 Excel:", width=14).grid(
            row=0, column=0, sticky=tk.W, pady=3)
        ttk.Entry(file_frame, textvariable=self.ef_input).grid(
            row=0, column=1, sticky=tk.EW, padx=(5, 5), pady=3)
        ttk.Button(file_frame, text="浏览", width=6,
                   command=lambda: self._browse_file(
                       self.ef_input, [("Excel 文件", "*.xlsx *.xls"), ("所有文件", "*.*")]
                   )).grid(row=0, column=2, pady=3)

        ttk.Label(file_frame, text="输出 FASTA:", width=14).grid(
            row=1, column=0, sticky=tk.W, pady=3)
        ttk.Entry(file_frame, textvariable=self.ef_output).grid(
            row=1, column=1, sticky=tk.EW, padx=(5, 5), pady=3)
        ttk.Button(file_frame, text="浏览", width=6,
                   command=lambda: self._browse_save(
                       self.ef_output, [("FASTA 文件", "*.fasta *.fa *.fna"), ("所有文件", "*.*")]
                   )).grid(row=1, column=2, pady=3)

        file_frame.columnconfigure(1, weight=1)

        # 参数
        param_frame = ttk.Labelframe(tab, text="参数设置", padding="8")
        param_frame.pack(fill=tk.X, padx=8, pady=(0, 8))

        ttk.Label(param_frame, text="ID 列名:", width=14).grid(
            row=0, column=0, sticky=tk.W, pady=3)
        ttk.Entry(param_frame, textvariable=self.ef_id_col, width=20).grid(
            row=0, column=1, sticky=tk.W, padx=(5, 10), pady=3)

        ttk.Label(param_frame, text="序列列名:", width=14).grid(
            row=0, column=2, sticky=tk.W, pady=3)
        ttk.Entry(param_frame, textvariable=self.ef_seq_col, width=20).grid(
            row=0, column=3, sticky=tk.W, padx=(5, 0), pady=3)

        # GO 按钮
        ttk.Button(tab, text="▶  GO", style='Go.TButton',
                   command=lambda: self._process("ef")).pack(pady=(0, 8))

    def _create_fasta_to_excel_tab(self):
        """FASTA → Excel 选项卡。"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="fasta → Excel")

        file_frame = ttk.Labelframe(tab, text="文件路径", padding="8")
        file_frame.pack(fill=tk.X, padx=8, pady=(8, 4))

        ttk.Label(file_frame, text="输入 FASTA:", width=14).grid(
            row=0, column=0, sticky=tk.W, pady=3)
        ttk.Entry(file_frame, textvariable=self.fe_input).grid(
            row=0, column=1, sticky=tk.EW, padx=(5, 5), pady=3)
        ttk.Button(file_frame, text="浏览", width=6,
                   command=lambda: self._browse_file(
                       self.fe_input, [("FASTA 文件", "*.fasta *.fa *.fna *.txt"), ("所有文件", "*.*")]
                   )).grid(row=0, column=2, pady=3)

        ttk.Label(file_frame, text="输出 Excel:", width=14).grid(
            row=1, column=0, sticky=tk.W, pady=3)
        ttk.Entry(file_frame, textvariable=self.fe_output).grid(
            row=1, column=1, sticky=tk.EW, padx=(5, 5), pady=3)
        ttk.Button(file_frame, text="浏览", width=6,
                   command=lambda: self._browse_save(
                       self.fe_output, [("Excel 文件", "*.xlsx"), ("所有文件", "*.*")]
                   )).grid(row=1, column=2, pady=3)

        file_frame.columnconfigure(1, weight=1)

        # GO 按钮
        ttk.Button(tab, text="▶  GO", style='Go.TButton',
                   command=lambda: self._process("fe")).pack(pady=(8, 8))

    def _create_label_fasta_end_tab(self):
        """FASTA ID 标记选项卡。"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="fastaID → fastaIDxxx")

        file_frame = ttk.Labelframe(tab, text="文件路径", padding="8")
        file_frame.pack(fill=tk.X, padx=8, pady=(8, 4))

        ttk.Label(file_frame, text="输入 FASTA:", width=14).grid(
            row=0, column=0, sticky=tk.W, pady=3)
        ttk.Entry(file_frame, textvariable=self.lf_input).grid(
            row=0, column=1, sticky=tk.EW, padx=(5, 5), pady=3)
        ttk.Button(file_frame, text="浏览", width=6,
                   command=lambda: self._browse_file(
                       self.lf_input, [("FASTA 文件", "*.fasta *.fa *.fna *.txt"), ("所有文件", "*.*")]
                   )).grid(row=0, column=2, pady=3)

        ttk.Label(file_frame, text="输出 FASTA:", width=14).grid(
            row=1, column=0, sticky=tk.W, pady=3)
        ttk.Entry(file_frame, textvariable=self.lf_output).grid(
            row=1, column=1, sticky=tk.EW, padx=(5, 5), pady=3)
        ttk.Button(file_frame, text="浏览", width=6,
                   command=lambda: self._browse_save(
                       self.lf_output, [("FASTA 文件", "*.fasta *.fa"), ("所有文件", "*.*")]
                   )).grid(row=1, column=2, pady=3)

        file_frame.columnconfigure(1, weight=1)

        # 参数
        param_frame = ttk.Labelframe(tab, text="参数设置", padding="8")
        param_frame.pack(fill=tk.X, padx=8, pady=(0, 8))

        ttk.Label(param_frame, text="自定义字符串:", width=14).grid(
            row=0, column=0, sticky=tk.W, pady=3)
        ttk.Entry(param_frame, textvariable=self.lf_custom, width=30).grid(
            row=0, column=1, sticky=tk.W, padx=(5, 0), pady=3)

        # GO 按钮
        ttk.Button(tab, text="▶  GO", style='Go.TButton',
                   command=lambda: self._process("lf")).pack(pady=(0, 8))

    def _create_seq_to_fasta_tab(self):
        """SEQ → FASTA 选项卡。"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="seq → fasta")

        file_frame = ttk.Labelframe(tab, text="文件路径", padding="8")
        file_frame.pack(fill=tk.X, padx=8, pady=(8, 4))

        ttk.Label(file_frame, text="输入文件夹:", width=14).grid(
            row=0, column=0, sticky=tk.W, pady=3)
        ttk.Entry(file_frame, textvariable=self.sf_input).grid(
            row=0, column=1, sticky=tk.EW, padx=(5, 5), pady=3)
        ttk.Button(file_frame, text="浏览", width=6,
                   command=lambda: self._browse_folder(self.sf_input)
                   ).grid(row=0, column=2, pady=3)

        ttk.Label(file_frame, text="输出文件夹:", width=14).grid(
            row=1, column=0, sticky=tk.W, pady=3)
        ttk.Entry(file_frame, textvariable=self.sf_output).grid(
            row=1, column=1, sticky=tk.EW, padx=(5, 5), pady=3)
        ttk.Button(file_frame, text="浏览", width=6,
                   command=lambda: self._browse_folder(self.sf_output)
                   ).grid(row=1, column=2, pady=3)

        file_frame.columnconfigure(1, weight=1)

        # 参数
        param_frame = ttk.Labelframe(tab, text="参数设置", padding="8")
        param_frame.pack(fill=tk.X, padx=8, pady=(0, 8))

        ttk.Label(param_frame, text="每个 FASTA 包含的序列数:", width=22).grid(
            row=0, column=0, sticky=tk.W, pady=3)
        vcmd = (self.root.register(self._validate_int), '%P')
        ttk.Spinbox(param_frame, from_=1, to=9999, textvariable=self.sf_count,
                    width=8, validate='key', validatecommand=vcmd).grid(
            row=0, column=1, sticky=tk.W, padx=(5, 0), pady=3)

        # GO 按钮
        ttk.Button(tab, text="▶  GO", style='Go.TButton',
                   command=lambda: self._process("sf")).pack(pady=(0, 8))

    # ---- 文件浏览 ----

    def _browse_file(self, var, filetypes):
        """选择输入文件。"""
        path = filedialog.askopenfilename(
            title="选择文件",
            filetypes=filetypes,
        )
        if path:
            var.set(path)

    def _browse_folder(self, var):
        """选择文件夹。"""
        folder = filedialog.askdirectory(title="选择文件夹")
        if folder:
            var.set(folder)

    def _browse_save(self, var, filetypes):
        """选择保存文件路径。"""
        path = filedialog.asksaveasfilename(
            title="保存文件",
            filetypes=filetypes,
        )
        if path:
            var.set(path)

    # ---- 输入验证 ----

    @staticmethod
    def _validate_int(value):
        """验证输入是否为正整数。"""
        if value == "":
            return True
        return value.isdigit()

    # ---- 处理入口 ----

    def _process(self, module):
        """主处理入口。

        Args:
            module: 'ef' | 'fe' | 'lf' | 'sf'
        """
        # 清晰的模块→描述映射
        module_desc = {
            'ef': ("Excel → fasta", self._process_excel_to_fasta),
            'fe': ("fasta → Excel", self._process_fasta_to_excel),
            'lf': ("fastaID → fastaIDxxx", self._process_label_fasta_end),
            'sf': ("seq → fasta", self._process_seq_to_fasta),
        }

        desc, handler = module_desc[module]

        self._log(f"========== {desc} 开始 ==========", "info")

        try:
            handler()
        except Exception as e:
            self._log(f"处理失败: {e}", "error")
            self._log(traceback.format_exc(), "error")
            messagebox.showerror("错误", f"{desc} 处理失败:\n{e}")

    # ---- 各模块处理逻辑 ----

    def _process_excel_to_fasta(self):
        """Excel → FASTA 转换。"""
        input_file = self.ef_input.get().strip()
        output_file = self.ef_output.get().strip()
        id_col = self.ef_id_col.get().strip()
        seq_col = self.ef_seq_col.get().strip()

        # 校验
        if not all([input_file, output_file, id_col, seq_col]):
            raise ValueError("请填写所有字段：输入文件、输出文件、ID 列名、序列列名")

        self._log(f"输入: {input_file}", "info")
        self._log(f"输出: {output_file}", "info")
        self._log(f"ID 列: {id_col}  |  序列列: {seq_col}", "info")

        excel_to_fasta(input_file, output_file, id_col, seq_col, log_cb=self._log)

        self._log("Excel → fasta 搞定~", "success")
        messagebox.showinfo("成功", "Excel → fasta, 搞定~")

    def _process_fasta_to_excel(self):
        """FASTA → Excel 转换。"""
        input_file = self.fe_input.get().strip()
        output_file = self.fe_output.get().strip()

        if not input_file or not output_file:
            raise ValueError("请选择输入文件和输出文件路径")

        self._log(f"输入: {input_file}", "info")
        self._log(f"输出: {output_file}", "info")

        fasta_to_excel(input_file, output_file, log_cb=self._log)

        self._log("fasta → Excel 搞定~", "success")
        messagebox.showinfo("成功", "fasta → Excel, 搞定~")

    def _process_label_fasta_end(self):
        """FASTA ID 末尾添加自定义字符串。"""
        input_file = self.lf_input.get().strip()
        output_file = self.lf_output.get().strip()
        custom = self.lf_custom.get().strip()

        if not input_file or not output_file:
            raise ValueError("请选择输入文件和输出文件路径")
        if not custom:
            raise ValueError("请输入自定义字符串")

        self._log(f"输入: {input_file}", "info")
        self._log(f"输出: {output_file}", "info")
        self._log(f"自定义字符串: {custom}", "info")

        add_string_to_fasta(input_file, output_file, custom)

        self._log("fastaID → fastaIDxxx 搞定~", "success")
        messagebox.showinfo("成功", "fastaID → fastaIDxxx, 搞定~")

    def _process_seq_to_fasta(self):
        """SEQ → FASTA 转换。"""
        input_dir = self.sf_input.get().strip()
        output_dir = self.sf_output.get().strip()
        count_str = self.sf_count.get().strip()

        if not input_dir or not output_dir:
            raise ValueError("请选择输入文件夹和输出文件夹")
        if not count_str or not count_str.isdigit() or int(count_str) < 1:
            raise ValueError("请输入有效的序列数量（≥1 的正整数）")

        seq_count = int(count_str)
        self._log(f"输入文件夹: {input_dir}", "info")
        self._log(f"输出文件夹: {output_dir}", "info")
        self._log(f"每个 FASTA 文件包含: {seq_count} 条序列", "info")

        # convert_seq_to_fasta 内部有 print，这里通过线程执行并捕获日志
        convert_seq_to_fasta(input_dir, output_dir, seq_count)

        self._log("seq → fasta 搞定~", "success")
        messagebox.showinfo("成功", "seq → fasta, 搞定~")

    # ---- 日志 ----

    def _log(self, msg, tag=None):
        """向日志区域追加消息（必须在主线程调用）。

        Args:
            msg: 消息文本
            tag: 颜色标签 ('success', 'error', 'warn', 'info', None)
        """
        # 线程安全：如果不在主线程，用 after 调度
        if threading.current_thread() is not threading.main_thread():
            self.root.after(0, lambda: self._log(msg, tag))
            return

        self.log_text.configure(state=tk.NORMAL)

        # 限制最大行数
        if self._log_line_count >= self._max_log_lines:
            self.log_text.delete("1.0", "100.0")
            self._log_line_count -= 100

        timestamp = time.strftime("%H:%M:%S")
        line = f"[{timestamp}] {msg}\n"
        if tag:
            self.log_text.insert(tk.END, line, tag)
        else:
            self.log_text.insert(tk.END, line)

        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)
        self._log_line_count += 1


# ============================================================
# 入口点
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = FastaProcessorApp(root)
    root.mainloop()
