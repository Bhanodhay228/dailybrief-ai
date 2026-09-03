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

const generateBtn =
    document.getElementById("generateBtn");

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
    document.getElementById(
        "preferencesBtn"
    );

const preferencesModal =
    document.getElementById(
        "preferencesModal"
    );

const preferencesList =
    document.getElementById(
        "preferencesList"
    );



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

    const formatted =
        now.toLocaleDateString(
            "en-IN",
            {
                weekday: "long",
                day: "numeric",
                month: "long",
                year: "numeric",
            }
        );


    document.getElementById(
        "currentDate"
    ).textContent = formatted;

}


// ==================================================
// CATEGORY BUTTONS
// ==================================================

document
    .querySelectorAll(".category")
    .forEach(button => {

        button.addEventListener(
            "click",
            () => {

                document
                    .querySelectorAll(".category")
                    .forEach(item => {

                        item.classList.remove(
                            "active"
                        );

                    });


                button.classList.add(
                    "active"
                );


                currentCategory =
                    button.dataset.category;


                if (currentBrief) {

                    renderBrief(
                        currentBrief,
                        false
                    );

                }

            }
        );

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

                        categories: [
                            "All"
                        ],

                        priorities:
                            preferences,

                    }),

                }
            );


        const data =
            await response.json();


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

    brief.classList.remove(
        "hidden"
    );


    chatSection.classList.remove(
        "hidden"
    );


    briefDate.textContent =
        data.date;


    renderImportant(
        data.important
    );


    renderNews(
        data.news
    );


    if (rebuildChat) {

        buildChatStories(
            data
        );

    }


    const total =
        filterEvents(
            [
                ...data.important,
                ...data.news,
            ]
        ).length;


    storyCount.textContent =
        `${total} stories`;

}


// ==================================================
// FILTER
// ==================================================

function filterEvents(
    events
) {

    if (
        currentCategory === "All"
    ) {

        return events;

    }


    return events.filter(
        event =>
            event.category ===
            currentCategory
    );

}


// ==================================================
// IMPORTANT STORIES
// ==================================================

