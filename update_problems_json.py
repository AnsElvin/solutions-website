import os
import re
import json

solutions_dir = r'c:\Users\AnSeL\OneDrive\Desktop\2026年程序设计实践例题题解\docs\solutions'
html_file = r'c:\Users\AnSeL\OneDrive\Desktop\2026年程序设计实践例题题解\docs\ojsolutions.html'

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

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = 'const problems = ['
end_marker = '];'

start_idx = content.find(start_marker)
if start_idx == -1:
    print("ERROR: 找不到 'const problems = ['")
    exit(1)

before = content[:start_idx]

array_start = start_idx + len(start_marker)

end_idx = content.find(end_marker, array_start)
if end_idx == -1:
    print("ERROR: 找不到 '];'")
    exit(1)

after = content[end_idx + len(end_marker):]

json_str = content[array_start:end_idx]

try:
    problems_data = json.loads(json_str)
    print(f"成功解析 {len(problems_data)} 个题目")
except json.JSONDecodeError as e:
    print(f"JSON解析错误: {e}")
    exit(1)

for num in [44, 45, 46, 47, 48]:
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
        
        pid = str(num).zfill(2)
        
        found = False
        for i, p in enumerate(problems_data):
            if p.get('id') == pid:
                problems_data[i] = {
                    'id': pid,
                    'section': section,
                    'title': title,
                    'content': html_content
                }
                print(f"已更新题目 {num}: {title}")
                found = True
                break
        if not found:
            print(f"警告: 未找到题目 {pid}")

new_problems_json = json.dumps(problems_data, ensure_ascii=False)

final_html = before + start_marker + new_problems_json + end_marker + after

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(final_html)

print("\n更新完成！")

with open(html_file, 'r', encoding='utf-8') as f:
    check_content = f.read()

if '最低位位置' in check_content:
    print("验证: 第45题内容已更新")
else:
    print("验证: 第45题内容未更新！")

if '真假记忆碎片' in check_content:
    print("验证: 第46题内容已更新")
else:
    print("验证: 第46题内容未更新！")
