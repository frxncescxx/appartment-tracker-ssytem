import re
import streamlit as st
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
                st.success(f"✅ '{r_name.strip()}' added!")
                st.rerun()
            except Exception as ex:
                if "unique" in str(ex).lower():
                    st.error("That email address is already registered.")
                else:
                    st.error(f"Database error: {ex}")

st.divider()

# ── Search & list ─────────────────────────────────────────────────────────────
st.subheader("Current roommates")
search = st.text_input("🔍 Search by name or email")

conn = get_connection()
cur = conn.cursor()
if search.strip():
    cur.execute(
        """
        SELECT r.id, r.name, r.email, r.created_at,
               COUNT(rt.id) AS num_ratings
        FROM roommates r
        LEFT JOIN ratings rt ON rt.roommate_id = r.id
        WHERE r.name ILIKE %s OR r.email ILIKE %s
        GROUP BY r.id ORDER BY r.name;
        """,
        (f"%{search.strip()}%", f"%{search.strip()}%"),
    )
else:
    cur.execute(
        """
        SELECT r.id, r.name, r.email, r.created_at,
               COUNT(rt.id) AS num_ratings
        FROM roommates r
        LEFT JOIN ratings rt ON rt.roommate_id = r.id
        GROUP BY r.id ORDER BY r.name;
        """
    )
roommates = cur.fetchall()
cur.close()
conn.close()

if not roommates:
    st.info("No roommates found.")
else:
    for row in roommates:
        rm_id, rm_name, rm_email, created_at, num_ratings = row

        with st.container(border=True):
            hcol, bcol, dcol = st.columns([5, 1, 1])
            with hcol:
                st.markdown(f"**{rm_name}** — {rm_email}")
                st.caption(f"Joined {created_at.strftime('%b %d, %Y')} · {num_ratings} rating(s) submitted")
            with bcol:
                if st.button("✏️ Edit", key=f"edit_{rm_id}"):
                    st.session_state[f"editing_rm_{rm_id}"] = True
            with dcol:
                if st.button("🗑️ Delete", key=f"del_{rm_id}"):
                    st.session_state[f"confirm_del_rm_{rm_id}"] = True

            # Confirm delete
            if st.session_state.get(f"confirm_del_rm_{rm_id}"):
                st.warning(
                    f"Delete **{rm_name}**? Their ratings will also be removed."
                )
                cc1, cc2 = st.columns(2)
                if cc1.button("Yes, delete", key=f"yes_rm_{rm_id}", type="primary"):
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("DELETE FROM roommates WHERE id = %s;", (rm_id,))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.session_state.pop(f"confirm_del_rm_{rm_id}", None)
                    st.success(f"Deleted '{rm_name}'.")
                    st.rerun()
                if cc2.button("Cancel", key=f"no_rm_{rm_id}"):
                    st.session_state.pop(f"confirm_del_rm_{rm_id}", None)
                    st.rerun()

            # Inline edit form
            if st.session_state.get(f"editing_rm_{rm_id}"):
                with st.form(f"edit_rm_{rm_id}"):
                    ec1, ec2 = st.columns(2)
                    with ec1:
                        e_name = st.text_input("Name *", value=rm_name)
                    with ec2:
                        e_email = st.text_input("Email *", value=rm_email)
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
