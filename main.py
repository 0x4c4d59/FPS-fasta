import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from ExcelToFasta import excel_to_fasta
from FastaToExcel import fasta_to_excel
from LabelFastaEnd import add_string_to_fasta
from SeqToFasta import convert_seq_to_fasta  # 导入修改后的函数


class FastaProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FPS-fasta")

        # 创建 Notebook（选项卡容器）
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

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
        self.create_common_file_inputs(self.excel_to_fasta_tab)

        self.id_column_label = tk.Label(self.excel_to_fasta_tab, text="Excel ID 列名:")
        self.id_column_label.grid(row=2, column=0, padx=10, pady=5)

        self.id_column_entry = tk.Entry(self.excel_to_fasta_tab, width=40)
        self.id_column_entry.grid(row=2, column=1, padx=10, pady=5)

        self.sequence_column_label = tk.Label(self.excel_to_fasta_tab, text="Excel 序列列名:")
        self.sequence_column_label.grid(row=3, column=0, padx=10, pady=5)

        self.sequence_column_entry = tk.Entry(self.excel_to_fasta_tab, width=40)
        self.sequence_column_entry.grid(row=3, column=1, padx=10, pady=5)

    def create_fasta_to_excel_tab(self):
        self.create_common_file_inputs(self.fasta_to_excel_tab)

    def create_label_fasta_end_tab(self):
        self.create_common_file_inputs(self.label_fasta_end_tab)

        self.custom_string_label = tk.Label(self.label_fasta_end_tab, text="自定义字符串:")
        self.custom_string_label.grid(row=2, column=0, padx=10, pady=5)

        self.custom_string_entry = tk.Entry(self.label_fasta_end_tab, width=40)
        self.custom_string_entry.grid(row=2, column=1, padx=10, pady=5)

    def create_seq_to_fasta_tab(self):
        self.create_common_file_inputs(self.seq_to_fasta_tab)

        self.tans_number_label = tk.Label(self.seq_to_fasta_tab, text="每个FASTA文件包含的序列数量:")
        self.tans_number_label.grid(row=2, column=0, padx=10, pady=5)

        self.tans_number_entry = tk.Entry(self.seq_to_fasta_tab, width=40)
        self.tans_number_entry.grid(row=2, column=1, padx=10, pady=5)

    def create_common_file_inputs(self, parent):
        # 输入文件路径
        self.input_label = tk.Label(parent, text="输入文件路径:")
        self.input_label.grid(row=0, column=0, padx=10, pady=5)

        self.input_entry = tk.Entry(parent, width=40)
        self.input_entry.grid(row=0, column=1, padx=10, pady=5)

        self.input_button = tk.Button(parent, text="选择文件", command=lambda: self.select_file(self.input_entry))
        self.input_button.grid(row=0, column=2, padx=10, pady=5)

        # 输出文件路径
        self.output_label = tk.Label(parent, text="输出文件路径:")
        self.output_label.grid(row=1, column=0, padx=10, pady=5)

        self.output_entry = tk.Entry(parent, width=40)
        self.output_entry.grid(row=1, column=1, padx=10, pady=5)

        self.output_button = tk.Button(parent, text="选择文件", command=lambda: self.select_file(self.output_entry))
        self.output_button.grid(row=1, column=2, padx=10, pady=5)

        # 处理按钮
        self.process_button = tk.Button(parent, text="开始处理", command=self.process_file)
        self.process_button.grid(row=4, column=0, columnspan=3, pady=20)

    def select_file(self, entry_widget):
        file = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
        if file:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, file)

    def process_file(self):
        # 获取当前选中的选项卡
        current_tab = self.notebook.select()

        input_file = self.input_entry.get()
        output_file = self.output_entry.get()

        if not input_file or not output_file:
            messagebox.showerror("错误", "请输入有效的文件路径")
            return

        if current_tab == str(self.excel_to_fasta_tab):
            # Excel 转 FASTA
            id_column = self.id_column_entry.get()
            sequence_column = self.sequence_column_entry.get()
            if not id_column or not sequence_column:
                messagebox.showerror("错误", "请输入Excel文件中的ID列和序列列名")
                return
            excel_to_fasta(input_file, output_file, id_column, sequence_column)
            messagebox.showinfo("成功", "Excel -> fasta, 搞定~")

        elif current_tab == str(self.fasta_to_excel_tab):
            # FASTA 转 Excel
            fasta_to_excel(input_file, output_file)
            messagebox.showinfo("成功", "fasta -> Excel, 搞定~")

        elif current_tab == str(self.label_fasta_end_tab):
            # FASTA ID 字符串添加
            custom_string = self.custom_string_entry.get()
            if not custom_string:
                messagebox.showerror("错误", "请输入自定义字符串")
                return
            add_string_to_fasta(input_file, output_file, custom_string)
            messagebox.showinfo("成功", "fastaID, 追加完成~")

        elif current_tab == str(self.seq_to_fasta_tab):
            # 批量 .seq 到 .fasta
            try:
                tans_number = int(self.tans_number_entry.get())
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字作为每个fasta文件的序列数量")
                return
            convert_seq_to_fasta(input_file, output_file, tans_number)
            messagebox.showinfo("成功", "批量seq -> fasta, 搞定~")


if __name__ == "__main__":
    root = tk.Tk()
    app = FastaProcessorApp(root)
    root.mainloop()
