import streamlit as st
import requests


# ==========================================================
# CONFIGURATION
# ==========================================================

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Documentation Chatbot",
    page_icon="🤖",
    layout="wide"
)


# ==========================================================
# SESSION STATE
# ==========================================================

if "token" not in st.session_state:
    st.session_state.token = None


# ==========================================================
# LOGIN PAGE
# ==========================================================

# ==========================================================
# LOGIN / SIGNUP PAGE
# ==========================================================

if st.session_state.token is None:

    st.title("🤖 Documentation Chatbot")

    st.write(
        "Upload your documents and ask questions using AI."
    )

    st.divider()

    login_tab, signup_tab = st.tabs(
        ["🔐 Login", "📝 Sign Up"]
    )

    # ======================================================
    # LOGIN
    # ======================================================

    with login_tab:

        st.subheader("Login")

        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            if not email or not password:

                st.warning(
                    "Please enter your email and password."
                )

            else:

                try:

                    response = requests.post(
                        f"{API_URL}/login",
                        json={
                            "email": email,
                            "password": password
                        }
                    )

                    if response.status_code == 200:

                        data = response.json()

                        st.session_state.token = (
                            data["access_token"]
                        )

                        st.success(
                            "Login successful!"
                        )

                        st.rerun()

                    else:

                        try:
                            error = response.json().get(
                                "detail",
                                "Login failed"
                            )
                        except:
                            error = "Login failed"

                        st.error(error)

                except requests.exceptions.ConnectionError:

                    st.error(
                        "Cannot connect to FastAPI."
                    )


    # ======================================================
    # SIGN UP
    # ======================================================

    with signup_tab:

        st.subheader("Create an Account")

        name = st.text_input(
            "Full Name",
            key="signup_name"
        )

        signup_email = st.text_input(
            "Email",
            key="signup_email"
        )

        signup_password = st.text_input(
            "Password",
            type="password",
            key="signup_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="confirm_password"
        )

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            if not name or not signup_email or not signup_password:

                st.warning(
                    "Please fill in all fields."
                )

            elif signup_password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            else:

                try:

                    response = requests.post(
                        f"{API_URL}/signup",
                        json={
                            "name": name,
                            "email": signup_email,
                            "password": signup_password
                        }
                    )

                    if response.status_code == 200:

                        st.success(
                            "Account created successfully! "
                            "You can now login."
                        )

                    else:

                        try:
                            error = response.json().get(
                                "detail",
                                "Signup failed"
                            )
                        except:
                            error = "Signup failed"

                        st.error(error)

                except requests.exceptions.ConnectionError:

                    st.error(
                        "Cannot connect to FastAPI."
                    )


# ==========================================================
# MAIN APPLICATION
# ==========================================================

else:

    token = st.session_state.token

    headers = {
        "Authorization": f"Bearer {token}"
    }


    # ======================================================
    # SIDEBAR
    # ======================================================

    with st.sidebar:

        st.title("🤖 DocBot")

        st.write(
            "Documentation Intelligence Platform"
        )

        st.divider()

        st.subheader("📌 Features")

        st.write("📄 PDF Document Upload")
        st.write("🔎 Semantic Search")
        st.write("🧠 AI Answers")
        st.write("📚 Source Citations")
        st.write("🕘 Chat History")

        st.divider()

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.token = None

            st.rerun()


    # ======================================================
    # MAIN TITLE
    # ======================================================

    st.title("📚 Documentation Chatbot")

    st.write(
        "Upload your documents and ask questions "
        "using natural language."
    )


    # ======================================================
    # DOCUMENT UPLOAD
    # ======================================================

    st.divider()

    st.subheader("📄 Upload Document")

    uploaded_file = st.file_uploader(
        "Choose a PDF document",
        type=["pdf"]
    )

    if uploaded_file is not None:

        st.info(
            f"Selected document: {uploaded_file.name}"
        )

        if st.button(
            "⬆️ Upload PDF",
            use_container_width=True
        ):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/pdf"
                )
            }

            try:

                response = requests.post(
                    f"{API_URL}/upload",
                    files=files,
                    headers=headers
                )

                if response.status_code == 200:

                    data = response.json()

                    st.success(
                        data.get(
                            "message",
                            "Document uploaded successfully!"
                        )
                    )

                else:

                    try:
                        error = response.json().get(
                            "detail",
                            "Upload failed"
                        )
                    except:
                        error = "Upload failed"

                    st.error(error)

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to FastAPI."
                )


    # ======================================================
    # ASK QUESTION
    # ======================================================

    st.divider()

    st.subheader("💬 Ask a Question")

    question = st.text_input(
        "Enter your question",
        placeholder="Example: What programming languages are mentioned?"
    )

    if st.button(
        "🔍 Ask Question",
        use_container_width=True
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            try:

                response = requests.get(
                    f"{API_URL}/ask",
                    params={
                        "question": question
                    },
                    headers=headers
                )

                if response.status_code == 200:

                    data = response.json()

                    # --------------------------------------
                    # ANSWER
                    # --------------------------------------

                    st.subheader("🤖 Answer")

                    st.write(
                        data["answer"]
                    )


                    # --------------------------------------
                    # SOURCES
                    # --------------------------------------

                    st.subheader("📚 Sources")

                    sources = data.get(
                        "sources",
                        []
                    )

                    if sources:

                        for source in sources:

                            st.write(
                                f"📄 {source['filename']} "
                                f"— Page {source['page']}"
                            )

                    else:

                        st.info(
                            "No sources found."
                        )

                else:

                    try:
                        error = response.json().get(
                            "detail",
                            "Unable to get answer"
                        )
                    except:
                        error = "Unable to get answer"

                    st.error(error)

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to FastAPI."
                )


    # ======================================================
    # CHAT HISTORY
    # ======================================================

    st.divider()

    st.subheader("🕘 Chat History")

    if st.button(
        "View Chat History",
        use_container_width=True
    ):

        try:

            response = requests.get(
                f"{API_URL}/history",
                headers=headers
            )

            if response.status_code == 200:

                history = response.json().get(
                    "history",
                    []
                )

                if not history:

                    st.info(
                        "No chat history yet."
                    )

                else:

                    for chat in history:

                        st.markdown(
                            f"### ❓ {chat['question']}"
                        )

                        st.markdown(
                            f"**🤖 Answer:** "
                            f"{chat['answer']}"
                        )

                        if chat.get("created_at"):

                            st.caption(
                                f"🕒 {chat['created_at']}"
                            )

                        st.divider()

            else:

                st.error(
                    "Unable to load chat history."
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to FastAPI."
            )