# 🏠 Apartment Rental Data Analysis
### *A Malloy data analysis project by Francesca Strickland-Anderson*

---

## The Question That Started This

I am currently apartment hunting in Seattle with two roommates. After weeks of scrolling through listings on Zillow and Apartments.com, I realized I was making decisions based on gut feeling rather than data. Does parking actually cost more? Are pet-friendly apartments a premium? Which cities give you the most square footage for your money?

I decided to stop guessing and start analyzing.

---

## The Dataset

**Source:** [UCI Machine Learning Repository — Apartment for Rent Classified](https://archive.ics.uci.edu/dataset/555/apartment+for+rent+classified)

**Size:** 10,000 listings across the United States

**Key columns:** `price`, `square_feet`, `bedrooms`, `bathrooms`, `amenities`, `pets_allowed`, `cityname`, `state`, `fee`

The amenities column contains free-text descriptions like "gym, pool, parking, AC" which I parsed using Malloy's regex matching to create boolean flags for each amenity type.

---

## What I Found

### 1. The bedroom jump is smaller than you think

Going from a 2-bedroom to a 3-bedroom nationally costs about $350/month on average. Split three ways, that is only about $117 per person for an entire extra bedroom. This single finding changed our apartment search — we had been ruling out 3-bedrooms assuming they were too expensive.

![Rent by Bedroom Count](screenshots/rent_by_bedrooms.png)

### 2. Parking is a premium — but it depends

Listings that advertise parking cost more on average, but this is partially because parking tends to come bundled with higher-end buildings that have other amenities too. In a city like Seattle where street parking can cost $150-200/month separately, an apartment that includes parking may actually be a net savings even at a higher listed rent.

![Parking Premium](screenshots/parking_premium.png)

### 3. Pet-friendly is not always more expensive

This surprised me most. Apartments that allow cats are sometimes *cheaper* than apartments with no pet policy listed. My interpretation: landlords in competitive markets who accept pets are using pet-friendliness to attract tenants, which means they keep rent reasonable as part of the deal. High-end buildings allow pets because their tenants can afford deposits — so the premium there reflects building quality, not the pet policy itself.

![Pet Friendly Pricing](screenshots/pet_pricing.png)

### 4. Seattle is expensive — but Tacoma is not

When I filtered to Pacific Northwest listings (Washington and Oregon), the gap between Seattle and nearby cities was striking. Tacoma runs roughly 30-40% cheaper than Seattle with comparable square footage. For three people who could work remotely even part-time, Tacoma represents significant savings.

![Pacific Northwest Cities](screenshots/pnw_cities.png)

### 5. Gyms and pools add the most to rent

Of all the amenities I tested, gym and pool listings carried the biggest average premium. In-unit laundry had a smaller but real premium. For three roommates splitting rent, skipping the gym amenity and keeping individual gym memberships is almost certainly cheaper than paying the premium embedded in rent across 12 months.

![Amenity Premiums](screenshots/amenity_premiums.png)

---

## How to Run This Analysis Yourself

### Requirements
- [VS Code](https://code.visualstudio.com/)
- [Malloy VS Code Extension](https://marketplace.visualstudio.com/items?itemName=malloydata.malloy-vscode)
- [DuckDB](https://duckdb.org/) (installed automatically with the Malloy extension)

### Steps

```bash
# 1. Clone this repo
git clone https://github.com/YOUR_USERNAME/apartment-rental-malloy.git
cd apartment-rental-malloy

# 2. Download the dataset
# Go to: https://archive.ics.uci.edu/dataset/555/apartment+for+rent+classified
# Download apartments_for_rent_classified_10K.csv
# Place it in the root of this repo

# 3. Open in VS Code with the Malloy extension installed
code .

# 4. Open apartments.malloy to see the data model
# Open queries.malloy to run individual queries
# Open analysis.malloynb to read the narrative notebook
```

### Files in this repo

| File | Description |
|---|---|
| `apartments.malloy` | Data model — dimensions, measures, derived fields |
| `queries.malloy` | All individual analysis queries |
| `analysis.malloynb` | Narrative notebook with the full data story |
| `README.md` | This write-up |

---

## Key Takeaways

| Question | Answer |
|---|---|
| Does an extra bedroom cost a lot? | 2→3 bed is ~$350/mo — only ~$117/person split three ways |
| Does parking cost extra? | Yes, but may offset street parking costs in cities |
| Are pet-friendly apartments more expensive? | Not always — competitive markets keep pet-friendly rents reasonable |
| Which Pacific NW city is best value? | Tacoma, WA — 30-40% cheaper than Seattle |
| Do gyms and pools raise rent? | Yes — significantly more than laundry or AC |

---

## Who Would Care About This

This analysis is directly useful for anyone currently renting or apartment hunting, particularly in the Pacific Northwest. Property managers and landlords could use similar analysis to price competitively in their market. Real estate investors evaluating rental markets would benefit from the value-per-square-foot comparison across cities. Urban planners and housing policy researchers interested in affordability could use this type of analysis to identify which markets are most and least accessible for renters at different income levels. Finally, anyone splitting rent with roommates should run the bedroom count analysis before assuming a larger apartment is out of budget — the per-person math often surprises people.

---

## Data Citation

Apartment for Rent Classified [Dataset]. (2019). UCI Machine Learning Repository. https://doi.org/10.24432/C5X623
