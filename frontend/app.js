// ============================================================
// DAILYBRIEF AI
// FRONTEND JAVASCRIPT
// ============================================================


// ============================================================
// DEFAULT PREFERENCES
// ============================================================

const DEFAULT_PREFERENCES = {
    "India / National": "Medium",
    "Politics & Government": "Medium",
    "Economy & Business": "Medium",
    "Technology & AI": "Medium",
    "Science & Space": "Medium",
    "Environment": "Medium",
    "Health": "Medium",
    "Law & Judiciary": "Medium",
    "Education": "Medium",
    "Sports": "Medium",
    "Entertainment": "Medium",
    "Other": "Medium",
};


// ============================================================
// APPLICATION STATE
// ============================================================

let currentBrief = null;
let currentCategory = "All";
let currentEvents = [];
let selectedStoryIndex = 0;
let conversationHistory = [];

let preferences = loadPreferences();


// ============================================================
// DOM ELEMENTS
// ============================================================

const generateBtn =
    document.getElementById("generateBtn");

const examBriefBtn =
    document.getElementById("examBriefBtn");

const loading =
    document.getElementById("loading");

const errorBox =
    document.getElementById("error");

const brief =
    document.getElementById("brief");

const chatSection =
    document.getElementById("chatSection");

const importantSection =
    document.getElementById("importantSection");

const importantStories =
    document.getElementById("importantStories");

const newsStories =
    document.getElementById("newsStories");

const briefDate =
    document.getElementById("briefDate");

const storyCount =
    document.getElementById("storyCount");

const storySelect =
    document.getElementById("storySelect");

const chatMessages =
    document.getElementById("chatMessages");

const questionInput =
    document.getElementById("questionInput");

const askBtn =
    document.getElementById("askBtn");

const preferencesBtn =
    document.getElementById("preferencesBtn");

const preferencesModal =
    document.getElementById("preferencesModal");

const preferencesList =
    document.getElementById("preferencesList");

const themeToggle =
    document.getElementById("themeToggle");

const themeIcon =
    document.getElementById("themeIcon");


// ============================================================
// INITIALIZATION
// ============================================================

initTheme();
displayCurrentDate();
renderPreferences();


// ============================================================
// THEME
// ============================================================

function applyTheme(theme) {

    document.body.classList.toggle(
        "dark-mode",
        theme === "dark"
    );

    if (themeIcon) {
        themeIcon.textContent =
            theme === "dark"
                ? "☀️"
                : "🌙";
    }

    if (themeToggle) {

        const isDark =
            theme === "dark";

        themeToggle.setAttribute(
            "aria-label",
            isDark
                ? "Switch to light mode"
                : "Switch to dark mode"
        );

        themeToggle.setAttribute(
            "title",
            isDark
                ? "Switch to light mode"
                : "Switch to dark mode"
        );
    }

    localStorage.setItem(
        "dailybrief-theme",
        theme
    );
}


function initTheme() {

    const savedTheme =
        localStorage.getItem(
            "dailybrief-theme"
        );

    const systemDark =
        window.matchMedia &&
        window.matchMedia(
            "(prefers-color-scheme: dark)"
        ).matches;

    applyTheme(
        savedTheme ||
        (systemDark ? "dark" : "light")
    );
}


if (themeToggle) {

    themeToggle.addEventListener("click", () => {
        const isDark = !document.body.classList.contains("dark-mode");

        applyTheme(isDark ? "dark" : "light");

        // Replay the sky animation
        const sky = document.querySelector(".theme-sky");

        if (sky) {
            sky.classList.remove("theme-changing");

            // Force browser to restart the animation
            void sky.offsetWidth;

            sky.classList.add("theme-changing");

            setTimeout(() => {
                sky.classList.remove("theme-changing");
            }, 1600);
        }
    });
}

// ============================================================
// DATE
// ============================================================

function displayCurrentDate() {

    const now =
        new Date();

    const currentDate =
        document.getElementById(
            "currentDate"
        );

    if (!currentDate) {
        return;
    }

    currentDate.textContent =
        now.toLocaleDateString(
            "en-IN",
            {
                weekday: "short",
                day: "numeric",
                month: "short",
                year: "numeric",
            }
        );
}


