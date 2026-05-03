# 🔐 API 密钥安全配置指南

## ⚠️ 重要提示

**绝对不要将 API Key 直接写在代码中并提交到 GitHub！**

为了保护您的 API 密钥安全，我们使用 `.env` 文件来存储敏感信息。

---

## 📋 配置步骤

### 1. 创建 .env 文件

项目根目录已包含 `.env.example` 模板文件，请复制并重命名：

```bash
# Windows PowerShell
Copy-Item .env.example .env

# 或者手动创建 .env 文件
```

### 2. 编辑 .env 文件

打开 `.env` 文件，填入您的真实 API Key：

```env
# 火山方舟 API 配置
VOLCANO_API_KEY=你的真实API密钥
VOLCANO_REGION=cn-beijing
VOLCANO_MODEL_ID=doubao-seed-2-0-pro-260215
```

### 3. 验证配置

运行脚本测试配置是否正确：

```bash
python generate_all_articles.py
```

如果看到 "✅ 火山方舟API连接成功"，说明配置正确！

---

## 🔒 安全保护

### .gitignore 已配置

`.gitignore` 文件已包含以下规则，确保 `.env` 文件不会被提交到 Git：

```gitignore
# 环境变量文件（包含敏感信息）
.env
```

### 检查清单

在提交代码到 GitHub 之前，请确认：

- ✅ `.env` 文件存在且包含正确的 API Key
- ✅ `.gitignore` 文件包含 `.env` 规则
- ✅ 代码中没有硬编码的 API Key
- ✅ 运行 `git status` 时看不到 `.env` 文件

---

## 📁 相关文件

| 文件 | 用途 | 是否提交到Git |
|------|------|--------------|
| `.env` | 存储真实的 API Key | ❌ **不提交** |
| `.env.example` | API 配置模板 | ✅ **提交** |
| `.gitignore` | Git 忽略规则 | ✅ **提交** |
| `generate_all_articles.py` | 从环境变量读取配置 | ✅ **提交** |

---

## 🚀 首次使用

### 新用户配置流程

1. **克隆仓库后**
   ```bash
   git clone <repository-url>
   cd mechanics-abc-website
   ```

2. **复制配置文件**
   ```bash
   cp .env.example .env
   ```

3. **编辑 .env 文件**
   - 用文本编辑器打开 `.env`
   - 填入您的 API Key

4. **安装依赖**
   ```bash
   pip install python-dotenv requests
   ```

5. **开始使用**
   ```bash
   python generate_all_articles.py
   ```

---

## 💡 常见问题

### Q1: 为什么不能直接把 API Key 写在代码里？

**A:** 
- ❌ 安全风险：代码提交到公开仓库后，任何人都能看到您的 API Key
- ❌ 滥用风险：他人可能盗用您的 API Key，产生高额费用
- ❌ 难以管理：更换 API Key 需要修改代码并重新提交

### Q2: .env 文件丢失了怎么办？

**A:** 
1. 复制 `.env.example` 为 `.env`
2. 重新填入您的 API Key
3. 继续正常使用

### Q3: 如何确认 .env 没有被提交到 Git？

**A:** 
运行以下命令检查：
```bash
git status
```

如果输出中**没有** `.env` 文件，说明配置正确。

### Q4: 团队成员如何获取配置？

**A:** 
- 分享 `.env.example` 文件（已包含在仓库中）
- 每个成员自行创建 `.env` 并填入自己的 API Key
- **永远不要**分享真实的 `.env` 文件

---

## 🔍 检查代码安全性

运行以下命令检查是否有硬编码的 API Key：

```bash
# 搜索代码中的 API Key
grep -r "your_api_key_here" .
grep -r "API_KEY.*=" *.py
```

如果只在 `.env` 文件中找到，说明配置安全！

---

## ✨ 最佳实践

1. **永远不要**将 `.env` 文件提交到版本控制系统
2. **定期更新** `.env.example` 以反映新的配置项
3. **使用强密码**和 API Key，定期轮换
4. **限制 API Key 权限**，只授予必要的访问权限
5. **监控 API 使用情况**，及时发现异常

---

## 📞 需要帮助？

如果遇到问题：

1. 检查 `.env` 文件格式是否正确
2. 确认 `python-dotenv` 已安装
3. 查看控制台错误信息
4. 参考 `.env.example` 示例

---

**保护好您的 API Key，就是保护您的账户安全！** 🔐

© 2026 机械知识科普站
