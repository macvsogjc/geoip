async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();
    plotDataOnMap(data.geolocations);
    displayAnalytics(data.analytics);
}

function plotDataOnMap(geolocations) {
    const map = L.map('map').setView([0, 0], 2);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
    }).addTo(map);

    geolocations.forEach(location => {
        const marker = L.marker([location.latitude, location.longitude]).addTo(map);
        marker.bindPopup(`IP: ${location.ip}<br>Country: ${location.country}`);
    });
}

function displayAnalytics(analytics) {
    const analyticsDiv = document.getElementById('analytics');
    analyticsDiv.innerHTML = `<pre>${JSON.stringify(analytics, null, 2)}</pre>`;
}
