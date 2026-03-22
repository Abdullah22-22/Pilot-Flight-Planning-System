import { getCountries, getAirportsByCountry } from "./api/locationApi.js";

// =========================
// STATE
// =========================
let allCountries = [];
let selectedCountry = null;

// =========================
// INIT
// =========================
async function initLocation() {
  allCountries = await getCountries();
  renderCountries(allCountries);

  document
    .getElementById("countrySearch")
    .addEventListener("input", applyFilters);

  document
    .getElementById("continentFilter")
    .addEventListener("change", applyFilters);
}

// =========================
// FILTER
// =========================
function applyFilters() {
  if (selectedCountry) return;

  const search =
    document.getElementById("countrySearch").value.toLowerCase();
  const continent =
    document.getElementById("continentFilter").value;

  const filtered = allCountries.filter(c => {
    const okSearch = c.name.toLowerCase().includes(search);
    const okContinent =
      continent === "ALL" || c.continent === continent;
    return okSearch && okContinent;
  });

  renderCountries(filtered);
}

// =========================
// RENDER COUNTRIES
// =========================
function renderCountries(countries) {
  const grid = document.getElementById("countryGrid");
  grid.innerHTML = "";

  const list = selectedCountry ? [selectedCountry] : countries;

  list.forEach(country => {
    const card = document.createElement("div");
    card.className = "country-card";

    const iso = country.code.toLowerCase();

    card.innerHTML = `
      <img class="country-flag"
           src="https://flagcdn.com/w80/${iso}.png" />
      <div class="country-name">${country.name}</div>
      <div class="country-code">${country.code}</div>
    `;

    if (!selectedCountry) {
      card.onclick = () => selectCountry(country);
    }

    grid.appendChild(card);
  });
}

// =========================
// SELECT COUNTRY
// =========================
async function selectCountry(country) {
  selectedCountry = country;
  renderCountries(allCountries);

  const airports = await getAirportsByCountry(country.code);
  renderAirports(country, airports);
}

// =========================
// RENDER AIRPORTS (CARDS)
// =========================
function renderAirports(country, airports) {
  document.getElementById("airportSection").style.display = "block";
  document.getElementById("airportTitle").innerText =
    `Airports in ${country.name}`;

  const grid = document.getElementById("airportGrid");
  grid.innerHTML = "";

  airports.forEach(ap => {
    const card = document.createElement("div");
    card.className = "airport-card";

    card.innerHTML = `
      <div class="airport-name">${ap.name}</div>
      <div class="airport-code">${ap.ident}</div>
      <div class="airport-code">${ap.type}</div>
    `;

    card.onclick = () => {
      console.log("✈️ Airport selected:", ap);

      if (!sessionStorage.getItem("departureAirport")) {
        sessionStorage.setItem(
          "departureAirport",
          JSON.stringify(ap)
        );

        resetToCountrySelection();
        return;
      }

      sessionStorage.setItem(
        "destinationAirport",
        JSON.stringify(ap)
      );

      // window.location.href = "../index.html";
      // window.location.href = "/client/index.html";
       window.location.href = "/index.html";
    };


    grid.appendChild(card);
  });
}

// =========================
// RESET TO COUNTRY SELECTION
// =========================
function resetToCountrySelection() {
  selectedCountry = null;

  document.getElementById("airportSection").style.display = "none";
  renderCountries(allCountries);
}

// =========================
// START
// =========================
initLocation();
