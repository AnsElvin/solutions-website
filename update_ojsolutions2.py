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
    
    return html_content

problems_to_update = ['44', '45', '46', '47']

for pid in problems_to_update:
    filepath = os.path.join(solutions_dir, f'{pid}.md')
    with open(filepath, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    html_content = md_to_html(md_content)
    html_content = html_content.replace('\\', '\\\\')
    html_content = html_content.replace('\n', '\\n')
    html_content = html_content.replace('\r', '')
    
    with open(filepath.replace('.md', '_html.txt'), 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"生成题目 {pid} 的HTML内容")

print("\n请手动将生成的HTML内容替换到ojsolutions.html中")
