import base64
import sys

def add_appendix_with_images(html_path, image_paths):
    img_tags = []
    for i, image_path in enumerate(image_paths, 1):
        with open(image_path, 'rb') as img_file:
            img_data = img_file.read()
            img_base64 = base64.b64encode(img_data).decode('utf-8')
        
        img_ext = image_path.split('.')[-1].lower()
        if img_ext == 'jpg':
            img_ext = 'jpeg'
        
        img_tag = f'<img src="data:image/{img_ext};base64,{img_base64}" alt="解题完成截图{i}" style="max-width: 100%; border-radius: 8px; margin-bottom: 15px;" />'
        img_tags.append(img_tag)
    
    images_html = '\n'.join(img_tags)
    
    appendix_section = f'''
</section>

<section id="appendix" data-s="all">
<h1>附录：解题完成记录</h1>
<p style="text-align: center; margin: 20px 0;">
{images_html}
</p>
<p style="text-align: center; color: #22d3ee;">以上图片记录了55道题全部完成的状态</p>
</section>
'''
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('</section>\n\n<div class="f">', appendix_section + '\n\n<div class="f">')
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'附录已成功添加到 {html_path}')
    for i, image_path in enumerate(image_paths, 1):
        img_size = len(open(image_path, 'rb').read())
        print(f'图片{i}：{image_path}，大小：{img_size / 1024:.2f} KB')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('用法：python add_appendix.py <all-solutions.html路径> <图片1路径> [图片2路径] [图片3路径]')
        sys.exit(1)
    
    html_path = sys.argv[1]
    image_paths = sys.argv[2:]
    add_appendix_with_images(html_path, image_paths)

