# FPS-fasta
![Static Badge](https://img.shields.io/badge/Language-Python-green)
![Static Badge](https://img.shields.io/badge/License-GPL--3.0-blue)
---
Fast Process Sequence - fasta

集成了一些快速处理fasta文件的小功能 :P

### 已有功能
- Excel -> fasta：将`Excel`文件中特定行提取为`fasta`文件
- fasta -> Excel：将`fasta`文件根据标签和序列作为`列 (column)`存储为`Excel`文件
- fastaID -> fastaIDxxx：将`fasta`文件标签添加后缀
    - 目前只做了添加后缀。~~前缀什么的以后应该会更新罢，划掉~~
- seq -> fasta：将下机后的`seq`文件批量转为`fasta`文件
    - 可以自定义每个`fasta`中包含`seq`的个数

### 备注
seq -> fasta功能内的输（入）出文件路径选择当前文件夹即可。
其余功能模块，输入文件路径需要选择到具体文件，输出文件路径需要选择到文件夹，同时手动输入文件名与后缀。

