var map = L.map('map').setView([42.3736, -71.1097], 13); // Coordinates for Cambridge, MA

var bounds = [
    [42.3201, -71.1500], // Southwest corner (approximate)
    [42.4201, -71.0500]  // Northeast corner (approximate)
];

map.setMaxBounds(bounds);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Fit the map to the defined bounds
map.fitBounds(bounds);

// Optional: Set a minimum zoom level to prevent zooming out too far
map.setMinZoom(12);