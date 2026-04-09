import re
import streamlit as st
from db import get_connection

st.set_page_config(page_title="Apartments", page_icon="🏠", layout="wide")
st.title("🏠 Manage Apartments")

URL_RE = re.compile(r"^https?://", re.IGNORECASE)


def validate_apartment(name, listing_url, image_url, bedrooms, bathrooms, rent):
    errors = []
    if not name.strip():
        errors.append("**Name** is required.")
    if not listing_url.strip():
        errors.append("**Listing URL** is required.")
    elif not URL_RE.match(listing_url.strip()):
        errors.append("**Listing URL** must start with http:// or https://")
    if image_url.strip() and not URL_RE.match(image_url.strip()):
        errors.append("**Image URL** must start with http:// or https:// (or leave it blank).")
    if bedrooms < 1:
        errors.append("**Bedrooms** must be at least 1.")
    if bathrooms < 0.5:
        errors.append("**Bathrooms** must be at least 0.5.")
    if rent <= 0:
        errors.append("**Monthly rent** must be greater than $0.")
    return errors


# ── Add apartment ─────────────────────────────────────────────────────────────
with st.expander("➕ Add new apartment", expanded=True):
    with st.form("add_apartment"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Apartment name *", placeholder="e.g. Cozy Downtown Studio")
            listing_url = st.text_input("Listing URL *", placeholder="https://...")
            image_url = st.text_input("Image URL", placeholder="https://...")
            address = st.text_input("Address", placeholder="123 Main St, Spokane WA")
        with c2:
            bedrooms = st.number_input("Bedrooms *", min_value=1, max_value=10, value=1)
            bathrooms = st.number_input("Bathrooms *", min_value=0.5, max_value=10.0, value=1.0, step=0.5)
            rent = st.number_input("Monthly rent ($) *", min_value=0.0, value=1000.0, step=50.0)
            parking = st.checkbox("Has parking")
            pets = st.checkbox("Pet-friendly")
            laundry = st.checkbox("In-unit laundry")

        submitted = st.form_submit_button("Add apartment", use_container_width=True)

    if submitted:
        errors = validate_apartment(name, listing_url, image_url, bedrooms, bathrooms, rent)
        if errors:
            for e in errors:
                st.error(e)
        else:
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(
                    """
                    INSERT INTO apartments
                        (name, listing_url, image_url, address, bedrooms,
                         bathrooms, monthly_rent, has_parking, is_pet_friendly,
                         has_in_unit_laundry)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """,
                    (
                        name.strip(), listing_url.strip(),
                        image_url.strip() or None, address.strip() or None,
                        bedrooms, bathrooms, rent, parking, pets, laundry,
                    ),
                )
                conn.commit()
                cur.close()
                conn.close()
                st.success(f"✅ '{name.strip()}' added!")
                st.rerun()
            except Exception as ex:
                st.error(f"Database error: {ex}")

st.divider()

# ── Search & list ─────────────────────────────────────────────────────────────
st.subheader("Current apartments")
search = st.text_input("🔍 Search by name or address", placeholder="Type to filter…")

conn = get_connection()
cur = conn.cursor()
if search.strip():
    cur.execute(
        """
        SELECT id, name, address, bedrooms, bathrooms, monthly_rent,
               has_parking, is_pet_friendly, has_in_unit_laundry, listing_url
        FROM apartments
        WHERE name ILIKE %s OR address ILIKE %s
        ORDER BY name;
        """,
        (f"%{search.strip()}%", f"%{search.strip()}%"),
    )
else:
    cur.execute(
        """
        SELECT id, name, address, bedrooms, bathrooms, monthly_rent,
               has_parking, is_pet_friendly, has_in_unit_laundry, listing_url
        FROM apartments ORDER BY name;
        """
    )
apartments = cur.fetchall()
cur.close()
conn.close()

if not apartments:
    st.info("No apartments found.")
else:
    for row in apartments:
        (apt_id, name, address, beds, baths, rent,
         parking, pets, laundry, listing_url) = row

        amenity_str = " | ".join(
            filter(None, [
                "🚗 Parking" if parking else "",
                "🐾 Pets" if pets else "",
                "🧺 Laundry" if laundry else "",
            ])
        ) or "No special amenities"

        with st.container(border=True):
            hcol, bcol, dcol = st.columns([5, 1, 1])
            with hcol:
                st.markdown(f"**{name}**  —  ${rent:,.0f}/mo  |  {beds}bd / {baths}ba")
                st.caption(f"{address or 'No address'} · {amenity_str}")
            with bcol:
                if st.button("✏️ Edit", key=f"edit_{apt_id}"):
                    st.session_state[f"editing_{apt_id}"] = True
            with dcol:
                if st.button("🗑️ Delete", key=f"del_{apt_id}"):
                    st.session_state[f"confirm_del_{apt_id}"] = True

            # Confirm delete
            if st.session_state.get(f"confirm_del_{apt_id}"):
                st.warning(
                    f"Are you sure you want to delete **{name}**? "
                    "This will also delete all its ratings."
                )
                cc1, cc2 = st.columns(2)
                if cc1.button("Yes, delete", key=f"yes_{apt_id}", type="primary"):
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("DELETE FROM apartments WHERE id = %s;", (apt_id,))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.session_state.pop(f"confirm_del_{apt_id}", None)
                    st.success(f"Deleted '{name}'.")
                    st.rerun()
                if cc2.button("Cancel", key=f"no_{apt_id}"):
                    st.session_state.pop(f"confirm_del_{apt_id}", None)
                    st.rerun()

            # Inline edit form
            if st.session_state.get(f"editing_{apt_id}"):
                with st.form(f"edit_form_{apt_id}"):
                    ec1, ec2 = st.columns(2)
                    with ec1:
                        e_name = st.text_input("Name *", value=name)
                        e_url = st.text_input("Listing URL *", value=listing_url)
                        e_addr = st.text_input("Address", value=address or "")
                    with ec2:
                        e_beds = st.number_input("Bedrooms *", min_value=1, max_value=10, value=beds)
                        e_baths = st.number_input("Bathrooms *", min_value=0.5, max_value=10.0,
                                                  value=float(baths), step=0.5)
                        e_rent = st.number_input("Rent ($) *", min_value=0.0,
                                                 value=float(rent), step=50.0)
                        e_parking = st.checkbox("Parking", value=parking)
                        e_pets = st.checkbox("Pet-friendly", value=pets)
                        e_laundry = st.checkbox("Laundry", value=laundry)

                    save, cancel = st.columns(2)
                    save_btn = save.form_submit_button("💾 Save", use_container_width=True)
                    cancel_btn = cancel.form_submit_button("Cancel", use_container_width=True)

                if save_btn:
                    errors = validate_apartment(e_name, e_url, "", e_beds, e_baths, e_rent)
                    if errors:
                        for e in errors:
                            st.error(e)
                    else:
                        conn = get_connection()
                        cur = conn.cursor()
                        cur.execute(
                            """
                            UPDATE apartments SET
                                name=%s, listing_url=%s, address=%s, bedrooms=%s,
                                bathrooms=%s, monthly_rent=%s, has_parking=%s,
                                is_pet_friendly=%s, has_in_unit_laundry=%s
                            WHERE id=%s;
                            """,
                            (e_name.strip(), e_url.strip(), e_addr.strip() or None,
                             e_beds, e_baths, e_rent, e_parking, e_pets, e_laundry, apt_id),
                        )
                        conn.commit()
                        cur.close()
                        conn.close()
                        st.session_state.pop(f"editing_{apt_id}", None)
                        st.success("Updated!")
                        st.rerun()

                if cancel_btn:
                    st.session_state.pop(f"editing_{apt_id}", None)
                    st.rerun()