// ============================================================
// NORMAL DAILY BRIEF
// ============================================================

if (generateBtn) {

    generateBtn.addEventListener(
        "click",
        generateBrief
    );
}


async function generateBrief() {

    showLoading(true);
    hideError();

    try {

        const response =
            await fetch(
                "/api/brief",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",
                    },

                    body: JSON.stringify({
                        categories: ["All"],
                        preferences:
                            preferences,
                    }),
                }
            );


        if (!response.ok) {

            let errorMessage =
                "Failed to generate today's brief.";

            try {

                const errorData =
                    await response.json();

                if (errorData.detail) {

                    errorMessage =
                        typeof errorData.detail ===
                        "string"
                            ? errorData.detail
                            : JSON.stringify(
                                  errorData.detail
                              );
                }

            } catch (_) {}

            throw new Error(
                errorMessage
            );
        }


        currentBrief =
            await response.json();


        renderBrief(
            currentBrief
        );


        if (brief) {

            brief.scrollIntoView({
                behavior: "smooth",
                block: "start",
            });
        }

    } catch (error) {

        console.error(
            "Daily brief error:",
            error
        );

        showError(
            error.message ||
            "Something went wrong."
        );

    } finally {

        showLoading(false);
    }
}


// ============================================================
// GOVERNMENT EXAM CURRENT AFFAIRS
// ============================================================

if (examBriefBtn) {

    examBriefBtn.addEventListener(
        "click",
        generateExamBrief
    );
}


async function generateExamBrief() {

    console.log(
        "Government Exam Current Affairs clicked"
    );

    showLoading(true);
    hideError();


    if (examBriefBtn) {

        examBriefBtn.disabled =
            true;

        examBriefBtn.textContent =
            "Building Exam Brief...";
    }


    try {

        const response =
            await fetch(
                "/api/exam-brief",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",
                    },
                }
            );


        let data;


        try {

            data =
                await response.json();

        } catch (_) {

            throw new Error(
                "The server returned an invalid response."
            );
        }


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Unable to generate exam brief."
            );
        }


        renderExamBrief(
            data
        );

    } catch (error) {

        console.error(
            "Exam brief error:",
            error
        );

        showError(
            error.message ||
            "Unable to generate exam brief."
        );

    } finally {

        showLoading(false);


        if (examBriefBtn) {

            examBriefBtn.disabled =
                false;

            examBriefBtn.textContent =
                "Get Exam Current Affairs";
        }
    }
}


// ============================================================
// RENDER EXAM BRIEF
// ============================================================

function renderExamBrief(data) {

    const items =
        Array.isArray(data.items)
            ? data.items
            : [];


    if (!items.length) {

        showError(
            "No government exam current affairs were found."
        );

        return;
    }


    currentBrief =
        null;

    currentEvents =
        [];


    if (brief) {

        brief.classList.remove(
            "hidden"
        );
    }


    if (importantSection) {

        importantSection.classList.add(
            "hidden"
        );
    }


    if (chatSection) {

        chatSection.classList.add(
            "hidden"
        );
    }


    if (briefDate) {

        briefDate.textContent =
            "Government Exam Current Affairs";
    }


    if (storyCount) {

        storyCount.textContent =
            `${items.length} exam-focused stories`;
    }


    if (newsStories) {

        newsStories.innerHTML =
            items
                .map(
                    item =>
                        createExamCard(
                            item
                        )
                )
                .join("");

        newsStories.classList.remove(
            "hidden"
        );
    }


    if (brief) {

        brief.scrollIntoView({
            behavior: "smooth",
            block: "start",
        });
    }
}


// ============================================================
// EXAM STORY CARD
// ============================================================

