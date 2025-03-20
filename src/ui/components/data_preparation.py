import io
import streamlit as st



def upload_file(file_type: list, key: str = "is_file_uploaded") -> list[io.BytesIO]:
    """Upload a file from the user.

    Args:
        file_type (list): List of acceptable file extensions.
        key (str): The key for the Streamlit session state. Defaults to "is_file_uploaded".

    Returns:
        list[io.BytesIO]: A list of uploaded file objects.
    """
    
    uploaded_file = st.file_uploader(
        "Upload a ZIP file containing multiple files", 
        type=file_type,
        accept_multiple_files=False,
        key=key
    )

    if uploaded_file is not None:
        return uploaded_file
    return []
    #return uploaded_files