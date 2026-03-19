from services.sql import fetch_countries, fetch_airports_by_country

# =========================
# LOCATION SERVICE
# Country and airport lookup
# =========================

def get_countries():
    # Return list of available countries
    return fetch_countries()


def get_airports_for_country(country_code: str):
    # Return airports for a given country code
    if not country_code:
        return []
    
    return fetch_airports_by_country(country_code)
