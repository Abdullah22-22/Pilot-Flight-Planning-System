import { MAP } from "./mapConfig.js";

// =========================
// LAT/LON TO SVG COORDINATES
// =========================
export function latLonToSvg(lat, lon) {
  const x =
    ((lon - MAP.minLon) / (MAP.maxLon - MAP.minLon)) * MAP.width;

  const y =
    MAP.height -
    ((lat - MAP.minLat) / (MAP.maxLat - MAP.minLat)) * MAP.height;

  return { x, y };
}

// =========================
// DISTANCE BETWEEN TWO LAT/LON POINTS
// =========================
export function distanceLatLon(a, b) {
  const dx = a.lat - b.lat;
  const dy = a.lon - b.lon;
  return Math.sqrt(dx * dx + dy * dy);
}
