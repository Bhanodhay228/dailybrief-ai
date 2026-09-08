// ==================================================
// DEFAULT PREFERENCES
// ==================================================

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


// ==================================================
// STATE
// ==================================================

let currentBrief = null;
let currentCategory = "All";
let currentEvents = [];
let selectedStoryIndex = 0;
let preferences = loadPreferences();


// ==================================================
// ELEMENTS
// ==================================================

const generateBtn = document.getElementById("generateBtn");
const loading = document.getElementById("loading");
const errorBox = document.getElementById("error");
const brief = document.getElementById("brief");
const chatSection = document.getElementById("chatSection");
const importantSection = document.getElementById("importantSection");
const importantStories = document.getElementById("importantStories");
const newsStories = document.getElementById("newsStories");
const briefDate = document.getElementById("briefDate");
const storyCount = document.getElementById("storyCount");
const storySelect = document.getElementById("storySelect");
const chatMessages = document.getElementById("chatMessages");
const questionInput = document.getElementById("questionInput");
const askBtn = document.getElementById("askBtn");
const preferencesBtn = document.getElementById("preferencesBtn");
const preferencesModal = document.getElementById("preferencesModal");
const preferencesList = document.getElementById("preferencesList");


// ==================================================
// INIT
// ==================================================

displayCurrentDate();
renderPreferences();


// ==================================================
// CURRENT DATE
// ==================================================

function displayCurrentDate() {
    const now = new Date();

    const formatted = now.toLocaleDateString(
        "en-IN",
        {
            weekday: "long",
            day: "numeric",
            month: "long",
            year: "numeric"
        }
    );

    document.getElementById("currentDate").textContent = formatted;
}


// ==================================================
// CATEGORY BUTTONS
// ==================================================

document.querySelectorAll(".category").forEach(button => {

    button.addEventListener("click", () => {

        document.querySelectorAll(".category").forEach(item => {
            item.classList.remove("active");
        });

        button.classList.add("active");

        currentCategory = button.dataset.category;

        if (currentBrief) {
            renderBrief(currentBrief, false);
        }
    });

});


// ==================================================
// GENERATE
// ==================================================

generateBtn.addEventListener(
    "click",
    generateBrief
);


async function generateBrief() {

    setLoading(true);
    hideError();
    generateBtn.disabled = true;

    try {

        const response = await fetch(
            "/api/brief",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    categories: ["All"],
                    priorities: preferences
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail ||
                "Unable to generate brief."
            );
        }

        currentBrief = data;

        renderBrief(
            data,
            true
        );

    } catch (error) {

        showError(
            error.message
        );

    } finally {

        setLoading(false);
        generateBtn.disabled = false;

    }
}


// ==================================================
// RENDER BRIEF
// ==================================================

function renderBrief(
    data,
    rebuildChat = true
) {

    brief.classList.remove("hidden");
    chatSection.classList.remove("hidden");

    briefDate.textContent = data.date;

    renderImportant(
        data.important
    );

    renderNews(
        data.news
    );

    if (rebuildChat) {
        buildChatStories(data);
    }

    const total = filterEvents([
        ...data.important,
        ...data.news
    ]).length;

    storyCount.textContent =
        `${total} stories`;
}


// ==================================================
// FILTER
// ==================================================

function filterEvents(events) {

    if (currentCategory === "All") {
        return events;
    }

    return events.filter(
        event =>
            event.category === currentCategory
    );
}


// ==================================================
// IMPORTANT STORIES
// ==================================================

function renderImportant(events) {

    const filtered =
        filterEvents(events);

    if (!filtered.length) {

        importantSection.classList.add(
            "hidden"
        );

        return;
    }

    importantSection.classList.remove(
        "hidden"
    );

    importantStories.innerHTML =
        filtered
            .map(
                event =>
                    createStoryCard(
                        event,
                        true
                    )
            )
            .join("");
}


// ==================================================
// NEWS
// ==================================================

function renderNews(events) {

    const filtered =
        filterEvents(events);

    if (!filtered.length) {

        newsStories.innerHTML = `
            <div class="empty-state">
                <div>📰</div>

                <h3>
                    No stories in this category
                </h3>

                <p>
                    Try another category.
                </p>
            </div>
        `;

        return;
    }

    newsStories.innerHTML =
        filtered
            .map(
                event =>
                    createStoryCard(
                        event,
                        false
                    )
            )
            .join("");
}


// ==================================================
// STORY CARD
// ==================================================

