import os
import json
import re

solutions_dir = r'c:\Users\AnSeL\OneDrive\Desktop\2026年程序设计实践例题题解\docs\solutions'
html_file = r'c:\Users\AnSeL\OneDrive\Desktop\2026年程序设计实践例题题解\docs\ojsolutions.html'

solution_files = {
    '44': '44.md',
    '45': '45.md',
    '46': '46.md',
    '47': '47.md'
}

for problem_id, filename in solution_files.items():
    filepath = os.path.join(solutions_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    title_match = re.search(r'^#\s+(.*)$', md_content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else f'题目{problem_id}'
    
    html_content = md_content
    
    html_content = html_content.replace('\r\n', '\n')
    
    html_content = re.sub(r'^#\s+(.*)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^##\s+(.*)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^###\s+(.*)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    
    html_content = re.sub(r'```(\w*)\n([\s\S]*?)```', r'<pre><code class="lang-\1">\2</code></pre>', html_content)
    
    html_content = re.sub(r'`([^`]+)`', r'<code>\1</code>', html_content)
    
    html_content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html_content)
    
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
    
    solution_files[problem_id] = {
        'title': title,
        'content': html_content
    }
    print(f"处理题目 {problem_id}: {title}")

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('const problems = [')
end = content.find('];', start) + 2

if start == -1 or end == -1:
    print("找不到 problems 数组")
    exit(1)

problems_json = content[start:end]

fixed_json = problems_json.replace('\n', '').replace('\r', '')

try:
    problems = json.loads(fixed_json)
    print(f"\n当前题目数量: {len(problems)}")
    
    for p in problems:
        pid = p['id']
        if pid in solution_files:
            p['title'] = solution_files[pid]['title']
            p['content'] = solution_files[pid]['content']
            print(f"更新题目 {pid}: {p['title']}")
    
    updated_json = json.dumps(problems, ensure_ascii=False)
    
    new_content = content[:start] + updated_json + content[end:]
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"\n更新成功！文件大小: {len(new_content)} 字节")
    
except Exception as e:
    print(f"错误: {e}")
