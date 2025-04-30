import streamlit as st
from src.ui.components import app_state, navigation


# Header Section with Icon
st.title("From Prompt to Process: Event Log Extraction from Relational Databases Using Large Language Models")

st.markdown("by reasearchers from Utrecht University and KLU""", unsafe_allow_html=True)


# App State
_app_state: app_state.AppState = st.session_state[app_state.KEY]

# Description with Markdown and Light Styling
st.markdown(
    """
        <span style="font-size: 1.5em; font-weight: bold;">P</span>rocess mining is a discipline that enables organizations to discover and analyze their work processes. A prerequisite for conducting a process mining initiative is the so-called event log, which is not always readily available. In such cases, extracting an event log involves various time-consuming tasks, such as creating tailor-made structured query language (SQL) scripts to extract an event log from a relational database. With this work, we investigate the use of large language models (LLMs) to support event log extraction, particularly by leveraging LLMs ability to produce SQL scripts.
        This web application is an implementation based on our previous work [[1](https://link.springer.com/chapter/10.1007/978-3-031-81375-7_4)] and enables users to upload their own database or choose from sample example database, fostering an intuitive and seamless exploration experience. 
        Developed by researchers from <strong>Kühne Logistics University</strong>, this tool serves as a solid foundation for event log generation, allowing users to ask targeted questions and receive real-time responses.
        <br>
        <br>
    """,
    unsafe_allow_html=True
)
st.text("[1] Vinicius Stein Dani, Marcus Dees, Henrik Leopold, Kiran Busch, Iris Beerepoot, Jan Martijn EM van der Werf, Hajo A Reijers (2024) Event Log Extraction for Process Mining Using Large Language Models.")

# Feature Section Header
st.markdown('CURRENT FUNCTIONALITIES', unsafe_allow_html=True)

# Functionality List with Link Button
st.markdown(
    """
    <strong>DB</strong>: Upload or select an database. Users can upload their own database or choose from preloaded example databases to generate event log. The file must be in <code>.zip</code> format to ensure compatibility. See [here](https://github.com/KiriBu10/event-log-extraction-for-process-mining-webapp/blob/dev_kiran/README.md) the file requirements.
    <br>
    <br>
    <strong>Single Question Response</strong>: The chatbot is designed to respond to one question at a time, optimizing for security and clarity in interactions. Due to prompt injection concerns and other security considerations, the chatbot only processes the most recent question, without relying on prior context. This means that each query should be self-contained, as previous context is not retained or considered when generating responses. 
    <br>
    <br>
    """,
    unsafe_allow_html=True
)

# How to Use Section Header
st.markdown('HOW TO USE', unsafe_allow_html=True)

# How to Use Description
st.markdown(
    """
    To get started with the **EventLog Insights Chatbot**, you only need an **OpenAI API key**. 
    This key enables the chatbot to process your questions and provide insightful responses based on the event log data you upload or select.

    1. **Get an API Key**: If you don’t already have an OpenAI API key, you can obtain one by signing up at the 
      <a href="https://platform.openai.com/signup" target="_blank">OpenAI website</a>. Once registered, you’ll be able to generate a key from your account dashboard.
    2. **DB**: Upload a db.zip file or choose a sample db dataset.
    3. **Enter the API Key**: When prompted in the EventLog Insights Chatbot application, enter your OpenAI API key.
    4. **Start Exploring**: Start extracting event logs!
    """,
    unsafe_allow_html=True
)


navigation.previous_and_next(
        next_page="src/ui/pages/data_upload.py",
        next_label="LET'S START!",
        #next_callback=update_state
        #next_callback=lambda: update_state() and database.create_db(df_event_log)
)


st.markdown("""
            **For inquiries or support, please contact:**\\
            :material/mail: Kiran Busch (kiran.busch(at)klu.org)
            """)
