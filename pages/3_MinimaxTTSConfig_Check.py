import streamlit as st
import json


def validate_config(config):
    errors = []

    # 检查必填字段
    required_fields = ["TTSType", "Model", "ApiUrl",
                       "GroupId", "ApiKey", "VoiceType", "Speed"]
    for field in required_fields:
        if not config.get(field):
            errors.append(f"{field} 是必填项")

    # 验证TTSType
    if config["TTSType"] != "minimax":
        errors.append("TTSType 必须是 'minimax'")

    # 验证Speed
    try:
        speed = float(config["Speed"])
        if speed <= 0:
            errors.append("Speed 必须是正数")
    except ValueError:
        errors.append("Speed 必须是数字")

    # 验证ApiUrl
    if not config["ApiUrl"].startswith("https://"):
        errors.append("ApiUrl 必须以 'https://' 开头")

    return errors


st.title("Minimax TTS 配置验证")

tts_type = st.selectbox("TTS类型", ["minimax"])
model = st.text_input("模型", value="speech-01-turbo-240228")
api_url = st.text_input("API URL", value="https://api.minimax.chat/v1/t2a_v2")
group_id = st.text_input("Group ID")
api_key = st.text_input("API Key", type="password")
voice_type = st.text_input("语音类型", value="female-tianmei-jingpin")
speed = st.number_input("语速", value=1.2, min_value=0.1, step=0.1)

if st.button("验证配置"):
    config = {
        "TTSType": tts_type,
        "Model": model,
        "ApiUrl": api_url,
        "GroupId": group_id,
        "ApiKey": api_key,
        "VoiceType": voice_type,
        "Speed": speed
    }

    errors = validate_config(config)

    if errors:
        for error in errors:
            st.error(error)
    else:
        st.success("配置有效!")
        st.json(config)
