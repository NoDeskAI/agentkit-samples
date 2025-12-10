<div align="center">
  <h1>
    AgentKit Platform Python Samples
  </h1>

  <div align="center">
    <a href="https://github.com/volcengine/agentkit-samples/graphs/commit-activity"><img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/m/volcengine/agentkit-samples"/></a>
    <a href="https://github.com/volcengine/agentkit-samples/pulls"><img alt="GitHub open pull requests" src="https://img.shields.io/github/issues-pr/volcengine/agentkit-samples"/></a>
    <a href="https://github.com/volcengine/agentkit-samples/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/volcengine/agentkit-samples"/></a>
    <a href="https://python.org"><img alt="Python versions" src="https://img.shields.io/pypi/pyversions/agentkit-sdk-python"/></a>
  </div>

  <p>
  <a href="https://console.volcengine.com/agentkit/"> Volcengine AgentKit</a>
    ◆ <a href="https://volcengine.github.io/agentkit-sdk-python/">SDK/CLI Documentation</a>
    ◆ <a href="https://github.com/volcengine/agentkit-samples/tree/main">Samples</a>
    ◆ <a href="https://pypi.org/project/agentkit-sdk-python/">PyPI Package</a>
    ◆ <a href="https://github.com/volcengine/agentkit-sdk-python">SDK/CLI GitHub</a>

  </p>
</div>

# AgentKit Samples

欢迎来到 AgentKit Samples 代码库！

AgentKit 是火山引擎推出的企业级 AI Agent 开发平台，为开发者提供完整的 Agent 构建、部署和运维解决方案。平台通过标准化的开发工具链和云原生基础设施，显著降低复杂智能体应用的开发部署门槛。

本代码库包含了一系列示例和教程，帮助您理解、实现和集成 AgentKit 的各项功能到您的应用中。

## 项目结构
```bash
.
├── 01-tutorials
│   └── README.md
├── 02-use-cases
│   ├── ai_coding
│   ├── beginner
│   │   ├── a2a_simple
│   │   ├── callback
│   │   ├── episode_generation
│   │   ├── hello_world
│   │   ├── mcp_simple
│   │   ├── multi_agents
│   │   ├── restaurant_ordering
│   │   ├── travel_concierge
│   │   ├── vikingdb
│   │   ├── vikingmem
│   │   └── README.md
│   ├── customer_support
│   └── video_gen
├── README.md
└── README.zh.md
```

### 01-tutorials/ - 交互式学习与基础（即将推出）

此文件夹将包含基于教程的学习材料，通过实际示例教授 AgentKit 的核心功能。

**组件分类：**

- **Runtime**: AgentKit 运行时环境，提供安全、可扩展的智能体部署能力
- **Gateway**: 工具网关，自动转换 API 和外部服务为智能体可用的工具
- **Memory**: 智能体记忆管理，支持智能体跨会话、上下文感知和个性化的交互
- **Identity**: 智能体身份认证与权限控制，构建用户→Agent→工具全链路的安全信任机制
- **Tools**: 内置工具集，包括代码解释器和浏览器工具
- **Observability**: 智能体可观测性，提供追踪、调试和监控能力

这些示例非常适合初学者和希望在实际构建智能体应用前理解核心概念的用户。

### 02-use-cases/ - 端到端应用示例

探索实用的业务场景实现，展示如何应用 AgentKit 功能解决真实业务问题。

**当前包含的用例：**

- **ai_coding/**: AI 编程助手，帮助开发者编写和优化代码
- **beginner/**: 入门级示例，从基础到进阶的智能体开发
- **customer_support/**: 客户服务智能体，提供自动的售后咨询和售前导购
- **video_gen/**: 视频生成智能体，结合多种工具实现视频内容创作

每个用例都包含完整的实现，并详细说明如何结合 AgentKit 组件构建应用。

## 快速开始

### 环境要求

- Python 3.10+
- AgentKit SDK
- 可选：Docker（用于容器化部署）

### 安装依赖

所有的案例都需要您先安装 AgentKit SDK [如何安装参考](https://volcengine.github.io/agentkit-sdk-python/content/1.introduction/2.installation.html)

## 开发指南

### 代码结构

每个示例都遵循标准的 AgentKit 应用结构：

```
示例目录/
├── agent.py          # 智能体主程序
├── requirements.txt  # 依赖列表
├── config/           # 配置文件
└── README.md         # 详细说明
```

### 最佳实践

1. **模块化设计**: 将工具、智能体和配置分离
2. **错误处理**: 实现完善的异常处理机制
3. **日志记录**: 使用结构化日志便于调试
4. **配置管理**: 使用环境变量和配置文件

## 贡献指南

我们欢迎社区贡献！如果您有新的示例或改进建议，请：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-example`)
3. 提交更改 (`git commit -m 'Add amazing example'`)
4. 推送到分支 (`git push origin feature/amazing-example`)
5. 创建 Pull Request

## 许可证
本项目采用 [Apache 2.0 许可证](./LICENSE)

## 支持与反馈

- **文档**: 查看 [AgentKit 官方文档](https://www.volcengine.com/docs/86681/1844823?lang=zh)
- **问题**: 在 GitHub Issues 中报告问题

## 相关资源

- [AgentKit 官方网站](https://www.volcengine.com/docs/86681/1844823?lang=zh)
- [AgentKit SDK/CLI文档](https://volcengine.github.io/agentkit-sdk-python/)
- [veadk 官方文档](https://volcengine.github.io/veadk-python/)

---

**开始探索 AgentKit 的强大功能吧！选择您感兴趣的示例，跟随教程，构建属于您的智能体应用。**