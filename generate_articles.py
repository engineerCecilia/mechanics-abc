# -*- coding: utf-8 -*-
"""
批量生成机械知识科普网站的文章页面
"""

import os

# 定义所有分类和文章数据
categories = {
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

def generate_article_html(cat_id, cat_title, article_index, article_title, total_articles):
    """生成单篇文章的HTML内容"""
    
    # 计算上一篇和下一篇
    prev_link = ""
    next_link = ""
    
    if article_index > 1:
        prev_num = article_index - 1
        prev_title = categories[cat_id]["articles"][prev_num - 1]
        prev_link = f'<a href="article{prev_num:02d}.html">← 上一篇：{prev_title}</a>'
    
    if article_index < total_articles:
        next_num = article_index + 1
        next_title = categories[cat_id]["articles"][next_num - 1]
        next_link = f'<a href="article{next_num:02d}.html">下一篇：{next_title} →</a>'
    
    # 构建导航链接
    nav_items = []
    for cid, cdata in categories.items():
        short_name = cdata["title"].split("、")[1][:4]  # 提取简短名称
        active = 'active' if cid == cat_id else ''
        nav_items.append(f'<a href="../../categories/{cid}/index.html" class="nav-item {active}">{short_name}</a>')
    
    nav_html = '\n            '.join(nav_items)
    
    html_content = f'''<!DOCTYPE html>
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
            {nav_html}
        </div>
    </nav>

    <div class="container">
        <div class="article-content">
            <h1>{article_index}. {article_title}</h1>
            
            <div class="highlight-box">
                <strong>📖 文章说明：</strong>这是一篇关于"{article_title}"的科普文章，正在编写中...
            </div>

            <h2>核心概念</h2>
            <p>这里是关于"{article_title}"的详细讲解内容。文章将用通俗易懂的语言，配合生活中的例子，帮助零基础的朋友快速理解这个机械知识点。</p>

            <h2>详细讲解</h2>
            <p>文章内容将包括：</p>
            <ul>
                <li>基本概念解释</li>
                <li>工作原理说明</li>
                <li>实际应用场景</li>
                <li>常见问题解答</li>
            </ul>

            <div class="tip-box">
                <strong>💡 学习提示：</strong>建议先理解基本概念，再结合实际生活中的例子来加深记忆。
            </div>

            <h2>实际应用</h2>
            <p>在我们的日常生活和工业生产中，这个知识点有着广泛的应用。通过理解它，你可以更好地认识和使用各种机械设备。</p>

            <div class="article-nav">
                <a href="index.html">← 返回分类列表</a>
                {prev_link}
                {next_link}
            </div>
        </div>

        <div class="footer">
            <p>© 2026 机械知识科普站 | 让机械知识变得简单易懂</p>
        </div>
    </div>
</body>
</html>'''
    
    return html_content

def main():
    """主函数：生成所有文章页面"""
    base_path = r"d:\92 html办公小工具\04 mechanics-abc-website\categories"
    
    total_count = 0
    
    for cat_id, cat_data in categories.items():
        cat_path = os.path.join(base_path, cat_id)
        
        # 确保目录存在
        if not os.path.exists(cat_path):
            os.makedirs(cat_path)
        
        print(f"正在处理分类：{cat_data['title']}")
        
        for idx, article_title in enumerate(cat_data["articles"], 1):
            filename = f"article{idx:02d}.html"
            filepath = os.path.join(cat_path, filename)
            
            html_content = generate_article_html(
                cat_id, 
                cat_data["title"], 
                idx, 
                article_title,
                len(cat_data["articles"])
            )
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            total_count += 1
            print(f"  ✓ 已生成：{filename} - {article_title}")
    
    print(f"\n✅ 完成！共生成 {total_count} 篇文章页面")

if __name__ == "__main__":
    main()
