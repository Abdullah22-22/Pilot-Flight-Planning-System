import { enableManual, enableAI } from "../api/gameApi.js";
import { enableKeyboard, disableKeyboard } from "./keyboardControls.js";

const PILOT_ID = 1;


// =========================
// CONTROL MODE UI
// Manual / AI switch buttons
// =========================
export function initControlModeButtons() {
  const panel = document.querySelector(".controls-card");
  if (!panel) return;

  // Prevent duplicate buttons
  if (document.getElementById("modeBox")) return;

  const box = document.createElement("div");
  box.id = "modeBox";
  box.style.display = "flex";
  box.style.gap = "8px";
  box.style.marginBottom = "10px";

  const btnManual = document.createElement("button");
  btnManual.innerText = "🎮 Manual";

  const btnAI = document.createElement("button");
  btnAI.innerText = "🤖 AI";

  box.appendChild(btnManual);
  box.appendChild(btnAI);
  panel.prepend(box);

  // =========================
  // MANUAL MODE
  // Enable keyboard control
  // =========================
  btnManual.onclick = async () => {
    await enableManual(PILOT_ID);
    enableKeyboard(PILOT_ID);
  };

  // =========================
  // AI MODE
  // Disable keyboard control
  // =========================
  btnAI.onclick = async () => {
    await enableAI(PILOT_ID);
    disableKeyboard();
  };
}
