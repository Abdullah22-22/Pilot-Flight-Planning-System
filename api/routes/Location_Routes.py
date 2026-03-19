from flask import Blueprint, jsonify
from services.location_service import get_countries,get_airports_for_country


# =========================
# LOCATION BLUEPRINT
# =========================
location_bp = Blueprint("location", __name__)


# =========================
# GET COUNTRIES
# =========================

@location_bp.route("/locations/countries", methods=["GET"])
def countries():
    countries = get_countries()
    return jsonify(countries)


# =========================
# GET AIRPORTS BY COUNTRY
# =========================
@location_bp.route("/locations/airports/<country_code>", methods=["GET"])
def airports_by_country(country_code):
    airports = get_airports_for_country(country_code)
    return jsonify(airports)