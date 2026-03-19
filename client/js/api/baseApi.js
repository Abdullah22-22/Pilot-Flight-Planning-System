// =========================
// API BASE CONFIGURATION
// =========================
// Base URL for backend API
// const BASE_URL = "http://127.0.0.1:5000";
const BASE_URL = "https://pilot-flight-planning-system.onrender.com";

// =========================
// GENERIC API REQUEST HELPER
// =========================
export async function request(url, method = "GET", data = null) {
  // Request configuration
  const options = {
    method,
    headers: {
      "Content-Type": "application/json"
    }
  };

  // Attach request body if provided
  if (data) {
    options.body = JSON.stringify(data);
  }

  // Execute HTTP request
  const response = await fetch(`${BASE_URL}${url}`, options);

  // Handle API-level errors
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || "API Error");
  }

  // Return parsed JSON response
  return response.json();
}