function createExamCard(item) {

    const facts =
        Array.isArray(
            item.exam_facts
        )
            ? item.exam_facts
            : [];


    const factsHTML =
        facts.length
            ? `
                <div class="exam-facts">

                    <div class="exam-facts-title">
                        📝 Exam Facts
                    </div>

                    <ul>
                        ${facts
                            .map(
                                fact =>
                                    `
                                    <li>
                                        ${escapeHtml(
                                            fact
                                        )}
                                    </li>
                                    `
                            )
                            .join("")}
                    </ul>

                </div>
            `
            : "";


    const sourceHTML =
        item.url
            ? `
                <a
                    href="${escapeAttribute(
                        item.url
                    )}"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="source-link"
                >
                    🔗
                    ${escapeHtml(
                        item.source ||
                        "Source"
                    )}
                </a>
            `
            : "";


    return `
        <article class="news-card exam-card">

            <div class="story-top">

                <span class="story-category">
                    ${escapeHtml(
                        item.category ||
                        "Current Affairs"
                    )}
                </span>

                <span class="exam-badge">
                    🎯 EXAM
                </span>

            </div>


            <h3 class="story-title">
                ${escapeHtml(
                    item.title ||
                    ""
                )}
            </h3>


            ${
                item.why_important
                    ? `
                        <div class="why">

                            <div class="why-header">

                                <span>
                                    💡
                                </span>

                                <strong>
                                    Why Important
                                </strong>

                            </div>

                            <p>
                                ${escapeHtml(
                                    item.why_important
                                )}
                            </p>

                        </div>
                    `
                    : ""
            }


            ${
                item.summary
                    ? `
                        <div class="summarized">

                            <div class="summarized-header">

                                <span class="summary-icon">
                                    ✦
                                </span>

                                <span>
                                    Summary
                                </span>

                            </div>

                            <p class="summary-fallback">
                                ${escapeHtml(
                                    item.summary
                                )}
                            </p>

                        </div>
                    `
                    : ""
            }


            ${factsHTML}


            ${
                item.one_line_revision
                    ? `
                        <div class="revision-box">

                            <strong>
                                ⚡ One-Line Revision
                            </strong>

                            <p>
                                ${escapeHtml(
                                    item.one_line_revision
                                )}
                            </p>

                        </div>
                    `
                    : ""
            }


            ${
                sourceHTML
                    ? `
                        <div class="exam-source">
                            ${sourceHTML}
                        </div>
                    `
                    : ""
            }

        </article>
    `;
}


// ============================================================
// RENDER NORMAL BRIEF
// ============================================================

function renderBrief(data) {

    if (!data) {
        return;
    }


    if (brief) {

        brief.classList.remove(
            "hidden"
        );
    }


    if (chatSection) {

        chatSection.classList.remove(
            "hidden"
        );
    }


    if (
        data.date &&
        briefDate
    ) {

        briefDate.textContent =
            formatDate(
                data.date
            );
    }


    currentEvents =
        data.events ||
        data.stories ||
        data.news ||
        [];


    if (!Array.isArray(
        currentEvents
    )) {

        currentEvents =
            [];
    }


    renderImportant(
        currentEvents
    );


    renderNews(
        currentEvents
    );


    buildChatStories(
        currentEvents
    );


    updateStoryCount();


    if (
        data.message &&
        currentEvents.length === 0 &&
        newsStories
    ) {

        newsStories.innerHTML = `
            <div class="empty-state">

                <div class="empty-icon">
                    📰
                </div>

                <h3>
                    No stories available
                </h3>

                <p>
                    ${escapeHtml(
                        data.message
                    )}
                </p>

            </div>
        `;
    }
}


// ============================================================
// CATEGORY FILTERING
// ============================================================

document
    .querySelectorAll(".category")
    .forEach(
        button => {

            button.addEventListener(
                "click",
                () => {

                    document
                        .querySelectorAll(
                            ".category"
                        )
                        .forEach(
                            item => {

                                item.classList.remove(
                                    "active"
                                );
                            }
                        );


                    button.classList.add(
                        "active"
                    );


                    currentCategory =
                        button.dataset.category ||
                        button.textContent.trim();


                    renderImportant(
                        currentEvents
                    );


                    renderNews(
                        currentEvents
                    );


                    updateStoryCount();
                }
            );
        }
    );


function filterEvents(events) {

    if (!Array.isArray(events)) {

        return [];
    }


    if (
        currentCategory ===
        "All"
    ) {

        return events;
    }


    return events.filter(
        event => {

            const category =
                event.category ||
                event.topic ||
                "Other";


            return (
                normalizeCategory(
                    category
                ) ===
                normalizeCategory(
                    currentCategory
                )
            );
        }
    );
}


