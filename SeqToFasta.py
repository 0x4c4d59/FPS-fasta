import os
import re

def _label_from_filename(fname):
    """从文件名尝试提取标签（优先括号内内容），没有则返回整个文件名（不含扩展名）。"""
    base = os.path.splitext(fname)[0]
    m = re.search(r'\((.*?)\)', base)
    if m:
        return m.group(1)
    return base

def _clean_seq_part(s):
    """清理一行中的非字母字符（只保留字母），并返回大写序列片段。"""
    return re.sub(r'[^A-Za-z]', '', s).upper()

def _parse_seq_file(filepath, filename_base):
    """
    解析单个 .seq 文件，返回拼接好的序列字符串（大写）。
    规则：
      - 忽略以 '>' 开头的 header 行（除非 header 行中包含与 filename_base 一样的前缀，
        这时把 header 前缀后的尾部视作序列的一部分）。
      - 其它非空行视为序列行，清理后拼接。
    """
    parts = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as fh:
            for raw in fh:
                line = raw.strip()
                if not line:
                    continue
                if line.startswith('>'):
                    content = line[1:].strip()
                    # 如果 header 内容以文件名（不含扩展名）开头，可能是 header+seq 连在一起的情况
                    if content.startswith(filename_base):
                        tail = content[len(filename_base):].strip()
                        if tail:
                            parts.append(_clean_seq_part(tail))
                    # 否则把这行当作 header，忽略（避免被并入序列）
                else:
                    parts.append(_clean_seq_part(line))
    except Exception as e:
        # 读取出错时返回空序列（调用处可打印警告）
        return ''
    return ''.join(parts)

def convert_seq_to_fasta(input_folder, output_folder, tans_number):
    os.makedirs(output_folder, exist_ok=True)

    seq_files = sorted([f for f in os.listdir(input_folder) if f.lower().endswith('.seq')])
    num_fasta_files = 0

    for i in range(0, len(seq_files), tans_number):
        fasta_filename = f'sequences_{i // tans_number + 1}.fasta'
        fasta_filepath = os.path.join(output_folder, fasta_filename)

        with open(fasta_filepath, 'w', encoding='utf-8') as fasta_file:
            for j in range(i, min(i + tans_number, len(seq_files))):
                seq_file = seq_files[j]
                filename_base = os.path.splitext(seq_file)[0]
                label = _label_from_filename(seq_file)  # 仍然用文件名（或括号内）作为输出 header

                seq_path = os.path.join(input_folder, seq_file)
                sequence = _parse_seq_file(seq_path, filename_base)

                if not sequence:
                    print(f'警告: 文件 {seq_file} 未解析到有效序列，已跳过。')
                    continue

                # 写入：header + 单行序列（如需换行包装可改写这里）
                fasta_file.write(f'>{label}\n')
                fasta_file.write(f'{sequence}\n')

        num_fasta_files += 1

    print(f'成功生成{num_fasta_files}个.fasta文件，保存在 {output_folder} 中。')
