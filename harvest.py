from homeharvest import scrape_property
from datetime import datetime

# Generate filename based on current timestamp
current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"HomeHarvest_{current_timestamp}.csv"

properties = scrape_property(
  location="South San Francisco, CA",
  listing_type="for_sale",  # or (for_sale, for_rent, pending)
  past_days=30,  # sold in last 30 days - listed in last 30 days if (for_sale, for_rent)

  # property_type=['single_family','multi_family'],
  # date_from="2023-05-01", # alternative to past_days
  # date_to="2023-05-28",
  # foreclosure=True
  # mls_only=True,  # only fetch MLS listings
)

dict = {
    "property_url": 0,
    "property_id": 1,
    "listing_id": 2,
    "mls": 3,
    "mls_id": 4,
    "status": 5,
    "text": 6,
    "style": 7,
    "full_street_line": 8,
    "street": 9,
    "unit": 10,
    "city": 11,
    "state": 12,
    "zip_code": 13,
    "beds": 14,
    "full_baths": 15,
    "half_baths": 16,
    "sqft": 17,
    "year_built": 18,
    "days_on_mls": 19,
    "list_price": 20,
    "list_price_min": 21,
    "list_price_max": 22,
    "list_date": 23,
    "sold_price": 24,
    "last_sold_date": 25,
    "assessed_value": 26,
    "estimated_value": 27,
    "tax": 28,
    "tax_history": 29,
    "new_construction": 30,
    "lot_sqft": 31,
    "price_per_sqft": 32,
    "latitude": 33,
    "longitude": 34,
    "neighborhoods": 35,
    "county": 36,
    "fips_code": 37,
    "stories": 38,
    "hoa_fee": 39,
    "parking_garage": 40,
    "agent_id": 41,
    "agent_name": 42,
    "agent_email": 43,
    "agent_phones": 44,
    "agent_mls_set": 45,
    "agent_nrds_id": 46,
    "broker_id": 47,
    "broker_name": 48,
    "builder_id": 49,
    "builder_name": 50,
    "office_id": 51,
    "office_mls_set": 52,
    "office_name": 53,
    "office_email": 54,
    "office_phones": 55,
    "nearby_schools": 56,
    "primary_photo": 57,
    "alt_photos": 58
}

for index, row in properties.iterrows():
    print(f"{row['full_street_line']:<30}{row['city'] + ", " + row['state']:^20}\t{row['text']:^50.80}...")

print(properties)


print(f"Number of properties: {len(properties)}")

# Export to csv
# properties.to_csv(filename, index=False)
# print(properties.head())
