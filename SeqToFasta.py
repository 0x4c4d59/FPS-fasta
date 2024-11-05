# 主要用于批量将seq文件转换为fasta格式

import os

def convert_seq_to_fasta(input_folder, output_folder, tans_number):
    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    # 遍历输入文件夹中的所有.seq文件
    seq_files = [f for f in os.listdir(input_folder) if f.endswith('.seq')]

    # 分批合并为.fasta文件
    num_fasta_files = 0  # 用于计数生成的.fasta文件数量

    for i in range(0, len(seq_files), tans_number):
        fasta_filename = f'sequences_{i // tans_number + 1}.fasta'
        fasta_filepath = os.path.join(output_folder, fasta_filename)

        with open(fasta_filepath, 'w') as fasta_file:
            for j in range(i, i + tans_number):
                if j < len(seq_files):
                    seq_file = seq_files[j]
                    # 提取文件名中括号中间的数字部分
                    filename = os.path.splitext(seq_file)[0]
                    numbers = filename.split('(')[-1].split(')')[0]

                    # 读取序列内容
                    with open(os.path.join(input_folder, seq_file), 'r') as seq_file_contents:
                        lines = seq_file_contents.read().splitlines()
                        if len(lines) >= 2:
                            sequence = lines[1]

                            # 写入合并的.fasta文件，添加文件名中的数字部分
                            fasta_file.write(f'>{numbers}\n')
                            fasta_file.write(f'{sequence}\n')

        num_fasta_files += 1

    print(f'成功生成{num_fasta_files}个.fasta文件，保存在{output_folder}中。')