function createStoryCard(
    event,
    featured
) {

    const facts =
        Array.isArray(event.key_facts)
            ? event.key_facts
            : [];

    /*
     * Show the first 3 key facts directly.
     * This is the main "Summarized" section.
     */
    const summaryPoints =
        facts.slice(0, 3);

    const summarizedHTML =
        summaryPoints.length
            ? `
                <div class="summarized">

                    <div class="summarized-header">
                        <span class="summary-icon">✦</span>
                        <span>Summarized</span>
                    </div>

                    <ul class="summary-points">

                        ${summaryPoints
                            .map(
                                fact =>
                                    `
                                    <li>
                                        ${escapeHtml(fact)}
                                    </li>
                                    `
                            )
                            .join("")
                        }

                    </ul>

                </div>
            `
            : event.summary
                ? `
                    <div class="summarized">

                        <div class="summarized-header">
                            <span class="summary-icon">✦</span>
                            <span>Summarized</span>
                        </div>

                        <p class="summary-fallback">
                            ${escapeHtml(event.summary)}
                        </p>

                    </div>
                `
                : "";


    /*
     * Remaining facts are available
     * through the expandable section.
     */
    const remainingFacts =
        facts.slice(3);

    const factsHTML =
        remainingFacts.length
            ? `
                <details class="details">

                    <summary>
                        More key facts
                    </summary>

                    <ul>

                        ${remainingFacts
                            .map(
                                fact =>
                                    `<li>${escapeHtml(fact)}</li>`
                            )
                            .join("")
                        }

                    </ul>

                </details>
            `
            : "";


    const whyHTML =
        event.why_it_matters
            ? `
                <div class="why">

                    <div class="why-header">
                        <span>💡</span>
                        <strong>
                            Why it matters
                        </strong>
                    </div>

                    <p>
                        ${escapeHtml(
                            event.why_it_matters
                        )}
                    </p>

                </div>
            `
            : "";


    const sourcesHTML =
        createSources(
            event.articles
        );


    const importance =
        Number(event.importance || 0);


    let importanceClass = "low";

    if (importance >= 8) {
        importanceClass = "high";
    } else if (importance >= 6) {
        importanceClass = "medium";
    }


    return `

        <article
            class="${
                featured
                    ? "featured-card"
                    : "news-card"
            }"
        >

            <div class="story-top">

                <span class="story-category">
                    ${escapeHtml(
                        event.category || "News"
                    )}
                </span>

                <span class="importance-pill ${importanceClass}">
                    ${importance.toFixed(1)}
                    <span>/10</span>
                </span>

            </div>


            <h3 class="story-title">

                ${
                    featured
                        ? `<span class="alert-icon">🚨</span>`
                        : ""
                }

                ${escapeHtml(
                    event.title
                )}

            </h3>


            ${summarizedHTML}


            ${whyHTML}


            ${factsHTML}


            ${sourcesHTML}


            <div class="story-footer">

                <span>
                    ${event.articles?.length || 0}
                    source${
                        (event.articles?.length || 0) === 1
                            ? ""
                            : "s"
                    }
                </span>

                <button
                    class="ask-story-button"
                    type="button"
                    onclick="askAboutStory(${escapeAttribute(
                        JSON.stringify(event.title)
                    )})"
                >
                    Ask about this →
                </button>

            </div>

        </article>

    `;
}


// ==================================================
// SOURCES
// ==================================================

function createSources(
    articles
) {

    if (
        !articles ||
        !articles.length
    ) {
        return "";
    }

    return `

        <div class="sources">

            <div class="sources-title">
                SOURCES
            </div>

            ${articles
                .map(article => {

                    let time =
                        "Time unavailable";

                    if (
                        article.published_at
                    ) {

                        const date =
                            new Date(
                                article.published_at
                            );

                        if (!isNaN(date.getTime())) {

                            time =
                                date.toLocaleString(
                                    "en-IN",
                                    {
                                        day: "2-digit",
                                        month: "short",
                                        year: "numeric",
                                        hour: "2-digit",
                                        minute: "2-digit"
                                    }
                                );

                        }
                    }

                    return `

                        <div class="source">

                            <a
                                href="${escapeAttribute(
                                    article.url || "#"
                                )}"
                                target="_blank"
                                rel="noopener noreferrer"
                            >
                                <span class="source-link-icon">
                                    ↗
                                </span>

                                ${escapeHtml(
                                    article.source ||
                                    "News source"
                                )}
                            </a>

                            <span>
                                ${time}
                            </span>

                        </div>

                    `;

                })
                .join("")
            }

        </div>

    `;
}


