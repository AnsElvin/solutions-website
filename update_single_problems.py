import os
import re

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
    
    html_content = html_content.replace('&', '&amp;')
    html_content = html_content.replace('<', '&lt;')
    html_content = html_content.replace('>', '&gt;')
    html_content = html_content.replace('"', '&quot;')
    html_content = html_content.replace("'", '&#39;')
    
    html_content = html_content.replace('&lt;h1&gt;', '<h1>')
    html_content = html_content.replace('&lt;/h1&gt;', '</h1>')
    html_content = html_content.replace('&lt;h2&gt;', '<h2>')
    html_content = html_content.replace('&lt;/h2&gt;', '</h2>')
    html_content = html_content.replace('&lt;h3&gt;', '<h3>')
    html_content = html_content.replace('&lt;/h3&gt;', '</h3>')
    html_content = html_content.replace('&lt;pre&gt;', '<pre>')
    html_content = html_content.replace('&lt;/pre&gt;', '</pre>')
    html_content = html_content.replace('&lt;code', '<code')
    html_content = html_content.replace('&lt;/code&gt;', '</code>')
    html_content = html_content.replace('&lt;p&gt;', '<p>')
    html_content = html_content.replace('&lt;/p&gt;', '</p>')
    html_content = html_content.replace('&lt;strong&gt;', '<strong>')
    html_content = html_content.replace('&lt;/strong&gt;', '</strong>')
    html_content = html_content.replace('&lt;table&gt;', '<table>')
    html_content = html_content.replace('&lt;/table&gt;', '</table>')
    html_content = html_content.replace('&lt;thead&gt;', '<thead>')
    html_content = html_content.replace('&lt;/thead&gt;', '</thead>')
    html_content = html_content.replace('&lt;tbody&gt;', '<tbody>')
    html_content = html_content.replace('&lt;/tbody&gt;', '</tbody>')
    html_content = html_content.replace('&lt;tr&gt;', '<tr>')
    html_content = html_content.replace('&lt;/tr&gt;', '</tr>')
    html_content = html_content.replace('&lt;th&gt;', '<th>')
    html_content = html_content.replace('&lt;/th&gt;', '</th>')
    html_content = html_content.replace('&lt;td&gt;', '<td>')
    html_content = html_content.replace('&lt;/td&gt;', '</td>')
    html_content = html_content.replace('&lt;blockquote&gt;', '<blockquote>')
    html_content = html_content.replace('&lt;/blockquote&gt;', '</blockquote>')
    
    return html_content

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

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
        
        pattern = rf'"id":"{pid}","section":"[^"]+","title":"[^"]+","content":"[^"]+"'
        replacement = f'"id":"{pid}","section":"{section}","title":"{title}","content":"{html_content}"'
        
        old_len = len(content)
        content = re.sub(pattern, replacement, content)
        new_len = len(content)
        
        if old_len != new_len:
            print(f"已更新题目 {num}: {title}")
        else:
            print(f"警告: 题目 {num} 未找到或未更新")

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n更新完成！")

with open(html_file, 'r', encoding='utf-8') as f:
    check_content = f.read()

if '最低位位置' in check_content:
    print("验证: 第45题内容已更新")
else:
    print("验证: 第45题内容未更新！")