function normalizeCategory(
    category
) {

    return String(
        category || ""
    )
        .trim()
        .toLowerCase()
        .replace(
            /&/g,
            "and"
        )
        .replace(
            /\s+/g,
            " "
        );
}


// ============================================================
// IMPORTANT STORIES
// ============================================================

function renderImportant(events) {

    if (
        !importantSection ||
        !importantStories
    ) {

        return;
    }


    const filtered =
        filterEvents(
            events
        );


    const important =
        filtered.filter(
            event => {

                const importance =
                    String(
                        event.importance ||
                        ""
                    )
                        .trim()
                        .toLowerCase();


                return (
                    importance ===
                        "high" ||
                    importance ===
                        "critical" ||
                    importance ===
                        "very high"
                );
            }
        );


    if (!important.length) {

        importantSection.classList.add(
            "hidden"
        );

        importantStories.innerHTML =
            "";

        return;
    }


    importantSection.classList.remove(
        "hidden"
    );


    importantStories.innerHTML =
        important
            .map(
                event =>
                    createStoryCard(
                        event,
                        true
                    )
            )
            .join("");
}


// ============================================================
// NORMAL NEWS
// ============================================================

function renderNews(events) {

    if (!newsStories) {
        return;
    }


    const filtered =
        filterEvents(
            events
        );


    const normal =
        filtered.filter(
            event => {

                const importance =
                    String(
                        event.importance ||
                        ""
                    )
                        .trim()
                        .toLowerCase();


                return !(
                    importance ===
                        "high" ||
                    importance ===
                        "critical" ||
                    importance ===
                        "very high"
                );
            }
        );


    if (!normal.length) {

        newsStories.innerHTML = `
            <div class="empty-state">

                <div class="empty-icon">
                    🔎
                </div>

                <h3>
                    No stories in this category
                </h3>

                <p>
                    Try selecting another category.
                </p>

            </div>
        `;

        return;
    }


    newsStories.innerHTML =
        normal
            .map(
                event =>
                    createStoryCard(
                        event,
                        false
                    )
            )
            .join("");
}


// ============================================================
// NORMAL STORY CARD
// ============================================================

function createStoryCard(
    event,
    isImportant = false
) {

    const title =
        event.title ||
        event.headline ||
        event.name ||
        "Untitled story";


    const category =
        event.category ||
        event.topic ||
        "Other";


    const importance =
        String(
            event.importance ||
            "Medium"
        )
            .trim()
            .toLowerCase();


    const summary =
        event.summary ||
        event.description ||
        "No summary available.";


    const facts =
        Array.isArray(
            event.key_facts
        )
            ? event.key_facts
            : [];


    let summaryPoints =
        facts.slice(
            0,
            3
        );


    if (
        !summaryPoints.length &&
        event.summary
    ) {

        summaryPoints =
            event.summary
                .split(
                    /(?<=[.!?])\s+/
                )
                .filter(
                    Boolean
                )
                .slice(
                    0,
                    3
                );
    }


    const whyMatters =
        event.why_it_matters ||
        event.why_matters ||
        event.significance ||
        "";


    const sources =
        Array.isArray(
            event.sources
        )
            ? event.sources
            : [];


    const importanceClass =
        importance === "high" ||
        importance === "critical" ||
        importance === "very high"
            ? "high"
            : importance === "low"
            ? "low"
            : "medium";


    const cardClass =
        isImportant
            ? "featured-card"
            : "news-card";


    const storyIndex =
        currentEvents.indexOf(
            event
        );


    return `
        <article
            class="${cardClass} importance-${importanceClass}"
        >

            <div class="story-top">

                <span class="story-category">
                    ${escapeHtml(
                        category
                    )}
                </span>


                <span
                    class="importance-pill ${importanceClass}"
                >

                    ${
                        isImportant
                            ? "🚨 "
                            : ""
                    }

                    ${escapeHtml(
                        capitalizeFirstLetter(
                            event.importance ||
                            "Medium"
                        )
                    )}

                </span>

            </div>


            <h3 class="story-title">

                ${
                    isImportant
                        ? `
                            <span class="alert-icon">
                                🚨
                            </span>
                        `
                        : ""
                }

                ${escapeHtml(
                    title
                )}

            </h3>


            <div class="summarized">

                <div class="summarized-header">

                    <span class="summary-icon">
                        ✦
                    </span>

                    <span>
                        Summarized
                    </span>

                </div>


                ${
                    summaryPoints.length
                        ? `
                            <ul class="summary-points">

                                ${summaryPoints
                                    .map(
                                        point =>
                                            `
                                                <li>
                                                    ${escapeHtml(
                                                        String(
                                                            point
                                                        )
                                                    )}
                                                </li>
                                            `
                                    )
                                    .join("")}

                            </ul>
                        `
                        : `
                            <p class="summary-fallback">
                                ${escapeHtml(
                                    summary
                                )}
                            </p>
                        `
                }

            </div>


            ${
                facts.length > 3
                    ? `
                        <details class="details">

                            <summary>
                                More key facts
                            </summary>

                            <ul>

                                ${facts
                                    .slice(3)
                                    .map(
                                        fact =>
                                            `
                                                <li>
                                                    ${escapeHtml(
                                                        String(
                                                            fact
                                                        )
                                                    )}
                                                </li>
                                            `
                                    )
                                    .join("")}

                            </ul>

                        </details>
                    `
                    : ""
            }


            ${
                whyMatters
                    ? `
                        <div class="why">

                            <div class="why-header">

                                <span>
                                    💡
                                </span>

                                <span>
                                    Why it matters
                                </span>

                            </div>

                            <p>
                                ${escapeHtml(
                                    whyMatters
                                )}
                            </p>

                        </div>
                    `
                    : ""
            }


            ${
                sources.length
                    ? createSources(
                          sources
                      )
                    : ""
            }


            <div class="story-footer">

                <button
                    class="ask-story-button"
                    type="button"
                    onclick="askAboutStory(${storyIndex})"
                >

                    Ask about this

                    <span>
                        →
                    </span>

                </button>

            </div>

        </article>
    `;
}


