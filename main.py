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

st.write(
    "Personalized Indian Current Affairs & News Agent"
)

today = datetime.now()

st.caption(
    f"📅 {today.strftime('%A, %d %B %Y')}"
)


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.header("🎯 News Preferences")

selected_categories = st.sidebar.multiselect(
    "News Categories",
    ["All"] + CATEGORIES,
    default=["All"],
)


st.sidebar.markdown("---")

st.sidebar.subheader("⭐ Category Priorities")

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
)


# ==================================================
# GENERATE
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

            # New brief = new conversation
            st.session_state.chat_messages = []

            st.success(
                "Today's brief is ready! 🎉"
            )

        except Exception as e:

            st.error(
                f"Unable to generate the brief: {e}"
            )


# ==================================================
# INTRO
# ==================================================

if not st.session_state.generated:

    st.info(
        "Choose your preferences and click "
        "'🚀 Generate Today's Brief'."
    )

    st.markdown("## What DailyBrief AI does")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("### 🇮🇳 Indian News")

        st.write(
            "Collects Indian news across politics, "
            "business, technology, science, sports, "
            "health and other categories."
        )

    with col2:

        st.markdown("### 🤖 AI News Synthesis")

        st.write(
            "Combines related reports into one "
            "clear and factual news story."
        )

    with col3:

        st.markdown("### 💬 Follow-up Q&A")

        st.write(
            "Ask questions about a story and get "
            "fresh information from the web."
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
    # IMPORTANT NEWS
    # ==================================================

    st.header("🚨 You Should Know")

    if not important_events:

        st.info(
            "No critical Indian news events found."
        )

    else:

        for event in important_events:

            with st.container(border=True):

                st.subheader(
                    f"🚨 {event.title}"
                )

                st.caption(
                    f"📂 {event.category} • "
                    f"Importance: "
                    f"{event.importance:.1f}/10"
                )

                if event.summary:

                    st.write(
                        event.summary
                    )

                if event.key_facts:

                    st.markdown(
                        "### 🔑 Key Points"
                    )

                    for fact in event.key_facts:

                        st.markdown(
                            f"- {fact}"
                        )

                if event.why_it_matters:

                    st.markdown(
                        "### 💡 Why It Matters"
                    )

                    st.write(
                        event.why_it_matters
                    )

                st.markdown(
                    "### 🔗 Sources"
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
    # TODAY'S NEWS
    # ==================================================

    st.header("📰 Today's News")

    if "All" in selected_categories:

        display_events = (
            high_events
            + medium_events
            + low_events
        )[:35]

    else:

        high_events = high_events[:15]
        medium_events = medium_events[:10]
        low_events = low_events[:10]

        display_events = (
            high_events
            + medium_events
            + low_events
        )


    if not display_events:

        st.info(
            "No news found for the selected categories."
        )

    else:

        for event in display_events:

            with st.container(border=True):

                st.subheader(
                    event.title
                )

                st.caption(
                    f"📂 {event.category} • "
                    f"Importance: "
                    f"{event.importance:.1f}/10"
                )

                if event.summary:

                    st.write(
                        event.summary
                    )

                if event.key_facts:

                    st.markdown(
                        "### 🔑 Key Points"
                    )

                    for fact in event.key_facts:

                        st.markdown(
                            f"- {fact}"
                        )

                if event.why_it_matters:

                    st.markdown(
                        "### 💡 Why It Matters"
                    )

                    st.write(
                        event.why_it_matters
                    )

                st.markdown(
                    "### 🔗 Sources"
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
    # TELL ME MORE
    # ==================================================

    st.markdown("---")

    st.header("💬 Tell Me More")

    st.write(
        "Select a story and ask follow-up questions. "
        "DailyBrief AI searches for fresh information "
        "before answering."
    )


    # ==================================================
    # ALL EVENTS FOR CHAT
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

        # ----------------------------------------------
        # EVENT SELECTION
        # ----------------------------------------------

        selected_event = st.selectbox(
            "Select a news story",
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
        # SHOW PREVIOUS MESSAGES
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
            "Ask something about this story..."
        )


        if question:

            # Show user message

            with st.chat_message("user"):

                st.write(
                    question
                )


            # ------------------------------------------
            # GET AI ANSWER
            # ------------------------------------------

            with st.chat_message("assistant"):

                with st.spinner(
                    "Finding fresh information..."
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

                        # Save conversation

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


    else:

        st.info(
            "No stories are available for "
            "follow-up questions."
        )