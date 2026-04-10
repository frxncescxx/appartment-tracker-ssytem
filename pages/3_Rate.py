import streamlit as st
import pandas as pd
from db import get_connection

st.set_page_config(page_title="Rate Apartments", page_icon="⭐", layout="wide")
st.title("⭐ Rate Apartments")
st.caption("Each roommate can submit one rating per apartment. Submitting again updates your previous rating.")

# ── Load dropdowns from DB ──────────────────────────────────────────────────
conn = get_connection()
cur = conn.cursor()

cur.execute("SELECT id, name FROM roommates ORDER BY name;")
roommate_rows = cur.fetchall()

cur.execute("SELECT id, name, address FROM apartments ORDER BY name;")
apartment_rows = cur.fetchall()

cur.close()
conn.close()

if not roommate_rows:
    st.warning("No roommates yet. Add some on the **Roommates** page first.")
    st.stop()

if not apartment_rows:
    st.warning("No apartments yet. Add some on the **Apartments** page first.")
    st.stop()

roommate_options = {f"{r[1]}": r[0] for r in roommate_rows}
apartment_options = {
    f"{a[1]}" + (f" — {a[2]}" if a[2] else ""): a[0] for a in apartment_rows
}

# ── Rating form ───────────────────────────────────────────────────────────────
with st.form("rate_apartment"):
    c1, c2 = st.columns(2)
    with c1:
        selected_roommate = st.selectbox("Roommate *", options=roommate_options.keys())
    with c2:
        selected_apartment = st.selectbox("Apartment *", options=apartment_options.keys())

    score = st.slider("Score *", min_value=1, max_value=5, value=3,
                      help="1 = Not interested, 5 = Love it!")
    
    st.markdown(
        f"{'⭐' * score}{'☆' * (5 - score)}  —  "
        + ["", "Not interested", "Below average", "It's okay", "Pretty good", "Love it!"][score]
    )
    comment = st.text_area("Comment (optional)", placeholder="What did you like or dislike?")
    submitted = st.form_submit_button("Submit rating", use_container_width=True)

if submitted:
    roommate_id = roommate_options[selected_roommate]
    apartment_id = apartment_options[selected_apartment]
    try:
        conn = get_connection()
        cur = conn.cursor()
        # This requires the UNIQUE (apartment_id, roommate_id) constraint in DB
        cur.execute(
            """
            INSERT INTO ratings (apartment_id, roommate_id, score, comment, rated_at)
            VALUES (%s, %s, %s, %s, NOW())
            ON CONFLICT (apartment_id, roommate_id)
            DO UPDATE SET 
                score = EXCLUDED.score,
                comment = EXCLUDED.comment,
                rated_at = NOW();
            """,
            (apartment_id, roommate_id, score, comment.strip() or None),
        )
        conn.commit()
        cur.close()
        conn.close()
        st.success(f"✅ Rating saved! {selected_roommate} gave **{selected_apartment}** {score}/5 ⭐")
        st.rerun()
    except Exception as ex:
        st.error(f"Database error: {ex}")

st.divider()

# ── All ratings table ─────────────────────────────────────────────────────────
st.subheader("All ratings")

filter_apt = st.selectbox(
    "Filter by apartment",
    options=["All apartments"] + list(apartment_options.keys()),
)

conn = get_connection()
cur = conn.cursor()

if filter_apt == "All apartments":
    cur.execute(
        """
        SELECT a.name, rm.name, r.score, r.comment, r.rated_at
        FROM ratings r
        JOIN apartments a ON a.id = r.apartment_id
        JOIN roommates rm ON rm.id = r.roommate_id
        ORDER BY a.name, rm.name;
        """
    )
else:
    apt_id = apartment_options[filter_apt]
    cur.execute(
        """
        SELECT a.name, rm.name, r.score, r.comment, r.rated_at
        FROM ratings r
        JOIN apartments a ON a.id = r.apartment_id
        JOIN roommates rm ON rm.id = r.roommate_id
        WHERE r.apartment_id = %s
        ORDER BY rm.name;
        """,
        (apt_id,),
    )

ratings = cur.fetchall()
cur.close()
conn.close()

if not ratings:
    st.info("No ratings yet.")
else:
    for apt_name, rm_name, score, comment, rated_at in ratings:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{apt_name}** — rated by **{rm_name}**")
                if comment:
                    st.caption(f'\"{comment}\"')
                
                # Robust date formatting
                if rated_at:
                    dt = pd.to_datetime(rated_at)
                    st.caption(f"Rated on {dt.strftime('%b %d, %Y')}")
            with col2:
                st.markdown(
                    f"<div style='font-size:24px;text-align:right'>{'⭐' * score}</div>",
                    unsafe_allow_html=True,
                )