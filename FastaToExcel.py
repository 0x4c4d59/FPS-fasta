# pip install pandas openpyxl

import pandas as pd


def fasta_to_excel(fasta_file, output_file, log_cb=None):
    """将 FASTA 文件转换为 Excel。

    Args:
        fasta_file: 输入的 FASTA 文件路径
        output_file: 输出的 Excel 文件路径
        log_cb: 可选，日志回调函数 log_cb(msg: str)
    """
    if log_cb:
        log_cb(f"正在读取 FASTA 文件: {fasta_file}")

    names = []
    sequences = []

    with open(fasta_file, 'r', encoding='utf-8') as file:
        name = None
        sequence = ""
        for line in file:
            line = line.strip()
            if line.startswith(">"):
                if name:
                    names.append(name)
                    sequences.append(sequence)
                name = line[1:]
                sequence = ""
            else:
                sequence += line

        # 处理最后一个序列
        if name:
            names.append(name)
            sequences.append(sequence)

    if log_cb:
        log_cb(f"解析到 {len(names)} 条序列")

    if not names:
        raise ValueError("未能从 FASTA 文件中解析到任何有效序列")

    df = pd.DataFrame({
        'Name': names,
        'Sequence': sequences
    })

    if log_cb:
        log_cb(f"正在写入 Excel 文件: {output_file}")

    df.to_excel(output_file, index=False)

    if log_cb:
        log_cb(f"完成：成功导出 {len(names)} 条序列到 {output_file}")
