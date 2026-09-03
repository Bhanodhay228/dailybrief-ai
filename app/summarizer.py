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
You are summarizing Indian news events.

Each EVENT below represents one real-world news event.

Create one factual synthesized story for EACH event.

Use ONLY the information provided.

Do not invent facts.

{events_text}

For every event, return exactly this format:

EVENT 0
TITLE: ...
SUMMARY: ...
KEY_FACTS:
- ...
- ...
- ...
WHY_IT_MATTERS: ...

EVENT 1
TITLE: ...
SUMMARY: ...
KEY_FACTS:
- ...
- ...
- ...
WHY_IT_MATTERS: ...

Continue for every event.

Rules:

- Keep the same event number.
- TITLE should be a clear news headline.
- SUMMARY should be 3-4 sentences.
- KEY_FACTS should contain 3-5 factual points.
- WHY_IT_MATTERS should contain 2-3 sentences.
- Do not combine different events.
- Do not invent information.
- If information is insufficient, say so.
"""

        response = self.llm.generate(prompt)

        self._parse_response(
            response,
            events,
        )

        return events


    def _parse_response(
        self,
        response: str,
        events: list[NewsEvent],
    ):

        current_event = None
        current_section = None

        for raw_line in response.splitlines():

            line = raw_line.strip()

            if not line:
                continue

            # ----------------------------------
            # EVENT
            # ----------------------------------

            if line.startswith("EVENT "):

                try:
                    event_number = int(
                        line.replace("EVENT ", "").strip()
                    )

                    if 0 <= event_number < len(events):

                        current_event = events[event_number]
                        current_section = None

                except ValueError:
                    pass

                continue


            # ----------------------------------
            # TITLE
            # ----------------------------------

            if line.startswith("TITLE:"):

                if current_event:

                    current_event.title = (
                        line.replace("TITLE:", "", 1)
                        .strip()
                    )

                current_section = "title"

                continue


            # ----------------------------------
            # SUMMARY
            # ----------------------------------

            if line.startswith("SUMMARY:"):

                if current_event:

                    current_event.summary = (
                        line.replace("SUMMARY:", "", 1)
                        .strip()
                    )

                current_section = "summary"

                continue


            # ----------------------------------
            # KEY FACTS
            # ----------------------------------

            if line.startswith("KEY_FACTS:"):

                current_section = "facts"

                continue


            # ----------------------------------
            # WHY IT MATTERS
            # ----------------------------------

            if line.startswith("WHY_IT_MATTERS:"):

                if current_event:

                    current_event.why_it_matters = (
                        line.replace(
                            "WHY_IT_MATTERS:",
                            "",
                            1,
                        ).strip()
                    )

                current_section = "why"

                continue


            # ----------------------------------
            # CONTINUATION / FACTS
            # ----------------------------------

            if current_event:

                if current_section == "summary":

                    current_event.summary += (
                        " " + line
                    )

                elif current_section == "facts":

                    if line.startswith("-"):

                        current_event.key_facts.append(
                            line.lstrip("- ").strip()
                        )

                elif current_section == "why":

                    current_event.why_it_matters += (
                        " " + line
                    )


    def summarize(
        self,
        event: NewsEvent,
    ) -> NewsEvent:

        return self.summarize_many([event])[0]