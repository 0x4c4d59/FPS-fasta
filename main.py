import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from ExcelToFasta import excel_to_fasta
from FastaToExcel import fasta_to_excel
from LabelFastaEnd import add_string_to_fasta
from SeqToFasta import convert_seq_to_fasta


class FastaProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FPS-fasta")

        # 创建 Notebook（选项卡容器）
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # 为每个选项卡单独创建输入框引用
        self.excel_to_fasta_input = {"input": None, "output": None}
        self.fasta_to_excel_input = {"input": None, "output": None}
        self.label_fasta_end_input = {"input": None, "output": None}
        self.seq_to_fasta_input = {"input": None, "output": None}

        # 创建模块页面
        self.create_tabs()

    def create_tabs(self):
        # ExcelToFasta 页面
        self.excel_to_fasta_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.excel_to_fasta_tab, text="Excel -> fasta")
        self.create_excel_to_fasta_tab()

        # FastaToExcel 页面
        self.fasta_to_excel_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.fasta_to_excel_tab, text="fasta -> Excel")
        self.create_fasta_to_excel_tab()

        # LabelFastaEnd 页面
        self.label_fasta_end_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.label_fasta_end_tab, text="fastaID -> fastaIDxxx")
        self.create_label_fasta_end_tab()

        # SeqToFasta 页面
        self.seq_to_fasta_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.seq_to_fasta_tab, text="seq -> fasta")
        self.create_seq_to_fasta_tab()

    def create_excel_to_fasta_tab(self):
        # 定义输入框
        self.excel_to_fasta_input["input"], self.excel_to_fasta_input["output"] = self.create_file_input_widgets(self.excel_to_fasta_tab)

        # 额外输入框：ID列 和 序列列
        tk.Label(self.excel_to_fasta_tab, text="Excel ID 列名:").grid(row=2, column=0, padx=10, pady=5)
        self.id_column_entry = tk.Entry(self.excel_to_fasta_tab, width=40)
        self.id_column_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.excel_to_fasta_tab, text="Excel 序列列名:").grid(row=3, column=0, padx=10, pady=5)
        self.sequence_column_entry = tk.Entry(self.excel_to_fasta_tab, width=40)
        self.sequence_column_entry.grid(row=3, column=1, padx=10, pady=5)

    def create_fasta_to_excel_tab(self):
        self.fasta_to_excel_input["input"], self.fasta_to_excel_input["output"] = self.create_file_input_widgets(self.fasta_to_excel_tab)

    def create_label_fasta_end_tab(self):
        self.label_fasta_end_input["input"], self.label_fasta_end_input["output"] = self.create_file_input_widgets(self.label_fasta_end_tab)

        tk.Label(self.label_fasta_end_tab, text="自定义字符串:").grid(row=2, column=0, padx=10, pady=5)
        self.custom_string_entry = tk.Entry(self.label_fasta_end_tab, width=40)
        self.custom_string_entry.grid(row=2, column=1, padx=10, pady=5)

    def create_seq_to_fasta_tab(self):
        self.seq_to_fasta_input["input"], self.seq_to_fasta_input["output"] = self.create_file_input_widgets(self.seq_to_fasta_tab)

        tk.Label(self.seq_to_fasta_tab, text="每个FASTA文件包含的序列数量:").grid(row=2, column=0, padx=10, pady=5)
        self.seq_count_entry = tk.Entry(self.seq_to_fasta_tab, width=40)
        self.seq_count_entry.grid(row=2, column=1, padx=10, pady=5)

    def create_file_input_widgets(self, parent):
        """创建输入文件和输出文件选择控件"""
        # 输入文件
        tk.Label(parent, text="输入文件路径:").grid(row=0, column=0, padx=10, pady=5)
        input_entry = tk.Entry(parent, width=40)
        input_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Button(parent, text="选择文件", command=lambda: self.select_file(input_entry)).grid(row=0, column=2, padx=10, pady=5)

        # 输出文件
        tk.Label(parent, text="输出文件路径:").grid(row=1, column=0, padx=10, pady=5)
        output_entry = tk.Entry(parent, width=40)
        output_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Button(parent, text="选择文件", command=lambda: self.select_file(output_entry)).grid(row=1, column=2, padx=10, pady=5)

        # 处理按钮
        tk.Button(parent, text="开始处理", command=self.process_file).grid(row=4, column=0, columnspan=3, pady=20)

        return input_entry, output_entry

    def select_file(self, entry_widget):
        """选择文件路径"""
        file = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
        if file:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, file)

    def process_file(self):
        # 获取当前选中的选项卡
        current_tab = self.notebook.select()

        if current_tab == str(self.excel_to_fasta_tab):
            input_file = self.excel_to_fasta_input["input"].get()
            output_file = self.excel_to_fasta_input["output"].get()
            id_column = self.id_column_entry.get()
            sequence_column = self.sequence_column_entry.get()
            if not input_file or not output_file or not id_column or not sequence_column:
                messagebox.showerror("错误", "请填写所有必要信息")
                return
            excel_to_fasta(input_file, output_file, id_column, sequence_column)
            messagebox.showinfo("成功", "Excel -> fasta, 搞定~")

        elif current_tab == str(self.fasta_to_excel_tab):
            input_file = self.fasta_to_excel_input["input"].get()
            output_file = self.fasta_to_excel_input["output"].get()
            fasta_to_excel(input_file, output_file)
            messagebox.showinfo("成功", "fasta -> Excel, 搞定~")

        elif current_tab == str(self.label_fasta_end_tab):
            input_file = self.label_fasta_end_input["input"].get()
            output_file = self.label_fasta_end_input["output"].get()
            custom_string = self.custom_string_entry.get()
            if not custom_string:
                messagebox.showerror("错误", "请输入自定义字符串")
                return
            add_string_to_fasta(input_file, output_file, custom_string)
            messagebox.showinfo("成功", "fastaID -> fastaIDxxx, 搞定~")

        elif current_tab == str(self.seq_to_fasta_tab):
            input_file = self.seq_to_fasta_input["input"].get()
            output_file = self.seq_to_fasta_input["output"].get()
            try:
                seq_count = int(self.seq_count_entry.get())
                convert_seq_to_fasta(input_file, output_file, seq_count)
                messagebox.showinfo("成功", "seq -> fasta, 搞定~")
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字")

if __name__ == "__main__":
    root = tk.Tk()
    app = FastaProcessorApp(root)
    root.mainloop()
