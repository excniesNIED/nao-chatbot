import base64
import os
from pathlib import Path

def decode_bin_to_txt():
    # 获取当前目录下所有.bin文件
    bin_files = Path('.').glob('*.bin')
    
    for bin_path in bin_files:
        # 构建输出txt文件路径（与bin文件同名，后缀改为txt）
        txt_path = bin_path.with_suffix('.txt')
        decoded_lines = []
        
        try:
            # 读取bin文件内容（按文本模式读取，假设bin文件内是Base64编码的字符串行）
            with open(bin_path, 'r', encoding='utf-8') as bin_file:
                lines = bin_file.readlines()
            
            for line_num, line in enumerate(lines, 1):
                # 去除行首尾空白字符（包括换行符、空格等）
                raw_line = line.strip()
                if not raw_line:
                    decoded_lines.append('')  # 保留空行
                    continue
                
                try:
                    # 尝试Base64解码
                    decoded_bytes = base64.b64decode(raw_line)
                    # 解码为UTF-8字符串
                    decoded_str = decoded_bytes.decode('utf-8')
                    decoded_lines.append(decoded_str)
                except (base64.binascii.Error, UnicodeDecodeError) as e:
                    # 解码失败时保留原始行，并记录错误
                    print(f"警告：文件 {bin_path} 第 {line_num} 行解码失败 - {e}")
                    decoded_lines.append(raw_line)  # 保留原始内容
            
            # 写入解码后的内容到txt文件
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write('\n'.join(decoded_lines))
            
            print(f"成功处理：{bin_path} -> {txt_path}")
        
        except Exception as e:
            print(f"处理文件 {bin_path} 时出错：{e}")

if __name__ == '__main__':
    decode_bin_to_txt()
    print("所有.bin文件处理完成")