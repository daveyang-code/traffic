function colormap(min, max, value) {
  const normalizedValue = (value - min) / (max - min);

  const colors = [
    [1, 1, 0], // yellow
    [1, 0.5, 0], // orange
    [1, 0, 0], // red
  ];

  const index = Math.floor(normalizedValue * (colors.length - 1));

  const position =
    (normalizedValue - index / (colors.length - 1)) * (colors.length - 1);

  const [r1, g1, b1] = colors[index];
  const [r2, g2, b2] = colors[index + 1] || colors[index];
  const red = r1 + (r2 - r1) * position;
  const green = g1 + (g2 - g1) * position;
  const blue = b1 + (b2 - b1) * position;

  const color = `rgb(${Math.round(red * 255)}, ${Math.round(
    green * 255
  )}, ${Math.round(blue * 255)})`;

  return color;
}

var mymap = L.map("map").setView([43.744, -79.466], 11);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(mymap);

var layerGroup = L.layerGroup().addTo(mymap);
var src_Labels = [];
var src_Data = [];
var locations = 50;

setInterval(function () {
  $.getJSON("/refreshData", {}, function (data) {
    src_Labels = data.sLabel;
    src_Data = data.sData;
  });

  var max = Math.max(...src_Data.slice(0, locations));
  var min = Math.min(...src_Data.slice(0, locations));

  layerGroup.clearLayers();

  for (var i = 0; i < locations; i++) {
    if (src_Labels[i] != null) {
      var clr = colormap(min, max, src_Data[i]);
      var circle = L.circle(src_Labels[i], {
        color: clr,
        fillColor: clr,
        fillOpacity: 0.2,
        radius: 50 * Math.log2(src_Data[i]),
      }).addTo(layerGroup);
    }
  }
}, 5000);
