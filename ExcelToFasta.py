# 从excel中提取某列sequence形成fasta

import pandas as pd

def excel_to_fasta(input_file, output_file, id_column, sequence_column):
    # 读取Excel文件
    df = pd.read_excel(input_file)

    with open(output_file, 'w') as f:
        # 遍历每一行，将信息写入FASTA文件
        for index, row in df.iterrows():
            identifier = row[id_column]
            sequence = row[sequence_column]
            f.write(f'>{identifier}\n{sequence}\n')


# # 参数定义
# input_file = 'example.xlsx'  # 输入的Excel文件名
# output_file = 'example.fasta'  # 输出的FASTA文件名
# id_column = 'index colname'  # ID列名
# sequence_column = 'sequence colname'  # 序列列名
# excel_to_fasta(input_file, output_file, id_column, sequence_column)