// ============================================================
// SOURCES
// ============================================================

function createSources(
    sources
) {

    if (
        !Array.isArray(
            sources
        ) ||
        !sources.length
    ) {

        return "";
    }


    return `
        <div class="sources">

            <div class="sources-title">
                Sources
            </div>


            <div class="sources-list">

                ${sources
                    .map(
                        source => {

                            const sourceName =
                                source.source ||
                                source.name ||
                                source.publisher ||
                                "Source";


                            const url =
                                source.url ||
                                source.link ||
                                source.article_url ||
                                "#";


                            const publishedAt =
                                source.published_at ||
                                source.date ||
                                "";


                            return `
                                <div class="source">

                                    <a
                                        href="${escapeAttribute(
                                            url
                                        )}"
                                        target="_blank"
                                        rel="noopener noreferrer"
                                    >
                                        ${escapeHtml(
                                            sourceName
                                        )}
                                    </a>

                                    ${
                                        publishedAt
                                            ? `
                                                <span class="source-date">
                                                    ${escapeHtml(
                                                        formatDateTime(
                                                            publishedAt
                                                        )
                                                    )}
                                                </span>
                                            `
                                            : ""
                                    }

                                </div>
                            `;
                        }
                    )
                    .join("")}

            </div>

        </div>
    `;
}


// ============================================================
// STORY COUNT
// ============================================================

function updateStoryCount() {

    if (!storyCount) {
        return;
    }


    const filtered =
        filterEvents(
            currentEvents
        );


    storyCount.textContent =
        `${filtered.length} ${
            filtered.length === 1
                ? "story"
                : "stories"
        }`;
}


// ============================================================
// ASK ABOUT STORY
// ============================================================

function askAboutStory(
    index
) {

    if (
        !Array.isArray(
            currentEvents
        ) ||
        !currentEvents[index]
    ) {

        return;
    }


    selectedStoryIndex =
        index;


    if (storySelect) {

        storySelect.value =
            String(index);
    }


    resetChat();


    if (chatSection) {

        chatSection.classList.remove(
            "hidden"
        );


        chatSection.scrollIntoView({
            behavior: "smooth",
            block: "start",
        });
    }


    if (questionInput) {

        setTimeout(
            () => {
                questionInput.focus();
            },
            400
        );
    }
}


