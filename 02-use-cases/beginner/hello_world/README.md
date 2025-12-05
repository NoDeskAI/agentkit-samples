# Hello World Demo

## 简介
构建一个最简单的聊天 Agent

## 项目说明
本示例演示了 VeADK 的核心功能：
- **Agent 创建**：使用简单的配置创建 AI Agent
- **短期记忆**：使用本地后端（local backend）存储对话历史，实现会话级别的上下文记忆
- **多轮对话**：通过 session_id 关联对话，Agent 能记住之前的对话内容

## 前置依赖
1. **开通火山方舟模型服务**：前往 [Ark console](https://exp.volcengine.com/ark?mode=chat)
2. **准备 model_api_key**：在控制台获取 **API Key**。

## 运行方法
### 1. 安装veadk和agentkit python sdk 配置环境变量

```bash
uv pip install veadk-python
uv pip install agentkit-sdk-python
```

在 `config.yaml` 中设置你的模型信息：
```yaml
model:
  agent:
    name: doubao-seed-1-6-251015
    api_key: XXXX
```

### 2. 运行本地客户端
```bash
python agent.py
```

### 3. 运行veadk web客户端并使用浏览器登录 http://127.0.0.1:8000
```bash
cd ..
veadk web

```

### 4. 部署到vefaas
> **安全提示：请勿在生产环境中禁用密钥认证。确保 `VEFAAS_ENABLE_KEY_AUTH` 保持为 `true`（或不设置，默认为开启），并正确配置访问密钥和角色。只有在本地受控环境调试时，才可临时关闭认证，并务必加以警告。**

```bash
cd hello_world
# 这一步直接运行即可
export VEFAAS_ENABLE_KEY_AUTH=false
# 这一步需要把YOUR_AK换成自己的ak
export VOLCENGINE_ACCESS_KEY=YOUR_AK
# 这一步需要把YOUR_AK换成自己的sk
export VOLCENGINE_SECRET_KEY=YOUR_SK
# 这一步部署应用到云上
veadk deploy --vefaas-app-name=hello-world --use-adk-web --veapig-instance-name=<your veapig instance name> --iam-role "trn:iam::<your account id>:role/<your iam role name>"

```

### 5. 部署到AgentKit 并且使用client.py测试

```bash
cd hello_world
# Uncomment the following line in agent.py to run the agentkit app server
# agent_server_app.run(host="0.0.0.0", port=8000)
agentkit config
agentkit launch
```

## 示例 Prompt
示例代码展示了一个简单的两轮对话：

**第一轮对话**：
```
输入：我叫VeADK
输出：你好VeADK！很高兴认识你。
```

**第二轮对话**（测试记忆功能）：
```
输入：你还记得我叫什么吗？
输出：当然记得，你叫VeADK。
```

你也可以尝试以下对话：
- "我今年25岁" → "我多大了？"
- "我喜欢编程" → "你知道我的爱好吗？"
- "我住在北京" → "你记得我住在哪里吗？"

这些示例展示了 Agent 如何在同一会话中保持上下文记忆。