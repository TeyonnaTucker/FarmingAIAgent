import os
import time
import requests
from collections import Counter
from dotenv import load_dotenv

# Load API keys
load_dotenv()
QS_KEY = os.getenv("QUICKSTATS_KEY")
TOG_KEY = os.getenv("TOGETHERAI_API_KEY")
if not QS_KEY or not TOG_KEY:
    raise ValueError("Missing QUICKSTATS_KEY or TOGETHERAI_API_KEY in .env")

def get_lat_lon_from_zip(zip_code):
    r = requests.get(f"https://api.zippopotam.us/us/{zip_code}")
    if r.status_code != 200:
        return None, None
    p = r.json()['places'][0]
    return float(p['latitude']), float(p['longitude'])

def get_county_state(lat, lon):
    url = "https://geo.fcc.gov/api/census/block/find"
    params = {"latitude": lat, "longitude": lon, "format": "json"}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"FCC API error: {response.status_code}")
        return None, None

    data = response.json()
    county = data.get("County", {}).get("name")
    state = data.get("State", {}).get("name")

    if county and state:
        print(f"Parsed county: {county}, state: {state}")
        return county, state
    else:
        print("Could not determine county/state for that location.")
        return None, None

def fetch_crop_data_county(state, county):
    params = {
        "key": QS_KEY,
        "source_desc": "SURVEY",
        "sector_desc": "CROPS",
        "agg_level_desc": "COUNTY",
        "state_alpha": state,
        "county_name": county,
        "year": "2023",
        "format": "JSON"
    }
    r = requests.get("https://quickstats.nass.usda.gov/api/api_GET/", params=params)
    r.raise_for_status()
    return r.json().get("data", [])

def summarize_crops(data):
    counter = Counter()
    for rec in data:
        crop = rec["commodity_desc"]
        try:
            acres = float(rec["Value"].replace(",", ""))
        except:
            continue
        counter[crop] += acres
    return counter, counter.most_common(5)

def interpret_with_together(text):
    res = requests.post(
        "https://api.together.xyz/inference",
        headers={
            "Authorization": f"Bearer {TOG_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "prompt": f"As an agriculture expert, analyze this crop summary:\n\n{text}",
            "max_tokens": 300
        }
    )
    if res.status_code == 200:
        return res.json().get("output", "[no output]")
    return f"[ERROR {res.status_code}] {res.text}"

def main():
    zip_code = input("Enter ZIP code: ").strip()
    lat, lon = get_lat_lon_from_zip(zip_code)
    if lat is None:
        print("Invalid ZIP code.")
        return

    print(f"Coordinates: lat={lat}, lon={lon}")
    county, state = get_county_state(lat, lon)
    if not county or not state:
        print("Could not determine county/state for that location.")
        return

    print(f"Location identified: {county}, {state}")
    crop_data = fetch_crop_data_county(state, county)
    if not crop_data:
        print("No crop data found for this county.")
        return

    counter, top5 = summarize_crops(crop_data)
    total = sum(counter.values())
    summary = f"Top 5 crops in {county}, {state} (2023 acreage):\n"
    for crop, acres in top5:
        summary += f" - {crop}: {int(acres):,} acres ({acres/total:.1%})\n"
    print("\n" + summary)

    print(" AI Interpretation:")
    print(interpret_with_together(summary))

if __name__ == "__main__":
    main()

