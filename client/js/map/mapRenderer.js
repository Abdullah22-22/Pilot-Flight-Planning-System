import { latLonToSvg } from "./mapUtils.js";

const svg = document.getElementById("map");

// =========================
// DRAW AIRPORT
// =========================
export function drawAirport(lat, lon, color = "green", id) {
  const { x, y } = latLonToSvg(lat, lon);

  let airport = document.getElementById(id);
  if (!airport) {
    airport = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    airport.setAttribute("id", id);
    airport.setAttribute("r", 5);
    airport.setAttribute("fill", color);

    document
      .getElementById("airports-layer")
      .appendChild(airport);
  }

  airport.setAttribute("cx", x);
  airport.setAttribute("cy", y);
}

// =========================
// DRAW PLANE (SVG IMAGE)
// =========================
export function drawPlane(lat, lon, heading = 0) {
  const { x, y } = latLonToSvg(lat, lon);

  let plane = document.getElementById("plane-icon");

  if (!plane) {
    plane = document.createElementNS("http://www.w3.org/2000/svg", "image");
    plane.setAttribute("id", "plane-icon");
    plane.setAttribute("href", "./public/assets/plane.svg");
    plane.setAttribute("width", 30);
    plane.setAttribute("height", 30);

    document
      .getElementById("planes-layer")
      .appendChild(plane);
  }

  plane.setAttribute("x", x - 15);
  plane.setAttribute("y", y - 15);

  plane.setAttribute(
    "transform",
    `rotate(${heading}, ${x}, ${y})`
  );
}

// =========================
// DRAW ROUTE
// =========================
export function drawRoute(route) {
  if (!route || route.length === 0) return;

  const points = route
    .map(p => {
      const { x, y } = latLonToSvg(p.lat, p.lon);
      return `${x},${y}`;
    })
    .join(" ");

  let line = document.getElementById("route-line");

  if (!line) {
    line = document.createElementNS("http://www.w3.org/2000/svg", "polyline");
    line.setAttribute("id", "route-line");
    line.setAttribute("fill", "none");
    line.setAttribute("stroke", "orange");
    line.setAttribute("stroke-width", "2");

    document
      .getElementById("routes-layer")
      .appendChild(line);
  }

  line.setAttribute("points", points);
}
