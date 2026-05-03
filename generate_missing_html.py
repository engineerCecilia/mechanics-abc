# -*- coding: utf-8 -*-
"""
将 Markdown 文件转换为 HTML，并更新分类页面链接
"""

import os
import re
from pathlib import Path

BASE_DIR = r"d:\92 html办公小工具\04 mechanics-abc-website"
CATEGORIES_DIR = os.path.join(BASE_DIR, "categories")

def markdown_to_html_content(md_content, article_title):
    """简单的 Markdown 转 HTML 内容"""
    html_lines = []
    lines = md_content.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if not line:
            i += 1
            continue
        
        # 跳过第一个 H1 标题（已经在模板中）
        if line.startswith('# ') and i == 0:
            i += 1
            continue
        
        # 处理 H2 标题
        if line.startswith('## '):
            title = line[3:].strip()
            html_lines.append(f'<h2>{title}</h2>')
        
        # 处理列表
        elif line.startswith('- ') or line.startswith('* '):
            if not html_lines or html_lines[-1] != '<ul>':
                html_lines.append('<ul>')
            item = line[2:].strip()
            html_lines.append(f'  <li>{item}</li>')
            j = i + 1
            while j < len(lines) and (lines[j].strip().startswith('- ') or lines[j].strip().startswith('* ')):
                item = lines[j].strip()[2:].strip()
                html_lines.append(f'  <li>{item}</li>')
                j += 1
            html_lines.append('</ul>')
            i = j - 1
        
        elif re.match(r'^\d+\.\s', line):
            if not html_lines or html_lines[-1] != '<ol>':
                html_lines.append('<ol>')
            parts = line.split('. ', 1)
            if len(parts) == 2:
                item = parts[1].strip()
                html_lines.append(f'  <li>{item}</li>')
            j = i + 1
            while j < len(lines):
                stripped = lines[j].strip()
                if re.match(r'^\d+\.\s', stripped):
                    parts = stripped.split('. ', 1)
                    if len(parts) == 2:
                        item = parts[1].strip()
                        html_lines.append(f'  <li>{item}</li>')
                    j += 1
                else:
                    break
            html_lines.append('</ol>')
            i = j - 1
        
        # 处理段落
        else:
            paragraph = line
            j = i + 1
            while j < len(lines) and lines[j].strip() and not lines[j].strip().startswith('#') and not lines[j].strip().startswith('- ') and not lines[j].strip().startswith('* ') and not re.match(r'^\d+\.\s', lines[j].strip()):
                paragraph += ' ' + lines[j].strip()
                j += 1
            html_lines.append(f'<p>{paragraph}</p>')
            i = j - 1
        
        i += 1
    
    return '\n'.join(html_lines)

def create_article_html(category_id, article_index, article_title, md_content):
    """创建文章 HTML 文件"""
    category_path = os.path.join(CATEGORIES_DIR, category_id)
    html_filename = f"article{article_index:02d}.html"
    html_filepath = os.path.join(category_path, html_filename)
    
    # 如果已存在且不为空，跳过
    if os.path.exists(html_filepath) and os.path.getsize(html_filepath) > 1000:
        print(f"   ⏭️  跳过（已存在）：{html_filename}")
        return True
    
    # 转换 Markdown 为 HTML
    html_body = markdown_to_html_content(md_content, article_title)
    
    # 读取模板（使用已有的 article01.html 作为模板）
    template_path = os.path.join(category_path, "article01.html")
    if not os.path.exists(template_path):
        # 如果没有模板，使用通用模板
        template_html = get_default_template(article_title, category_id, article_index)
    else:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_html = f.read()
    
    # 替换标题和内容
    template_html = re.sub(r'<title>.*?</title>', f'<title>{article_title} - 机械知识科普</title>', template_html)
    template_html = re.sub(r'<h1>.*?</h1>', f'<h1>{article_index}. {article_title}</h1>', template_html, count=1)
    
    # 替换内容区域
    start_marker = '<div class="article-content">'
    end_marker = '<div class="article-nav">'
    
    start_idx = template_html.find(start_marker)
    end_idx = template_html.find(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        # 保留 h1 标题
        h1_start = template_html.find('<h1>', start_idx)
        h1_end = template_html.find('</h1>', h1_start) + 5
        
        new_content = template_html[start_idx:h1_end] + '\n            \n' + html_body + '\n            '
        updated_html = template_html[:start_idx] + new_content + template_html[end_idx:]
        
        with open(html_filepath, 'w', encoding='utf-8') as f:
            f.write(updated_html)
        
        print(f"   ✅ 已生成：{html_filename}")
        return True
    
    return False

def get_default_template(article_title, category_id, article_index):
    """获取默认模板"""
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article_title} - 机械知识科普</title>
    <link rel="stylesheet" href="../../css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <a href="../../index.html" class="nav-item">首页</a>
            <a href="../category01/index.html" class="nav-item">基础概念</a>
            <a href="../category02/index.html" class="nav-item">轴承类</a>
            <a href="../category03/index.html" class="nav-item">齿轮齿条</a>
            <a href="../category04/index.html" class="nav-item">减速器</a>
            <a href="../category05/index.html" class="nav-item">传送带</a>
            <a href="../category06/index.html" class="nav-item">润滑油品</a>
            <a href="../category07/index.html" class="nav-item">电机动力</a>
            <a href="../category08/index.html" class="nav-item">连杆结构</a>
            <a href="../category09/index.html" class="nav-item">密封紧固</a>
            <a href="../category10/index.html" class="nav-item">气动液压</a>
            <a href="../category11/index.html" class="nav-item">常见故障</a>
            <a href="../category12/index.html" class="nav-item">生活机械</a>
        </div>
    </nav>

    <div class="container">
        <div class="article-content">
            <h1>{article_index}. {article_title}</h1>
            
            <div class="article-nav">
                <a href="index.html">← 返回分类列表</a>
            </div>
        </div>

        <div class="footer">
            <p>© 2026 机械知识科普站 | 让机械知识变得简单易懂</p>
        </div>
    </div>
