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
    "AI-powered news synthesis • "
    "Event clustering • "
    "Personalized ranking • "
    "Conversational Q&A"
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


# ==================================================
# GENERATE NEW BRIEF
# ==================================================

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
        "📅 Today's brief • "
        + today.strftime("%A, %d %B %Y")
    )


    st.markdown(
        "## How DailyBrief AI works"
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.markdown("### 🇮🇳")

        st.markdown(
            "**Indian News**"
        )

        st.caption(
            "News across major Indian categories."
        )


    with col2:

        st.markdown("### 🧩")

        st.markdown(
            "**Event Clustering**"
        )

        st.caption(
            "Related reports are combined into one story."
        )


    with col3:

        st.markdown("### 🎯")

        st.markdown(
            "**Personalized Ranking**"
        )

        st.caption(
            "Your priorities influence story ranking."
        )


    with col4:

        st.markdown("### 💬")

        st.markdown(
            "**Ask Questions**"
        )

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


    # ==================================================
    # EVENTS
    # ==================================================

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
    # BRIEF DATE
    # ==================================================

    today = datetime.now()


    st.markdown(
        "## 📰 Today's Indian News"
    )


    st.info(
        "📅 "
        + today.strftime("%A, %d %B %Y")
        + " • Latest available reports"
    )


    # ==================================================
    # YOU SHOULD KNOW
    # ==================================================

    st.markdown("---")


    st.header(
        "🚨 You Should Know"
    )


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


                # --------------------------------------
                # TITLE
                # --------------------------------------

                st.markdown(
                    f"## 🚨 {event.title}"
                )


                # --------------------------------------
                # CATEGORY / IMPORTANCE
                # --------------------------------------

                st.caption(
                    f"📂 {event.category}   •   "
                    f"🔥 Importance "
                    f"{event.importance:.1f}/10"
                )


                # --------------------------------------
                # SUMMARY
                # --------------------------------------

                if event.summary:

                    st.write(
                        event.summary
                    )


                # --------------------------------------
                # KEY POINTS
                # --------------------------------------

                if event.key_facts:

                    st.markdown(
                        "**🔑 Key Points**"
                    )


                    for fact in event.key_facts:

                        st.markdown(
                            f"- {fact}"
                        )


                # --------------------------------------
                # WHY IT MATTERS
                # --------------------------------------

                if event.why_it_matters:

                    st.markdown(
                        "**💡 Why It Matters**"
                    )


                    st.write(
                        event.why_it_matters
                    )


                # --------------------------------------
                # SOURCES
                # --------------------------------------

                st.markdown(
                    "**🔗 Sources & Publication Time**"
                )


                for article in event.articles:

                    source_name = (
                        article.source
                        or "Unknown source"
                    )


                    if article.url:

                        st.markdown(
                            f"- [{source_name}]"
                            f"({article.url})"
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


    # ==================================================
    # TODAY'S NEWS
    # ==================================================

    st.markdown("---")


    st.header(
        "📰 Today's News"
    )


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


        for event in display_events:

            with st.container(border=True):


                # --------------------------------------
                # TITLE
                # --------------------------------------

                st.markdown(
                    f"### {event.title}"
                )


                # --------------------------------------
                # CATEGORY / IMPORTANCE
                # --------------------------------------

                st.caption(
                    f"📂 {event.category}   •   "
                    f"🔥 Importance "
                    f"{event.importance:.1f}/10"
                )


                # --------------------------------------
                # SUMMARY
                # --------------------------------------

                if event.summary:

                    st.write(
                        event.summary
                    )


                # --------------------------------------
                # KEY POINTS
                # --------------------------------------

                if event.key_facts:

                    st.markdown(
                        "**🔑 Key Points**"
                    )


                    for fact in event.key_facts:

                        st.markdown(
                            f"- {fact}"
                        )


                # --------------------------------------
                # WHY IT MATTERS
                # --------------------------------------

                if event.why_it_matters:

                    st.markdown(
                        "**💡 Why It Matters**"
                    )


                    st.write(
                        event.why_it_matters
                    )


                # --------------------------------------
                # SOURCES / TIME
                # --------------------------------------

                st.markdown(
                    "**🔗 Sources & Publication Time**"
                )


                for article in event.articles:

                    source_name = (
                        article.source
                        or "Unknown source"
                    )


                    if article.url:

                        st.markdown(
                            f"- [{source_name}]"
                            f"({article.url})"
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


    # ==================================================
    # SPECIFIC CATEGORY MODE
    # ==================================================

    else:


        # ==================================================
        # HIGH PRIORITY
        # ==================================================

        high_events = high_events[:15]


        if high_events:

            st.subheader(
                "🔥 High Priority"
            )


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
                        "**🔗 Sources & Publication Time**"
                    )


                    for article in event.articles:

                        source_name = (
                            article.source
                            or "Unknown source"
                        )


                        if article.url:

                            st.markdown(
                                f"- [{source_name}]"
                                f"({article.url})"
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


        # ==================================================
        # MEDIUM PRIORITY
        # ==================================================

        medium_events = medium_events[:10]


        if medium_events:

            st.markdown("---")


            st.subheader(
                "📰 Medium Priority"
            )


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
                        "**🔗 Sources & Publication Time**"
                    )


                    for article in event.articles:

                        source_name = (
                            article.source
                            or "Unknown source"
                        )


                        if article.url:

                            st.markdown(
                                f"- [{source_name}]"
                                f"({article.url})"
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


        # ==================================================
        # LOW PRIORITY
        # ==================================================

        low_events = low_events[:10]


        if low_events:

            st.markdown("---")


            st.subheader(
                "📌 Low Priority"
            )


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
                        "**🔗 Sources & Publication Time**"
                    )


                    for article in event.articles:

                        source_name = (
                            article.source
                            or "Unknown source"
                        )


                        if article.url:

                            st.markdown(
                                f"- [{source_name}]"
                                f"({article.url})"
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


    # ==================================================
    # TELL ME MORE
    # ==================================================

    st.markdown("---")


    st.header(
        "💬 Tell Me More"
    )


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

            seen_titles.add(
                event.title
            )

            unique_events.append(
                event
            )


    if unique_events:

        # ----------------------------------------------
        # SELECT STORY
        # ----------------------------------------------

        selected_event = st.selectbox(
            "Choose a story",
            unique_events,
            format_func=lambda event: event.title,
        )


        # ----------------------------------------------
        # RESET CHAT WHEN STORY CHANGES
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
        # SHOW CHAT HISTORY
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

            # ------------------------------------------
            # SHOW USER QUESTION
            # ------------------------------------------

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


            # ------------------------------------------
            # GENERATE ANSWER
            # ------------------------------------------

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


                        # Save answer

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


    else:

        st.info(
            "No stories are available for "
            "follow-up questions."
        )