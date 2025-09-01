import sys
import os

def deduplicate_terms(input_file, output_file=None):
    """
    对TXT文件中的词条进行去重处理，区分大小写
    
    参数:
        input_file: 输入的TXT文件路径
        output_file: 输出的TXT文件路径，默认为原文件加上"_dedup"后缀
    """
    # 如果未指定输出文件，则在原文件名后添加"_dedup"后缀
    if output_file is None:
        file_name, file_ext = os.path.splitext(input_file)
        output_file = f"{file_name}_dedup{file_ext}"
    
    # 读取文件内容并去重
    seen_terms = set()
    unique_terms = []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                # 保留每行的原始状态（包括换行符），但去除前后空白后判断是否重复
                stripped_line = line.strip()
                # 只处理非空行
                if stripped_line:
                    if stripped_line not in seen_terms:
                        seen_terms.add(stripped_line)
                        unique_terms.append(line)
                else:
                    # 保留空行
                    unique_terms.append(line)
        
        # 写入去重后的内容
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(unique_terms)
        
        print(f"去重完成！")
        print(f"原始词条数: {len(seen_terms) + (len(unique_terms) - len(seen_terms))}")
        print(f"去重后词条数: {len(seen_terms)}")
        print(f"结果已保存至: {output_file}")
        
    except FileNotFoundError:
        print(f"错误: 找不到文件 '{input_file}'")
        sys.exit(1)
    except Exception as e:
        print(f"处理文件时出错: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # 检查命令行参数
    if len(sys.argv) < 2:
        print("用法: python deduplicate_words.py <输入文件路径> [输出文件路径]")
        print("示例: python deduplicate_words.py terms.txt")
        print("示例: python deduplicate_words.py terms.txt unique_terms.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    deduplicate_terms(input_file, output_file)