// Make available to inline onclick
window.askAboutStory =
    askAboutStory;


// ============================================================
// CHAT STORY SELECT
// ============================================================

function buildChatStories(
    events
) {

    if (!storySelect) {
        return;
    }


    storySelect.innerHTML =
        "";


    if (
        !Array.isArray(events) ||
        !events.length
    ) {

        storySelect.innerHTML =
            `
                <option value="">
                    No stories available
                </option>
            `;

        return;
    }


    events.forEach(
        (
            event,
            index
        ) => {

            const option =
                document.createElement(
                    "option"
                );


            option.value =
                String(index);


            option.textContent =
                event.title ||
                event.headline ||
                `Story ${index + 1}`;


            storySelect.appendChild(
                option
            );
        }
    );


    selectedStoryIndex =
        Math.min(
            selectedStoryIndex,
            events.length - 1
        );


    storySelect.value =
        String(
            selectedStoryIndex
        );
}


if (storySelect) {

    storySelect.addEventListener(
        "change",
        () => {

            selectedStoryIndex =
                Number(
                    storySelect.value
                ) || 0;


            resetChat();
        }
    );
}


// ============================================================
// RESET CHAT
// ============================================================

function resetChat() {

    conversationHistory =
        [];


    if (!chatMessages) {
        return;
    }


    chatMessages.innerHTML = `
        <div class="chat-empty">

            <div class="chat-empty-icon">
                💬
            </div>

            <h3>
                Ask about today's news
            </h3>

            <p>
                Ask a question about any story
                and I'll search for fresh information.
            </p>

        </div>
    `;
}


// ============================================================
// ASK BUTTON
// ============================================================

if (askBtn) {

    askBtn.addEventListener(
        "click",
        askQuestion
    );
}


if (questionInput) {

    questionInput.addEventListener(
        "keydown",
        event => {

            if (
                event.key === "Enter" &&
                !event.shiftKey
            ) {

                event.preventDefault();

                askQuestion();
            }
        }
    );
}


// ============================================================
// ASK QUESTION
// ============================================================

async function askQuestion() {

    if (
        !questionInput ||
        !askBtn
    ) {

        return;
    }


    const question =
        questionInput.value.trim();


    if (!question) {
        return;
    }


    const selectedEvent =
        currentEvents[
            selectedStoryIndex
        ];


    if (!selectedEvent) {

        showError(
            "Please generate a brief first."
        );

        return;
    }


    const title =
        selectedEvent.title ||
        selectedEvent.headline ||
        "Selected story";


    appendChatMessage(
        question,
        "user"
    );


    questionInput.value =
        "";


    askBtn.disabled =
        true;


    const loadingMessage =
        appendChatMessage(
            "Searching for fresh information…",
            "assistant",
            true
        );


    try {

        const response =
            await fetch(
                "/api/ask",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",
                    },

                    body: JSON.stringify({

                        question:
                            question,

                        story:
                            selectedEvent,

                        story_title:
                            title,

                        history:
                            conversationHistory,

                    }),
                }
            );


        if (!response.ok) {

            let message =
                "Failed to answer the question.";


            try {

                const data =
                    await response.json();


                if (data.detail) {

                    message =
                        typeof data.detail ===
                        "string"
                            ? data.detail
                            : JSON.stringify(
                                  data.detail
                              );
                }

            } catch (_) {}


            throw new Error(
                message
            );
        }


        const data =
            await response.json();


        if (loadingMessage) {

            loadingMessage.remove();
        }


        const answer =
            data.answer ||
            data.response ||
            data.message ||
            "I couldn't find an answer.";


        appendChatMessage(
            answer,
            "assistant"
        );


        conversationHistory.push({
            role: "user",
            content: question,
        });


        conversationHistory.push({
            role: "assistant",
            content: answer,
        });


    } catch (error) {

        console.error(
            "Question error:",
            error
        );


        if (loadingMessage) {

            loadingMessage.remove();
        }


        appendChatMessage(
            `Sorry, I couldn't answer that. ${
                error.message || ""
            }`,
            "assistant error-message"
        );


    } finally {

        askBtn.disabled =
            false;


        questionInput.focus();
    }
}


