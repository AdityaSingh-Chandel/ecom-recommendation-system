const userIdSelect = document.getElementById('userIdSelect');
const userIdInput = document.getElementById('userIdInput');
const getRecsButton = document.getElementById('getRecsButton');
const recommendationsDiv = document.getElementById('recommendations');
const API_BASE_URL = 'http://127.0.0.1:5000';

// Function to fetch the list of valid user IDs from the API
async function fetchUserIds() {
    try {
        const response = await fetch(`${API_BASE_URL}/users`);
        if (!response.ok) {
            throw new Error('Could not fetch user IDs from the API.');
        }
        const userIds = await response.json();
        
        // Clear the default option
        userIdSelect.innerHTML = '';
        
        // Add a placeholder option
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.textContent = '-- Select an ID --';
        defaultOption.disabled = true;
        defaultOption.selected = true;
        userIdSelect.appendChild(defaultOption);

        // Populate the dropdown with the fetched IDs
        userIds.forEach(id => {
            const option = document.createElement('option');
            option.value = id;
            option.textContent = id;
            userIdSelect.appendChild(option);
        });

        // Pre-select the first ID for convenience
        if (userIds.length > 0) {
            userIdSelect.value = userIds[0];
            userIdInput.value = userIds[0];
        }
    } catch (error) {
        console.error(error);
        userIdSelect.innerHTML = '<option>-- Error fetching IDs --</option>';
    }
}

// Call the function to fetch IDs when the page loads
document.addEventListener('DOMContentLoaded', fetchUserIds);

// Event listener for the dropdown
userIdSelect.addEventListener('change', () => {
    userIdInput.value = userIdSelect.value;
});

getRecsButton.addEventListener('click', async () => {
    const userId = userIdInput.value.trim();
    if (!userId) {
        recommendationsDiv.innerHTML = '<p class="error">Please select or enter a User ID.</p>';
        return;
    }
    recommendationsDiv.innerHTML = '<p class="loading">Fetching recommendations...</p>';
    
    const apiUrl = `${API_BASE_URL}/recommendations/${userId}`;

    try {
        const response = await fetch(apiUrl);
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'An unknown error occurred.');
        }

        const recommendations = await response.json();

        if (recommendations.length > 0) {
            const html = recommendations.map(item => `
                <div class="product-card">
                    <img src="${item.image_url}" alt="${item.name}">
                    <h3>${item.name}</h3>
                    <p>Score: ${item.score.toFixed(4)}</p>
                </div>
            `).join('');
            recommendationsDiv.innerHTML = html;
        } else {
            recommendationsDiv.innerHTML = `<p class="error">No recommendations found for user "${userId}".</p>`;
        }

    } catch (error) {
        recommendationsDiv.innerHTML = `<p class="error">Error: ${error.message}</p>`;
    }
});