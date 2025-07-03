// Base URL for your FastAPI backend
// IMPORTANT: Replace with your actual backend URL if different
const API_BASE_URL = window.location.origin; // Assumes API is on the same origin

// Function to fetch filters from the backend
async function fetchFilters() {
    const filtersContainer = document.getElementById('filters-container');
    filtersContainer.innerHTML = '<p class="text-gray-500">Loading filters...</p>';

    try {
        const [usernamesRes, keywordsRes, feelingsRes, intentionsRes] = await Promise.all([
            fetch(`${API_BASE_URL}/distinct_usernames/`),
            fetch(`${API_BASE_URL}/distinct_keywords/`),
            fetch(`${API_BASE_URL}/distinct_feelings/`),
            fetch(`${API_BASE_URL}/distinct_intentions/`)
        ]);

        if (!usernamesRes.ok || !keywordsRes.ok || !feelingsRes.ok || !intentionsRes.ok) {
            throw new Error("Failed to fetch one or more filter lists.");
        }

        const usernames = await usernamesRes.json();
        const keywords = await keywordsRes.json();
        const feelings = await feelingsRes.json();
        const intentions = await intentionsRes.json();

        // Order filters as requested: username first
        const filters = {
            username: usernames,
            keywords: keywords,
            feeling: feelings,
            intention: intentions
        };
        renderFilters(filters);

    } catch (error) {
        console.error("Error fetching filters:", error);
        filtersContainer.innerHTML = '<p class="text-red-500">Failed to load filters.</p>';
    }
}

// Function to render filters
function renderFilters(filters) {
    const filtersContainer = document.getElementById('filters-container');
    filtersContainer.innerHTML = ''; // Clear existing content

    // Add Date Range filter
    const dateFilterGroup = document.createElement('div');
    dateFilterGroup.className = 'filter-group';
    dateFilterGroup.innerHTML = `
        <h3 class="text-lg font-medium text-gray-700 mb-2">Date Range</h3>
        <label for="start_date" class="block text-sm font-medium text-gray-700">Start Date/Time:</label>
        <input type="datetime-local" id="start_date" name="start_date" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
        <label for="end_date" class="block text-sm font-medium text-gray-700 mt-2">End Date/Time:</label>
        <input type="datetime-local" id="end_date" name="end_date" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
    `;
    filtersContainer.appendChild(dateFilterGroup);

    if (filters && Object.keys(filters).length > 0) {
        for (const category in filters) {
            const filterGroup = document.createElement('div');
            filterGroup.className = 'filter-group';
            filterGroup.innerHTML = `
                <h3 class="text-lg font-medium text-gray-700 mb-2">${category.charAt(0).toUpperCase() + category.slice(1)}</h3>
                <select name="${category}" class="block w-full px-3 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                    <option value="">All ${category.charAt(0).toUpperCase() + category.slice(1)}</option>
                    ${filters[category].map(option => `
                        <option value="${option}">${option}</option>
                    `).join('')}
                </select>
            `;
            filtersContainer.appendChild(filterGroup);
        }
    } else {
        filtersContainer.innerHTML = '<p class="text-gray-500">No filters available.</p>';
    }
}

// Function to fetch messages from the backend
async function fetchMessages(selectedFilters = {}) {
    const messagesContainer = document.getElementById('messages-container');
    const noMessagesFound = document.getElementById('no-messages-found');
    messagesContainer.innerHTML = '<p class="text-gray-500">Loading messages...</p>'; // Show loading state
    noMessagesFound.classList.add('hidden');

    try {
        // Construct query parameters from selected filters
        const queryParams = new URLSearchParams();
        for (const category in selectedFilters) {
            // For dropdowns, we expect a single value per category
            if (selectedFilters[category] && selectedFilters[category] !== "") {
                queryParams.append(category, selectedFilters[category]);
            }
        }
        const queryString = queryParams.toString();
        const url = `${API_BASE_URL}/list_messages/${queryString ? `?${queryString}` : ''}`;

        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const messages = await response.json();
        renderMessages(messages);
    } catch (error) {
        console.error("Error fetching messages:", error);
        messagesContainer.innerHTML = '<p class="text-red-500">Failed to load messages.</p>';
    }
}

 // Function to render messages
