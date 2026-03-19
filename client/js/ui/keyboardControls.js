import { manualMove } from "../api/gameApi.js";

let enabled = false;
let pilotId = null;

export function enableKeyboard(pId) {
    pilotId = pId;
    enabled = true;
}
export function disableKeyboard() {
    enabled = false;
    pilotId = null;
}

window.addEventListener("keydown", (e) => {
    if (!enabled || !pilotId) return;

    let direction = null;

    switch (e.key) {
        case "ArrowUp":
            direction = "FORWARD";
            break;
        case "ArrowLeft":
            direction = "LEFT";
            break;
        case "ArrowRight":
            direction = "RIGHT";
            break;
        default:
            return;
    }

    e.preventDefault();
    manualMove(pilotId, direction);
});
