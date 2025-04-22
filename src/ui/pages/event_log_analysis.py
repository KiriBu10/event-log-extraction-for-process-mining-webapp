import streamlit as st
from src.ui.components import app_state
from src.ui.components.workflow import SimpleApp
from src.ui.components import app_state
#from openai import OpenAI
from langchain_openai import ChatOpenAI
import time
import os

with app_state.manage() as _app_state:
    event_log_available = _app_state.page_state.is_upload_page_done
    dfs = _app_state.data
    db_selected=True
    try:
        db_schema = _app_state.db_schema
        path_to_groud_truth_eventlog = _app_state.path_to_groud_truth_eventlog
        conn = _app_state.conn
    except:
        db_selected=False


def text_to_stream(text):
    # Create a generator that yields each character one at a time
    for char in text:
        yield char
        time.sleep(0.03)


def display_txt_files(folder_path):

    if not os.path.isdir(folder_path):
        st.error("Invalid folder path!")
        return
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):  # Process only .txt files
            file_path = os.path.join(folder_path, file_name)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    st.text(file_name.split('.txt')[0])
                    st.code(content, language='text', wrap_lines =True)  # Display in Streamlit
            except Exception as e:
                st.error(f"Error reading {file_name}: {e}")


def get_assistant_response(messages, llm_model_name, openai_api_key, conn):
    
    llm_model = ChatOpenAI(model=llm_model_name, temperature=0, api_key=openai_api_key)
    
    user_query = messages[1]["content"]
    agentState = {"messages": [user_query]}
    a = SimpleApp(conn = conn, path_to_groud_truth_eventlog=path_to_groud_truth_eventlog, llm_model = llm_model)
    result = a.invoke(agentState)

    st.write_stream(text_to_stream(str(result['result'])))
    #if result['sqlexecuter']:
    #    st.dataframe(result['sqlexecuter'])

    return result
    
    # app = SimpleApp(event_log=df_event_log,llm_model=llm_model)
    # user_query = messages[1]["content"]
    # agentState = {"user_query": user_query}
    # text_result, tbl_result = app.invoke(agentState)
    # st.write_stream(text_to_stream(text_result))
    # if tbl_result:
    #     st.dataframe(tbl_result)

def create_event_log_visualisation(data):
    import plotly.graph_objects as go
    from collections import Counter
    import pandas as pd
    df = pd.DataFrame(data)
    df = df.sort_values(['case_id', 'timestamp'])
    # Create transition pairs
    df['next_activity'] = df.groupby('case_id')['activity_id'].shift(-1)
    transitions = df.dropna(subset=['next_activity'])
    transition_counts = Counter(zip(transitions['activity_id'], transitions['next_activity']))
    labels = list(set([a for a, b in transition_counts] + [b for a, b in transition_counts]))
    label_to_index = {label: i for i, label in enumerate(labels)}
    sources = [label_to_index[a] for a, b in transition_counts]
    targets = [label_to_index[b] for a, b in transition_counts]
    values = list(transition_counts.values())
    fig = go.Figure(go.Sankey(
        node=dict(label=labels, pad=20),
        link=dict(source=sources, target=targets, value=values)
    ))
    fig.update_layout(title_text="Activity Transition Flow", font_size=10)
    st.plotly_chart(fig)


def render_header():
    st.header("Let's chat!", divider="gray")

if db_selected:
    if db_schema:
        render_header()
        valid_key = False
        if openai_api_key := st.text_input("Enter your OpenAI API key:", type="password"):
            try:
                test = ChatOpenAI(model='gpt-4', temperature=0, api_key=openai_api_key)
                test.invoke('Hi')
                valid_key = True
                llm_model_name = st.selectbox("Select OpenAI model:", ["gpt-4o", "gpt-4"])
            except:
                valid_key = False
                st.error("Seems like your OpenAI API key is invalid. Please check your OpenAI API key and try again.")

        if valid_key:

            #example prmompts
            with st.expander("See example prompts"):
                display_txt_files("data/prompts/")


            st.divider()

            with st.expander("See database tables."):
                for df in dfs:
                    st.dataframe(df)
            # Chat
            #client = OpenAI(api_key=openai_api_key)
            messages = [{"role": "assistant", "content": "Hello, I am an expert in event log extraction from databases. I will try to answer your questions as best I can. How can I help you?"}]

            for message in messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if user_input := st.chat_input("Ask something about your event log."):
                prompt=(f"""Consider the following db schema: {db_schema}. """
                    +'User question: ' + user_input
                    +f""" Context: If the user ask you to write a sql statement that return an event log make sure the event log has the following columns: case_id, activity_id, timestamp. """
                    +f"""And use quotes for identifiers. """
                    +f"""And make sure that all columns of the event log are interpreted as varchar values. """               
                    +f"""And return only the complete SQL query, leave out any other comments in the response. Return the query in plain text without markdown syntax. """ 
                    +'Your task: Try to answer the user question. ')

                messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(user_input)

                with st.chat_message("assistant"):
                    try:
                        result = get_assistant_response(messages, llm_model_name, openai_api_key, conn)
                        if type(result['sqlexecuter']) != str:
                            st.dataframe(result['sqlexecuter'])
                            
                    except:
                        st.error("Seems like your OpenAI API key is invalid. Please check your OpenAI API key and try again.")
                    # try:
                    #     st.write_stream(text_to_stream('Let me try to create also a visualisation of that event log: '))
                    #     create_event_log_visualisation(result['sqlexecuter'])
                    # except:
                    #     st.write_stream(text_to_stream('Oh, something went wrong with the visualisation. You can try another prompt.'))

                #st.write(messages)
else:
    st.error("Please upload or select an example database before accessing the chat :)")

