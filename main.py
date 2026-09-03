import streamlit as st
from datetime import datetime

from app.pipeline import DailyBriefPipeline
from app.categories import CATEGORIES
from app.date_utils import format_published_date


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="DailyBrief AI",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==================================================
# SESSION STATE
# ==================================================

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


# ==================================================
# HEADER
# ==================================================

st.title("📰 DailyBrief AI")

st.markdown(
    "### Your personalized Indian current affairs brief"
)

st.caption(
    "AI-powered news synthesis • Event clustering • "
    "Personalized ranking • Conversational Q&A"
)

st.markdown("---")


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("🎯 Preferences")

st.sidebar.caption(
    "Customize how your daily brief is ranked."
)

selected_categories = st.sidebar.multiselect(
    "News Categories",
    ["All"] + CATEGORIES,
    default=["All"],
    help="Choose All or select specific categories.",
)

st.sidebar.markdown("---")

st.sidebar.subheader("⭐ Priority")

st.sidebar.caption(
    "Higher priority categories appear first."
)

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


# ==================================================
# GENERATE BRIEF
# ==================================================

if generate:

    for category, priority in priorities.items():

        pipeline.preferences.set_priority(
            category,
            priority,
        )

    with st.spinner(
        "Fetching and analyzing Indian news..."
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


# ==================================================
# INTRO SCREEN
# ==================================================

if not st.session_state.generated:

    today = datetime.now()

    st.info(
        f"📅 Today's brief • "
        f"{today.strftime('%A, %d %B %Y')}"
    )

    st.markdown("## How DailyBrief AI works")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown("### 🇮🇳")

        st.markdown("**Indian News**")

        st.caption(
            "News across major Indian categories."
        )

    with col2:

        st.markdown("### 🧩")

        st.markdown("**Event Clustering**")

        st.caption(
            "Related reports are combined into one story."
        )

    with col3:

        st.markdown("### 🎯")

        st.markdown("**Personalized Ranking**")

        st.caption(
            "Your priorities influence story ranking."
        )

    with col4:

        st.markdown("### 💬")

        st.markdown("**Ask Questions**")

        st.caption(
            "Ask follow-up questions using fresh web information."
        )

    st.markdown("---")

    st.markdown(
        "### Ready to start?"
    )

    st.write(
        "Choose your categories and priorities from "
        "the sidebar, then generate today's brief."
    )


# ==================================================
# DISPLAY BRIEF
# ==================================================

if st.session_state.brief:

    brief = st.session_state.brief

    important_events = brief["important"]
    high_events = brief["high"]
    medium_events = brief["medium"]
    low_events = brief["low"]


    # ==================================================
    # CATEGORY FILTER
    # ==================================================

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


    # ==================================================
    # DATE
    # ==================================================

    today = datetime.now()

    st.markdown(
        f"## 📅 {today.strftime('%A, %d %B %Y')}"
    )

    st.caption(
        "Today's personalized Indian news briefing"
    )


    # ==================================================
    # IMPORTANT NEWS
    # ==================================================

    st.markdown("---")

    st.header("🚨 You Should Know")

    st.caption(
        "Major events that deserve attention regardless "
        "of your selected priorities."
    )

    if not important_events:

        st.info(
            "No critical events found."
        )

    else:

        for event in important_events:

            with st.container(border=True):

                st.markdown(
                    f"## 🚨 {event.title}"
                )

                st.caption(
                    f"📂 {event.category}   •   "
                    f"🔥 Importance "
                    f"{event.importance:.1f}/10"
                )

                if event.summary:

                    st.write(
                        event.summary
                    )

                if event.key_facts:

                    st.markdown(
                        "**🔑 Key Points**"
                    )

                    for fact in event.key_facts:

                        st.markdown(
                            f"- {fact}"
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

                    if article.url:

                        source_name = (
                            article.source
                            or "Read source"
                        )

                        st.markdown(
                            f"- [{source_name}]"
                            f"({article.url})"
                        )

                        if article.published_at:

                            st.caption(
                                "📅 "
                                + format_published_date(
                                    article.published_at
                                )
                            )


    # ==================================================
    # NEWS SECTIONS
    # ==================================================

    st.markdown("---")

    st.header("📰 Today's News")


    # ==================================================
    # ALL MODE
    # ==================================================

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

    # ==================================================
    # SPECIFIC CATEGORIES
    # ==================================================

    else:

        high_events = high_events[:15]
        medium_events = medium_events[:10]
        low_events = low_events[:10]


        # ----------------------------------------------
        # HIGH PRIORITY
        # ----------------------------------------------

        if high_events:

            st.subheader("🔥 High Priority")

            st.caption(
                f"Up to 15 stories • "
                f"{len(high_events)} available"
            )

            for event in high_events:

                with st.container(border=True):

                    st.markdown(
                        f"### {event.title}"
                    )

                    st.caption(
                        f"📂 {event.category}   •   "
                        f"🔥 {event.importance:.1f}/10"
                    )

                    if event.summary:

                        st.write(
                            event.summary
                        )

                    if event.key_facts:

                        st.markdown(
                            "**🔑 Key Points**"
                        )

                        for fact in event.key_facts:

                            st.markdown(
                                f"- {fact}"
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

                        if article.url:

                            source_name = (
                                article.source
                                or "Read source"
                            )

                            st.markdown(
                                f"- [{source_name}]"
                                f"({article.url})"
                            )


        # ----------------------------------------------
        # MEDIUM PRIORITY
        # ----------------------------------------------

        if medium_events:

            st.markdown("---")

            st.subheader("📰 Medium Priority")

            st.caption(
                f"Up to 10 stories • "
                f"{len(medium_events)} available"
            )

            for event in medium_events:

                with st.container(border=True):

                    st.markdown(
                        f"### {event.title}"
                    )

                    st.caption(
                        f"📂 {event.category}   •   "
                        f"Importance "
                        f"{event.importance:.1f}/10"
                    )

                    if event.summary:

                        st.write(
                            event.summary
                        )

                    if event.key_facts:

                        st.markdown(
                            "**🔑 Key Points**"
                        )

                        for fact in event.key_facts:

                            st.markdown(
                                f"- {fact}"
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

                        if article.url:

                            source_name = (
                                article.source
                                or "Read source"
                            )

                            st.markdown(
                                f"- [{source_name}]"
                                f"({article.url})"
                            )


        # ----------------------------------------------
        # LOW PRIORITY
        # ----------------------------------------------

        if low_events:

            st.markdown("---")

            st.subheader("📌 Low Priority")

            st.caption(
                f"Up to 10 stories • "
                f"{len(low_events)} available"
            )

            for event in low_events:

                with st.container(border=True):

                    st.markdown(
                        f"### {event.title}"
                    )

                    st.caption(
                        f"📂 {event.category}   •   "
                        f"Importance "
                        f"{event.importance:.1f}/10"
                    )

                    if event.summary:

                        st.write(
                            event.summary
                        )

                    if event.key_facts:

                        st.markdown(
                            "**🔑 Key Points**"
                        )

                        for fact in event.key_facts:

                            st.markdown(
                                f"- {fact}"
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

                        if article.url:

                            source_name = (
                                article.source
                                or "Read source"
                            )

                            st.markdown(
                                f"- [{source_name}]"
                                f"({article.url})"
                            )


    # ==================================================
    # FOLLOW-UP Q&A
    # ==================================================

    st.markdown("---")

    st.header("💬 Tell Me More")

    st.write(
        "Choose a story and ask follow-up questions. "
        "Fresh web information is retrieved before "
        "the answer is generated."
    )


    # ==================================================
    # BUILD EVENT LIST
    # ==================================================

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

            seen_titles.add(event.title)

            unique_events.append(event)


    if unique_events:

        selected_event = st.selectbox(
            "Choose a story",
            unique_events,
            format_func=lambda event: event.title,
        )


        # ----------------------------------------------
        # RESET CONVERSATION WHEN STORY CHANGES
        # ----------------------------------------------

        if (
            st.session_state.selected_event_title
            != selected_event.title
        ):

            st.session_state.chat_messages = []

            st.session_state.selected_event_title = (
                selected_event.title
            )


        # ----------------------------------------------
        # CHAT HISTORY
        # ----------------------------------------------

        for message in st.session_state.chat_messages:

            with st.chat_message(
                message["role"]
            ):

                st.write(
                    message["content"]
                )


        # ----------------------------------------------
        # CHAT INPUT
        # ----------------------------------------------

        question = st.chat_input(
            "Ask about this story..."
        )


        if question:

            st.session_state.chat_messages.append(
                {
                    "role": "user",
                    "content": question,
                }
            )


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
                                "role": "assistant",
                                "content": answer,
                            }
                        )

                    except Exception as e:

                        st.error(
                            f"Unable to answer: {e}"
                        )