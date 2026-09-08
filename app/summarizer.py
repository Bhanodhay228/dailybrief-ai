from app.llm import MistralClient
from app.models import NewsEvent


class EventSummarizer:

    def __init__(self):
        self.llm = MistralClient()

    def summarize_many(
        self,
        events: list[NewsEvent],
    ) -> list[NewsEvent]:

        if not events:
            return []

        events_text = ""

        for index, event in enumerate(events):

            articles_text = ""

            for article in event.articles:

                articles_text += f"""
SOURCE:
{article.source}

TITLE:
{article.title}

DESCRIPTION:
{article.description}
"""

            events_text += f"""
EVENT {index}

CATEGORY:
{event.category}

IMPORTANCE:
{event.importance}

ARTICLES:
{articles_text}
"""

        prompt = f"""
You are DailyBrief AI, an Indian news summarization assistant.

Summarize every news event below.

Use ONLY the information provided.
Do NOT invent facts.

{events_text}

IMPORTANT:
Return ONLY the following format.
Do not use Markdown.
Do not use **.
Do not use ###.

EVENT 0
TITLE: headline
SUMMARY: 3-4 sentence factual summary
KEY_FACTS:
- factual point 1
- factual point 2
- factual point 3
WHY_IT_MATTERS: 2-3 sentence explanation

EVENT 1
TITLE: headline
SUMMARY: 3-4 sentence factual summary
KEY_FACTS:
- factual point 1
- factual point 2
- factual point 3
WHY_IT_MATTERS: 2-3 sentence explanation

Continue for every event.

RULES:
- Keep event numbers exactly the same.
- Give exactly 3 useful key facts when possible.
- Every key fact must start with "-".
- Summary must contain actual information from the articles.
- Do not simply repeat the headline.
- Do not combine different events.
- Do not invent information.
"""

        response = self.llm.generate(prompt)

        # Debug: lets us see exactly what Mistral returned
        print("\n========== MISTRAL SUMMARY RESPONSE ==========")
        print(response)
        print("================================================\n")

        self._parse_response(response, events)

        # -------------------------------------------------
        # FALLBACK
        # -------------------------------------------------

        for event in events:

            # If Mistral returned nothing usable,
            # use the original article descriptions.
            if not event.summary:

                descriptions = []

                for article in event.articles:

                    if article.description:
                        descriptions.append(
                            article.description.strip()
                        )

                if descriptions:

                    event.summary = " ".join(
                        descriptions[:2]
                    )

            # Create visible key points
            if not event.key_facts:

                if event.summary:

                    sentences = (
                        event.summary
                        .replace("!", ".")
                        .replace("?", ".")
                        .split(".")
                    )

                    sentences = [
                        s.strip()
                        for s in sentences
                        if s.strip()
                    ]

                    event.key_facts = sentences[:3]

                # Last fallback: article titles
                if not event.key_facts:

                    event.key_facts = [
                        article.title
                        for article in event.articles[:3]
                        if article.title
                    ]

            if not event.summary:

                event.summary = (
                    "This event was identified from "
                    "the latest available Indian news."
                )

            if not event.why_it_matters:

                event.why_it_matters = (
                    "This story was included in the daily "
                    "brief based on its relevance and importance."
                )

        return events

    def _parse_response(
        self,
        response: str,
        events: list[NewsEvent],
    ):

        print("\n========== PARSING MISTRAL RESPONSE ==========")

        current_event = None
        current_section = None

        for raw_line in response.splitlines():

            line = raw_line.strip()

            if not line:
                continue

            # Remove markdown formatting
            line = line.replace("**", "")
            line = line.lstrip("#").strip()

            # ------------------------------------------
            # EVENT
            # ------------------------------------------

            if line.upper().startswith("EVENT "):

                try:
                    event_number = int(
                        line[6:].strip().rstrip(":")
                    )

                    if 0 <= event_number < len(events):

                        current_event = events[event_number]

                        current_event.summary = ""
                        current_event.key_facts = []
                        current_event.why_it_matters = ""

                        current_section = None

                        print(
                            f"Parsing EVENT {event_number}"
                        )

                except Exception as e:

                    print(
                        "EVENT parsing error:",
                        e
                    )

                continue

            if current_event is None:
                continue

            upper = line.upper()

            # ------------------------------------------
            # TITLE
            # ------------------------------------------

            if upper.startswith("TITLE:"):

                current_event.title = (
                    line.split(":", 1)[1].strip()
                )

                current_section = "title"

                continue

            # ------------------------------------------
            # SUMMARY
            # ------------------------------------------

            if upper.startswith("SUMMARY:"):

                current_event.summary = (
                    line.split(":", 1)[1].strip()
                )

                current_section = "summary"

                continue

            # ------------------------------------------
            # KEY FACTS
            # ------------------------------------------

            if (
                upper.startswith("KEY_FACTS:")
                or upper.startswith("KEY FACTS:")
                or upper.startswith("KEY-FACTS:")
            ):

                current_section = "facts"

                # Sometimes the first fact is on
                # the same line as KEY_FACTS:
                remainder = (
                    line.split(":", 1)[1].strip()
                )

                if remainder:

                    if remainder.startswith("-"):

                        fact = (
                            remainder
                            .lstrip("-")
                            .strip()
                        )

                        if fact:
                            current_event.key_facts.append(
                                fact
                            )

                continue

            # ------------------------------------------
            # WHY IT MATTERS
            # ------------------------------------------

            if (
                upper.startswith("WHY_IT_MATTERS:")
                or upper.startswith("WHY IT MATTERS:")
                or upper.startswith("WHY-IT-MATTERS:")
            ):

                current_event.why_it_matters = (
                    line.split(":", 1)[1].strip()
                )

                current_section = "why"

                continue

            # ------------------------------------------
            # CONTINUATION
            # ------------------------------------------

            if current_section == "summary":

                current_event.summary += (
                    " " + line
                )

            elif current_section == "facts":

                # -
                if line.startswith("-"):

                    fact = (
                        line
                        .lstrip("-")
                        .strip()
                    )

                    if fact:
                        current_event.key_facts.append(
                            fact
                        )

                # •
                elif line.startswith("•"):

                    fact = (
                        line
                        .lstrip("•")
                        .strip()
                    )

                    if fact:
                        current_event.key_facts.append(
                            fact
                        )

                # *
                elif line.startswith("*"):

                    fact = (
                        line
                        .lstrip("*")
                        .strip()
                    )

                    if fact:
                        current_event.key_facts.append(
                            fact
                        )

            elif current_section == "why":

                current_event.why_it_matters += (
                    " " + line
                )

    # ------------------------------------------
    # FINAL DEBUG
    # ------------------------------------------

        print("\n========== PARSED EVENTS ==========")

        for index, event in enumerate(events):

            print(f"\nEVENT {index}")
            print("TITLE:", event.title)
            print("SUMMARY:", event.summary)
            print("KEY FACTS:", event.key_facts)
            print(
                "WHY:",
                event.why_it_matters
            )

        print(
            "\n====================================\n"
        )

    # ==================================================
    # SINGLE EVENT
    # ==================================================

    def summarize(
        self,
        event: NewsEvent,
    ) -> NewsEvent:

        return self.summarize_many([event])[0]