// ==================================================
// ASK ABOUT STORY
// ==================================================

function askAboutStory(title) {

    if (!currentEvents.length) {
        return;
    }

    const index =
        currentEvents.findIndex(
            event =>
                event.title === title
        );

    if (index === -1) {
        return;
    }

    selectedStoryIndex = index;

    storySelect.value = String(index);

    resetChat();

    chatSection.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });

    setTimeout(() => {
        questionInput.focus();
    }, 500);
}


// ==================================================
// CHAT STORY LIST
// ==================================================

function buildChatStories(
    data
) {

    currentEvents = [
        ...data.important,
        ...data.news
    ];

    storySelect.innerHTML =
        currentEvents
            .map(
                (event, index) => `
                    <option value="${index}">
                        ${escapeHtml(
                            event.title
                        )}
                    </option>
                `
            )
            .join("");

    selectedStoryIndex = 0;

    resetChat();
}


// ==================================================
// STORY CHANGE
// ==================================================

storySelect.addEventListener(
    "change",
    () => {

        selectedStoryIndex =
            Number(
                storySelect.value
            );

        resetChat();

    }
);


// ==================================================
// CHAT HISTORY
// ==================================================

const conversationHistory = {};

function getHistory() {

    if (
        !conversationHistory[
            selectedStoryIndex
        ]
    ) {

        conversationHistory[
            selectedStoryIndex
        ] = [];

    }

    return conversationHistory[
        selectedStoryIndex
    ];
}


// ==================================================
// RESET CHAT
// ==================================================

function resetChat() {

    chatMessages.innerHTML = `

        <div class="chat-empty">

            <div class="chat-empty-icon">
                ✦
            </div>

            <p>
                Ask anything about this story.
            </p>

            <span>
                DailyBrief will search for fresh information.
            </span>

        </div>

    `;
}


// ==================================================
// ASK
// ==================================================

askBtn.addEventListener(
    "click",
    askQuestion
);


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


async function askQuestion() {

    const question =
        questionInput.value.trim();

    if (!question) {
        return;
    }

    if (
        !currentEvents.length
    ) {
        return;
    }

    const event =
        currentEvents[
            selectedStoryIndex
        ];

    const history =
        getHistory();


    addMessage(
        "user",
        question
    );


    questionInput.value = "";


    askBtn.disabled = true;
    questionInput.disabled = true;
    storySelect.disabled = true;


    const loadingMessage =
        addLoadingMessage();


    try {

        const response =
            await fetch(
                "/api/ask",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        question:
                            question,

                        event:
                            event,

                        history:
                            history

                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Unable to answer."
            );

        }


        removeLoadingMessage(
            loadingMessage
        );


        addAssistantMessage(
            data.answer
        );


        history.push({
            role: "user",
            content: question
        });


        history.push({
            role: "assistant",
            content: data.answer
        });


    } catch (error) {

        removeLoadingMessage(
            loadingMessage
        );

        addMessage(
            "assistant",
            `Sorry, something went wrong: ${error.message}`
        );

    } finally {

        askBtn.disabled = false;
        questionInput.disabled = false;
        storySelect.disabled = false;

        questionInput.focus();

    }

}


// ==================================================
// ADD MESSAGE
// ==================================================

function addMessage(
    role,
    content
) {

    const message =
        document.createElement(
            "div"
        );

    message.className =
        `message ${role}`;

    message.textContent =
        content;

    chatMessages.appendChild(
        message
    );

    chatMessages.scrollTop =
        chatMessages.scrollHeight;

}


// ==================================================
// LOADING MESSAGE
// ==================================================

function addLoadingMessage() {

    const message =
        document.createElement(
            "div"
        );

    message.className =
        "message assistant ai-loading";

    message.innerHTML = `

        <div class="loading-content">

            <span>
                DailyBrief is researching
            </span>

            <span class="thinking-dots">
                <span></span>
                <span></span>
                <span></span>
            </span>

        </div>

        <div class="loading-subtext">
            Searching fresh information and
            preparing a concise answer...
        </div>

    `;

    chatMessages.appendChild(
        message
    );

    chatMessages.scrollTop =
        chatMessages.scrollHeight;

    return message;
}


function removeLoadingMessage(
    message
) {

    if (
        message &&
        message.parentNode
    ) {

        message.remove();

    }

}


// ==================================================
// AI ANSWER
// ==================================================

