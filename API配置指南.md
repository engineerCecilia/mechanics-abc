# 🔧 火山方舟API配置指南

## ❗ 当前问题

脚本运行时返回404错误：
```
The model or endpoint doubao-pro-32k does not exist or you do not have access to it
```

这说明 **MODEL_ID 配置不正确**，需要修改为您账户下可用的模型或接入点。

---

## ✅ 解决方案

### 步骤1：登录火山引擎控制台

访问：https://console.volcengine.com/ark/region:ark+cn-beijing/endpoint

使用您的账号登录。

### 步骤2：查看推理接入点

1. 在左侧菜单找到 **"推理接入点"** 或 **"Endpoint"**
2. 查看您已创建的接入点列表
3. 找到状态为 **"运行中"** 的接入点

### 步骤3：复制接入点ID

接入点ID格式通常为：`ep-xxxxxxxxxxxxxxxxxxxxxxxxxxx`

例如：`ep-20240512xxxxx`

### 步骤4：修改脚本配置

打开 `generate_all_articles.py` 文件，找到第18-30行：

```python
# ⚠️ 重要：请根据您的火山方舟账户配置修改以下参数
# 选项1：使用模型ID（如果您有直接访问权限）
# MODEL_ID = "ep-xxxxxxxxxxxxx"  # 替换为您的endpoint ID

# 选项2：使用常见的模型ID（需要确认您的账户是否有权访问）
MODEL_ID = "doubao-pro-32k"  # 如果这个不行，尝试下面的
```

**修改为：**

```python
MODEL_ID = "ep-您的实际接入点ID"  # 例如：ep-20240512xxxxx
```

### 步骤5：重新运行脚本

保存文件后，重新执行：
```bash
python generate_all_articles.py
```

---

## 📋 如果没有接入点怎么办？

### 创建新的推理接入点

1. 在火山方舟控制台，点击 **"创建接入点"**
2. 选择模型：
   - 推荐：**Doubao-pro**（质量好）
   - 或者：**Doubao-lite**（速度快，成本低）
3. 配置参数（可使用默认值）
4. 点击创建，等待部署完成
5. 复制生成的接入点ID

---

## 🔍 常见模型ID参考

如果您使用的是公开模型（非私有接入点），可以尝试以下ID：

| 模型名称 | 模型ID | 说明 |
|---------|--------|------|
| Doubao-pro-32k | `doubao-pro-32k` | 高质量，32k上下文 |
| Doubao-lite-32k | `doubao-lite-32k` | 快速响应，32k上下文 |
| Doubao-pro-4k | `doubao-pro-4k` | 高质量，4k上下文 |

⚠️ **注意**：这些公开模型ID需要您的账户有相应权限才能使用。

---

## 💡 快速测试配置是否正确

创建一个测试文件 `test_api.py`：

```python
import requests

API_KEY = "your_api_key_here"
MODEL_ID = "ep-您的接入点ID"  # 修改这里

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": MODEL_ID,
    "messages": [
        {"role": "user", "content": "你好"}
    ],
    "max_tokens": 10
}

response = requests.post(
    "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
    headers=headers,
    json=data
)

print(f"状态码：{response.status_code}")
print(f"响应：{response.text}")
```

运行测试：
```bash
python test_api.py
```

如果返回200状态码和正常响应，说明配置正确！

---

## 📞 需要帮助？

如果仍然遇到问题：

1. **检查API密钥是否有效**
   - 登录控制台确认密钥状态
   - 确认密钥未过期

2. **检查网络连接**
   - 确保可以访问 `ark.cn-beijing.volces.com`

3. **查看账户余额**
   - 确认账户有足够的额度

4. **联系火山引擎支持**
   - 提交工单咨询具体的接入点配置

---

## ✨ 配置完成后的预期效果

配置正确后，脚本将：
- ✅ API连接测试通过
- ✅ 自动为61篇文章生成内容
- ✅ 保存Markdown文件
- ✅ 更新HTML页面
- ✅ 约3-5分钟完成全部生成

---

祝您配置顺利！🎉
