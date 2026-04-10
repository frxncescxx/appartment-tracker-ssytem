# appartment-tracker-ssytem
# Description:
This system is an apartment search tracker designed for roommates who are deciding on a place to live together. Users can add apartment listings sourced from sites like Zillow or Apartments.com by entering the listing URL, key details, and an image URL. Each listing tracks the number of bedrooms and bathrooms, monthly rent, parking availability, pet-friendliness, in-unit laundry, and a photo. Roommates can each rate every apartment on a 1–5 scale and leave a comment, allowing the group to compare scores side-by-side and make a housing decision together. The system was built because I am currently in the process of finding an apartment in Seattle and thought this system would be super helpful to have.

# ERD:
![ERD](erd.png) 

# Table explanations:
1. apartments
This table acts as the primary repository for all listing data. It stores both quantitative data (rent, beds/baths) and qualitative features (laundry, pets) to allow for easy filtering.

Primary Key: apartment_id

Key Columns: listing_url, monthly_rent, bedrooms, bathrooms, and various boolean flags for amenities (e.g., has_parking).

2. roommates
This table manages the profiles of individuals participating in the search. It ensures that each person's ratings are uniquely identified.

Primary Key: roommate_id

Key Columns: name and email (used to distinguish between different users).

3. ratings
This is a junction table that connects Roommates to Apartments. It allows multiple roommates to rate the same apartment, facilitating a collaborative decision-making process.

Primary Key: rating_id

Foreign Keys: apartment_id (links to apartments) and roommate_id (links to roommates).

Key Columns: score (1–5 scale) and comment for detailed feedback.

# Setup Instructions:

    1. Clone the repository
    git clone https://github.com/frxncescxx/appartment-tracker-ssytem.git 
    cd apartment-tracker

    2. Install dependencies
    pip install -r requirements.txt

    3. Configure your secrets
    Create a file at .streamlit/secrets.toml, this file is gitignored and will never be uploaded to GitHub:
    DB_URL = 'postgresql://retool:npg_TxcWHyD8Uo0J@ep-lively-frost-ak1mhdhf-pooler.c-3.us-west-2.retooldb.com/retool?sslmode=require' 
   
    4. Run the app
    streamlit run streamlit_app.py

# Live URL: (https://appartment-tracker-ssytem-eieh6cznwwlbjhcxb9hdtt.streamlit.app/)