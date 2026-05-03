# -*- coding: utf-8 -*-
"""
安全检查脚本 - 确认 API Key 没有硬编码在代码中
"""

import os
import re

def check_for_hardcoded_keys():
    """检查代码中是否有硬编码的 API Key"""
    
    print("=" * 60)
    print("🔍 API Key 安全检查")
    print("=" * 60)
    
    # 要检查的文件
    files_to_check = [
        'generate_all_articles.py',
        'generate_articles.py',
        'generate_missing_html.py',
    ]
    
    # 已知的 API Key（不应该出现在代码中）
    known_api_key = "your_api_key_here"
    
    issues_found = False
    
    for filename in files_to_check:
        if not os.path.exists(filename):
            continue
            
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 检查是否包含完整的 API Key
        if known_api_key in content:
            print(f"\n❌ 发现安全问题：{filename}")
            print(f"   包含硬编码的 API Key！")
            issues_found = True
        
        # 检查是否有类似 API_KEY = "xxx" 的模式
        pattern = r'API_KEY\s*=\s*["\'][a-zA-Z0-9\-]{20,}["\']'
        matches = re.findall(pattern, content)
        if matches:
            print(f"\n⚠️  警告：{filename}")
            for match in matches:
                print(f"   发现可能的 API Key 赋值：{match[:50]}...")
            issues_found = True
    
    if not issues_found:
        print("\n✅ 安全检查通过！")
        print("   没有在代码中发现硬编码的 API Key")
    
    # 检查 .env 文件是否存在
    print("\n" + "=" * 60)
    print("📁 配置文件检查")
    print("=" * 60)
    
    if os.path.exists('.env'):
        print("✅ .env 文件存在")
        
        # 检查 .env 是否在 gitignore 中
        if os.path.exists('.gitignore'):
            with open('.gitignore', 'r', encoding='utf-8') as f:
                gitignore_content = f.read()
            
            if '.env' in gitignore_content:
                print("✅ .env 已在 .gitignore 中（不会被提交到 Git）")
            else:
                print("❌ 警告：.env 不在 .gitignore 中！")
                issues_found = True
    else:
        print("❌ .env 文件不存在")
        print("   请复制 .env.example 为 .env 并配置 API Key")
        issues_found = True
    
    if os.path.exists('.env.example'):
        print("✅ .env.example 模板文件存在")
    
    if os.path.exists('.gitignore'):
        print("✅ .gitignore 文件存在")
    
    # 总结
    print("\n" + "=" * 60)
    if issues_found:
        print("❌ 发现安全问题，请在提交到 GitHub 前修复！")
    else:
        print("✅ 所有安全检查通过！可以安全提交到 GitHub")
    print("=" * 60)
    
    return not issues_found

if __name__ == "__main__":
    check_for_hardcoded_keys()