function renderMessages(messages) {
    const messagesContainer = document.getElementById('messages-container');
    const noMessagesFound = document.getElementById('no-messages-found');
    messagesContainer.innerHTML = ''; // Clear existing content

    if (messages && messages.length > 0) {
        messages.forEach(message => {
            const messageCard = document.createElement('div');
            messageCard.className = 'bg-gray-50 p-4 rounded-lg shadow-sm mb-4 border border-gray-200';

            // Prepare tags for each category
            let keywordsHtml = '';
            if (message.keywords) {
                const keywordTags = message.keywords.split(',').map(tag => tag.trim());
                if (keywordTags.length > 0 && keywordTags[0] !== "") { // Ensure there are actual keywords
                    keywordsHtml = `
                        <div class="flex items-center mt-2">
                            <span class="text-xs font-semibold text-gray-500 mr-2">Keywords:</span>
                            <div class="flex flex-wrap gap-1">
                                ${keywordTags.map(tag => `<span class="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-0.5 rounded-full">${tag}</span>`).join('')}
                            </div>
                        </div>
                    `;
                }
            }

            let feelingHtml = '';
            if (message.feeling) {
                feelingHtml = `
                    <div class="flex items-center mt-2">
                        <span class="text-xs font-semibold text-gray-500 mr-2">Feeling:</span>
                        <span class="bg-green-100 text-green-800 text-xs font-medium px-2 py-0.5 rounded-full">${message.feeling.trim()}</span>
                    </div>
                `;
            }

            let intentionHtml = '';
            if (message.intention) {
                intentionHtml = `
                    <div class="flex items-center mt-2">
                        <span class="text-xs font-semibold text-gray-500 mr-2">Intention:</span>
                        <span class="bg-purple-100 text-purple-800 text-xs font-medium px-2 py-0.5 rounded-full">${message.intention.trim()}</span>
                    </div>
                `;
            }

            messageCard.innerHTML = `
                <h3 class="text-lg font-semibold text-gray-800">${message.username || 'Unknown User'}</h3>
                <p class="text-sm text-gray-500 mb-2">
                    ${message.username || 'Unknown User'} - ${message.created_at ? new Date(message.created_at).toLocaleString() : 'Unknown Date'}
                </p>
                <p class="text-gray-700">${message.message || 'No content.'}</p>
                <div class="mt-3 border-t border-gray-200 pt-3 space-y-2">
                    ${keywordsHtml}
                    ${feelingHtml}
                    ${intentionHtml}
                </div>
            `;
            messagesContainer.appendChild(messageCard);
        });
    } else {
        noMessagesFound.classList.remove('hidden');
    }
}

// Event listener for the Reset Filters button
document.getElementById('reset-filters-btn').addEventListener('click', () => {
    // Reset all dropdowns to their default "All" option
    document.querySelectorAll('#filters-container select').forEach(selectElement => {
        selectElement.value = "";
    });
    // Fetch messages without any filters applied
    fetchMessages({});
});

// Event listener for the Apply Filters button
document.getElementById('apply-filters-btn').addEventListener('click', () => {
    const selectedFilters = {};
    // Get values from dropdowns
    document.querySelectorAll('#filters-container select').forEach(selectElement => {
        const category = selectElement.name;
        const value = selectElement.value;
        if (value !== "") { // Only add if a specific option is selected (not "All")
            selectedFilters[category] = value;
        }
    });
    // Get values from date inputs
    const startDatetime = document.getElementById('start_date').value;
    const endDatetime = document.getElementById('end_date').value;

    if (startDatetime) {
        selectedFilters.start_date = startDatetime;
    }
    if (endDatetime) {
        selectedFilters.end_date = endDatetime;
    }

    fetchMessages(selectedFilters);
});

// Initial data load on page load
document.addEventListener('DOMContentLoaded', () => {
    fetchFilters();
    fetchMessages(); // Load all messages initially
});