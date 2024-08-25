import json
import os
import sys
import inspect
import streamlit as st
import datetime

ENGINE_MODEL_TYPE = "16k_zh"
SLICE_SIZE = 6400


currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


TEXT = "欢迎使用腾讯云实时语音合成"
VOICETYPE = 101001  # 音色类型
CODEC = "pcm"  # 音频格式：pcm/mp3
SAMPLE_RATE = 16000  # 音频采样率：8000/16000
ENABLE_SUBTITLE = True


if True:
    from tts import synthesizer


class Credential:
    def __init__(self, secret_id, secret_key, token=""):
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.token = token


class MySpeechSynthesisListener(synthesizer.SpeechSynthesisListener):

    def on_message(self, response):
        pass

    def on_complete(self, response):
        pass

    def on_fail(self, response):
        pass


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

    listener = MySpeechSynthesisListener()
    credential_var = Credential(config["SecretId"], config["SecretKey"])
    _synthesizer = synthesizer.SpeechSynthesizer(
        config["AppId"], credential_var, config["VoiceType"], listener)
    _synthesizer.set_voice_type(config["VoiceType"])
    _synthesizer.set_codec(CODEC)
    _synthesizer.set_sample_rate(SAMPLE_RATE)

    response = _synthesizer.synthesis(TEXT)
    print(response)

    if response:
        errors.append("请求失败!， 错误码: " + response.get("Code") +
                      "， 错误信息: " + response.get("Message"))

    return errors


st.title("Tencent TTS 配置验证")

tts_type = st.text_input("TTS类型", value="tencent")
app_id = st.text_input("应用ID")
secret_id = st.text_input("密钥ID")
secret_key = st.text_input("密钥Key", type="password")
voice_type = st.number_input("音色ID", value=101001)
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
