# Hello World Demo

## Introduction
Build the simplest chat Agent

## Project Overview
This example demonstrates the core features of VeADK:
- **Agent Creation**: Create an AI Agent with simple configuration
- **Short-term Memory**: Store conversation history using a local backend to achieve session-level context memory
- **Multi-turn Conversation**: Associate conversations via session_id, allowing the Agent to remember previous dialogue content

## Prerequisites
1. **Enable Volcano Ark Model Service**: Go to [Ark console](https://exp.volcengine.com/ark?mode=chat)
2. **Prepare model_api_key**: Obtain the **API Key** from the console.

## Usage
### 1. Install veadk and agentkit Python SDK and configure environment variables

```bash
uv pip install veadk-python
uv pip install agentkit-sdk-python
```

Set your model information in `config.yaml`:
```yaml
model:
  agent:
    name: doubao-seed-1-6-251015
    api_key: XXXX
```

### 2. Run the local client
```bash
python agent.py
```

### 3. Run the veadk web client and login via browser at http://127.0.0.1:8000
```bash
cd ..
veadk web

```

### 4. Deploy to vefaas
```bash
cd hello_world
# This step can be run directly
export VEFAAS_ENABLE_KEY_AUTH=false
# Replace YOUR_AK with your own ak
export VOLCENGINE_ACCESS_KEY=YOUR_AK
# Replace YOUR_SK with your own sk
export VOLCENGINE_SECRET_KEY=YOUR_SK
# This step deploys the application to the cloud
veadk deploy --vefaas-app-name=hello-world --use-adk-web --veapig-instance-name=<your veapig instance name> --iam-role "trn:iam::<your account id>:role/<your iam role name>"

```

### 5. Deploy to AgentKit and test with client.py

```bash
cd hello_world
# Uncomment the following line in agent.py to run the agentkit app server
# agent_server_app.run(host="0.0.0.0", port=8000)
agentkit config
agentkit launch
```

## Example Prompts
The sample code demonstrates a simple two-turn conversation:

**First turn**:
```
Input: My name is VeADK
Output: Hello VeADK! Nice to meet you.
```

**Second turn** (testing memory function):
```
Input: Do you remember my name?
Output: Of course, your name is VeADK.
```

You can also try the following conversations:
- "I'm 25 years old" → "How old am I?"
- "I like programming" → "Do you know my hobby?"
- "I live in Beijing" → "Do you remember where I live?"

These examples demonstrate how the Agent maintains context memory during the same session.