</body>
</html>'''

def update_category_index(category_id, articles):
    """更新分类页面的 index.html，使文章标题可点击"""
    category_path = os.path.join(CATEGORIES_DIR, category_id)
    index_path = os.path.join(category_path, "index.html")
    
    if not os.path.exists(index_path):
        print(f"   ⚠️  分类页面不存在：{index_path}")
        return
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新每个文章项，添加链接
    for idx, article_title in enumerate(articles, 1):
        old_link = f'<div class="article-item"><a href="article{idx:02d}.html">{idx}. {article_title}</a></div>'
        # 检查是否已经是链接格式
        if f'article{idx:02d}.html' not in content:
            # 查找并替换
            pattern = rf'<div class="article-item">\s*{idx}\. {re.escape(article_title)}\s*</div>'
            replacement = f'<div class="article-item"><a href="article{idx:02d}.html">{idx}. {article_title}</a></div>'
            content = re.sub(pattern, replacement, content)
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"   ✅ 已更新分类页面链接")

def main():
    """主函数"""
    print("=" * 60)
    print("🔄 生成缺失的 HTML 文件并更新链接")
    print("=" * 60)
    
    # 遍历所有分类
    for category_dir in sorted(os.listdir(CATEGORIES_DIR)):
        category_path = os.path.join(CATEGORIES_DIR, category_dir)
        
        if not os.path.isdir(category_path):
            continue
        
        print(f"\n📂 处理分类：{category_dir}")
        
        # 读取该分类下的所有 .md 文件
        md_files = {}
        for filename in sorted(os.listdir(category_path)):
            if filename.endswith('.md'):
                match = re.match(r'article(\d+)\.md', filename)
                if match:
                    article_index = int(match.group(1))
                    md_files[article_index] = filename
        
        if not md_files:
            print(f"   ℹ️  没有找到 .md 文件")
            continue
        
        # 读取 topics.md 获取文章标题
        topics_path = os.path.join(BASE_DIR, "topics.md")
        articles = []
        current_category = None
        
        with open(topics_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('## '):
                    current_category = line.strip()
                elif line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.')):
                    if category_dir in ['category01'] and '一、机械最基础' in current_category:
                        articles.append(line.strip())
                    elif category_dir in ['category02'] and '二、轴承类' in current_category:
                        articles.append(line.strip())
                    elif category_dir in ['category03'] and '三、齿轮' in current_category:
                        articles.append(line.strip())
                    elif category_dir in ['category04'] and '四、减速器' in current_category:
                        articles.append(line.strip())
                    elif category_dir in ['category05'] and '五、传送带' in current_category:
                        articles.append(line.strip())
                    elif category_dir in ['category06'] and '六、润滑' in current_category:
                        articles.append(line.strip())
                    elif category_dir in ['category07'] and '七、电机' in current_category:
                        articles.append(line.strip())
                    elif category_dir in ['category08'] and '八、连杆' in current_category:
                        articles.append(line.strip())
                    elif category_dir in ['category09'] and '九、密封' in current_category:
                        articles.append(line.strip())
                    elif category_dir in ['category10'] and '十、气动' in current_category:
                        articles.append(line.strip())
                    elif category_dir in ['category11'] and '十一、机械常见故障' in current_category:
                        articles.append(line.strip())
                    elif category_dir in ['category12'] and '十二、生活中的机械' in current_category:
                        articles.append(line.strip())
        
        # 为每个 .md 文件生成 HTML
        for article_index in sorted(md_files.keys()):
            md_filename = md_files[article_index]
            md_filepath = os.path.join(category_path, md_filename)
            
            with open(md_filepath, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # 提取文章标题（去掉开头的 "1. "）
            first_line = md_content.split('\n')[0]
            article_title = re.sub(r'^#\s*\d+\.\s*', '', first_line).strip()
            
            create_article_html(category_dir, article_index, article_title, md_content)
        
        # 更新分类页面链接
        if articles:
            update_category_index(category_dir, articles)
    
    print(f"\n{'='*60}")
    print("✅ 完成！所有 HTML 文件已生成，链接已更新")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
