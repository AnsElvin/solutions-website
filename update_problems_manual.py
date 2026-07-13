import os
import re
import json

solutions_dir = r'c:\Users\AnSeL\OneDrive\Desktop\2026年程序设计实践例题题解\docs\solutions'
source_file = r'c:\Users\AnSeL\OneDrive\Desktop\2026年程序设计实践例题题解\docs\all-solutions.html'
output_file = r'c:\Users\AnSeL\OneDrive\Desktop\2026年程序设计实践例题题解\docs\ojsolutions.html'

with open(source_file, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"原始文件长度: {len(content)}")

start_marker = 'const problems = ['
start_idx = content.find(start_marker)
array_start = start_idx + len(start_marker)

json_str = content[array_start:]

objects = []
i = 0
while i < len(json_str):
    if json_str[i] == '{':
        depth = 1
        j = i + 1
        while j < len(json_str) and depth > 0:
            if json_str[j] == '"':
                k = j + 1
                escaped = False
                while k < len(json_str):
                    if json_str[k] == '\\' and not escaped:
                        escaped = True
                        k += 1
                    elif json_str[k] == '"' and not escaped:
                        break
                    else:
                        escaped = False
                        k += 1
                j = k + 1
                continue
            if json_str[j] == '{':
                depth += 1
            elif json_str[j] == '}':
                depth -= 1
            j += 1
        
        obj_str = json_str[i:j]
        obj = json.loads(obj_str)
        objects.append((i, j, obj))
        
        i = j
        
        if i < len(json_str) and json_str[i] == ',':
            i += 1
        elif i < len(json_str) and json_str[i] == ']':
            break
        else:
            break
    else:
        i += 1

print(f"共解析 {len(objects)} 个对象")

def md_to_html(md_content):
    html_content = md_content.replace('\r\n', '\n')
    html_content = re.sub(r'^#\s+(.*)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^##\s+(.*)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^###\s+(.*)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'```(\w*)\n([\s\S]*?)```', r'<pre><code class="lang-\1">\2</code></pre>', html_content)
    html_content = re.sub(r'`([^`]+)`', r'<code>\1</code>', html_content)
    html_content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html_content)
    html_content = re.sub(r'^(\d+)\.\s+(.*)$', r'<p>\1. \2</p>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^- \s+(.*)$', r'<p>• \1</p>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^> (.*)$', r'<blockquote>\1</blockquote>', html_content, flags=re.MULTILINE)
    
    lines = html_content.split('\n')
    result_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            result_lines.append('')
        elif stripped.startswith('<'):
            result_lines.append(line)
        else:
            result_lines.append(f'<p>{line}</p>')
    
    html_content = '\n'.join(result_lines)
    html_content = html_content.replace('\n\n', '\n')
    
    return html_content

updated_count = 0
new_objects = []

for start, end, obj in objects:
    pid = obj.get('id', '')
    num = int(pid) if pid.isdigit() else 0
    
    if 44 <= num <= 48:
        filename = f'{num:02d}.md'
        filepath = os.path.join(solutions_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            title_match = re.search(r'^#\s+(.*)$', md_content, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else f'题目{num}'
            
            if num <= 40:
                section = f'{((num-1)//10)*10+1}-{((num-1)//10)*10+10}'
            else:
                section = '41-48'
            
            html_content = md_to_html(md_content)
            
            new_obj = {
                'id': pid,
                'section': section,
                'title': title,
                'content': html_content
            }
            new_objects.append(new_obj)
            print(f"已更新题目 {num}: {title}")
            updated_count += 1
        else:
            new_objects.append(obj)
            print(f"题目 {num} 文件不存在，保持原样")
    else:
        new_objects.append(obj)

new_problems_json = json.dumps(new_objects, ensure_ascii=False)

before = content[:array_start]
after = content[array_start + end + 1:]

final_html = before + new_problems_json + after

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(final_html)

print(f"\n更新完成！文件大小: {len(final_html)} 字节")
print(f"共更新 {updated_count} 个题目")

with open(output_file, 'r', encoding='utf-8') as f:
    check_content = f.read()

if '最低位位置' in check_content:
    print("验证: 第45题内容已更新")
else:
    print("验证: 第45题内容未更新！")

if '真假记忆碎片' in check_content:
    print("验证: 第46题内容已更新")
else:
    print("验证: 第46题内容未更新！")

if '寻找林克的回忆(1)' in check_content:
    print("验证: 第47题内容已更新")
else:
    print("验证: 第47题内容未更新！")

if '寻找林克的回忆(2)' in check_content:
    print("验证: 第48题内容已更新")
else:
    print("验证: 第48题内容未更新！")
