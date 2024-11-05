# pip install pandas openpyxl

import pandas as pd


def fasta_to_excel(fasta_file, output_file):
    # 初始化列表，用于存储数据
    names = []
    sequences = []

    # 打开FASTA文件并读取
    with open(fasta_file, 'r') as file:
        name = None
        sequence = ""
        for line in file:
            line = line.strip()
            if line.startswith(">"):
                # 如果是名称行，保存当前序列并准备处理新的序列
                if name:
                    names.append(name)
                    sequences.append(sequence)
                name = line[1:]  # 去掉">"符号
                sequence = ""
            else:
                # 否则是序列行，拼接到sequence
                sequence += line

        # 处理最后一个序列
        if name:
            names.append(name)
            sequences.append(sequence)

    # 创建DataFrame
    df = pd.DataFrame({
        'Name': names,
        'Sequence': sequences
    })

    # 将DataFrame保存为Excel文件
    df.to_excel(output_file, index=False)


# # 使用示例
# fasta_to_excel('input.fasta', 'output.xlsx')