function renderImportant(
    events
) {

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

function renderNews(
    events
) {

    const filtered =
        filterEvents(events);


    if (!filtered.length) {

        newsStories.innerHTML = `
            <div class="empty-state">

                <div>
                    📰
                </div>

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
        event.key_facts || [];


    const factsHTML =
        facts.length
            ? `
                <details class="details">

                    <summary>
                        🔑 Key facts
                    </summary>

                    <ul>

                        ${facts
                            .map(
                                fact =>
                                    `<li>${escapeHtml(
                                        fact
                                    )}</li>`
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

                    <strong>
                        💡 Why it matters
                    </strong>

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


    return `

        <article
            class="${
                featured
                    ? "featured-card"
                    : "news-card"
            }"
        >

            <div class="story-category">

                ${escapeHtml(
                    event.category
                )}

            </div>


            <h3 class="story-title">

                ${featured
                    ? "🚨 "
                    : ""
                }

                ${escapeHtml(
                    event.title
                )}

            </h3>


            <div class="story-meta">

                Importance
                ${Number(
                    event.importance
                ).toFixed(1)}/10

            </div>


            <p class="story-summary">

                ${escapeHtml(
                    event.summary
                )}

            </p>


            ${factsHTML}

            ${whyHTML}

            ${sourcesHTML}

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


                        time =
                            date.toLocaleString(
                                "en-IN",
                                {
                                    day: "2-digit",
                                    month: "short",
                                    year: "numeric",
                                    hour: "2-digit",
                                    minute: "2-digit",
                                }
                            );

                    }


                    return `

                        <div class="source">

                            <a
                                href="${escapeAttribute(
                                    article.url
                                )}"
                                target="_blank"
                                rel="noopener noreferrer"
                            >
                                🔗
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
// CHAT STORY LIST
// ==================================================

function buildChatStories(
    data
) {

    currentEvents = [
        ...data.important,
        ...data.news,
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

            <div>
                💡
            </div>

            <p>
                Ask anything about this story.
            </p>

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
            event.key === "Enter"
        ) {

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


    // ------------------------------------------
    // Show user message
    // ------------------------------------------

    addMessage(
        "user",
        question
    );


    questionInput.value = "";


    // ------------------------------------------
    // Disable controls
    // ------------------------------------------

    askBtn.disabled = true;

    questionInput.disabled = true;

    storySelect.disabled = true;


    // ------------------------------------------
    // AI loading
    // ------------------------------------------

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
                            "application/json",
                    },

                    body: JSON.stringify({

                        question:
                            question,

                        event:
                            event,

                        history:
                            history,

                    }),

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


        // --------------------------------------
        // Save conversation
        // --------------------------------------

        history.push({
            role: "user",
            content: question,
        });


        history.push({
            role: "assistant",
            content: data.answer,
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
            /\n/g,
            "<br>"
        );


    return clean;

}


// ==================================================
// PREFERENCES
// ==================================================

preferencesBtn.addEventListener(
    "click",
    openPreferences
);


document
    .getElementById(
        "closePreferences"
    )
    .addEventListener(
        "click",
        closePreferences
    );


document
    .getElementById(
        "savePreferences"
    )
    .addEventListener(
        "click",
        savePreferences
    );


document
    .getElementById(
        "resetPreferences"
    )
    .addEventListener(
        "click",
        resetPreferences
    );


function renderPreferences() {

    preferencesList.innerHTML =
        Object.entries(
            preferences
        )
            .map(
                ([category, priority]) => `

                    <div class="preference-row">

                        <div>

                            <strong>
                                ${escapeHtml(
                                    category
                                )}
                            </strong>

                            <small>
                                ${
                                    priority === "High"
                                        ? "Show more prominently"
                                        : priority === "Low"
                                            ? "Lower ranking"
                                            : "Balanced ranking"
                                }
                            </small>

                        </div>


                        <div class="priority-buttons">

                            ${createPriorityButton(
                                category,
                                "High",
                                priority
                            )}

                            ${createPriorityButton(
                                category,
                                "Medium",
                                priority
                            )}

                            ${createPriorityButton(
                                category,
                                "Low",
                                priority
                            )}

                        </div>

                    </div>

                `
            )
            .join("");

}


function createPriorityButton(
    category,
    value,
    current
) {

    return `

        <button
            class="priority-button ${
                current === value
                    ? "selected"
                    : ""
            }"
            data-category="${escapeAttribute(
                category
            )}"
            data-priority="${value}"
        >
            ${value}
        </button>

    `;

}


preferencesList.addEventListener(
    "click",
    event => {

        const button =
            event.target.closest(
                ".priority-button"
            );


        if (!button) {

            return;

        }


        const category =
            button.dataset.category;


        const priority =
            button.dataset.priority;


        preferences[
            category
        ] = priority;


        renderPreferences();

    }
);


function openPreferences() {

    preferencesModal.classList.remove(
        "hidden"
    );

}


function closePreferences() {

    preferencesModal.classList.add(
        "hidden"
    );

}


function savePreferences() {

    localStorage.setItem(
        "dailybrief_preferences",
        JSON.stringify(
            preferences
        )
    );


    closePreferences();

}


// ==================================================
// RESET PREFERENCES
// ==================================================

function resetPreferences() {

    preferences = {
        ...DEFAULT_PREFERENCES
    };


    renderPreferences();

}


// ==================================================
// LOCAL STORAGE
// ==================================================

function loadPreferences() {

    try {

        const saved =
            localStorage.getItem(
                "dailybrief_preferences"
            );


        if (saved) {

            return {
                ...DEFAULT_PREFERENCES,
                ...JSON.parse(saved),
            };

        }

    } catch (error) {

        console.error(
            "Could not load preferences",
            error
        );

    }


    return {
        ...DEFAULT_PREFERENCES
    };

}


// ==================================================
// LOADING
// ==================================================

function setLoading(
    state
) {

    if (state) {

        loading.classList.remove(
            "hidden"
        );

        brief.classList.add(
            "hidden"
        );

        chatSection.classList.add(
            "hidden"
        );

    } else {

        loading.classList.add(
            "hidden"
        );

    }

}


// ==================================================
// ERROR
// ==================================================

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

}


// ==================================================
// ESCAPING
// ==================================================

function escapeHtml(
    value
) {

    if (
        value === null ||
        value === undefined
    ) {

        return "";

    }


    return String(value)

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