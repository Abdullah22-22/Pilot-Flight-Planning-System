import { request } from "./baseApi.js";

// =========================
// GAME LIFECYCLE
// =========================


export function startGame(pilotId, data) {
  return request(`/game/${pilotId}/start`, "POST", data);
}
// end a new game session for a pilot
export function endGame(pilotId) {
  return request(`/game/${pilotId}`, "DELETE");
}

// =========================
// PREVIEW ROUTE 
// =========================
export function previewRoute(pilotId, destinationCode) {
  return request(`/game/${pilotId}/preview`, "POST", {
    destination_code: destinationCode
  })
}
// =========================
// TAKEOFF (INITIAL OR NEXT LEG)
// =========================
export function takeoff(pilotId, destinationCode = null) {
  // Initial takeoff (destination required)
  if (destinationCode) {
    return request(`/game/${pilotId}/takeoff`, "POST", {
      destination_code: destinationCode
    });
  }

  // Takeoff after refuel stop
  return request(`/game/${pilotId}/takeoff`, "POST");
}

// =========================
// STATUS & ROUTE
// =========================

// Retrieve current game status
export function getStatus(pilotId) {
  return request(`/game/${pilotId}/status`);
}

// Retrieve planned route for map rendering
export function getRoute(pilotId) {
  return request(`/game/${pilotId}/route`);
}

// =========================
// LAND
// =========================

// Trigger manual landing when allowed
export function land(pilotId) {
  return request(`/game/${pilotId}/land`, "POST");
}



// =========================
// CONTROL MODE
// =========================
export function enableManual(pilotId){
  return request(`/game/${pilotId}/mode/manual`, "POST");
}

export function enableAI(pilotId) {
  return request(`/game/${pilotId}/mode/ai`, "POST");
}

// =========================
// MANUAL MOVE
// =========================
export function manualMove(pilotId, direction) {
    return request(`/game/${pilotId}/manual/move`, "POST", {
    direction
  });
}