import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# TRTC Conversation AI! 👋")

    st.sidebar.error("Select a demo above.")

    st.markdown(
        """
        我们提供了三个功能页面，来辅助你验证TRTC Conversation AI的配置:


        - **LLMConfig 配置验证**: 验证OpenAI的配置
        - **Minimax TTS 配置验证**: 验证Minimax的配置
        - **Tencent TTS 配置验证**: 验证Tencent的配置
    """
    )


if __name__ == "__main__":
    run()
