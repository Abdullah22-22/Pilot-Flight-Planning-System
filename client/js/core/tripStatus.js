import { endGame } from "../api/gameApi.js";

// =========================
// TRIP STATUS (ALL LOGIC HERE)
// =========================
export async function handleTripCompletion(trip, pilotId) {
  if (!trip || !trip.completed) return;

  const stopsText =
    trip.stops && trip.stops.length > 0
      ? trip.stops.map((s, i) => ` ${i + 1}. ${s}`).join("\n")
      : " None";

  const message =
    "✈️ Trip Completed Successfully!\n\n" +
    `👨‍✈️ Pilot: ${trip.pilot_name}\n\n` +
    `From: ${trip.from}\n` +
    `Stops:\n${stopsText}\n` +
    `To: ${trip.to}\n\n` +
    `⛽ Fuel Remaining: ${trip.fuel_remaining}\n` +
    `📍 Status: Completed\n\n` +
    "Thank you for flying ✨";

  alert(message);

  try {
    await endGame(pilotId);
  } catch (err) {
    console.error("Failed to end game:", err.message);
  }

  sessionStorage.removeItem("departureAirport");
  sessionStorage.removeItem("destinationAirport");
  sessionStorage.removeItem("pendingDestination");

  window.location.href = "../html/location.html";
     window.location.href = "/client/location.html";
}