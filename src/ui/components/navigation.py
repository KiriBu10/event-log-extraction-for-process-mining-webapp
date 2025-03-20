from typing import Callable
import streamlit as st
import functools


def previous_and_next(
    *,
    previous_page: str | None = None,
    next_page: str | None = None,
    previous_label: str = "Zurück",
    next_label: str = "Weiter",
    previous_callback: Callable[[], bool | None] = lambda: True,
    next_callback: Callable[[], bool | None] = lambda: True,
):
    """Create navigation buttons for previous and next pages in a Streamlit app.

    Args:
        previous_page (str | None): The name of the previous page. Defaults to None.
        next_page (str | None): The name of the next page. Defaults to None.
        previous_label (str): The label for the previous button. Defaults to "Zurück".
        next_label (str): The label for the next button. Defaults to "Weiter".
        previous_callback (Callable[[], bool | None]): A callback function to be executed before switching to the previous page. Defaults to a lambda that returns True.
            If the callback returns False the switch page action will not be performed.
        next_callback (Callable[[], bool | None]): A callback function to be executed before switching to the next page. Defaults to a lambda that returns True.
            If the callback returns False the switch page action will not be performed.

    Raises:
        RuntimeError: If both `previous_page` and `next_page` are None.
    """
    if not (previous_page or next_page):
        raise RuntimeError(
            "You need to specify at least one eletement. Both `previous` and `next` are `None`"
        )

    def switch_page_button(label: str, page: str, callback: Callable[[], bool | None]):
        if st.button(label):
            check_passed = callback()
            if check_passed is None:
                check_passed = True

            if check_passed:
                st.switch_page(page)

    next_page_button = functools.partial(
        switch_page_button, next_label, next_page, next_callback
    )
    previous_page_button = functools.partial(
        switch_page_button, previous_label, previous_page, previous_callback
    )

    if not next_page:
        previous_page_button()
        return

    if not previous_page:
        next_page_button()
        return

    col1, col2, col3 = st.columns((1, 3, 4))
    with col1:
        previous_page_button()

    with col2:
        next_page_button()

    with col3:
        st.text("")


def next_only(
    *,
    next_page: str,
    next_label: str = "Weiter",
    next_callback: Callable[[], bool | None] = lambda: True,
):
    """Create a navigation button for the next page in a Streamlit app.

    Args:
        next_page (str): The name of the next page.
        next_label (str): The label for the next button. Defaults to "Weiter".
        next_callback (Callable[[], bool | None]): A callback function to be executed before switching to the next page. Defaults to a lambda that returns True.
            If the callback returns False, the switch page action will not be performed.

    Raises:
        RuntimeError: If `next_page` is None.
    """
    if not next_page:
        raise RuntimeError("You need to specify the `next_page`.")

    def switch_page_button(label: str, page: str, callback: Callable[[], bool | None]):
        if st.button(label):
            check_passed = callback()
            if check_passed is None:
                check_passed = True

            if check_passed:
                st.switch_page(page)

    next_page_button = functools.partial(
        switch_page_button, next_label, next_page, next_callback
    )

    # Display the button centered
    col1, col2, col3 = st.columns((1, 3, 1))
    with col2:
        next_page_button()