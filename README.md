# 📰 DailyBrief AI

## 🚀 Live Demo

[Try DailyBrief AI](https://dailybrief-ai.streamlit.app/)

> Personalized Indian Current Affairs & News Agent powered by GenAI.

DailyBrief AI is an AI-powered news briefing application that collects
Indian news, groups related reports into real-world events, generates
concise summaries, ranks stories according to user preferences, and
allows users to ask follow-up questions using fresh web information.

## ✨ Features

- 🇮🇳 Indian news across multiple categories
- 🧩 Related articles grouped into a single news event
- 🤖 AI-generated event summaries
- 🔑 Key facts for every story
- 💡 "Why It Matters" explanation
- 🎯 Personalized High / Medium / Low category priorities
- 🚨 "You Should Know" section for highly important events
- 🔗 Clickable original news sources
- 📅 Publication date and time
- 💬 Conversational follow-up questions
- 🔎 Fresh web retrieval for follow-up questions
- 📱 Streamlit web interface

## 🧠 Architecture

```text
                    Indian News
                         │
                         ▼
                  ┌─────────────┐
                  │  NewsData   │
                  └──────┬──────┘
                         │
                         ▼
                  News Articles
                         │
                         ▼
                   Deduplication
                         │
                         ▼
                 AI Categorization
                         │
                         ▼
                Importance Scoring
                         │
                         ▼
                 Event Clustering
                         │
                         ▼
                AI Event Synthesis
                         │
                         ▼
                Personalized Ranking
                         │
                         ▼
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
       🚨 You Should Know     📰 Today's News
                                    │
                                    ▼
                              💬 Tell Me More
                                    │
                                    ▼
                              Tavily Search
                                    │
                                    ▼
                              Mistral AI
                                    │
                                    ▼
                              Answer + Sources