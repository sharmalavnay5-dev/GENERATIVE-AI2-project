import streamlit as st
import google.generativeai as genai

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# Custom CSS Styling
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: white;
}

/* Grey headings */
h1, h2, h3 {
    color: #4B5563;
}

.stTextArea textarea {
    background-color: #1E1E1E !important;
    color: white !important;
    border-radius: 10px;
}

.stButton>button {
    background: linear-gradient(90deg, #4F46E5, #9333EA);
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
    font-weight: bold;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #6366F1, #A855F7);
}

.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown(
    "<h1 style='text-align:center;'>🤖 AI Code Reviewer & Converter</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; color:gray;'>Review • Debug • Optimize • Convert Code Instantly</p>",
    unsafe_allow_html=True
)
st.divider()

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("⚙️ Settings")

    # API Key Input
    api_key = st.text_input("🔑 Enter Gemini API Key", type="password")

    if api_key:
        st.success("✅ API Key loaded")

    task = st.selectbox(
        "Select Task",
        ["Review Code", "Debug Code", "Optimize Code", "Convert Language"]
    )

    if task == "Convert Language":
        target_language = st.text_input("Convert To Language")
    else:
        target_language = None

    st.markdown("---")
    st.info("Powered by Gemini 2.5 Flash")

# -----------------------------
# Configure Gemini
# -----------------------------
model = None

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
    except Exception as e:
        st.error(f"❌ API Configuration Error: {e}")

# -----------------------------
# Layout
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Input Code")
    code_input = st.text_area(
        "",
        height=400,
        placeholder="Paste your code here..."
    )

with col2:
    st.subheader("📢 AI Output")
    output_placeholder = st.empty()

# -----------------------------
# Button Action / BACKEND 
# -----------------------------
if st.button("🚀 Run AI Analysis"):

    if not api_key:
        st.error("❌ Please enter your Gemini API key.")
    elif not code_input.strip():
        st.warning("⚠️ Please paste some code first.")
    else:
        try:
            with st.spinner("Analyzing with Gemini AI..."):

                # Prompt Selection
                if task == "Review Code":
                    prompt = f"""
                    You are a senior software engineer.
                    Review the following code.
                    Provide:
                    - Code quality feedback
                    - Best practices suggestions
                    - Performance improvements
                    - Security issues if any

                    Code:
                    {code_input}
                    """

                elif task == "Debug Code":
                    prompt = f"""
                    You are an expert debugger.
                    Find errors in the following code.
                    Explain issues clearly.
                    Provide corrected code.

                    Code:
                    {code_input}
                    """

                elif task == "Optimize Code":
                    prompt = f"""
                    Optimize the following code for performance and readability.
                    Provide improved version with explanation.

                    Code:
                    {code_input}
                    """

                elif task == "Convert Language":
                    if not target_language:
                        st.warning("⚠️ Please enter target language.")
                        st.stop()

                    prompt = f"""
                    Convert the following code into {target_language}.
                    Keep logic same.
                    Add comments.

                    Code:
                    {code_input}
                    """

                # Generate Response
                response = model.generate_content(prompt)

                # Display Output
                output_placeholder.markdown(
                    f"""
                    <div style="
                        background-color:#1E1E1E;
                        padding:20px;
                        border-radius:10px;
                        border:1px solid #333;
                        color:white;
                        white-space: pre-wrap;
                    ">
                    {response.text}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        except Exception as e:
            st.error(f"⚠️ Error: {e}")