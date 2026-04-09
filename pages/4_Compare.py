import streamlit as st
from db import get_connection

st.set_page_config(page_title="Compare", page_icon="⚖️", layout="wide")
st.title("⚖️ Compare Apartments")
st.caption("Pick any two apartments to see them side-by-side.")

# ── Load apartments from DB ───────────────────────────────────────────────────
conn = get_connection()
cur = conn.cursor()
cur.execute("SELECT id, name, address FROM apartments ORDER BY name;")
apartment_rows = cur.fetchall()
cur.close()
conn.close()

if len(apartment_rows) < 2:
    st.warning("You need at least **2 apartments** in the system to compare. Add more on the Apartments page.")
    st.stop()

apartment_options = {
    f"{a[1]}" + (f" — {a[2]}" if a[2] else ""): a[0] for a in apartment_rows
}
labels = list(apartment_options.keys())

c1, c2 = st.columns(2)
with c1:
    left_label = st.selectbox("First apartment", options=labels, index=0)
with c2:
    right_label = st.selectbox("Second apartment", options=labels, index=min(1, len(labels) - 1))

if left_label == right_label:
    st.info("Select two different apartments to compare.")
    st.stop()

left_id = apartment_options[left_label]
right_id = apartment_options[right_label]


def fetch_apartment(apt_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            a.name, a.address, a.listing_url, a.image_url,
            a.bedrooms, a.bathrooms, a.monthly_rent,
            a.has_parking, a.is_pet_friendly, a.has_in_unit_laundry,
            ROUND(AVG(r.score)::numeric, 2) AS avg_score,
            COUNT(r.id) AS num_ratings
        FROM apartments a
        LEFT JOIN ratings r ON r.apartment_id = a.id
        WHERE a.id = %s
        GROUP BY a.id;
        """,
        (apt_id,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def fetch_ratings(apt_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT rm.name, r.score, r.comment
        FROM ratings r
        JOIN roommates rm ON rm.id = r.roommate_id
        WHERE r.apartment_id = %s
        ORDER BY rm.name;
        """,
        (apt_id,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


left = fetch_apartment(left_id)
right = fetch_apartment(right_id)
left_ratings = fetch_ratings(left_id)
right_ratings = fetch_ratings(right_id)

st.divider()

col_l, col_r = st.columns(2)


def render_apartment(col, data, ratings):
    (name, address, listing_url, image_url, beds, baths, rent,
     parking, pets, laundry, avg_score, num_ratings) = data

    with col:
        if image_url:
            st.image(image_url, use_container_width=True)
        else:
            st.markdown(
                "<div style='background:#f0f2f6;height:180px;display:flex;"
                "align-items:center;justify-content:center;border-radius:8px;"
                "color:#aaa'>No image</div>",
                unsafe_allow_html=True,
            )

        st.markdown(f"### {name}")
        if address:
            st.caption(f"📍 {address}")

        st.link_button("View listing →", listing_url, use_container_width=True)

        st.markdown("**Details**")
        m1, m2, m3 = st.columns(3)
        m1.metric("Rent/mo", f"${rent:,.0f}")
        m2.metric("Beds", beds)
        m3.metric("Baths", baths)

        st.markdown("**Amenities**")
        st.markdown(f"{'✅' if parking else '❌'} Parking")
        st.markdown(f"{'✅' if pets else '❌'} Pet-friendly")
        st.markdown(f"{'✅' if laundry else '❌'} In-unit laundry")

        st.markdown("**Roommate ratings**")
        if not ratings:
            st.caption("No ratings yet.")
        else:
            for rm_name, score, comment in ratings:
                st.markdown(
                    f"**{rm_name}**: {'⭐' * score} ({score}/5)"
                    + (f' — *"{comment}"*' if comment else "")
                )
            score_display = f"{avg_score:.1f} / 5" if avg_score else "—"
            st.metric("Average score", f"{score_display} ({'⭐' * round(avg_score) if avg_score else '—'})",
                      help=f"Based on {num_ratings} rating(s)")


render_apartment(col_l, left, left_ratings)
render_apartment(col_r, right, right_ratings)

# ── Quick verdict ─────────────────────────────────────────────────────────────
st.divider()
left_score = left[10] or 0
right_score = right[10] or 0

if left_score == right_score:
    st.info("🤝 It's a tie! Both apartments have the same average score.")
elif left_score > right_score:
    diff = float(left_score) - float(right_score)
    st.success(f"🏆 **{left[0]}** leads by {diff:.1f} point(s) based on roommate ratings.")
else:
    diff = float(right_score) - float(left_score)
    st.success(f"🏆 **{right[0]}** leads by {diff:.1f} point(s) based on roommate ratings.")
