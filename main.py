import streamlit as st
from few_shots import FewShotPosts
from post_generator import generate_post
from services.pdf_service import PDFService
from utils.chunking import ChunkingService
from vectorstore.chroma_service import ChromaService, get_chroma_service
from utils.linkedin_share import (
    build_linkedin_compose_url,
    can_prefill_via_url,
    copy_to_clipboard_button,
)

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI LinkedIn Post Generator",
    page_icon="🚀",
    layout="wide"
)

# ---------------- CSS ---------------- #

st.markdown("""
<style>

.main-title{
    text-align:center;
    font-size:42px;
    font-weight:bold;
    color:#0A66C2;
}

.sub-title{
    text-align:center;
    color:gray;
    margin-bottom:30px;
}

.stButton>button{
    width:100%;
    height:50px;
    font-size:18px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ---------------- OPTIONS ---------------- #

length_options = [
    "Short",
    "Medium",
    "Long"
]

language_options = [
    "English",
    "Hinglish"
]

audience_options = [
    "Students",
    "Recruiters",
    "Software Engineers",
    "Data Scientists",
    "AI Engineers",
    "HR Professionals",
    "Startup Founders"
]

tone_options = [
    "Professional",
    "Friendly",
    "Technical",
    "Storytelling",
    "Motivational",
    "Inspirational"
]

emoji_options = [
    "None",
    "Low",
    "Medium",
    "High"
]

model_options = [
    "Groq",
    "Gemini"
]


# ---------------- MAIN APP ---------------- #

def main():

    st.markdown(
        "<div class='main-title'>🚀 AI Powered LinkedIn Post Generator</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='sub-title'>Generate engaging LinkedIn posts using Generative AI</div>",
        unsafe_allow_html=True
    )

    # Initialize Services
    fs = FewShotPosts()
    pdf_service = PDFService()
    chunking_service = ChunkingService()

    # ---------------- PDF Upload ---------------- #

    uploaded_pdf = st.file_uploader(
        "📄 Upload Resume / Portfolio / Company PDF",
        type=["pdf"]
    )

    if uploaded_pdf:

        pdf_text = pdf_service.read_pdf(uploaded_pdf)

        chunks = chunking_service.create_chunks(pdf_text)

        chroma_service = ChromaService(get_chroma_service())
        chroma_service.add_documents(chunks)

        st.success("✅ PDF Uploaded Successfully!")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("📄 Chunks Created", len(chunks))

        with col2:
            st.metric("📝 Characters", len(pdf_text))

        st.divider()

    # ---------------- INPUTS ---------------- #

    col1, col2 = st.columns(2)

    with col1:

        selected_model = st.selectbox(
            "🤖 AI Model",
            model_options
        )

        selected_tag = st.text_input(
            "📌 Enter Topic",
            placeholder="Example: AI, Machine Learning, Spring Boot, React..."
        )

        selected_length = st.selectbox(
            "📏 Length",
            length_options
        )

        selected_language = st.selectbox(
            "🌍 Language",
            language_options
        )

    with col2:

        selected_audience = st.selectbox(
            "🎯 Target Audience",
            audience_options
        )

        selected_tone = st.selectbox(
            "✍ Writing Tone",
            tone_options
        )

        selected_emoji = st.selectbox(
            "😊 Emoji Level",
            emoji_options
        )

    include_cta = st.checkbox(
        "📢 Include Call-To-Action",
        value=True
    )

    st.divider()

    # ---------------- GENERATE ---------------- #

    if "generated_post" not in st.session_state:
        st.session_state.generated_post = None

    if st.button("🚀 Generate LinkedIn Post"):

        if selected_tag.strip() == "":
            st.warning("Please enter a topic.")
            st.stop()

        retrieved_context = ""

        # Perform RAG only if a PDF is uploaded
        if uploaded_pdf:

            with st.spinner("🔍 Searching Resume..."):

                search_query = f"{selected_tag} {selected_audience} {selected_tone}"

                chroma_service = ChromaService(get_chroma_service())
                docs = chroma_service.similarity_search(
                    search_query,
                    k=3
                )

                retrieved_context = "\n\n".join(
                    [doc.page_content for doc in docs]
                )

            st.subheader("🔍 Retrieved Chunks")

            for i, doc in enumerate(docs):

                with st.expander(f"Result {i+1}"):

                    st.write(doc.page_content)

        # Generate LinkedIn Post
        with st.spinner("✍ Generating LinkedIn Post..."):

            post = generate_post(
                selected_length,
                selected_language,
                selected_tag,
                selected_audience,
                selected_tone,
                selected_emoji,
                include_cta,
                selected_model,
                retrieved_context
            )

        st.session_state.generated_post = post

    if st.session_state.generated_post:

        post = st.session_state.generated_post

        st.success("🎉 LinkedIn Post Generated Successfully!")

        st.markdown("## ✨ Generated LinkedIn Post")

        st.write(post)

        st.divider()

        st.markdown("### 📤 Share on LinkedIn")

        st.info(
            "Click below to open LinkedIn's create post page with your content pre-filled. "
            "If you're not logged in, LinkedIn will ask you to sign in on their site. "
            "Nothing is posted automatically — review and click **Post** on LinkedIn when ready."
        )

        col_copy, col_linkedin = st.columns(2)

        with col_copy:
            copy_to_clipboard_button(
                "📋 Copy Post",
                post,
                key="copy_post_btn",
            )

        with col_linkedin:
            if can_prefill_via_url(post):
                linkedin_url = build_linkedin_compose_url(post)
                st.markdown(
                    f"""
                    <a href="{linkedin_url}" target="_blank" rel="noopener noreferrer" style="
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        width: 100%;
                        height: 50px;
                        font-size: 18px;
                        font-weight: bold;
                        background: #0A66C2;
                        color: white;
                        border-radius: 8px;
                        text-decoration: none;
                    ">
                        🔗 Open in LinkedIn
                    </a>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    """
                    <a href="https://www.linkedin.com/feed/?shareActive=true" target="_blank" rel="noopener noreferrer" style="
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        width: 100%;
                        height: 50px;
                        font-size: 18px;
                        font-weight: bold;
                        background: #0A66C2;
                        color: white;
                        border-radius: 8px;
                        text-decoration: none;
                    ">
                        🔗 Open LinkedIn
                    </a>
                    """,
                    unsafe_allow_html=True,
                )
                st.caption(
                    "Post is too long to pre-fill via URL. Copy it first, then paste on LinkedIn."
                )


# ---------------- RUN ---------------- #

if __name__ == "__main__":
    main()