function addAssistantMessage(
    content
) {

    const message =
        document.createElement(
            "div"
        );

    message.className =
        "message assistant";

    message.innerHTML =
        formatAssistantAnswer(
            content
        );

    chatMessages.appendChild(
        message
    );

    chatMessages.scrollTop =
        chatMessages.scrollHeight;

}


// ==================================================
// FORMAT ANSWER
// ==================================================

function formatAssistantAnswer(
    text
) {

    let clean =
        escapeHtml(
            text || ""
        );


    clean =
        clean.replace(
            /^#{1,6}\s*/gm,
            ""
        );


    clean =
        clean.replace(
            /\*\*(.*?)\*\*/g,
            "$1"
        );


    clean =
        clean.replace(
            /^[-•*]\s+(.+)$/gm,
            "<li>$1</li>"
        );


    clean =
        clean.replace(
            /(<li>.*?<\/li>\s*)+/gs,
            match =>
                `<ul class="answer-list">${match}</ul>`
        );


    clean =
        clean.replace(
            /Direct answer:/gi,
            "<strong>Direct answer:</strong>"
        );


    clean =
        clean.replace(
            /Sources:/gi,
            '<div class="answer-sources-title">Sources</div>'
        );


    clean =
        clean.replace(
            /(https?:\/\/[^\s<]+)/g,
            '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
        );


    clean =
        clean.replace(
            /\n{2,}/g,
            "<br><br>"
        );


    clean =
        clean.replace(
            /\n/g,
            "<br>"
        );


    return clean;
}


// ==================================================
// PREFERENCES
// ==================================================

function loadPreferences() {

    try {

        const saved =
            localStorage.getItem(
                "dailybrief_preferences"
            );

        if (!saved) {
            return {
                ...DEFAULT_PREFERENCES
            };
        }

        return {
            ...DEFAULT_PREFERENCES,
            ...JSON.parse(saved)
        };

    } catch {

        return {
            ...DEFAULT_PREFERENCES
        };

    }

}


function savePreferencesToStorage() {

    localStorage.setItem(
        "dailybrief_preferences",
        JSON.stringify(
            preferences
        )
    );

}


function renderPreferences() {

    if (!preferencesList) {
        return;
    }

    preferencesList.innerHTML =
        Object.entries(
            preferences
        )
            .map(
                ([category, priority]) => `

                    <div class="preference-row">

                        <div class="preference-category">
                            ${escapeHtml(category)}
                        </div>

                        <div class="priority-options">

                            ${["Low", "Medium", "High"]
                                .map(
                                    option => `
                                        <button
                                            type="button"
                                            class="priority-button ${
                                                priority === option
                                                    ? "active"
                                                    : ""
                                            }"
                                            data-category="${escapeAttribute(category)}"
                                            data-priority="${option}"
                                        >
                                            ${option}
                                        </button>
                                    `
                                )
                                .join("")
                            }

                        </div>

                    </div>

                `
            )
            .join("");


    preferencesList
        .querySelectorAll(
            ".priority-button"
        )
        .forEach(button => {

            button.addEventListener(
                "click",
                () => {

                    const category =
                        button.dataset.category;

                    const priority =
                        button.dataset.priority;

                    preferences[category] =
                        priority;

                    renderPreferences();

                }
            );

        });

}


// ==================================================
// PREFERENCE MODAL
// ==================================================

preferencesBtn.addEventListener(
    "click",
    () => {

        preferencesModal.classList.remove(
            "hidden"
        );

    }
);


document
    .getElementById("closePreferences")
    .addEventListener(
        "click",
        closePreferences
    );


document
    .querySelector(".modal-backdrop")
    .addEventListener(
        "click",
        closePreferences
    );


function closePreferences() {

    preferencesModal.classList.add(
        "hidden"
    );

}


document
    .getElementById("resetPreferences")
    .addEventListener(
        "click",
        () => {

            preferences = {
                ...DEFAULT_PREFERENCES
            };

            renderPreferences();

        }
    );


document
    .getElementById("savePreferences")
    .addEventListener(
        "click",
        () => {

            savePreferencesToStorage();

            closePreferences();

        }
    );


// ==================================================
// LOADING / ERROR
// ==================================================

function setLoading(
    state
) {

    if (state) {

        loading.classList.remove(
            "hidden"
        );

    } else {

        loading.classList.add(
            "hidden"
        );

    }

}


function showError(
    message
) {

    errorBox.textContent =
        message;

    errorBox.classList.remove(
        "hidden"
    );

}


function hideError() {

    errorBox.classList.add(
        "hidden"
    );

    errorBox.textContent = "";

}


// ==================================================
// ESCAPING
// ==================================================

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