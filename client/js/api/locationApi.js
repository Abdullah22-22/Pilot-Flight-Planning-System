import { request } from "./baseApi.js";

// =========================
// LOCATION API
// =========================

// GET all countries
export function getCountries() {
    return request("/locations/countries");
}

// GET airport by country code 
export function getAirportsByCountry(countryCode) {
    if (!countryCode) {
        return Promise.resolve([]);
    }

    return request(`/locations/airports/${countryCode}`);
}