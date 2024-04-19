#!/bin/zsh
echo "请输入Excel文件路径："
read excel_path
 
python3 py2gds.py "$excel_path" 
