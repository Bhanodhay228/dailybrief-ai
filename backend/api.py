from datetime import datetime
from pathlib import Path
import sys

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from app.pipeline import DailyBriefPipeline
from app.models import NewsArticle, NewsEvent
from app.categories import CATEGORIES


# ==================================================
# APP
# ==================================================

app = FastAPI(
    title="DailyBrief AI",
    description="Personalized Indian current affairs and news API",
    version="1.0.0",
)


# ==================================================
# CORS
# ==================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================================================
# PIPELINE
# ==================================================

pipeline = DailyBriefPipeline()


# ==================================================
# REQUEST MODELS
# ==================================================

class BriefRequest(BaseModel):

    categories: list[str] = Field(
        default_factory=lambda: ["All"]
    )

    priorities: dict[str, str] = Field(
        default_factory=dict
    )


class QuestionRequest(BaseModel):

    question: str

    event: dict

    history: list[dict] = Field(
        default_factory=list
    )


# ==================================================
# HEALTH
# ==================================================

@app.get("/api/health")
def health():

    return {
        "status": "ok",
        "service": "DailyBrief AI",
    }


# ==================================================
# CATEGORIES
# ==================================================

@app.get("/api/categories")
def get_categories():

    return {
        "categories": CATEGORIES
    }


# ==================================================
# GENERATE BRIEF
# ==================================================

@app.post("/api/brief")
def generate_brief(
    request: BriefRequest
):

    try:

        # ------------------------------------------
        # Apply user priorities
        # ------------------------------------------

        for category, priority in request.priorities.items():

            if category in CATEGORIES:

                pipeline.preferences.set_priority(
                    category,
                    priority,
                )


        # ------------------------------------------
        # Run AI news pipeline
        # ------------------------------------------

        brief = pipeline.run()


        important = brief["important"]
        high = brief["high"]
        medium = brief["medium"]
        low = brief["low"]


        # ------------------------------------------
        # Category filtering
        # ------------------------------------------

        selected_categories = request.categories


        if (
            "All" not in selected_categories
            and selected_categories
        ):

            important = [
                event
                for event in important
                if event.category in selected_categories
            ]

            high = [
                event
                for event in high
                if event.category in selected_categories
            ]

            medium = [
                event
                for event in medium
                if event.category in selected_categories
            ]

            low = [
                event
                for event in low
                if event.category in selected_categories
            ]


        # ------------------------------------------
        # Display limits
        # ------------------------------------------

        important = important

        high = high[:15]

        medium = medium[:10]

        low = low[:10]


        # ------------------------------------------
        # Normal stories
        # ------------------------------------------

        normal = (
            high
            + medium
            + low
        )


        if "All" in selected_categories:

            normal = normal[:35]


        # ------------------------------------------
        # Response
        # ------------------------------------------

        return {

            "date": datetime.now().strftime(
                "%A, %d %B %Y"
            ),

            "important": [
                serialize_event(event)
                for event in important
            ],

            "news": [
                serialize_event(event)
                for event in normal
            ],

        }


    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ==================================================
# ASK ABOUT STORY
# ==================================================

@app.post("/api/ask")
def ask_question(
    request: QuestionRequest
):

    try:

        question = request.question.strip()


        if not question:

            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty.",
            )


        # ------------------------------------------
        # Rebuild event from frontend data
        # ------------------------------------------

        event = deserialize_event(
            request.event
        )


        # ------------------------------------------
        # Use fresh search + conversation history
        # ------------------------------------------

        answer = pipeline.qa.answer(
            question=question,
            event=event,
            conversation_history=request.history,
        )


        return {
            "answer": answer
        }


    except HTTPException:

        raise


    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ==================================================
# SERIALIZE EVENT
# ==================================================

def serialize_event(event):

    articles = []


    for article in event.articles:

        published_at = None


        if article.published_at:

            published_at = (
                article.published_at.isoformat()
            )


        articles.append(
            {
                "title": article.title,
                "source": article.source,
                "url": article.url,
                "published_at": published_at,
            }
        )


    return {

        "title": event.title,

        "category": event.category,

        "importance": event.importance,

        "summary": event.summary,

        "key_facts": event.key_facts,

        "why_it_matters": event.why_it_matters,

        "articles": articles,

    }


# ==================================================
# DESERIALIZE EVENT
# ==================================================

def deserialize_event(data):

    articles = []


    for item in data.get(
        "articles",
        []
    ):

        published_at = None

        raw_date = item.get(
            "published_at"
        )


        if raw_date:

            try:

                published_at = datetime.fromisoformat(
                    raw_date
                )

            except ValueError:

                published_at = None


        articles.append(
            NewsArticle(
                title=item.get(
                    "title",
                    ""
                ),

                description="",

                source=item.get(
                    "source",
                    ""
                ),

                url=item.get(
                    "url",
                    ""
                ),

                published_at=published_at,
            )
        )


    return NewsEvent(

        title=data.get(
            "title",
            ""
        ),

        category=data.get(
            "category",
            "Other"
        ),

        articles=articles,

        importance=float(
            data.get(
                "importance",
                0
            )
        ),

        summary=data.get(
            "summary",
            ""
        ),

        key_facts=data.get(
            "key_facts",
            []
        ),

        why_it_matters=data.get(
            "why_it_matters",
            ""
        ),

    )


# ==================================================
# FRONTEND
# ==================================================

frontend_path = ROOT_DIR / "frontend"


if frontend_path.exists():

    app.mount(
        "/",
        StaticFiles(
            directory=frontend_path,
            html=True,
        ),
        name="frontend",
    )