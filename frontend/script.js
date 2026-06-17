// Configurable API URL - equivalent to an environment variable for this static frontend
const API_BASE_URL = 'http://localhost:8000';

const queryInput = document.getElementById('query-input');
const researchBtn = document.getElementById('research-btn');
const errorMessage = document.getElementById('error-message');
const loading = document.getElementById('loading');
const resultContainer = document.getElementById('result-container');
const markdownContent = document.getElementById('markdown-content');
const container = document.querySelector('.container');

researchBtn.addEventListener('click', async () => {
    const query = queryInput.value.trim();

    // 1. Restriction updated to 10 characters
    if (query.length < 10) {
        errorMessage.classList.remove('error-hidden');
        return;
    } else {
        errorMessage.classList.add('error-hidden');
    }

    // Move search bar to top
    container.classList.add('active');

    // UI State: Loading
    loading.classList.remove('hidden');
    resultContainer.classList.add('hidden');
    researchBtn.disabled = true;
    researchBtn.innerText = 'Searching...';

    try {
        // 2. Using API_BASE_URL constant
        const response = await fetch(`${API_BASE_URL}/research?question=${encodeURIComponent(query)}`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch research results');
        }

        const data = await response.json();
        
        // Render Markdown
        markdownContent.innerHTML = marked.parse(data.report);
        
        // Show Results
        resultContainer.classList.remove('hidden');
    } catch (error) {
        console.error('Error:', error);
        markdownContent.innerHTML = `<p style="color: #f87171;">Error: ${error.message}. Make sure the backend API is running at ${API_BASE_URL}</p>`;
        resultContainer.classList.remove('hidden');
    } finally {
        loading.classList.add('hidden');
        researchBtn.disabled = false;
        researchBtn.innerText = 'Research';
    }
});

// Clear error on input
queryInput.addEventListener('input', () => {
    if (queryInput.value.length >= 10) {
        errorMessage.classList.add('error-hidden');
    }
});

// Allow Enter key to trigger search
queryInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        researchBtn.click();
    }
});
