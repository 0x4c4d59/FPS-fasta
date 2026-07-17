# 从excel中提取某列sequence形成fasta

import pandas as pd


def excel_to_fasta(input_file, output_file, id_column, sequence_column, log_cb=None):
    """从 Excel 中读取指定列，生成 FASTA 文件。

    Args:
        input_file: Excel 文件路径
        output_file: 输出 FASTA 文件路径
        id_column: Excel 中作为 FASTA ID 的列名
        sequence_column: Excel 中作为序列的列名
        log_cb: 可选，日志回调函数 log_cb(msg: str)
    """
    if log_cb:
        log_cb(f"正在读取 Excel 文件: {input_file}")

    df = pd.read_excel(input_file)

    if log_cb:
        log_cb(f"读取到 {len(df)} 行数据")

    if id_column not in df.columns:
        raise ValueError(f"Excel 中找不到 ID 列 '{id_column}'，可用列: {list(df.columns)}")

    if sequence_column not in df.columns:
        raise ValueError(f"Excel 中找不到序列列 '{sequence_column}'，可用列: {list(df.columns)}")

    with open(output_file, 'w', encoding='utf-8') as f:
        written = 0
        for index, row in df.iterrows():
            identifier = row[id_column]
            sequence = row[sequence_column]

            # 跳过空值
            if pd.isna(identifier) or pd.isna(sequence):
                continue

            f.write(f'>{identifier}\n{sequence}\n')
            written += 1

    if log_cb:
        log_cb(f"完成：成功写入 {written} 条序列到 {output_file}")
