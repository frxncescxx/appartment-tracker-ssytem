import psycopg2
import streamlit as st


def get_connection():
    return psycopg2.connect(st.secrets["DB_URL"])


def init_db():
    """Create all tables if they don't exist yet."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS apartments (
            id SERIAL PRIMARY KEY,
            name VARCHAR(150) NOT NULL,
            listing_url TEXT NOT NULL,
            image_url TEXT,
            address VARCHAR(255),
            bedrooms INTEGER NOT NULL,
            bathrooms NUMERIC(3,1) NOT NULL,
            monthly_rent NUMERIC(10,2) NOT NULL,
            has_parking BOOLEAN DEFAULT false,
            is_pet_friendly BOOLEAN DEFAULT false,
            has_in_unit_laundry BOOLEAN DEFAULT false,
            status VARCHAR(50) DEFAULT 'active',
            date_added TIMESTAMP DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS roommates (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS ratings (
            id SERIAL PRIMARY KEY,
            apartment_id INTEGER NOT NULL REFERENCES apartments(id) ON DELETE CASCADE,
            roommate_id INTEGER NOT NULL REFERENCES roommates(id) ON DELETE CASCADE,
            score INTEGER NOT NULL CHECK (score BETWEEN 1 AND 5),
            comment TEXT,
            rated_at TIMESTAMP DEFAULT NOW(),
            UNIQUE (apartment_id, roommate_id)
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
