import streamlit as st
from groq import Groq

client = Groq(api_key="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")

st.set_page_config(page_title="AI Summarizer", page_icon="🤖")
st.title("🤖 AI Text Summarizer")
st.markdown("---")
st.write("✨ Paste any text below and get an instant AI summary!")

if "summary" not in st.session_state:
    st.session_state.summary = ""
if "original_text" not in st.session_state:
    st.session_state.original_text = ""

user_text = st.text_area("📝 Enter Your Text:", height=200)
style = st.selectbox("📊 Choose Summary Style:",
    ["📌 Bullet Points", "📝 Short Paragraph", "📖 Detailed Summary"])

col1, col2, col3 = st.columns([1,1,1])
with col2:
    summarize_btn = st.button("⚡ Summarize Now!", use_container_width=True)

if summarize_btn and user_text:
    if style == "📌 Bullet Points":
        prompt = "Summarize this in 3 bullet points: " + user_text
    elif style == "📝 Short Paragraph":
        prompt = "Summarize this in one short paragraph: " + user_text
    else:
        prompt = "Give a detailed summary of this: " + user_text

    with st.spinner("🤔 AI is thinking..."):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
    st.session_state.summary = response.choices[0].message.content
    st.session_state.original_text = user_text

if st.session_state.summary:
    st.success("✅ Summary Ready!")
    st.markdown("### 📋 Your Summary:")
    st.write(st.session_state.summary)
    st.markdown("---")
    st.markdown("### 🙋 Ask a Question About This Text:")
    question = st.text_input("Type your question here:")
    if st.button("Get Answer"):
        with st.spinner("🤔 Finding answer..."):
            answer = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": f"Based on this text: {st.session_state.original_text}\n\nAnswer this question: {question}"}]
            )
        st.markdown("### 💡 Answer:")
        st.write(answer.choices[0].message.content)