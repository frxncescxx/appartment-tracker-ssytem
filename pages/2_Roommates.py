import re
import streamlit as st
import pandas as pd
from db import get_connection

st.set_page_config(page_title="Roommates", page_icon="👥", layout="wide")
st.title("👥 Manage Roommates")

EMAIL_RE = re.compile(r"^\S+@\S+\.\S+$")


def validate_roommate(name, email):
    errors = []
    if not name.strip():
        errors.append("**Name** is required.")
    if not email.strip():
        errors.append("**Email** is required.")
    elif not EMAIL_RE.match(email.strip()):
        errors.append("**Email** is not a valid email address.")
    return errors


# ── Add roommate ──────────────────────────────────────────────────────────────
with st.expander("➕ Add new roommate", expanded=True):
    with st.form("add_roommate"):
        c1, c2 = st.columns(2)
        with c1:
            r_name = st.text_input("Name *", placeholder="e.g. Alex Smith")
        with c2:
            r_email = st.text_input("Email *", placeholder="alex@email.com")
        submitted = st.form_submit_button("Add roommate", use_container_width=True)

    if submitted:
        errors = validate_roommate(r_name, r_email)
        if errors:
            for e in errors:
                st.error(e)
        else:
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO roommates (name, email) VALUES (%s, %s);",
                    (r_name.strip(), r_email.strip().lower()),
                )
                conn.commit()
                cur.close()
                conn.close()
                st.success(f"Added {r_name}!")
                st.rerun()
            except Exception as ex:
                if "unique" in str(ex).lower():
                    st.error("A roommate with this email already exists.")
                else:
                    st.error(f"Database error: {ex}")

st.divider()

# ── List roommates ────────────────────────────────────────────────────────────
st.subheader("Current Roommates")

conn = get_connection()
cur = conn.cursor()
cur.execute("""
    SELECT 
        rm.id, 
        rm.name, 
        rm.email, 
        rm.created_at, 
        (SELECT COUNT(*) FROM ratings WHERE roommate_id = rm.id) as num_ratings
    FROM roommates rm
    ORDER BY rm.name;
""")
roommates = cur.fetchall()
cur.close()
conn.close()

if not roommates:
    st.info("No roommates added yet.")
else:
    for rm_id, rm_name, rm_email, created_at, num_ratings in roommates:
        # Check if we are currently editing this specific roommate
        is_editing = st.session_state.get(f"editing_rm_{rm_id}", False)

        if not is_editing:
            with st.container(border=True):
                hcol, bcol, dcol = st.columns([5, 1, 1])
                with hcol:
                    st.markdown(f"**{rm_name}** — {rm_email}")
                    
                    # FIX: Convert created_at using pandas to ensure it's a datetime object
                    if created_at:
                        dt_object = pd.to_datetime(created_at)
                        st.caption(f"Joined {dt_object.strftime('%b %d, %Y')} · {num_ratings} rating(s) submitted")
                    else:
                        st.caption(f"Joined date unknown · {num_ratings} rating(s) submitted")

                with bcol:
                    if st.button("Edit", key=f"edit_btn_{rm_id}", use_container_width=True):
                        st.session_state[f"editing_rm_{rm_id}"] = True
                        st.rerun()
                with dcol:
                    if st.button("🗑️", key=f"del_btn_{rm_id}", use_container_width=True):
                        conn = get_connection()
                        cur = conn.cursor()
                        cur.execute("DELETE FROM roommates WHERE id = %s;", (rm_id,))
                        conn.commit()
                        cur.close()
                        conn.close()
                        st.rerun()
        else:
            # Inline Edit Form
            with st.container(border=True):
                st.markdown(f"**Editing {rm_name}**")
                with st.form(f"edit_form_{rm_id}"):
                    e_name = st.text_input("Name", value=rm_name)
                    e_email = st.text_input("Email", value=rm_email)
                    save_btn, cancel_btn = st.columns(2)
                    save = save_btn.form_submit_button("💾 Save", use_container_width=True)
                    cancel = cancel_btn.form_submit_button("Cancel", use_container_width=True)

                if save:
                    errors = validate_roommate(e_name, e_email)
                    if errors:
                        for e in errors:
                            st.error(e)
                    else:
                        try:
                            conn = get_connection()
                            cur = conn.cursor()
                            cur.execute(
                                "UPDATE roommates SET name=%s, email=%s WHERE id=%s;",
                                (e_name.strip(), e_email.strip().lower(), rm_id),
                            )
                            conn.commit()
                            cur.close()
                            conn.close()
                            st.session_state.pop(f"editing_rm_{rm_id}", None)
                            st.success("Updated!")
                            st.rerun()
                        except Exception as ex:
                            if "unique" in str(ex).lower():
                                st.error("That email is already taken.")
                            else:
                                st.error(f"Database error: {ex}")

                if cancel:
                    st.session_state.pop(f"editing_rm_{rm_id}", None)
                    st.rerun()