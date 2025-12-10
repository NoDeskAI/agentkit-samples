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

Welcome to the AgentKit Samples repository!

AgentKit is an enterprise-level AI Agent development platform launched by Volcengine, providing developers with complete solutions for Agent construction, deployment, and operation. Through standardized development toolchains and cloud-native infrastructure, the platform significantly lowers the development and deployment threshold for complex intelligent agent applications.

This repository contains a collection of examples and tutorials to help you understand, implement, and integrate AgentKit functionalities into your applications.

## Project Structure
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

### 01-tutorials/ - Interactive Learning & Fundamentals (Coming Soon)

This folder will contain tutorial-based learning materials that teach AgentKit's core functionalities through practical examples.

**Component Categories:**

- **Runtime**: AgentKit runtime environment, providing secure and scalable agent deployment capabilities
- **Gateway**: Tool gateway, automatically converting APIs and external services into agent-usable tools
- **Memory**: Agent memory management, supporting cross-session, context-aware, and personalized interactions
- **Identity**: Agent identity authentication and permission control, building security trust mechanisms across the user→Agent→tool chain
- **Tools**: Built-in toolset, including code interpreter and browser tools
- **Observability**: Agent observability, providing tracing, debugging, and monitoring capabilities

These examples are perfect for beginners and users who want to understand core concepts before building actual agent applications.

### 02-use-cases/ - End-to-End Application Examples

Explore practical business scenario implementations that demonstrate how to apply AgentKit functionalities to solve real-world business problems.

**Current Use Cases:**

- **ai_coding/**: AI coding assistant, helping developers write and optimize code
- **beginner/**: Beginner-level examples, from basic to advanced agent development
- **customer_support/**: Customer support agent, providing automated after-sales consulting and pre-sales guidance
- **video_gen/**: Video generation agent, combining multiple tools for video content creation

Each use case includes complete implementations with detailed explanations on how to combine AgentKit components to build applications.

## Quick Start

### Prerequisites

- Python 3.10+
- AgentKit SDK
- Optional: Docker (for containerized deployment)

### Installation

All examples require you to first install the AgentKit SDK [Installation Reference](https://volcengine.github.io/agentkit-sdk-python/content/1.introduction/2.installation.html)

## Development Guide

### Code Structure

Each example follows the standard AgentKit application structure:

```
Example Directory/
├── agent.py          # Agent main program
├── requirements.txt  # Dependency list
├── config/           # Configuration files
└── README.md         # Detailed instructions
```

### Best Practices

1. **Modular Design**: Separate tools, agents, and configurations
2. **Error Handling**: Implement comprehensive exception handling
3. **Logging**: Use structured logging for easier debugging
4. **Configuration Management**: Use environment variables and config files

## Contributing

We welcome community contributions! If you have new examples or improvement suggestions, please:

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-example`)
3. Commit your changes (`git commit -m 'Add amazing example'`)
4. Push to the branch (`git push origin feature/amazing-example`)
5. Create a Pull Request

## License
This project is licensed under the [Apache 2.0 License](./LICENSE)

## Support & Feedback

- **Documentation**: Check [AgentKit Official Documentation](https://www.volcengine.com/docs/86681/1844823?lang=zh)
- **Issues**: Report problems in GitHub Issues

## Related Resources

- [AgentKit Official Website](https://www.volcengine.com/docs/86681/1844823?lang=zh)
- [AgentKit SDK/CLI Documentation](https://volcengine.github.io/agentkit-sdk-python/)
- [veadk Official Documentation](https://volcengine.github.io/veadk-python/)

---

**Start exploring the powerful capabilities of AgentKit! Choose an example that interests you, follow the tutorials, and build your own agent applications.**