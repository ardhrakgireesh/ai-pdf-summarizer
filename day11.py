import streamlit as st
import pdfplumber
from groq import Groq
import os
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
st.set_page_config(page_title="AI PDF Summarizer", page_icon="📄")
st.markdown("""
    <style>
    [data-testid="stSidebar"]{
        min-width: 200px;
        max-width: 200px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("📄 AI PDF Summarizer")
with st.sidebar:
    st.markdown("## 🤖 AI PDF Summarizer")
    st.markdown("---")
    st.markdown("### ✨ Features")
    st.markdown("""
    - 📄 Upload any PDF
    - 🎯 3 Summary styles
    - 🌐 4 Languages
    - 🙋 Ask questions
    - ⬇️ Download summary
    - 📊 PDF statistics
    """)
    st.markdown("---")
    st.markdown("### 🛠️ Built With")
    st.markdown("""
    - 🐍 Python
    - 🎈 Streamlit
    - 🤖 Groq AI
    - 📄 PDFPlumber
    """)
    st.markdown("---")
    st.markdown("### 👩‍💻 Built by")
    st.markdown("**Ardhra**")
    st.markdown("----")
    st.info("💡 Tip: Works best with text-based PDFs!")
st.markdown("---")
st.write("✨ Upload any PDF and get an instant AI summary!")

# Session state
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "original_text" not in st.session_state:
    st.session_state.original_text = ""
if "answer" not in st.session_state:
    st.session_state.answer = ""

# Upload section
uploaded_file = st.file_uploader("📄 Upload your PDF:", type="pdf")

if uploaded_file:
    st.info(f"📎 File uploaded: {uploaded_file.name}")

# Options
style = st.selectbox("📊 Choose Summary Style:",
    ["📌 Bullet Points", "📝 Short Paragraph", "📖 Detailed Summary"])
language = st.selectbox("🌐 Summary Language:",
    ["English", "Malayalam", "Hindi", "Tamil"])
# Button
col1, col2, col3 = st.columns([1,1,1])
with col2:
    summarize_btn = st.button("⚡ Summarize Now!", use_container_width=True)

# Summarize
if summarize_btn and uploaded_file:
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            text = ""
            total_pages = len(pdf.pages)
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

        if not text:
            st.error("❌ Could not read this PDF. It may be scanned or image-based.")
        else:
            total_words = len(text.split())
            text = text[:5000]
            processed_words = len(text.split())

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("📄 Total Pages", total_pages)
            with col_b:
                st.metric("📝 Total Words", total_words)
            with col_c:
                st.metric("⚡ Words Processed", processed_words)

            if style == "📌 Bullet Points":
                prompt = f"Summarize this in bullet points in {language}: " + text
            elif style == "📝 Short Paragraph":
                prompt = f"Summarize this in one short paragraph in {language}: " + text
            else:
                prompt = f"Give a detailed summary in {language}: " + text
        
            with st.spinner("🤔 AI is reading your PDF..."):
                progress = st.progress(0)
                progress.progress(30)
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                progress.progress(100)
            st.balloons()
            st.session_state.summary = response.choices[0].message.content
            st.session_state.original_text = text
            st.session_state.answer = ""

    except Exception as e:
        st.error(f"❌ Something went wrong: {str(e)}")

elif summarize_btn and not uploaded_file:
    st.warning("⚠️ Please upload a PDF first!")

# Results
if st.session_state.summary:
    st.success("✅ Summary Ready!")
    st.markdown("### 📋 Your Summary:")
    st.write(st.session_state.summary)

    from datetime import datetime
    date = datetime.now().strftime("%Y-%m-%d")

    download_text = f"""AI PDF SUMMARIZER
    ==================
    Date: {date}
    File: {uploaded_file.name if uploaded_file else 'Unknown'}
    Style: {style}
    Language: {language}
    ==================

    SUMMARY:
    {st.session_state.summary}
    """

    st.download_button(
    label="⬇️ Download Summary",
    data=download_text,
    file_name=f"summary_{date}.txt"
    )

    st.markdown("---")
    st.markdown("### 🙋 Ask a Question About This PDF:")
    question = st.text_input("Type your question here:")

    if st.button("💡 Get Answer"):
        with st.spinner("🤔 Finding answer..."):
            answer = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": f"Based on this text: {st.session_state.original_text}\n\nAnswer this question: {question}"}]
            )
        st.session_state.answer = answer.choices[0].message.content

    if st.session_state.answer:
        st.markdown("### 💡 Answer:")
        st.write(st.session_state.answer)

# Footer
st.markdown("---")
st.markdown("*Built with Python, Streamlit and Groq AI*")