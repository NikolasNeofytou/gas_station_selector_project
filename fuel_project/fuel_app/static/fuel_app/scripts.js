console.log("scripts.js is loaded");
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function populateCities() {
    const citySelect = document.getElementById('city');
    try {
        const response = await fetch('/get-cities/');
        if (!response.ok) {
            throw new Error(`Failed to fetch cities: ${response.status}`);
        }
        const data = await response.json();

        data.cities.forEach(city => {
            const option = document.createElement('option');
            option.value = city.name;
            option.textContent = city.name;
            citySelect.appendChild(option);
        });
    } catch (error) {
        console.error("Error populating cities:", error);
    }
}

document.addEventListener('DOMContentLoaded', populateCities);

document.getElementById('search-button').addEventListener('click', async () => {
    const city = document.getElementById('city').value;
    const fuelType = document.getElementById('fuel_type').value;
    const resultsDiv = document.getElementById('results');

    try {
        console.log("Sending initial request to /fetch-prices/ with city and fuelType:", city, fuelType);

        const response = await fetch('/fetch-prices/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ city, fuel_type: fuelType })
        });

        if (!response.ok) {
            resultsDiv.innerHTML = `<p>Error: Received status ${response.status}</p>`;
            return;
        }

        const responseText = await response.text();
        let data;
        try {
            data = JSON.parse(responseText);
            console.log("Parsed JSON data:", data);
        } catch (error) {
            console.error("Error parsing JSON:", error);
            resultsDiv.innerHTML = `<p>Error: Received non-JSON response from the server.</p><pre>${responseText}</pre>`;
            return;
        }

        resultsDiv.innerHTML = JSON.stringify(data); 
    } catch (error) {
        console.error('Error fetching data:', error);
        resultsDiv.innerHTML = `<p>Error: ${error.message}</p>`;
    }
});