// ============================================================
// APPEND CHAT MESSAGE
// ============================================================

function appendChatMessage(
    text,
    role,
    temporary = false
) {

    if (!chatMessages) {
        return null;
    }


    const message =
        document.createElement(
            "div"
        );


    message.className =
        `chat-message ${role}` +
        (
            temporary
                ? " temporary"
                : ""
        );


    if (
        role ===
        "assistant"
    ) {

        message.innerHTML = `
            <div class="chat-avatar">
                AI
            </div>

            <div class="chat-bubble">
                ${formatAnswer(
                    text
                )}
            </div>
        `;

    } else {

        message.innerHTML = `
            <div class="chat-bubble">
                ${escapeHtml(
                    text
                )}
            </div>
        `;
    }


    const empty =
        chatMessages.querySelector(
            ".chat-empty"
        );


    if (empty) {
        empty.remove();
    }


    chatMessages.appendChild(
        message
    );


    chatMessages.scrollTop =
        chatMessages.scrollHeight;


    return message;
}


// ============================================================
// PREFERENCES
// ============================================================

const PREFERENCES_KEY =
    "dailybrief_preferences";


function loadPreferences() {

    try {

        const stored =
            localStorage.getItem(
                PREFERENCES_KEY
            );


        if (!stored) {

            return {
                ...DEFAULT_PREFERENCES,
            };
        }


        const parsed =
            JSON.parse(
                stored
            );


        return {
            ...DEFAULT_PREFERENCES,
            ...parsed,
        };


    } catch (error) {

        console.error(
            "Could not load preferences:",
            error
        );


        return {
            ...DEFAULT_PREFERENCES,
        };
    }
}


function savePreferences() {

    localStorage.setItem(
        PREFERENCES_KEY,
        JSON.stringify(
            preferences
        )
    );
}


// ============================================================
// RENDER PREFERENCES
// ============================================================

function renderPreferences() {

    if (!preferencesList) {
        return;
    }


    preferencesList.innerHTML =
        Object.entries(
            preferences
        )
            .map(
                (
                    [
                        category,
                        priority
                    ]
                ) => `

                    <div class="preference-row">

                        <div class="preference-name">
                            ${escapeHtml(
                                category
                            )}
                        </div>


                        <div class="priority-buttons">

                            ${[
                                "Low",
                                "Medium",
                                "High"
                            ]
                                .map(
                                    level => `
                                        <button
                                            type="button"
                                            class="priority-button ${
                                                priority ===
                                                level
                                                    ? "active"
                                                    : ""
                                            }"
                                            data-category="${escapeAttribute(
                                                category
                                            )}"
                                            data-priority="${level}"
                                        >
                                            ${level}
                                        </button>
                                    `
                                )
                                .join("")}

                        </div>

                    </div>

                `
            )
            .join("");


    preferencesList
        .querySelectorAll(
            ".priority-button"
        )
        .forEach(
            button => {

                button.addEventListener(
                    "click",
                    () => {

                        const category =
                            button.dataset
                                .category;


                        const priority =
                            button.dataset
                                .priority;


                        preferences[
                            category
                        ] =
                            priority;


                        renderPreferences();
                    }
                );
            }
        );
}


// ============================================================
// PREFERENCES MODAL
// ============================================================

if (preferencesBtn) {

    preferencesBtn.addEventListener(
        "click",
        () => {

            if (preferencesModal) {

                preferencesModal.classList.remove(
                    "hidden"
                );
            }
        }
    );
}


const closePreferencesBtn =
    document.getElementById(
        "closePreferences"
    );


const cancelPreferencesBtn =
    document.getElementById(
        "cancelPreferences"
    );


const savePreferencesBtn =
    document.getElementById(
        "savePreferences"
    );


const resetPreferencesBtn =
    document.getElementById(
        "resetPreferences"
    );


if (closePreferencesBtn) {

    closePreferencesBtn.addEventListener(
        "click",
        closePreferences
    );
}


if (cancelPreferencesBtn) {

    cancelPreferencesBtn.addEventListener(
        "click",
        closePreferences
    );
}


