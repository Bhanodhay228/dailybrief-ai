from app.llm import MistralClient
from app.models import NewsEvent


class EventSummarizer:
    def __init__(self):
        self.llm = MistralClient()

    def summarize(self, event: NewsEvent) -> NewsEvent:

        articles_text = ""

        for index, article in enumerate(event.articles, start=1):
            articles_text += f"""
ARTICLE {index}

Title:
{article.title}

Source:
{article.source}

Description:
{article.description}

"""

        prompt = f"""
You are summarizing a real-world news event.

Multiple articles below may describe the same event.

Create ONE factual synthesized story using only the information
provided in these articles.

{articles_text}

Return exactly these sections:

TITLE:
Create a clear headline for the combined event.

SUMMARY:
Write a concise 3-4 sentence summary combining the information.

KEY_FACTS:
Provide 3-5 important factual points.
Each point must start with "- ".

WHY_IT_MATTERS:
Explain in 2-3 sentences why this event matters.

Do not invent facts.
Do not add information that is not present in the articles.
If articles disagree or information is unclear, do not guess.
"""

        response = self.llm.generate(prompt)

        current_section = None
        title_lines = []
        summary_lines = []
        key_facts = []
        why_lines = []

        for line in response.splitlines():
            line = line.strip()

            if not line:
                continue

            clean_line = line.strip("*").strip()

            if clean_line == "TITLE:":
                current_section = "title"
                continue

            if clean_line == "SUMMARY:":
                current_section = "summary"
                continue

            if clean_line == "KEY_FACTS:":
                current_section = "facts"
                continue

            if clean_line == "WHY_IT_MATTERS:":
                current_section = "why"
                continue

            if current_section == "title":
                title_lines.append(clean_line)

            elif current_section == "summary":
                summary_lines.append(clean_line)

            elif current_section == "facts":
                if clean_line.startswith("- "):
                    key_facts.append(clean_line[2:].strip())

            elif current_section == "why":
                why_lines.append(clean_line)

        event.title = " ".join(title_lines).strip()
        event.summary = " ".join(summary_lines).strip()
        event.key_facts = key_facts
        event.why_it_matters = " ".join(why_lines).strip()

        return event