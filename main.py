import streamlit as st
from datetime import datetime

from app.pipeline import DailyBriefPipeline
from app.categories import CATEGORIES
from app.date_utils import format_published_date


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="DailyBrief AI",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main container */
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* Header */
    .hero {
        padding: 1.5rem 0 1rem 0;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .hero-subtitle {
        font-size: 1.15rem;
        opacity: 0.75;
        margin-bottom: 0.8rem;
    }

    /* Section headings */
    .section-title {
        font-size: 1.7rem;
        font-weight: 750;
        margin-top: 1rem;
        margin-bottom: 0.2rem;
    }

    .section-subtitle {
        opacity: 0.65;
        margin-bottom: 1rem;
    }

    /* News cards */
    .news-card {
        border: 1px solid rgba(128, 128, 128, 0.25);
        border-radius: 14px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        min-height: 220px;
    }

    .featured-card {
        border: 1px solid rgba(220, 80, 80, 0.35);
        border-radius: 16px;
        padding: 1.4rem;
        margin-bottom: 1.2rem;
    }

    .card-title {
        font-size: 1.15rem;
        font-weight: 700;
        line-height: 1.35;
        margin-bottom: 0.5rem;
    }

    .card-meta {
        font-size: 0.82rem;
        opacity: 0.7;
        margin-bottom: 0.8rem;
    }

    .summary {
        line-height: 1.65;
    }

    .key-point {
        margin-bottom: 0.35rem;
        line-height: 1.5;
    }

    /* Priority labels */
    .priority-high {
        font-size: 0.78rem;
        font-weight: 700;
        padding: 0.25rem 0.55rem;
        border-radius: 999px;
        border: 1px solid rgba(220, 80, 80, 0.35);
    }

    .priority-medium {
        font-size: 0.78rem;
        font-weight: 700;
        padding: 0.25rem 0.55rem;
        border-radius: 999px;
        border: 1px solid rgba(200, 150, 50, 0.35);
    }

    .priority-low {
        font-size: 0.78rem;
        font-weight: 700;
        padding: 0.25rem 0.55rem;
        border-radius: 999px;
        border: 1px solid rgba(100, 130, 180, 0.35);
    }

    /* Sources */
    .source-line {
        font-size: 0.88rem;
        margin-top: 0.3rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        opacity: 0.55;
        padding-top: 2rem;
        font-size: 0.85rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "pipeline" not in st.session_state:
    st.session_state.pipeline = DailyBriefPipeline()

if "brief" not in st.session_state:
    st.session_state.brief = None

if "generated" not in st.session_state:
    st.session_state.generated = False

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if "selected_event_title" not in st.session_state:
    st.session_state.selected_event_title = None


pipeline = st.session_state.pipeline


# ============================================================
# HERO
# ============================================================

today = datetime.now()

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">📰 DailyBrief AI</div>
        <div class="hero-subtitle">
            Your personalized Indian current affairs briefing
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    f"📅 {today.strftime('%A, %d %B %Y')}  •  "
    "AI-powered news synthesis and conversational Q&A"
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎯 Customize Brief")

st.sidebar.caption(
    "Choose categories and set how strongly each category "
    "should be prioritized."
)


selected_categories = st.sidebar.multiselect(
    "News Categories",
    ["All"] + CATEGORIES,
    default=["All"],
    help="Select All or choose individual categories.",
)


st.sidebar.markdown("---")

st.sidebar.subheader("⭐ Category Priority")


priorities = {}

for category in CATEGORIES:

    priorities[category] = st.sidebar.selectbox(
        category,
        ["Low", "Medium", "High"],
        index=1,
        key=f"priority_{category}",
    )


st.sidebar.markdown("---")


generate = st.sidebar.button(
    "🚀 Generate Today's Brief",
    use_container_width=True,
    type="primary",
)


if st.session_state.brief:

    if st.sidebar.button(
        "🔄 Generate New Brief",
        use_container_width=True,
    ):

        st.session_state.brief = None
        st.session_state.generated = False
        st.session_state.chat_messages = []
        st.session_state.selected_event_title = None

        st.rerun()


# ============================================================
# GENERATE
# ============================================================

if generate:

    for category, priority in priorities.items():

        pipeline.preferences.set_priority(
            category,
            priority,
        )

    with st.spinner(
        "Fetching and analyzing today's Indian news..."
    ):

        try:

            brief = pipeline.run()

            st.session_state.brief = brief
            st.session_state.generated = True
            st.session_state.chat_messages = []
            st.session_state.selected_event_title = None

            st.rerun()

        except Exception as e:

            st.error(
                f"Unable to generate the brief: {e}"
            )


# ============================================================
# WELCOME SCREEN
# ============================================================

if not st.session_state.generated:

    st.markdown(
        '<div class="section-title">Your daily briefing, simplified.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">'
        "Get important Indian news, understand what happened, "
        "and ask questions about any story."
        "</div>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown("### 🚨")

        st.markdown("**Know what matters**")

        st.write(
            "Important events are highlighted so you "
            "don't have to scan everything."
        )


    with col2:

        st.markdown("### 🧩")

        st.markdown("**One story, multiple reports**")

        st.write(
            "Related articles are grouped into a single "
            "real-world news event."
        )


    with col3:

        st.markdown("### 💬")

        st.markdown("**Go deeper when you want**")

        st.write(
            "Ask follow-up questions and retrieve fresh "
            "information about a story."
        )


    st.markdown("---")

    st.info(
        "👈 Select your preferences from the sidebar "
        "and click **Generate Today's Brief**."
    )


# ============================================================
# DISPLAY BRIEF
# ============================================================

if st.session_state.brief:

    brief = st.session_state.brief

    important_events = brief["important"]
    high_events = brief["high"]
    medium_events = brief["medium"]
    low_events = brief["low"]


    # ========================================================
    # CATEGORY FILTER
    # ========================================================

    if "All" not in selected_categories:

        important_events = [
            event
            for event in important_events
            if event.category in selected_categories
        ]

        high_events = [
            event
            for event in high_events
            if event.category in selected_categories
        ]

        medium_events = [
            event
            for event in medium_events
            if event.category in selected_categories
        ]

        low_events = [
            event
            for event in low_events
            if event.category in selected_categories
        ]


    # ========================================================
    # DATE HEADER
    # ========================================================

    st.markdown("---")

    st.markdown(
        f'<div class="section-title">'
        f"📰 Today's Indian News"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.caption(
        f"📅 {today.strftime('%A, %d %B %Y')}  •  "
        "Latest available reports"
    )


    # ========================================================
    # YOU SHOULD KNOW
    # ========================================================

    st.markdown("---")

    st.markdown(
        '<div class="section-title">'
        "🚨 You Should Know"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">'
        "Major events that deserve attention."
        "</div>",
        unsafe_allow_html=True,
    )


    if not important_events:

        st.info(
            "No critical events found."
        )

    else:

        for event in important_events:

            with st.container():

                st.markdown(
                    '<div class="featured-card">',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f'<div class="card-title">'
                    f"🚨 {event.title}"
                    f"</div>",
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f'<div class="card-meta">'
                    f"📂 {event.category} &nbsp; • &nbsp; "
                    f"🔥 Importance {event.importance:.1f}/10"
                    f"</div>",
                    unsafe_allow_html=True,
                )


                if event.summary:

                    st.markdown(
                        f'<div class="summary">'
                        f"{event.summary}"
                        f"</div>",
                        unsafe_allow_html=True,
                    )


                if event.key_facts:

                    st.markdown(
                        "**🔑 Key Points**"
                    )

                    for fact in event.key_facts:

                        st.markdown(
                            f'<div class="key-point">'
                            f"• {fact}"
                            f"</div>",
                            unsafe_allow_html=True,
                        )


                if event.why_it_matters:

                    st.markdown(
                        "**💡 Why It Matters**"
                    )

                    st.write(
                        event.why_it_matters
                    )


                st.markdown(
                    "**🔗 Sources**"
                )


                for article in event.articles:

                    source_name = (
                        article.source
                        or "Unknown source"
                    )

                    if article.url:

                        st.markdown(
                            f'<div class="source-line">'
                            f"🔗 [{source_name}]"
                            f"({article.url})"
                            f"</div>",
                            unsafe_allow_html=True,
                        )


                    if article.published_at:

                        st.caption(
                            "🕐 Published: "
                            + format_published_date(
                                article.published_at
                            )
                        )

                    else:

                        st.caption(
                            "🕐 Published time unavailable"
                        )


                st.markdown(
                    "</div>",
                    unsafe_allow_html=True,
                )


    # ========================================================
    # NORMAL NEWS
    # ========================================================

    st.markdown("---")

    st.markdown(
        '<div class="section-title">'
        "📰 Today's News"
        "</div>",
        unsafe_allow_html=True,
    )


    # ========================================================
    # ALL MODE
    # ========================================================

    if "All" in selected_categories:

        display_events = (
            high_events
            + medium_events
            + low_events
        )[:35]


        if display_events:

            st.caption(
                f"Showing {len(display_events)} stories"
            )


        for i in range(
            0,
            len(display_events),
            2,
        ):

            row_events = display_events[
                i:i + 2
            ]

            columns = st.columns(2)


            for column, event in zip(
                columns,
                row_events,
            ):

                with column:

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            f'<div class="card-title">'
                            f"{event.title}"
                            f"</div>",
                            unsafe_allow_html=True,
                        )


                        st.caption(
                            f"📂 {event.category}  •  "
                            f"🔥 {event.importance:.1f}/10"
                        )


                        if event.summary:

                            st.write(
                                event.summary
                            )


                        if event.key_facts:

                            with st.expander(
                                "🔑 Key Points"
                            ):

                                for fact in event.key_facts:

                                    st.markdown(
                                        f"- {fact}"
                                    )


                        if event.why_it_matters:

                            with st.expander(
                                "💡 Why It Matters"
                            ):

                                st.write(
                                    event.why_it_matters
                                )


                        with st.expander(
                            "🔗 Sources & Time"
                        ):

                            for article in event.articles:

                                source_name = (
                                    article.source
                                    or "Unknown source"
                                )


                                if article.url:

                                    st.markdown(
                                        f"[{source_name}]"
                                        f"({article.url})"
                                    )


                                if article.published_at:

                                    st.caption(
                                        "🕐 "
                                        + format_published_date(
                                            article.published_at
                                        )
                                    )

                                else:

                                    st.caption(
                                        "🕐 Published time unavailable"
                                    )


    # ========================================================
    # SPECIFIC PRIORITY MODE
    # ========================================================

    else:


        # ----------------------------------------------------
        # HIGH
        # ----------------------------------------------------

        high_events = high_events[:15]


        if high_events:

            st.markdown("---")

            st.subheader(
                "🔥 High Priority"
            )

            st.caption(
                f"{len(high_events)} stories available • "
                "maximum 15"
            )


            for event in high_events:

                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"### {event.title}"
                    )

                    st.caption(
                        f"📂 {event.category}  •  "
                        f"🔥 {event.importance:.1f}/10"
                    )


                    if event.summary:

                        st.write(
                            event.summary
                        )


                    if event.key_facts:

                        with st.expander(
                            "🔑 Key Points"
                        ):

                            for fact in event.key_facts:

                                st.markdown(
                                    f"- {fact}"
                                )


                    if event.why_it_matters:

                        with st.expander(
                            "💡 Why It Matters"
                        ):

                            st.write(
                                event.why_it_matters
                            )


                    with st.expander(
                        "🔗 Sources & Time"
                    ):

                        for article in event.articles:

                            source_name = (
                                article.source
                                or "Unknown source"
                            )


                            if article.url:

                                st.markdown(
                                    f"[{source_name}]"
                                    f"({article.url})"
                                )


                            if article.published_at:

                                st.caption(
                                    "🕐 "
                                    + format_published_date(
                                        article.published_at
                                    )
                                )

                            else:

                                st.caption(
                                    "🕐 Published time unavailable"
                                )


        # ----------------------------------------------------
        # MEDIUM
        # ----------------------------------------------------

        medium_events = medium_events[:10]


        if medium_events:

            st.markdown("---")

            st.subheader(
                "📰 Medium Priority"
            )

            st.caption(
                f"{len(medium_events)} stories available • "
                "maximum 10"
            )


            for event in medium_events:

                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"### {event.title}"
                    )

                    st.caption(
                        f"📂 {event.category}  •  "
                        f"🔥 {event.importance:.1f}/10"
                    )


                    if event.summary:

                        st.write(
                            event.summary
                        )


                    if event.key_facts:

                        with st.expander(
                            "🔑 Key Points"
                        ):

                            for fact in event.key_facts:

                                st.markdown(
                                    f"- {fact}"
                                )


                    if event.why_it_matters:

                        with st.expander(
                            "💡 Why It Matters"
                        ):

                            st.write(
                                event.why_it_matters
                            )


                    with st.expander(
                        "🔗 Sources & Time"
                    ):

                        for article in event.articles:

                            source_name = (
                                article.source
                                or "Unknown source"
                            )


                            if article.url:

                                st.markdown(
                                    f"[{source_name}]"
                                    f"({article.url})"
                                )


                            if article.published_at:

                                st.caption(
                                    "🕐 "
                                    + format_published_date(
                                        article.published_at
                                    )
                                )

                            else:

                                st.caption(
                                    "🕐 Published time unavailable"
                                )


        # ----------------------------------------------------
        # LOW
        # ----------------------------------------------------

        low_events = low_events[:10]


        if low_events:

            st.markdown("---")

            st.subheader(
                "📌 Low Priority"
            )

            st.caption(
                f"{len(low_events)} stories available • "
                "maximum 10"
            )


            for event in low_events:

                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"### {event.title}"
                    )

                    st.caption(
                        f"📂 {event.category}  •  "
                        f"🔥 {event.importance:.1f}/10"
                    )


                    if event.summary:

                        st.write(
                            event.summary
                        )


                    if event.key_facts:

                        with st.expander(
                            "🔑 Key Points"
                        ):

                            for fact in event.key_facts:

                                st.markdown(
                                    f"- {fact}"
                                )


                    if event.why_it_matters:

                        with st.expander(
                            "💡 Why It Matters"
                        ):

                            st.write(
                                event.why_it_matters
                            )


                    with st.expander(
                        "🔗 Sources & Time"
                    ):

                        for article in event.articles:

                            source_name = (
                                article.source
                                or "Unknown source"
                            )


                            if article.url:

                                st.markdown(
                                    f"[{source_name}]"
                                    f"({article.url})"
                                )


                            if article.published_at:

                                st.caption(
                                    "🕐 "
                                    + format_published_date(
                                        article.published_at
                                    )
                                )

                            else:

                                st.caption(
                                    "🕐 Published time unavailable"
                                )


    # ========================================================
    # TELL ME MORE
    # ========================================================

    st.markdown("---")

    st.markdown(
        '<div class="section-title">'
        "💬 Tell Me More"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">'
        "Choose a story and ask follow-up questions using "
        "fresh web information."
        "</div>",
        unsafe_allow_html=True,
    )


    all_events = (
        brief["important"]
        + brief["high"]
        + brief["medium"]
        + brief["low"]
    )


    unique_events = []

    seen_titles = set()


    for event in all_events:

        if event.title not in seen_titles:

            seen_titles.add(
                event.title
            )

            unique_events.append(
                event
            )


    if unique_events:

        selected_event = st.selectbox(
            "Choose a story",
            unique_events,
            format_func=lambda event: event.title,
        )


        # Reset chat when story changes

        if (
            st.session_state.selected_event_title
            != selected_event.title
        ):

            st.session_state.chat_messages = []

            st.session_state.selected_event_title = (
                selected_event.title
            )


        # Show chat history

        for message in st.session_state.chat_messages:

            with st.chat_message(
                message["role"]
            ):

                st.write(
                    message["content"]
                )


        question = st.chat_input(
            "Ask about this story..."
        )


        if question:

            with st.chat_message("user"):

                st.write(
                    question
                )


            with st.chat_message("assistant"):

                with st.spinner(
                    "Searching for fresh information..."
                ):

                    try:

                        answer = (
                            pipeline.answer_question(
                                question,
                                selected_event,
                            )
                        )

                        st.write(
                            answer
                        )


                        st.session_state.chat_messages.append(
                            {
                                "role": "user",
                                "content": question,
                            }
                        )


                        st.session_state.chat_messages.append(
                            {
                                "role": "assistant",
                                "content": answer,
                            }
                        )


                    except Exception as e:

                        st.error(
                            f"Unable to answer: {e}"
                        )


    # ========================================================
    # FOOTER
    # ========================================================

    st.markdown(
        """
        <div class="footer">
            DailyBrief AI • Indian Current Affairs &
            Conversational News Assistant
        </div>
        """,
        unsafe_allow_html=True,
    )