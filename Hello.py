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
        We provide multiple functional pages to help you validate TRTC Conversation AI configurations:


        - **LLMConfig Validation**: Validate LLM configurations
        - **Minimax TTS Validation**: Validate Minimax configurations
        - **Tencent TTS Validation**: Validate Tencent configurations
    """
    )


if __name__ == "__main__":
    run()
