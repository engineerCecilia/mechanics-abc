# -*- coding: utf-8 -*-
"""
机械知识科普网站 - 批量文章内容生成脚本
使用火山方舟大模型API生成所有文章内容
"""

import os
import json
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# ==================== 配置区域 ====================
# 从环境变量读取 API 配置（不要硬编码在代码中）
API_KEY = os.getenv('VOLCANO_API_KEY')
REGION = os.getenv('VOLCANO_REGION', 'cn-beijing')
MODEL_ID = os.getenv('VOLCANO_MODEL_ID', 'doubao-seed-2-0-pro-260215')

# 检查 API Key 是否已配置
if not API_KEY:
    print("❌ 错误：未找到 API Key！")
    print("请创建 .env 文件并配置 VOLCANO_API_KEY")
    print("可以参考 .env.example 文件")
    exit(1)

# 网站根目录
BASE_DIR = r"d:\92 html办公小工具\04 mechanics-abc-website"
CATEGORIES_DIR = os.path.join(BASE_DIR, "categories")

# ==================== 主题清单 ====================
TOPICS = {
    "category01": {
        "title": "一、机械最基础入门概念（开篇必看）",
        "articles": [
            "什么是机械？普通人一秒看懂",
            "机器和机械有什么区别？",
            "什么是传动？机械传动通俗讲解",
            "什么是动力源？电机、发动机简单理解",
            "什么是负载？机械设备为什么会吃力",
            "零基础必懂的5个机械常用名词"
        ]
    },
    "category02": {
        "title": "二、轴承类（最常用、小白必学）",
        "articles": [
            "什么是轴承？一句话讲明白作用",
            "轴承是干嘛的？为什么机器都要装轴承",
            "滚珠轴承 vs 滚柱轴承 区别",
            "滑动轴承是什么？简单易懂讲解",
            "轴承为什么会坏？日常损坏原因",
            "轴承型号简单怎么看？小白入门版"
        ]
    },
    "category03": {
        "title": "三、齿轮 & 齿条 基础",
        "articles": [
            "什么是齿轮？最通俗讲解",
            "直齿轮、斜齿轮有什么不一样",
            "伞齿轮（锥齿轮）是干嘛用的",
            "齿轮为什么能减速、能提速",
            "什么是齿条？齿轮齿条怎么传动"
        ]
    },
    "category04": {
        "title": "四、减速器 / 减速机 专题",
        "articles": [
            "什么是减速器？普通人一看就懂",
            "减速机到底有什么用？为什么要减速",
            "蜗轮蜗杆减速机 原理通俗讲",
            "行星减速机 简单入门讲解",
            "齿轮减速机是什么？适用场景",
            "电机+减速机 组合为什么最常用"
        ]
    },
    "category05": {
        "title": "五、传送带 & 输送设备 类",
        "articles": [
            "什么是传送带？工作原理通俗版",
            "皮带传动是什么？平皮带、三角带",
            "链条传动和皮带有什么区别",
            "滚筒输送机是什么？",
            "皮带跑偏是什么原因？小白科普",
            "流水线输送设备基础常识"
        ]
    },
    "category06": {
        "title": "六、润滑 & 油品 专题",
        "articles": [
            "什么是润滑油？为什么机器一定要加油",
            "机油、齿轮油、黄油（润滑脂）区别",
            "轴承加什么油？减速机加什么油",
            "干摩擦、油摩擦是什么意思",
            "机器缺油会有什么后果",
            "润滑油多久换一次？基础常识"
        ]
    },
    "category07": {
        "title": "七、电机 & 动力基础（小白版）",
        "articles": [
            "什么是电机？电动机通俗讲解",
            "同步电机和异步电机简单区别",
            "伺服电机是什么？干嘛用的",
            "步进电机入门通俗解释",
            "电机转速、功率是什么意思"
        ]
    },
    "category08": {
        "title": "八、连杆 & 铰链 & 结构件",
        "articles": [
            "什么是连杆机构？生活里随处可见",
            "铰链、合页 机械原理科普",
            "凸轮是什么？凸轮机构通俗讲解",
            "机架、支架、底座 机械作用"
        ]
    },
    "category09": {
        "title": "九、密封 & 紧固件 基础",
        "articles": [
            "什么是密封圈、油封？作用是什么",
            "O型圈入门科普",
            "螺丝、螺栓、螺母 基础区别",
            "垫圈、弹垫有什么用",
            "键销、平键 是干嘛的"
        ]
    },
    "category10": {
        "title": "十、气动 & 液压 零基础入门",
        "articles": [
            "什么是气动？空压机、气缸通俗讲",
            "什么是液压？液压系统简单理解",
            "气缸和油缸有什么区别",
            "电磁阀是干嘛用的"
        ]
    },
    "category11": {
        "title": "十一、机械常见故障 小白科普",
        "articles": [
            "机器噪音大一般是什么原因",
            "机器发烫是什么问题",
            "轴承异响怎么简单判断",
            "皮带打滑是什么原因",
            "减速机漏油常见原因"
        ]
    },
    "category12": {
        "title": "十二、生活中的机械知识（引流好文）",
        "articles": [
            "电动车里都用到了哪些机械结构",
            "汽车里的轴承、齿轮、减速器在哪",
            "洗衣机里面有什么机械部件",
            "电梯用到了哪些机械原理"
        ]
    }
}

