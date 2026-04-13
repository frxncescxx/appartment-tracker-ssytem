import streamlit as st
import psycopg2
from db import init_db

st.set_page_config(page_title="Apartment Tracker", page_icon="🏠")

init_db()

def get_connection():
    return psycopg2.connect(st.secrets["DB_URL"])

st.title("🏠 Apartment Tracker")
st.write("Welcome! Use the sidebar to manage apartments, roommates, and ratings.")

st.markdown("---")
st.subheader("📊 Current Data")

try:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM apartments;")
    apt_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM roommates;")
    roommate_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM ratings;")
    rating_count = cur.fetchone()[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Apartments", apt_count)
    col2.metric("Roommates", roommate_count)
    col3.metric("Ratings", rating_count)

    st.markdown("---")
    st.subheader("📋 All Apartment Ratings")

    cur.execute("""
        SELECT a.name, a.address, a.monthly_rent, rm.name, r.score, r.comment
        FROM ratings r
        JOIN apartments a  ON a.id  = r.apartment_id
        JOIN roommates  rm ON rm.id = r.roommate_id
        ORDER BY a.name;
    """)
    rows = cur.fetchall()

    if rows:
        st.table([
            {
                "Apartment":  r[0],
                "Address":    r[1] or "—",
                "Rent/mo":    f"${r[2]:,.0f}",
                "Roommate":   r[3],
                "Score":      f"{r[4]}/5",
                "Comment":    r[5] or "—",
            }
            for r in rows
        ])
    else:
        st.info("No ratings yet. Add apartments and roommates, then submit ratings!")

    cur.close()
    conn.close()

except Exception as e:
    st.error(f"Database connection error: {e}")

st.markdown("---")
if st.button("🔄 Refresh data"):
    st.rerun()