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
# Design Tokens (calm, light, elegant palette)
# ============================================================

CHART_COLORWAY = [
    "#7c8cf0",  # periwinkle
    "#8fd3c4",  # mint
    "#f2b8c6",  # blush
    "#f5d6a0",  # sand
    "#b7a6ee",  # lavender
    "#9bc5ee",  # sky
]


# ============================================================
# Custom Styling
# ============================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #f8f8fd;
        --bg-soft: #f1f2fb;
        --card: #ffffff;
        --border: #e9ebf7;
        --border-strong: #d9ddf5;
        --text: #2b2f45;
        --text-soft: #6b7190;
        --text-faint: #9aa0bd;
        --accent: #6f7df0;
        --accent-deep: #5766e6;
        --accent-soft: #eef0ff;
        --mint: #8fd3c4;
        --shadow-sm: 0 2px 10px rgba(80, 90, 160, 0.05);
        --shadow-md: 0 10px 30px rgba(80, 90, 160, 0.08);
    }


    /* ========================================================
       Global
       ======================================================== */

    html, body, .stApp, .stMarkdown, button, input, textarea {
        font-family: 'Inter', -apple-system, 'Segoe UI', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(900px 500px at 85% -10%, #eceeff 0%, transparent 60%),
            radial-gradient(800px 500px at -10% 10%, #eefaf6 0%, transparent 55%),
            var(--bg);
    }

    .main .block-container {
        max-width: 1180px;
        padding-top: 3.5rem;
        padding-bottom: 3rem;
    }


    /* ========================================================
       Hero
       ======================================================== */

    .hero {
        background: linear-gradient(135deg, #ffffff 0%, #f3f4ff 100%);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 2.2rem 2.4rem;
        margin-bottom: 1.6rem;
        box-shadow: var(--shadow-md);
    }

    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: var(--text);
        margin-bottom: 0.25rem;
    }

    .hero-subtitle {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--accent);
        margin-bottom: 0.9rem;
    }

    .hero-description {
        font-size: 0.98rem;
        color: var(--text-soft);
        line-height: 1.75;
        max-width: 880px;
    }


    /* ========================================================
       Section Titles
       ======================================================== */

    .section-title {
        font-size: 1.2rem;
        font-weight: 700;
        letter-spacing: -0.01em;
        color: var(--text);
        margin-top: 1.7rem;
        margin-bottom: 0.8rem;
    }


    /* ========================================================
       Query Input
       ======================================================== */

    div[data-baseweb="input"],
    div[data-baseweb="input"] > div {
        background: var(--card) !important;
        border-radius: 14px !important;
    }

    div[data-baseweb="input"] {
        border: 1px solid var(--border-strong) !important;
        box-shadow: var(--shadow-sm);
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }

    div[data-baseweb="input"]:focus-within {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 4px rgba(111, 125, 240, 0.14);
    }

    div[data-baseweb="input"] input {
        color: var(--text);
        font-size: 1rem;
        padding: 0.8rem 1rem;
    }

    div[data-baseweb="input"] input::placeholder {
        color: var(--text-faint);
    }


    /* ========================================================
       Example Section
       ======================================================== */

    .examples-header {
        margin-top: 1.4rem;
        margin-bottom: 0.9rem;
    }

    .examples-title {
        color: var(--text);
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 0.15rem;
    }

    .examples-subtitle {
        color: var(--text-faint);
        font-size: 0.84rem;
    }

    .example-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1.15rem 1.2rem 0.6rem 1.2rem;
        min-height: 130px;
        box-shadow: var(--shadow-sm);
        transition:
            transform 0.25s ease,
            box-shadow 0.25s ease,
            border-color 0.25s ease;
    }

    .example-card:hover {
        transform: translateY(-3px);
        border-color: var(--border-strong);
        box-shadow: var(--shadow-md);
    }

    .example-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 34px;
        height: 34px;
        border-radius: 10px;
        background: var(--accent-soft);
        color: var(--accent-deep);
        font-size: 0.82rem;
        font-weight: 800;
        margin-bottom: 0.7rem;
    }

    .example-title {
        color: var(--text);
        font-size: 0.97rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }

    .example-description {
        color: var(--text-soft);
        font-size: 0.84rem;
        line-height: 1.5;
        margin-bottom: 0.4rem;
    }


    /* ========================================================
       Buttons
       ======================================================== */

    /* Example "Explore" buttons -> soft text links */
    [class*="st-key-example_"] button {
        width: auto !important;
        background: transparent !important;
        color: var(--accent) !important;
        border: none !important;
        padding: 0.2rem 0.2rem !important;
        font-size: 0.84rem;
        font-weight: 700;
        box-shadow: none !important;
        margin-top: 0.1rem;
    }

    [class*="st-key-example_"] button:hover {
        background: transparent !important;
        color: var(--accent-deep) !important;
        transform: translateX(3px);
    }

    /* Primary "Run Query" button */
    button[data-testid="stBaseButton-primary"],
    button[kind="primary"] {
        min-width: 190px;
        border-radius: 14px;
        background: linear-gradient(135deg, #7f8cf3 0%, #6573ea 100%);
        color: #ffffff;
        border: none;
        font-weight: 700;
        padding: 0.7rem 1.4rem;
        box-shadow: 0 8px 20px rgba(101, 115, 234, 0.28);
        transition: all 0.2s ease;
    }

    button[data-testid="stBaseButton-primary"]:hover,
    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #7482f0 0%, #5766e6 100%);
        color: #ffffff;
        border: none;
        transform: translateY(-1px);
        box-shadow: 0 12px 26px rgba(101, 115, 234, 0.34);
    }

    button[data-testid="stBaseButton-primary"]:active,
    button[kind="primary"]:active {
        transform: translateY(0);
    }


    /* ========================================================
       Answer Card
       (st.container(key="answer_card") -> .st-key-answer_card)
       ======================================================== */

    .st-key-answer_card {
        background: var(--card);
        border: 1px solid var(--border);
        border-left: 5px solid var(--accent);
        border-radius: 18px;
        padding: 1.3rem 1.5rem;
        margin-bottom: 1.3rem;
        box-shadow: var(--shadow-md);
    }

    .st-key-answer_card p,
    .st-key-answer_card li {
        color: var(--text);
        font-size: 1.03rem;
        line-height: 1.7;
    }

    .st-key-answer_card table {
        width: auto;
        border-collapse: collapse;
        margin-top: 0.6rem;
    }

    .st-key-answer_card th,
    .st-key-answer_card td {
        border: 1px solid var(--border);
        padding: 0.5rem 0.9rem;
    }

    .st-key-answer_card th {
        background: var(--bg-soft);
        color: var(--text);
    }

    .answer-label {
        color: var(--accent);
        font-weight: 700;
        font-size: 0.78rem;
        letter-spacing: 0.08em;
        margin-bottom: 0.45rem;
    }


    /* ========================================================
       Metric Cards
       ======================================================== */

    .metric-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1.2rem 1.2rem;
        text-align: center;
        box-shadow: var(--shadow-sm);
    }

    .metric-label {
        color: var(--text-soft);
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }

    .metric-value {
        color: var(--accent-deep);
        font-size: 1.5rem;
        font-weight: 800;
        margin-top: 0.3rem;
    }


    /* ========================================================
       Sidebar
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: #fcfcff;
        border-right: 1px solid var(--border);
    }

    .sidebar-brand {
        font-size: 1.3rem;
        font-weight: 800;
        letter-spacing: -0.01em;
        color: var(--text);
        margin-bottom: 0.2rem;
    }

    .sidebar-subtitle {
        color: var(--text-faint);
        font-size: 0.82rem;
        margin-bottom: 1.4rem;
    }

    .sidebar-card {
        background: var(--bg-soft);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1rem 1.05rem;
        margin-bottom: 1rem;
    }

    .sidebar-card-title {
        color: var(--accent-deep);
        font-weight: 700;
        font-size: 0.92rem;
        margin-bottom: 0.45rem;
    }

    .sidebar-item {
        color: var(--text-soft);
        font-size: 0.86rem;
        margin: 0.4rem 0;
    }


    /* ========================================================
       Code / Dataframe / Chart
       ======================================================== */

    pre {
        border-radius: 14px !important;
        border: 1px solid var(--border) !important;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 14px;
        overflow: hidden;
        box-shadow: var(--shadow-sm);
    }

    div[data-testid="stPlotlyChart"] {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 0.6rem;
        box-shadow: var(--shadow-sm);
    }

    div[data-testid="stAlert"] {
        border-radius: 14px;
    }


    /* ========================================================
       Streamlit Chrome
       ======================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* Frosted header so toolbar icons never collide with content */
    header[data-testid="stHeader"],
    header {
        background: rgba(248, 248, 253, 0.78) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Load Agent
# ============================================================

@st.cache_resource
def load_agent(provider="groq"):
    return SQLAgentGraph(provider=provider)


# Groq is the primary provider.
# Gemini is automatically used as a fallback by the backend.
provider = "groq"

st.sidebar.markdown("### LLM Provider")
st.sidebar.info(
    "Primary: Groq\n\n"
    "Automatic fallback: Gemini"
)

agent = load_agent(provider)


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


def style_chart(fig):
    """
    Give Plotly charts the same calm, light look as the rest of the UI.
    Falls back silently if the figure doesn't support it.
    """
    try:
        fig.update_layout(
            colorway=CHART_COLORWAY,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                family="Inter, sans-serif",
                color="#4a5070",
            ),
            title_font=dict(
                size=16,
                color="#2b2f45",
            ),
            margin=dict(l=20, r=20, t=60, b=20),
        )
        fig.update_xaxes(
            gridcolor="#eceefa",
            linecolor="#e1e4f5",
            zeroline=False,
        )
        fig.update_yaxes(
            gridcolor="#eceefa",
            linecolor="#e1e4f5",
            zeroline=False,
        )
        fig.update_traces(
            marker_line_width=0,
            selector=dict(type="bar"),
        )
    except Exception:
        pass
    return fig


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
        "<small style='color:#9aa0bd'>Built with Python · LangGraph · Gemini · Groq · SQLite · Plotly</small>",
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
            SQLAgent AI generates SQL with Gemini or Groq, validates it,
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

        st.button(
            "Explore →",
            key=f"example_{number}",
            on_click=set_example,
            args=(query,),
        )


# ============================================================
# Run Query
# ============================================================

st.write("")

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

            # The answer comes from the LLM as Markdown (bold text,
            # tables, lists). It must be rendered with st.markdown
            # (not injected into a raw HTML <div>), otherwise the
            # Markdown is not parsed and stray </div> tags show up.
            with st.container(key="answer_card"):

                st.markdown(
                    '<div class="answer-label">AI ANALYSIS</div>',
                    unsafe_allow_html=True,
                )

                st.markdown(result["answer"])


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
                    style_chart(result["chart"]),
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
        border-top:1px solid #e9ebf7;
        color:#9aa0bd;
        font-size:0.8rem;
    ">
        SQLAgent AI · Autonomous Text-to-SQL Analytics Agent
        <br>
        Python · LangGraph · Gemini · Groq · SQLite · Plotly
    </div>
    """,
    unsafe_allow_html=True,
)