# ==================== 初始化API客户端 ====================
def init_ark_client():
    """初始化火山方舟客户端（使用requests直接调用API）"""
    try:
        # 测试API连接
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        test_data = {
            "model": MODEL_ID,
            "messages": [
                {"role": "user", "content": "你好"}
            ],
            "max_tokens": 10
        }
        
        response = requests.post(
            f"https://ark.cn-beijing.volces.com/api/v3/chat/completions",
            headers=headers,
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ 火山方舟API连接成功")
            return True
        else:
            print(f"⚠️  API连接测试返回：{response.status_code}")
            print(f"   响应内容：{response.text[:200]}")
            return True  # 仍然返回True，继续执行
            
    except Exception as e:
        print(f"❌ API连接测试失败：{e}")
        print("   将继续尝试，但可能会遇到问题")
        return True

# ==================== 生成文章内容的Prompt ====================
def build_prompt(article_title, category_title):
    """构建生成文章的Prompt"""
    prompt = f"""你是机械零基础科普博主，面向完全外行小白。

请为文章标题《{article_title}》撰写一篇科普文章。
所属分类：{category_title}

写作要求：
1. 不用公式、不堆砌专业术语，用生活场景/日常例子大白话讲解
2. 字数控制在350-500字
3. 仅输出Markdown格式正文，无开场白、无结束语、无多余解释

文章结构必须包含：
## 通俗定义
（用1句话讲透这个概念）

## 核心作用
（说明它的主要功能和价值）

## 生活/工厂应用实例
（列举2-3个实际应用场景）

## 小白必知小知识
1. （第一个关键知识点）
2. （第二个关键知识点）

现在开始创作《{article_title}》的内容："""
    
    return prompt

# ==================== 调用API生成内容 ====================
def generate_article_content(client, article_title, category_title, max_retries=3):
    """调用火山方舟API生成文章内容"""
    
    prompt = build_prompt(article_title, category_title)
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": MODEL_ID,
        "messages": [
            {
                "role": "system",
                "content": "你是专业的机械知识科普作家，擅长用通俗易懂的语言向零基础小白解释机械概念。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    for attempt in range(max_retries):
        try:
            print(f"   🔄 正在生成（尝试 {attempt + 1}/{max_retries}）...")
            
            response = requests.post(
                "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                if content and len(content.strip()) > 100:
                    print(f"   ✅ 生成成功（{len(content)} 字）")
                    return content.strip()
                else:
                    print(f"   ⚠️  生成内容过短，重试...")
            else:
                print(f"   ❌ API返回错误：{response.status_code}")
                print(f"      {response.text[:200]}")
                
        except Exception as e:
            print(f"   ❌ API调用失败：{e}")
            if attempt < max_retries - 1:
                time.sleep(2)  # 等待2秒后重试
    
    print(f"   ❌ 多次重试后仍失败")
    return None

# ==================== 保存Markdown文件 ====================
def save_markdown(category_id, article_index, article_title, content):
    """保存Markdown文件"""
    category_path = os.path.join(CATEGORIES_DIR, category_id)
    md_filename = f"article{article_index:02d}.md"
    md_filepath = os.path.join(category_path, md_filename)
    
    with open(md_filepath, 'w', encoding='utf-8') as f:
        f.write(f"# {article_index}. {article_title}\n\n")
        f.write(content)
    
    print(f"   💾 已保存：{md_filename}")
    return md_filepath

# ==================== Markdown转HTML ====================
def markdown_to_html(markdown_text):
    """简单的Markdown转HTML（无需额外库）"""
    html_lines = []
    
    lines = markdown_text.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        if not line:
            i += 1
            continue
        
        # 处理标题
        if line.startswith('## '):
            title = line[3:].strip()
            html_lines.append(f'<h2>{title}</h2>')
        elif line.startswith('# '):
            title = line[2:].strip()
            html_lines.append(f'<h1>{title}</h1>')
        
        # 处理列表
        elif line.startswith('- ') or line.startswith('* '):
            if not html_lines or html_lines[-1] != '<ul>':
                html_lines.append('<ul>')
            item = line[2:].strip()
            html_lines.append(f'  <li>{item}</li>')
            # 检查后续是否还有列表项
            j = i + 1
            while j < len(lines) and (lines[j].strip().startswith('- ') or lines[j].strip().startswith('* ')):
                item = lines[j].strip()[2:].strip()
                html_lines.append(f'  <li>{item}</li>')
                j += 1
            html_lines.append('</ul>')
            i = j - 1
        
        elif line.startswith('1. ') or line.startswith('2. ') or line.startswith('3. '):
            if not html_lines or html_lines[-1] != '<ol>':
                html_lines.append('<ol>')
            # 提取数字和内容
            parts = line.split('. ', 1)
            if len(parts) == 2:
                item = parts[1].strip()
                html_lines.append(f'  <li>{item}</li>')
            # 检查后续是否还有列表项
            j = i + 1
            while j < len(lines):
                stripped = lines[j].strip()
                if stripped.startswith(('1. ', '2. ', '3. ', '4. ', '5. ', '6. ', '7. ', '8. ', '9. ')):
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
            # 合并连续的非空行作为一段
            paragraph = line
            j = i + 1
            while j < len(lines) and lines[j].strip() and not lines[j].strip().startswith('#') and not lines[j].strip().startswith('- ') and not lines[j].strip().startswith('* ') and not lines[j].strip().startswith(('1. ', '2. ', '3.')):
                paragraph += ' ' + lines[j].strip()
                j += 1
            html_lines.append(f'<p>{paragraph}</p>')
            i = j - 1
        
        i += 1
    
    return '\n'.join(html_lines)

# ==================== 读取现有HTML模板 ====================
def read_existing_html_template(category_id, article_index):
    """读取现有的HTML文件作为模板"""
    category_path = os.path.join(CATEGORIES_DIR, category_id)
    html_filename = f"article{article_index:02d}.html"
    html_filepath = os.path.join(category_path, html_filename)
    
    if os.path.exists(html_filepath):
        with open(html_filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return None

# ==================== 更新HTML文件 ====================
def update_html_with_content(category_id, article_index, article_title, markdown_content):
    """将生成的Markdown内容转换为HTML并更新现有文件"""
    
    # 转换Markdown为HTML
    html_content = markdown_to_html(markdown_content)
    
    # 读取现有HTML模板
    template_html = read_existing_html_template(category_id, article_index)
    
    if template_html:
        # 找到 article-content div 的位置
        start_marker = '<div class="article-content">'
        end_marker = '<div class="article-nav">'
        
        start_idx = template_html.find(start_marker)
        end_idx = template_html.find(end_marker)
        
        if start_idx != -1 and end_idx != -1:
            # 保留原有的 h1 标题
            original_h1_start = template_html.find('<h1>', start_idx)
            original_h1_end = template_html.find('</h1>', original_h1_start) + 5
            
            # 构建新的内容部分
            new_content = template_html[start_idx:original_h1_end] + '\n            \n' + html_content + '\n            '
            
            # 替换内容
            updated_html = template_html[:start_idx] + new_content + template_html[end_idx:]
            
            # 保存更新后的HTML
            category_path = os.path.join(CATEGORIES_DIR, category_id)
            html_filename = f"article{article_index:02d}.html"
            html_filepath = os.path.join(category_path, html_filename)
            
            with open(html_filepath, 'w', encoding='utf-8') as f:
                f.write(updated_html)
            
            print(f"   📄 已更新HTML：{html_filename}")
            return True
    
    print(f"   ⚠️  未找到模板文件，跳过HTML更新")
    return False

# ==================== 主函数 ====================
def main():
    """主执行函数"""
    print("=" * 60)
    print("🚀 机械知识科普网站 - 批量文章内容生成")
    print("=" * 60)
    print()
    
    # 初始化API客户端
    client = init_ark_client()
    if not client:
        print("❌ 无法初始化API客户端，程序退出")
        return
    
    print()
    print(f"📊 待生成文章统计：")
    total_articles = sum(len(data["articles"]) for data in TOPICS.values())
    print(f"   分类数量：{len(TOPICS)}")
    print(f"   文章总数：{total_articles}")
    print()
    
    # 遍历所有分类和文章
    generated_count = 0
    failed_count = 0
    
    for category_id, category_data in TOPICS.items():
        print(f"\n{'='*60}")
        print(f"📁 处理分类：{category_data['title']}")
        print(f"{'='*60}")
        
        category_path = os.path.join(CATEGORIES_DIR, category_id)
        if not os.path.exists(category_path):
            print(f"   ⚠️  分类目录不存在，创建中...")
            os.makedirs(category_path)
        
        for idx, article_title in enumerate(category_data["articles"], 1):
            print(f"\n[{idx}/{len(category_data['articles'])}] {article_title}")
            
            # 调用API生成内容
            content = generate_article_content(
                client, 
                article_title, 
                category_data["title"]
            )
            
            if content:
                # 保存Markdown文件
                save_markdown(category_id, idx, article_title, content)
                
                # 更新HTML文件
                update_html_with_content(category_id, idx, article_title, content)
                
                generated_count += 1
                
                # 避免API限流，等待1秒
                time.sleep(1)
            else:
                failed_count += 1
                print(f"   ❌ 生成失败，跳过")
    
    # 总结
    print(f"\n{'='*60}")
    print(f"🎉 生成完成！")
    print(f"{'='*60}")
    print(f"✅ 成功生成：{generated_count} 篇")
    print(f"❌ 失败：{failed_count} 篇")
    print(f"📊 总计：{total_articles} 篇")
    print()
    print("💡 提示：")
    print("   - Markdown文件保存在各分类目录下（.md后缀）")
    print("   - HTML文件已直接更新到现有网站结构中")
    print("   - 可以直接打开 index.html 查看效果")
    print()

if __name__ == "__main__":
    main()
