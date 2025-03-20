import streamlit as st
import base64
from src.ui.components import app_state
from PIL import Image


if app_state.KEY not in st.session_state:
    st.session_state[app_state.KEY] = app_state.AppState()

if app_state.LOCAL_KEY not in st.session_state:
    st.session_state[app_state.LOCAL_KEY] = dict()


st.logo("data/logo/klu_png.png", size="large")
# # Loading Image using PIL
im = Image.open('data/logo/klu_png.png')
# Adding Image to web app
st.set_page_config(page_title="Event Log Extraction for Process Mining Using Large Language Models", page_icon = im)

home_page = st.Page("src/ui/pages/home.py", 
                    title="About", icon=":material/info:")
data_upload_page = st.Page("src/ui/pages/data_upload.py", 
                           title="Upload DB", icon=":material/upload:")
event_log_analysis_page = st.Page("src/ui/pages/event_log_analysis.py", 
                                  title="Let's chat!", icon=":material/chat:")
terms_of_use_page = st.Page("src/ui/pages/terms_of_use.py",
                            title="Terms of Use")
impressum_page = st.Page("src/ui/pages/impressum.py",
                         title="Impressum")


# hide_default_format = """
#        <style>
#        #MainMenu {visibility: hidden; }
#        footer {visibility: hidden;}
#        </style>
#        """
# st.markdown(hide_default_format, unsafe_allow_html=True)

def set_bg_hack(main_bg):
    '''
    A function to unpack an image from root folder and set as bg.
 
    Returns
    -------
    The background.
    '''
    # set bg name
    main_bg_ext = "png"
        
    st.markdown(
         f"""
         <style>
         [data-testid="stApp"] {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover
         }}
         [data-testid="stHeader"] {{
            background: rgba(0,0,0,0);
            }}
        [data-testid="stToolbar"] {{
            right: 2rem;
            }}
         [data-testid="stSidebar"]{{
            background-color: #522871;
            }}
         </style>
         """,
         unsafe_allow_html=True
     )

set_bg_hack("data/logo/background.jpg")

pg = st.navigation(
    {
        "Home": [home_page],
        "Event Log Extraction": [
            data_upload_page,
            event_log_analysis_page
        ],
        "": [terms_of_use_page, impressum_page],
    }
)
st.sidebar.markdown("""
<br>
""", unsafe_allow_html=True)

st.sidebar.markdown("This is a prototype designed for informational purposes only :material/favorite: .")
pg.run()