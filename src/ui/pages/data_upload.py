# data_upload.py
import streamlit as st
from src.ui.components import navigation, app_state, data_preparation, database
import os
import pm4py
import pandas as pd
import zipfile
import io

st.header("Database upload", divider="gray")
st.text("Upload your DB or choose an existing one.")

# Toggle for choosing between existing dataset or uploading a new one
use_uploaded_file = st.toggle("Use your own DB", value=False)

dataset_selected = False
uploaded_files = None
user_upload = False
dfs=[]

# Case 1: User chooses to select an existing db 
if not use_uploaded_file:
    existing_folders = [f for f in os.listdir("data/example_dbs/")]
    selected_db = st.selectbox("Select an example DB:", ["None"] + existing_folders)
    if selected_db != "None":
        dataset_selected = True
        file_path = os.path.join("data/example_dbs/", selected_db)
        uploaded_files = [file_path]

# Case 2: User chooses to upload a new file
elif use_uploaded_file:
    st.write("Visit the [project repository](https://github.com/KiriBu10/event-log-extraction-for-process-mining-webapp/blob/dev_kiran/README.md) to check the zip structure.")
    uploaded_files = data_preparation.upload_file(file_type=["zip"], key="is_file_uploaded")
    if uploaded_files:
        with zipfile.ZipFile(io.BytesIO(uploaded_files.read()), "r") as z:
            file_names = z.namelist()

            # Detect common root folder (e.g., "test/")
            root_folder = os.path.commonprefix(file_names).rstrip('/')
            if not root_folder.endswith('/'):
                root_folder += '/'  # Ensure it's recognized as a folder

            # Extract each file while removing the root folder prefix
            for file_name in file_names:
                if file_name.endswith('/'):  # Skip directories (they will be created later)
                    continue
                
                # Remove root folder from path if it exists
                relative_path = file_name[len(root_folder):] if file_name.startswith(root_folder) else file_name

                # Construct the full extraction path
                file_path = os.path.join('user_db', relative_path)

                # Create directories if needed
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                # Extract the file
                with z.open(file_name) as source, open(file_path, "wb") as target:
                    target.write(source.read())
            st.success("Files uploaded successfully!")
        user_upload=True
        dataset_selected = True


def update_state() -> bool:
    """Update the application state based on the uploaded files.

    This function checks if any files have been uploaded or selected. If no files are uploaded or selected, it displays an error message.
    If a file is uploaded or selected, it updates the application state to indicate that the upload page process is complete
    and stores the uploaded data in the application state.

    Returns:
        bool: True if the state was successfully updated, False otherwise.
    """
    if not dataset_selected or not uploaded_files:
        st.error("A dataset must be selected or uploaded to proceed!")
        return False

    with app_state.manage() as _app_state:
        _app_state.page_state.is_upload_page_done = True
        _app_state.data = dfs
        _app_state.db_schema = db_schema
        _app_state.conn=conn
        if path_to_ground_truth_eventlog:
            _app_state.path_to_groud_truth_eventlog = path_to_ground_truth_eventlog
    return True


# Only proceed if either an existing dataset is selected or a file is uploaded
if dataset_selected and uploaded_files:
    st.divider()
    try:
        #Load db
        if uploaded_files:
            
            if user_upload:
                db_path = 'user_db'
            else:
                db_path = uploaded_files[0]

            path_to_db = os.path.join(db_path+'/', 'db/')
            tables = [f for f in os.listdir(path_to_db)]
            for table in tables:
                path_to_table = os.path.join(path_to_db, table)
                df = pd.read_csv(path_to_table)
                if len(df)>0:
                    st.write("Table preview: ", table)
                    st.dataframe(df.head())
                    dfs.append(df)
            path_to_db_schema = db_path+ '/csv_schema.xlsx'
            path_to_ground_truth_eventlog = db_path+ '/ground-truth-eventlog.csv'

            # create database
            path_to_csv_files = path_to_db
            path_to_csv_schema_file = path_to_db_schema
            db_output_dir = 'example.db'
            db_schema, conn = database.get_database_schema_execute_all(path_to_csv_files = path_to_csv_files,path_to_csv_schema_file=path_to_csv_schema_file, db_output_dir= db_output_dir)
    except:
        path_to_db_schema = False
        dfs = []
        user_upload=False
        st.error("It seems like there is an error in the uploaded file. Upload another file.")
    
    if len(dfs) > 0 and path_to_db_schema:
        navigation.previous_and_next(
        previous_page="src/ui/pages/home.py",
        next_page="src/ui/pages/event_log_analysis.py",
        previous_label="Back",
        next_label="Looks good. Let's chat!",
        next_callback=update_state
        #next_callback=lambda: update_state() and database.create_db(df_event_log)
        )
        #st.write("Event log preview")
        #st.dataframe(df_event_log)


st.divider()