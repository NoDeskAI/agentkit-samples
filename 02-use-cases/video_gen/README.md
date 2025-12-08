# 绘本故事视频生成 Agent

## 项目概述

本项目提供一个基于火山引擎 AgentKit 的“成语绘本故事视频生成”Agent。它会根据用户输入的成语故事情节：

- 生成四张卡通风格的分镜插画
- 以相邻分镜为首尾帧生成三段过渡视频
- 通过本地 MCP 工具将三段视频顺序拼接为完整成片
- 上传成片到火山引擎 TOS，并返回可访问的签名 URL

核心组件：

- Agent 服务：`agent.py`，基于 `AgentkitSimpleApp`
- 工具集：图片生成、视频生成、文件下载、视频拼接（MCP）、TOS 上传
- 短期记忆：用于维持对话会话上下文

## 目录结构

```
video_gen/
├── agent.py         # Agent 应用入口，注册 MCP 工具并运行
├── agent.yaml       # Agent 配置：模型、系统指令与工具列表
├── tool/            # 自定义工具
│   ├── file_download.py  # 批量下载文件到本地
│   └── tos_upload.py     # 上传文件到 TOS 并生成签名 URL
├── requirements.txt # Python 依赖列表
├── pyproject.toml   # 项目配置（uv/pip 依赖与元数据）
├── __init__.py      # 包初始化文件
├── .python-version  # Python 版本声明（开发环境）
├── README.md        # 项目说明文档
└── .dockerignore    # Docker 构建忽略文件
```

## 快速开始

### 1. 安装依赖

```bash
cd 02-use-cases/video_gen
# 若未安装 uv，请先安装（任选其一）
# macOS / Linux（官方安装脚本）
curl -LsSf https://astral.sh/uv/install.sh | sh
# 或使用 Homebrew（macOS）
brew install uv

# 初始化项目依赖
uv sync
source .venv/bin/activate
```

额外要求：
- 安装 Node.js 与 npm（用于运行本地 MCP 视频拼接工具）
- 确保本机可使用 `npx`（Node.js 18+ 推荐）

### 2. 准备视频剪辑 MCP 工具

本项目已在 `agent.py` 中集成 MCP 工具，运行时将通过 `npx @pickstar-2002/video-clip-mcp@latest` 启动，无需手动安装。

### 3. 配置环境变量

本地必需的环境变量（用于 TOS 上传）：

```bash
# 务必导出 VOLCENGINE_ACCESS_KEY、VOLCENGINE_SECRET_KEY、DATABASE_TOS_BUCKET 环境变量
export VOLCENGINE_ACCESS_KEY=<Your AK>
export VOLCENGINE_SECRET_KEY=<Your SK>
export DATABASE_TOS_BUCKET=<Your Bucket Name>
# 可选：指定下载目录（不设置则默认使用项目根目录）
export DOWNLOAD_DIR=/tmp # 配置视频下载目录
```

TOS 存储桶说明：

- 默认使用 `tool/tos_upload.py` 中的 `bucket_name="agentkit-platform-{{your account_id}}"`
- 如需自定义，可在调用工具时传入 `bucket_name`，或直接修改 `tool/tos_upload.py` 的默认参数为你的 Bucket 名称

### 4. 启动与部署

#### 配置环境变量

```
export VOLCENGINE_ACCESS_KEY=<Your AK>
export VOLCENGINE_SECRET_KEY=<Your SK>
export DATABASE_TOS_BUCKET=<Your Bucket Name>
```

#### 以本地方式运行（调试）：

```bash
uv run agent.py
# 服务默认监听 0.0.0.0:8000
```

##### 本地调试接口调用示例

1. **获取应用名称**

   通过 `list-apps` 接口获取当前运行的 Agent 名称，该名称与 `agent.yaml` 中的 `name` 保持一致,即 `storybook_illustrator`。

   ```bash
   curl --location 'http://localhost:8000/list-apps'
   ```
2. **创建 Session**

   使用获取到的应用名称（`storybook_illustrator`）创建会话。

   ```bash
   curl --location --request POST 'http://localhost:8000/apps/storybook_illustrator/users/u_123/sessions/s_123' \
   --header 'Content-Type: application/json' \
   --data ''
   ```
3. **发送消息**
   向 Agent 发起请求。

   ```bash
   curl --location 'http://localhost:8000/run_sse' \
   --header 'Content-Type: application/json' \
   --data '{
       "appName": "storybook_illustrator",
       "userId": "u_123",
       "sessionId": "s_123",
       "newMessage": {
           "role": "user",
           "parts": [{
               "text": "请根据寓言《狐假虎威》生成绘本故事视频"
           }]
       },
       "streaming": true
   }'
   ```

##### 使用veadk web命令进行便捷调试

1. **启动veadk web服务**

   ```bash
   cd 02-use-cases/  # 要在use-cases根目录下执行
   veadk web --port 8000
   ```
2. **通过veadk web调用Agent**
   打开浏览器，访问 `http://localhost:8000`，输入 Prompt 后点击“Send”即可调用 Agent。

#### 部署到火山引擎 AgentKit（runtime）：

1. 使用 `agentkit cli`命令部署到火山引擎 AgentKit（runtime）：

```bash
agentkit config \
--agent_name storybook_illustrator \
--entry_point 'agent.py' \
--runtime_envs DATABASE_TOS_BUCKET=<Your Bucket Name> \
--launch_type cloud && agentkit launch
```

2. 部署成功之后进入火山引擎 [AgentKit 控制台](https://console.volcengine.com/agentkit/region:agentkit+cn-beijing/runtime?pageSize=10&currentPage=1)，点击 Runtime 查看部署的智能体 `storybook_illustrator`详情，获取公网访问域名（如`https://xxxxx.apigateway-cn-beijing.volceapi.com`）和Api Key，然后通过一下API进行测试

**创建 Session**
   ```bash
   curl --location --request POST 'https://xxxxx.apigateway-cn-beijing.volceapi.com/apps/storybook_illustrator/users/u_123/sessions/s_124' \
--header 'Content-Type: application/json' \
--header 'Authorization: <your api key>' \
--data ''
   ```
  **发送消息**
   ```bash
   curl --location 'https://xxxxx.apigateway-cn-beijing.volceapi.com/run_sse' \
--header 'Authorization: <your api key>' \
--header 'Content-Type: application/json' \
--data '{
    "appName": "storybook_illustrator",
    "userId": "u_123",
    "sessionId": "s_124",
    "newMessage": {
        "role": "user",
        "parts": [{
        "text": "请根据寓言《狐假虎威》生成绘本故事视频"
        }]
    },
    "streaming": false
}'
   ```

期望行为：

- 自动生成 4 张分镜插画，并基于相邻分镜生成 3 段过渡视频
- 启动本地 MCP 工具拼接为完整视频
- 通过 TOS 上传生成签名 URL，并将该 URL 作为最终响应返回

## 常见问题

- `npx` 不可用或 Node 环境缺失：请安装 Node.js（推荐 18+）与 npm，确保命令行可执行 `npx`。
- TOS 上传失败：确认已设置 `VOLCENGINE_ACCESS_KEY` 与 `VOLCENGINE_SECRET_KEY`，并保证账户拥有目标 Bucket 的访问权限。
- 使用环境变量来指定Bucket DATABASE_TOS_BUCKET="agentkit-platform-{{account_id}}"

## 参考

- `agent.yaml` 的工作流程定义了从分镜生成到视频拼接与上传的完整链路
