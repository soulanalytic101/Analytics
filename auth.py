# auth.py

import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

APP_PASSWORD = os.environ.get(
    "APP_PASSWORD",
    "Soul@101"
)


def require_login():

    if st.session_state.get("authenticated"):
        return True

    st.markdown(
        """
        <h1 style="text-align:center;margin-top:4rem;">
            RetailIQ
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="text-align:center;color:gray;">
            Intelligence Suite
        </p>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:

        with st.form("login_form"):

            password = st.text_input(
                "Password",
                type="password"
            )

            submitted = st.form_submit_button(
                "Login",
                use_container_width=True
            )

        if submitted:

            if password == APP_PASSWORD:

                st.session_state[
                    "authenticated"
                ] = True


                st.rerun()

            else:

                st.error(
                    "Incorrect password"
                )

    st.stop()