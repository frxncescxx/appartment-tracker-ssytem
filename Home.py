import streamlit as st
import pandas as pd
from db import get_connection, init_db

st.set_page_config(page_title="Apartment Tracker", page_icon="🏠", layout="wide")

# Initialize database tables
init_db()

st.title("🏠 Apartment Tracker")
st.caption("Track, rate, and compare apartments with your roommates.")

# ── Summary metrics ──────────────────────────────────────────────────────────
conn = get_connection()
# IMPORTANT: Reset the transaction state to ensure we see the latest data
conn.rollback() 
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM apartments;")
total_apts = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM roommates;")
total_roommates = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM ratings;")
total_ratings = cur.fetchone()[0]

cur.execute("SELECT ROUND(AVG(score)::numeric, 1) FROM ratings;")
avg_score_val = cur.fetchone()[0] or "—"

col1, col2, col3, col4 = st.columns(4)
col1.metric("Apartments tracked", total_apts)
col2.metric("Roommates", total_roommates)
col3.metric("Ratings submitted", total_ratings)
col4.metric("Avg score (all)", avg_score_val)

st.divider()

# ── Apartment cards ───────────────────────────────────────────────────────────
st.subheader("All Apartments")

# Filter bar
fcol1, fcol2, fcol3 = st.columns([2, 1, 1])
with fcol1:
    rent_max = st.number_input("Max monthly rent ($)", min_value=0, value=5000, step=100)
with fcol2:
    filter_parking = st.checkbox("Parking required")
with fcol3:
    filter_pets = st.checkbox("Pet-friendly required")

query = """
    SELECT
        a.id,
        a.name,
        a.address,
        a.bedrooms,
        a.bathrooms,
        a.monthly_rent,
        a.has_parking,
        a.is_pet_friendly,
        a.has_in_unit_laundry,
        a.image_url,
        a.listing_url,
        ROUND(AVG(r.score)::numeric, 1) AS avg_score,
        COUNT(r.id) AS num_ratings
    FROM apartments a
    LEFT JOIN ratings r ON r.apartment_id = a.id
    WHERE a.monthly_rent <= %s
"""
params = [rent_max]

if filter_parking:
    query += " AND a.has_parking = true"
if filter_pets:
    query += " AND a.is_pet_friendly = true"

query += " GROUP BY a.id ORDER BY a.date_added DESC;"

cur.execute(query, params)
rows = cur.fetchall()
cur.close()
conn.close()

if not rows:
    st.info("No apartments match your filters. Add one on the **Manage Apartments** page.")
else:
    # Display in 2-column card grid
    for i in range(0, len(rows), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j >= len(rows):
                break
            row = rows[i + j]
            (apt_id, name, address, beds, baths, rent,
             parking, pets, laundry, image_url, listing_url,
             current_avg, current_count) = row

            with col:
                with st.container(border=True):
                    if image_url:
                        st.image(image_url, use_container_width=True)
                    else:
                        st.markdown(
                            "<div style='background:#f0f2f6;height:160px;"
                            "display:flex;align-items:center;justify-content:center;"
                            "border-radius:8px;color:#888;font-size:13px'>No image</div>",
                            unsafe_allow_html=True,
                        )
                    st.markdown(f"### {name}")
                    if address:
                        st.caption(f"📍 {address}")

                    mcol1, mcol2, mcol3 = st.columns(3)
                    mcol1.metric("Rent", f"${rent:,.0f}/mo")
                    mcol2.metric("Beds / Baths", f"{beds} / {baths}")
                    mcol3.metric(
                        "Avg score",
                        f"{current_avg} ★" if current_avg else "—",
                        help=f"{current_count} rating(s)",
                    )

                    amenities = []
                    if parking:
                        amenities.append("🚗 Parking")
                    if pets:
                        amenities.append("🐾 Pets OK")
                    if laundry:
                        amenities.append("🧺 In-unit laundry")
                    if amenities:
                        st.markdown(" &nbsp;·&nbsp; ".join(amenities))

                    st.link_button("View listing", listing_url, use_container_width=True)