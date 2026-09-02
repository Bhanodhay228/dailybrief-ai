from app.llm import MistralClient
from app.models import NewsArticle


class NewsSummarizer:
    def __init__(self):
        self.llm = MistralClient()

    def summarize(self, article: NewsArticle) -> NewsArticle:
        prompt = f"""
Analyze the following news article.

Title:
{article.title}

Description:
{article.description}

Return exactly two sections:

SUMMARY:
Write a concise 2-3 sentence summary of what happened.

WHY_IT_MATTERS:
Write 1-2 sentences explaining why this story matters to people.

Do not invent facts that are not present in the provided information.
"""

        response = self.llm.generate(prompt)

        summary_lines = []
        why_lines = []

        current_section = None

        for line in response.splitlines():
            line = line.strip()

            if line.startswith("**SUMMARY:") or line == "SUMMARY:":
                current_section = "summary"
                continue

            if (
                line.startswith("**WHY_IT_MATTERS:")
                or line == "WHY_IT_MATTERS:"
            ):
                current_section = "why"
                continue

            if line.startswith("**") and line.endswith("**"):
                line = line.strip("*").strip()

            if current_section == "summary":
                summary_lines.append(line)

            elif current_section == "why":
                why_lines.append(line)

        article.summary = " ".join(summary_lines).strip()
        article.why_it_matters = " ".join(why_lines).strip()

        return article