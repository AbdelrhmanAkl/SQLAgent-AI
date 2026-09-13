import streamlit as st

from src.graph import SQLAgentGraph


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="SQLAgent AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# Custom Styling
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       Global
       ======================================================== */

    .stApp {
        background-color: #f7fbff;
    }

    .main .block-container {
        max-width: 1200px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }


    /* ========================================================
       Hero
       ======================================================== */

    .hero {
        background: linear-gradient(
            135deg,
            #ffffff 0%,
            #eef7ff 100%
        );
        border: 1px solid #dbeafe;
        border-radius: 20px;
        padding: 2rem 2.2rem;
        margin-bottom: 1.5rem;
        box-shadow:
            0 8px 30px rgba(30, 64, 175, 0.06);
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #0f2a43;
        margin-bottom: 0.25rem;
    }

    .hero-subtitle {
        font-size: 1.15rem;
        font-weight: 600;
        color: #2563eb;
        margin-bottom: 0.8rem;
    }

    .hero-description {
        font-size: 1rem;
        color: #526579;
        line-height: 1.7;
        max-width: 900px;
    }


    /* ========================================================
       Section Titles
       ======================================================== */

    .section-title {
        font-size: 1.25rem;
        font-weight: 750;
        color: #17324d;
        margin-top: 1.5rem;
        margin-bottom: 0.7rem;
    }


    /* ========================================================
       Query Area
       ======================================================== */

    div[data-baseweb="input"] {
        border-radius: 11px;
    }


    /* ========================================================
       Example Section
       ======================================================== */

    .examples-header {
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }

    .examples-title {
        color: #17324d;
        font-size: 1rem;
        font-weight: 750;
        margin-bottom: 0.15rem;
    }

    .examples-subtitle {
        color: #64748b;
        font-size: 0.82rem;
    }

    .example-card {
        background: #ffffff;
        border: 1px solid #dbeafe;
        border-radius: 14px;
        padding: 1rem 1rem 0.9rem 1rem;
        min-height: 135px;
        box-shadow:
            0 4px 16px rgba(15, 42, 67, 0.035);
        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease,
            border-color 0.2s ease;
    }

    .example-card:hover {
        transform: translateY(-2px);
        border-color: #bfdbfe;
        box-shadow:
            0 8px 22px rgba(37, 99, 235, 0.08);
    }

    .example-icon {
        color: #2563eb;
        font-size: 1rem;
        font-weight: 800;
        margin-bottom: 0.45rem;
    }

    .example-title {
        color: #17324d;
        font-size: 0.92rem;
        font-weight: 750;
        margin-bottom: 0.3rem;
    }

    .example-description {
        color: #64748b;
        font-size: 0.78rem;
        line-height: 1.45;
        margin-bottom: 0.7rem;
    }


    /* ========================================================
       Example Buttons
       ======================================================== */

    .example-button-container {
        margin-top: -0.35rem;
    }

    .example-button-container .stButton > button {
        width: auto;
        background: transparent;
        color: #2563eb;
        border: none;
        padding: 0;
        font-size: 0.8rem;
        font-weight: 750;
        box-shadow: none;
    }

    .example-button-container .stButton > button:hover {
        background: transparent;
        color: #1d4ed8;
        border: none;
    }


    /* ========================================================
       Main Button
       ======================================================== */

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        background: #2563eb;
        color: white;
        border: none;
        font-weight: 700;
        padding: 0.65rem 1rem;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        background: #1d4ed8;
        border: none;
        color: white;
    }


    /* ========================================================
       Answer Card
       ======================================================== */

    .answer-card {
        background: #ffffff;
        border-left: 5px solid #2563eb;
        border-top: 1px solid #dbeafe;
        border-right: 1px solid #dbeafe;
        border-bottom: 1px solid #dbeafe;
        border-radius: 14px;
        padding: 1.25rem 1.4rem;
        margin-bottom: 1.2rem;
        box-shadow:
            0 5px 18px rgba(37, 99, 235, 0.05);
    }

    .answer-label {
        color: #2563eb;
        font-weight: 750;
        font-size: 0.9rem;
        margin-bottom: 0.35rem;
    }

    .answer-text {
        color: #17324d;
        font-size: 1.05rem;
        line-height: 1.65;
    }


    /* ========================================================
       Metric Cards
       ======================================================== */

    .metric-card {
        background: #ffffff;
        border: 1px solid #dbeafe;
        border-radius: 15px;
        padding: 1.1rem 1.2rem;
        text-align: center;
        box-shadow:
            0 5px 18px rgba(15, 42, 67, 0.04);
    }

    .metric-label {
        color: #64748b;
        font-size: 0.85rem;
        font-weight: 600;
    }

    .metric-value {
        color: #1d4ed8;
        font-size: 1.45rem;
        font-weight: 800;
        margin-top: 0.25rem;
    }


    /* ========================================================
       Sidebar
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #dbeafe;
    }

    .sidebar-brand {
        font-size: 1.35rem;
        font-weight: 800;
        color: #0f2a43;
        margin-bottom: 0.2rem;
    }

    .sidebar-subtitle {
        color: #64748b;
        font-size: 0.82rem;
        margin-bottom: 1.5rem;
    }

    .sidebar-card {
        background: #f0f7ff;
        border: 1px solid #dbeafe;
        border-radius: 14px;
        padding: 1rem;
        margin-bottom: 1rem;
    }

    .sidebar-card-title {
        color: #1d4ed8;
        font-weight: 750;
        margin-bottom: 0.45rem;
    }

    .sidebar-item {
        color: #475569;
        font-size: 0.88rem;
        margin: 0.45rem 0;
    }


    /* ========================================================
       Code
       ======================================================== */

    pre {
        border-radius: 12px !important;
    }


    /* ========================================================
       Streamlit Branding
       ======================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Load Agent
# ============================================================

@st.cache_resource
def load_agent():
    return SQLAgentGraph()


agent = load_agent()


# ============================================================
# Example Callback
# ============================================================

def set_example(query):
    """
    Safely update the query input using a Streamlit callback.
    This avoids modifying a widget's session state after
    the widget has already been instantiated.
    """
    st.session_state.question_input = query


# ============================================================
# Initialize Query State
# ============================================================

if "question_input" not in st.session_state:
    st.session_state.question_input = ""


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-brand">◈ SQLAgent AI</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-subtitle">'
        'Autonomous Text-to-SQL Analytics'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-card">
            <div class="sidebar-card-title">
                🔐 Security
            </div>
            <div class="sidebar-item">
                ✓ Read-only database access
            </div>
            <div class="sidebar-item">
                ✓ SELECT / WITH queries only
            </div>
            <div class="sidebar-item">
                ✓ SQL validation with sqlglot
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-card">
            <div class="sidebar-card-title">
                ⚙️ Agent Capabilities
            </div>
            <div class="sidebar-item">
                ✓ Natural Language → SQL
            </div>
            <div class="sidebar-item">
                ✓ SQLite execution
            </div>
            <div class="sidebar-item">
                ✓ Automatic SQL correction
            </div>
            <div class="sidebar-item">
                ✓ Result summarization
            </div>
            <div class="sidebar-item">
                ✓ Automatic visualization
            </div>
            <div class="sidebar-item">
                ✓ LangGraph orchestration
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-card">
            <div class="sidebar-card-title">
                🗄️ Database
            </div>
            <div class="sidebar-item">
                SQLite · Chinook
            </div>
            <div class="sidebar-item">
                11 tables
            </div>
            <div class="sidebar-item">
                Read-only analytics
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<small>Built with Python · LangGraph · Gemini · SQLite · Plotly</small>",
        unsafe_allow_html=True,
    )


# ============================================================
# Hero Section
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">
            ◈ SQLAgent AI
        </div>
        <div class="hero-subtitle">
            Autonomous Text-to-SQL Analytics Agent
        </div>
        <div class="hero-description">
            Ask questions about your database in natural language.
            SQLAgent AI generates SQL with Gemini, validates it,
            executes it safely in read-only mode, self-corrects SQL
            errors, summarizes results, and creates visualizations
            when useful.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Query Section
# ============================================================

st.markdown(
    '<div class="section-title">Ask your database</div>',
    unsafe_allow_html=True,
)


question = st.text_input(
    "Natural language question",
    placeholder="Example: Show me the top 10 customers by total spending",
    label_visibility="collapsed",
    key="question_input",
)


# ============================================================
# Try an Example
# ============================================================

st.markdown(
    """
    <div class="examples-header">
        <div class="examples-title">
            Try an example
        </div>
        <div class="examples-subtitle">
            Explore what SQLAgent AI can answer
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


example_cols = st.columns(3)


examples = [
    (
        "01",
        "Customer Analytics",
        "Find the highest-spending customers",
        "Show me the top 10 customers by total spending",
    ),
    (
        "02",
        "Revenue Insights",
        "Analyze revenue across countries",
        "Show me the total revenue by country",
    ),
    (
        "03",
        "Music Analytics",
        "Discover the most popular genres",
        "What are the most popular music genres?",
    ),
]


for col, (number, title, description, query) in zip(
    example_cols,
    examples,
):

    with col:

        st.markdown(
            f"""
            <div class="example-card">
                <div class="example-icon">
                    {number}
                </div>
                <div class="example-title">
                    {title}
                </div>
                <div class="example-description">
                    {description}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="example-button-container">',
            unsafe_allow_html=True,
        )

        st.button(
            "Explore →",
            key=f"example_{number}",
            on_click=set_example,
            args=(query,),
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )


# ============================================================
# Run Query
# ============================================================

if st.button(
    "Run Query  →",
    type="primary",
):

    if not question.strip():

        st.warning(
            "Please enter a question before running the agent."
        )

        st.stop()

    with st.spinner(
        "🤖 SQLAgent is analyzing your question..."
    ):

        try:

            result = agent.run(
                question.strip()
            )

            st.success(
                "Query completed successfully."
            )


            # ==================================================
            # Answer
            # ==================================================

            st.markdown(
                '<div class="section-title">💡 Answer</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div class="answer-card">
                    <div class="answer-label">
                        AI ANALYSIS
                    </div>
                    <div class="answer-text">
                        {result["answer"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


            # ==================================================
            # Metrics
            # ==================================================

            col1, col2, col3 = st.columns(3)


            with col1:

                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">
                            SQL Attempts
                        </div>
                        <div class="metric-value">
                            {result["attempts"]}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


            with col2:

                chart_status = (
                    "Generated"
                    if result["should_chart"]
                    else "Not needed"
                )

                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">
                            Visualization
                        </div>
                        <div class="metric-value">
                            {chart_status}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


            with col3:

                rows = len(result["result"])

                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">
                            Rows Returned
                        </div>
                        <div class="metric-value">
                            {rows}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


            # ==================================================
            # Generated SQL
            # ==================================================

            st.markdown(
                '<div class="section-title">🧠 Generated SQL</div>',
                unsafe_allow_html=True,
            )

            st.code(
                result["sql"],
                language="sql",
            )


            # ==================================================
            # Results
            # ==================================================

            if result["result"]:

                st.markdown(
                    '<div class="section-title">📊 Query Results</div>',
                    unsafe_allow_html=True,
                )

                st.dataframe(
                    result["result"],
                    use_container_width=True,
                    hide_index=True,
                )


            # ==================================================
            # Visualization
            # ==================================================

            if (
                result["should_chart"]
                and result["chart"] is not None
            ):

                st.markdown(
                    '<div class="section-title">📈 Visualization</div>',
                    unsafe_allow_html=True,
                )

                st.plotly_chart(
                    result["chart"],
                    use_container_width=True,
                )


        except Exception as exc:

            st.error(
                "The agent could not complete this request."
            )

            with st.expander(
                "Technical details"
            ):

                st.code(
                    str(exc)
                )


# ============================================================
# Footer
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        margin-top:3rem;
        padding-top:1.5rem;
        border-top:1px solid #dbeafe;
        color:#94a3b8;
        font-size:0.8rem;
    ">
        SQLAgent AI · Autonomous Text-to-SQL Analytics Agent
        <br>
        Python · LangGraph · Gemini · SQLite · Plotly
    </div>
    """,
    unsafe_allow_html=True,
)