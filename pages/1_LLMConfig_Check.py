
import streamlit as st
import json
import requests


def validate_config(config):
    required_fields = ["LLMType", "Model", "APIKey",
                       "APIUrl", "Streaming", "SystemPrompt", "Timeout"]
    for field in required_fields:
        if field not in config:
            return False, f"缺少必填字段: {field}"

    if not isinstance(config["Streaming"], bool):
        return False, "Streaming 必须是布尔值 (true/false)"

    try:
        float(config["Timeout"])
    except ValueError:
        return False, "Timeout 必须是一个数字"

    headers = {
        "Authorization": f"Bearer {config['APIKey']}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    data = {
        "model": config['Model'],
        "messages": [{"role": "user", "content": "Tell me a short joke."}],
        "stream": config["Streaming"]
    }
    response = requests.post(
        config['APIUrl'], headers=headers, stream=config["Streaming"], json=data)

    if response.status_code != 200:
        return False, f"请求失败: {response.text}"

    return True, "配置有效"


st.title("LLMConfig 配置验证")

llm_type = st.text_input("LLM类型", value="openai")
model = st.text_input(
    "模型", value="", placeholder="your-model-name, like ‘gpt-4’")
api_key = st.text_input("API密钥", type="password", )
api_url = st.text_input(
    "API URL", value="https://api.openai.com/chat/completions", placeholder="your model API URL")
streaming = st.checkbox("启用流式传输", value=True)
system_prompt = st.text_area("系统提示", value="你是一个个人助手")
timeout = st.number_input("超时 (秒)", value=3.0, step=1.0,
                          min_value=1.0, max_value=10.0)

if st.button("验证配置"):
    config = {
        "LLMConfig": {
            "LLMType": llm_type,
            "Model": model,
            "APIKey": api_key,
            "APIUrl": api_url,
            "Streaming": streaming,
            "SystemPrompt": system_prompt,
            "Timeout": timeout
        }
    }

    is_valid, message = validate_config(config["LLMConfig"])

    if is_valid:
        st.success("配置有效!")
        st.json(config)
    else:
        st.error(f"配置无效: {message}")
