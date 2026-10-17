"""Daily hotel price check: alert when a hotel's nightly price is at or below a threshold.

Usage: python example.py "Hotel Artemide Rome" "River Palace Hotel Rome" --max-price 150
"""
import argparse
import os
import sys

from apify_client import ApifyClient

ACTOR = "lagenuina_agency/google-hotels-scraper"
TOKEN = os.environ.get("APIFY_TOKEN")
if not TOKEN:
    sys.exit("Set APIFY_TOKEN first: https://console.apify.com/settings/integrations")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("hotels", nargs="+", help="hotel names or Google Hotels URLs")
    p.add_argument("--max-price", type=float, required=True, help="alert threshold per night")
    p.add_argument("--days-ahead", type=int, default=14)
    p.add_argument("--nights", type=int, default=1)
    p.add_argument("--currency", default="EUR")
    a = p.parse_args()

    client = ApifyClient(TOKEN)
    run = client.actor(ACTOR).call(run_input={
        "hotels": a.hotels,
        "checkInDate": f"{a.days_ahead} days",
        "checkOutDate": f"{a.days_ahead + a.nights} days",
        "adults": 2,
        "currency": a.currency,
        "includeBookingSources": True,
    })
    alerts = 0
    for h in client.dataset(run["defaultDatasetId"]).iterate_items():
        price = h.get("pricePerNight")
        if price is None:
            print(f"  no price: {h.get('hotelName')}")
            continue
        line = f"{h['hotelName']}: {price} {h.get('currency')} / night on {h.get('lowestPriceVendor')} ({h.get('checkInDate')})"
        if price <= a.max_price:
            alerts += 1
            print("ALERT " + line)
        else:
            print("      " + line)
        if h.get("cheaperThanOfficialSite"):
            print(f"      cheaper than official site ({h.get('officialSitePrice')}): {', '.join(h['cheaperThanOfficialSite'])}")
    print(f"{alerts} hotel(s) at or below {a.max_price} {a.currency}")


if __name__ == "__main__":
    main()
