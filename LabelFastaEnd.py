# 主要用于在fasta文件的id行末尾添加上自定义字符

def add_string_to_fasta(input_file, output_file, custom_string):
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            if line.startswith('>'):
                # 如果是ID行，添加自定义字符串
                line = line.strip() + custom_string + '\n'
            f_out.write(line)


# # 用法示例
# input_file = 'shi_rhizo.fasta'
# output_file = 'shi_rhizo_labeled.fasta'
# custom_string = '_shiRhizo'
# add_string_to_fasta(input_file, output_file, custom_string)
