import streamlit as st
import json


def validate_config(config):
    errors = []

    # 检查必填字段
    required_fields = ["TTSType", "AppId",
                       "SecretId", "SecretKey", "VoiceType"]
    for field in required_fields:
        if not config.get(field):
            errors.append(f"{field} 是必填项")

    # 验证TTSType
    if config["TTSType"] not in ["tencent", "minixmax"]:
        errors.append("TTSType 必须是 'tencent' 或 'minixmax'")

    # 验证VoiceType
    try:
        voice_type = int(config["VoiceType"])
        if voice_type < 0:
            errors.append("VoiceType 必须是正整数")
    except ValueError:
        errors.append("VoiceType 必须是整数")

    # 验证Speed (如果提供)
    if config.get("Speed"):
        try:
            speed = float(config["Speed"])
            if not -2 <= speed <= 6:
                errors.append("Speed 必须在 -2 到 6 之间")
        except ValueError:
            errors.append("Speed 必须是数字")

    # 验证Volume (如果提供)
    if config.get("Volume"):
        try:
            volume = int(config["Volume"])
            if not 0 <= volume <= 10:
                errors.append("Volume 必须在 0 到 10 之间")
        except ValueError:
            errors.append("Volume 必须是整数")

    return errors


st.title("Tencent TTS 配置验证")

tts_type = st.text_input("TTS类型", value="tencent")
app_id = st.text_input("应用ID")
secret_id = st.text_input("密钥ID")
secret_key = st.text_input("密钥Key", type="password")
voice_type = st.number_input("音色ID", min_value=0, step=1)
speed = st.slider("语速", min_value=-2.0, max_value=6.0, value=1.0, step=0.01)
volume = st.slider("音量", min_value=0, max_value=10, value=5)
primary_language = st.text_input("主要语言", value="zh-CN")

if st.button("验证配置"):
    config = {
        "TTSType": tts_type,
        "AppId": app_id,
        "SecretId": secret_id,
        "SecretKey": secret_key,
        "VoiceType": voice_type,
        "Speed": speed,
        "Volume": volume,
        "PrimaryLanguage": primary_language
    }

    errors = validate_config(config)

    if errors:
        for error in errors:
            st.error(error)
    else:
        st.success("配置有效!")
        st.json(config)
