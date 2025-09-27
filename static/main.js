// Инициализация карты
function initMapFromDiv() {
    const mapDiv = document.getElementById("map");
    if (!mapDiv) return;

    const coordsAttr = mapDiv.dataset.coords;
    if (!coordsAttr) return;

    const coords = coordsAttr.split(',').map(Number);

    const map = new ymaps.Map("map", {
        center: coords,
        zoom: 15
    });

    const placemark = new ymaps.Placemark(coords, {}, { preset: "islands#redIcon" });
    map.geoObjects.add(placemark);
}

ymaps.ready(initMapFromDiv);

// Флэши с автоскрытием
document.addEventListener("DOMContentLoaded", function() {
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(flash => {
        setTimeout(() => {
            flash.classList.add('hide');
            setTimeout(() => flash.remove(), 500);
        }, 4000);
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var mapContainer = document.getElementById('map');
    mapContainer.classList.add('loaded');
});
