from db import get_cursor


# =========================
# INSERT PILOT
# =========================
def insert_pilot(name, password_hash):
    conn, cursor = get_cursor()
    try:
        cursor.execute(
            """
            INSERT INTO pilot (name, password_hash)
            VALUES (%s, %s)
            """,
            (name, password_hash)
        )
        conn.commit()
    finally:
        conn.close()


# =========================
# GET PILOT BY NAME
# =========================
def get_pilot_by_name(name):
    conn, cursor = get_cursor()

    cursor.execute(
        """
        SELECT id, name, password_hash
        FROM pilot
        WHERE name = %s
        """,
        (name,)
    )

    pilot = cursor.fetchone()
    conn.close()
    return pilot


# =========================
# FETCH REFUEL AIRPORTS
# =========================
def fetch_refuel_airports():
    conn, cursor = get_cursor()

    cursor.execute("""
        SELECT
            ident,
            name,
            latitude_deg,
            longitude_deg,
            type
        FROM airport
        WHERE type IN ('large_airport', 'medium_airport')
    """)

    airports = cursor.fetchall()
    conn.close()
    return airports


# =========================
# FETCH AIRPORT BY CODE
# =========================
def fetch_airport_by_code(code: str):
    conn, cursor = get_cursor()
    code = code.upper()

    cursor.execute("""
        SELECT
            airport.ident,
            airport.name,
            airport.type,
            airport.latitude_deg,
            airport.longitude_deg
        FROM airport
        WHERE
            airport.ident = %s
            OR airport.gps_code = %s
            OR airport.iata_code = %s
        LIMIT 1
    """, (code, code, code))

    row = cursor.fetchone()
    conn.close()
    return row


# =========================
# FETCH COUNTRIES (JOIN airport + country)
# =========================
def fetch_countries():
    conn, cursor = get_cursor()

    cursor.execute("""
        SELECT DISTINCT
            c.iso_country AS code,
            c.name,
            c.continent,
            c.url
        FROM airport a
        JOIN country c
            ON a.iso_country = c.iso_country
        WHERE a.iso_country IS NOT NULL
        ORDER BY c.name
    """)

    countries = cursor.fetchall()
    conn.close()
    return countries



# =========================
# FETCH AIRPORTS BY COUNTRY
# =========================
def fetch_airports_by_country(country_code: str):
    conn, cursor = get_cursor()
    country_code = country_code.upper()

    cursor.execute("""
        SELECT
            ident,
            name,
            type,
            latitude_deg,
            longitude_deg
        FROM airport
        WHERE iso_country = %s
        ORDER BY
            CASE
                WHEN type = 'large_airport' THEN 1
                WHEN type = 'medium_airport' THEN 2
                ELSE 3
            END,
            name
    """, (country_code,))

    airports = cursor.fetchall()
    conn.close()
    return airports
