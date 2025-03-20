from dataclasses import dataclass, field
from contextlib import contextmanager
from typing import Generator

import pandas as pd
import streamlit as st

KEY = "app_state"
LOCAL_KEY = "local"


@dataclass
class PageState:
    """A class to represent the state of different pages in the application.

    Attributes:
        is_upload_page_done (bool): Indicates whether the upload page process is complete. Defaults to False.
        is_analysis_page_done (bool): Indicates whether the analysis page process is complete. Defaults to False.
        is_download_page_done (bool): Indicates whether the download page process is complete. Defaults to False.
    """

    is_upload_page_done: bool = field(default=False)
    is_analysis_page_done: bool = field(default=False)
    is_download_page_done: bool = field(default=False)


@dataclass
class AppState:
    """A class to represent the overall state of the application.

    Attributes:
        data (pd.DataFrame): The data used in the application. Defaults to None.
        page_state (PageState): The state of the different pages in the application. Defaults to a new instance of PageState.
    """

    data: pd.DataFrame = None
    page_state: PageState = field(default_factory=lambda: PageState())
    topics: list[str] = field(default_factory=list)


@contextmanager
def manage() -> Generator[AppState, None, None]:
    """Context manager to handle the application state.

    This context manager retrieves the application state from the Streamlit session state,
    yields it for use within the context, and then ensures that the updated state is saved
    back to the session state.

    Yields:
        AppState: The current application state.
    """
    try:
        _app_state: AppState = st.session_state[KEY]
        yield _app_state
    finally:
        st.session_state[KEY] = _app_state


@contextmanager
def local() -> Generator[dict, None, None]:
    """Context manager to handle the local state of a page.

    This context manager provides a dictionary to for storing arbitrary information in a local state.
    After using the local state dict it is automatically updated.

    Yields:
        Generator[dict, None, None]: The dict for storing arbitrary information in the context of a page.
    """
    try:
        _local = st.session_state[LOCAL_KEY]
        yield _local
    finally:
        st.session_state[LOCAL_KEY] = _local