if (savePreferencesBtn) {

    savePreferencesBtn.addEventListener(
        "click",
        () => {

            savePreferences();

            closePreferences();
        }
    );
}


if (resetPreferencesBtn) {

    resetPreferencesBtn.addEventListener(
        "click",
        () => {

            preferences = {
                ...DEFAULT_PREFERENCES,
            };


            renderPreferences();
        }
    );
}


if (preferencesModal) {

    preferencesModal.addEventListener(
        "click",
        event => {

            if (
                event.target ===
                preferencesModal
            ) {

                closePreferences();
            }
        }
    );
}


function closePreferences() {

    if (preferencesModal) {

        preferencesModal.classList.add(
            "hidden"
        );
    }
}


// ============================================================
// LOADING
// ============================================================

function showLoading(
    show
) {

    if (loading) {

        loading.classList.toggle(
            "hidden",
            !show
        );
    }


    if (generateBtn) {

        generateBtn.disabled =
            show;
    }
}


// ============================================================
// ERROR
// ============================================================

function showError(
    message
) {

    if (!errorBox) {
        return;
    }


    errorBox.textContent =
        message;


    errorBox.classList.remove(
        "hidden"
    );


    errorBox.scrollIntoView({
        behavior: "smooth",
        block: "center",
    });
}


function hideError() {

    if (errorBox) {

        errorBox.classList.add(
            "hidden"
        );

        errorBox.textContent =
            "";
    }
}


// ============================================================
// FORMATTING
// ============================================================

function formatDate(
    dateValue
) {

    if (!dateValue) {
        return "";
    }


    const date =
        new Date(
            dateValue
        );


    if (
        Number.isNaN(
            date.getTime()
        )
    ) {

        return String(
            dateValue
        );
    }


    return date.toLocaleDateString(
        "en-IN",
        {
            weekday:
                "long",

            day:
                "numeric",

            month:
                "long",

            year:
                "numeric",
        }
    );
}


function formatDateTime(
    dateValue
) {

    if (!dateValue) {
        return "";
    }


    const date =
        new Date(
            dateValue
        );


    if (
        Number.isNaN(
            date.getTime()
        )
    ) {

        return String(
            dateValue
        );
    }


    return date.toLocaleString(
        "en-IN",
        {
            day:
                "numeric",

            month:
                "short",

            year:
                "numeric",

            hour:
                "numeric",

            minute:
                "2-digit",
        }
    );
}


function capitalizeFirstLetter(
    value
) {

    const text =
        String(
            value || ""
        );


    if (!text) {
        return "";
    }


    return (
        text.charAt(0)
            .toUpperCase() +
        text.slice(1)
    );
}


// ============================================================
// SECURITY HELPERS
// ============================================================

function escapeHtml(
    value
) {

    return String(
        value ?? ""
    )
        .replace(
            /&/g,
            "&amp;"
        )
        .replace(
            /</g,
            "&lt;"
        )
        .replace(
            />/g,
            "&gt;"
        )
        .replace(
            /"/g,
            "&quot;"
        )
        .replace(
            /'/g,
            "&#039;"
        );
}


function escapeAttribute(
    value
) {

    return escapeHtml(
        value
    );
}


// ============================================================
// CHAT ANSWER FORMATTER
// ============================================================

function formatAnswer(
    text
) {

    if (!text) {
        return "";
    }


    let html =
        escapeHtml(
            String(text)
        );


    html =
        html.replace(
            /\*\*(.*?)\*\*/g,
            "<strong>$1</strong>"
        );


    html =
        html.replace(
            /^###\s+(.*)$/gm,
            "<h4>$1</h4>"
        );


    html =
        html.replace(
            /^##\s+(.*)$/gm,
            "<h3>$1</h3>"
        );


    html =
        html.replace(
            /^#\s+(.*)$/gm,
            "<h3>$1</h3>"
        );


    html =
        html.replace(
            /^[-•]\s+(.*)$/gm,
            "<li>$1</li>"
        );


    html =
        html.replace(
            /(<li>.*<\/li>)/gs,
            "<ul>$1</ul>"
        );


    html =
        html.replace(
            /\n{2,}/g,
            "<br><br>"
        );


    html =
        html.replace(
            /\n/g,
            "<br>"
        );


    return html;
}
