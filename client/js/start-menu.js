const startMenu = document.getElementById("startMenu");
const mainContent = document.getElementById("mainContent");
const startBtn = document.getElementById("startGameBtn");
const exitBtn = document.getElementById("exitGameBtn");

window.addEventListener("DOMContentLoaded", () => {
  if (startMenu) startMenu.style.display = "flex";
});

if (startBtn) {
  startBtn.addEventListener("click", () => {
    startMenu.style.display = "none";
    mainContent.classList.remove("hidden");
  });
}

if (exitBtn) {
  exitBtn.addEventListener("click", () => {
    window.close();
  });
}