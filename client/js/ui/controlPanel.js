// =========================
// CONTROL PANEL (DISPLAY ONLY)
// =========================

const panel = document.querySelector(".controls-card");

// Action button (Takeoff / Land)
const actionBtn = document.createElement("button");
panel.appendChild(actionBtn);

// Info fields
const infoStatus = document.getElementById("infoStatus");
const infoPlane = document.getElementById("infoPlane");
const infoFuel = document.getElementById("infoFuel");
const infoLeg = document.getElementById("infoLeg");
const infoTotalLegs = document.getElementById("infoTotalLegs");
const infoDestination = document.getElementById("infoDestination");
const infoCanLand = document.getElementById("infoCanLand");

let landingInProgress = false;

// =========================
// UPDATE INFO PANEL
// =========================
function updateInfoPanel(status) {
  infoStatus.innerText = status.control_panel?.status_text ?? "-";
  infoPlane.innerText = status.plane?.status ?? "-";
  infoFuel.innerText = status.plane?.fuel ?? "-";
  infoLeg.innerText = status.current_leg ?? "-";
  infoTotalLegs.innerText = status.total_legs ?? "-";
  infoDestination.innerText = status.plane?.destination ?? "-";
  infoCanLand.innerText = status.control_panel?.can_land ? "YES" : "NO";
}

// =========================
// UPDATE ACTION BUTTON
// =========================
function updateActionButtons(status, handlers) {
  const control = status.control_panel;

  if (control.can_land) {
    actionBtn.style.display = "block";
    actionBtn.innerText = "🛬 Land";
    actionBtn.disabled = landingInProgress;

    actionBtn.onclick = async () => {
      landingInProgress = true;
      actionBtn.disabled = true;
      await handlers.onLand();
      landingInProgress = false;
    };
    return;
  }

  if (control.can_takeoff) {
    actionBtn.style.display = "block";
    actionBtn.innerText = "🛫 Takeoff";
    actionBtn.disabled = false;

    actionBtn.onclick = async () => {
      actionBtn.disabled = true;
      await handlers.onTakeoff();
    };
    return;
  }

  actionBtn.style.display = "none";
}

// =========================
// PUBLIC UPDATE
// =========================
export function updateControlPanel(status, handlers) {
  if (!status) return;
  updateInfoPanel(status);
  updateActionButtons(status, handlers);
}
