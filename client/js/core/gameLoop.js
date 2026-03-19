import { getStatus, land, takeoff } from "../api/gameApi.js";
import { drawPlane } from "../map/mapRenderer.js";
import { updateControlPanel } from "../ui/controlPanel.js";
import { handleTripCompletion } from "./tripStatus.js";

let intervalId = null;
let arrivedHandled = false;

// =========================
// START GAME LOOP
// Poll backend and update UI
// =========================
export function startGameLoop(pilotId) {
  if (intervalId) return;

  arrivedHandled = false;

  intervalId = setInterval(async () => {
    try {
      const res = await getStatus(pilotId);
      const status = res.status;
      const plane = status.plane;

      // Draw plane on map
      drawPlane(plane.lat, plane.lon);

      // =========================
      // FINAL ARRIVAL
      // Handle trip completion once
      // =========================
      if (status.trip_status?.completed && !arrivedHandled) {
        arrivedHandled = true;
        stopGameLoop();
        await handleTripCompletion(status.trip_status, pilotId);
        return;
      }

      // =========================
      // CONTROL PANEL UPDATE
      // =========================
      updateControlPanel(status, {
        onLand: () => land(pilotId),
        onTakeoff: () => {
          const dest = sessionStorage.getItem("pendingDestination");
          return takeoff(pilotId, dest);
        }
      });

    } catch (e) {
      console.error("Game loop error:", e.message);
    }
  }, 1000);
}

// =========================
// STOP GAME LOOP
// Clear polling interval
// =========================
export function stopGameLoop() {
  if (intervalId) {
    clearInterval(intervalId);
    intervalId = null;
  }
}