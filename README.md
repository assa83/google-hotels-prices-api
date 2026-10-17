# Google Hotels Prices API – working example (Python, JS, n8n)

Get hotel prices from Google Hotels for any city or list of hotels and dates – nightly rate, total stay, the price on every booking site and a rate-parity check – and get an alert when a price drops below your threshold.

Powered by the [google-hotels-scraper](https://apify.com/lagenuina_agency/google-hotels-scraper) actor on Apify. No browser, no cookies, no account on Google.

## Example output (real result, shortened)

```json
{
  "hotelName": "River Palace Hotel",
  "entityId": "ChcItbiE_4Lfs4JqGgsvZy8xdGh2X2RtdBAB",
  "googleHotelsUrl": "https://www.google.com/travel/hotels/entity/ChcItbiE_4Lfs4JqGgsvZy8xdGh2X2RtdBAB",
  "pricePerNight": 136.02,
  "totalRate": 272.04,
  "currency": "EUR",
  "lowestPriceVendor": "Super.com",
  "officialSitePrice": 202.73,
  "cheaperThanOfficialSite": [
    "Hotelsnest.com",
    "Super.com",
    "Amimir.com",
    "trivago DEALS"
  ],
  "bookingSources": [
    {
      "vendorName": "Super.com",
      "isOfficialSite": false,
      "ratePerNight": 136.02,
      "totalRate": 272.05,
      "bookingUrl": "https://www.google.com/travel/lodging/clk?pc=AA80OsxGrOpYyAu..."
    }
  ],
  "starRating": 4,
  "overallRating": 4.4,
  "reviewCount": 767,
  "location": "hotels in Rome",
  "checkInDate": "2026-11-20",
  "checkOutDate": "2026-11-22",
  "nights": 2,
  "previousPricePerNight": 141.5,
  "priceChangePct": -3.9
}
```

## Quickstart (3 steps)

1. Create a free Apify account and copy your API token from [Settings → Integrations](https://console.apify.com/settings/integrations).
2. Put it in an environment variable (never in code): `export APIFY_TOKEN=your_token`
3. Run the example:

```bash
pip install -r python/requirements.txt
python python/example.py "Hotel Artemide Rome" "River Palace Hotel Rome" --max-price 150
```

JavaScript: `cd js && npm install && node example.mjs`

## Examples

**Python** (`pip install "apify-client<2"`)

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("lagenuina_agency/google-hotels-scraper").call(run_input={
  "locations": [
    "hotels in Rome"
  ],
  "checkInDate": "30 days",
  "checkOutDate": "32 days",
  "currency": "EUR",
  "maxResults": 20
})
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

**JavaScript / Node.js** (`npm install apify-client`)

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('lagenuina_agency/google-hotels-scraper').call({"locations": ["hotels in Rome"], "checkInDate": "30 days", "checkOutDate": "32 days", "currency": "EUR", "maxResults": 20});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

**cURL / any language** – one HTTP call, results in the response:

```bash
curl -X POST "https://api.apify.com/v2/acts/lagenuina_agency~google-hotels-scraper/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"hotels": ["Hotel Artemide Rome"], "checkInDate": "2026-12-05", "checkOutDate": "2026-12-07", "adults": 2, "currency": "EUR"}'
```

All input fields are documented on the [actor page](https://apify.com/lagenuina_agency/google-hotels-scraper) (Input tab).

## Use case: Daily hotel price check with a threshold alert

`python/example.py` prices your watch list for a stay N days ahead (relative dates like `"14 days"` keep a scheduled run looking the same distance ahead) and prints an ALERT for every hotel whose `pricePerNight` is at or below your threshold, plus the booking sites that undercut the official website. Run it daily from cron or use the n8n workflow.

## n8n workflow

[`n8n/workflow.json`](n8n/workflow.json): every day 07:00 → price the hotels 14 days ahead → a Code node keeps only hotels at or below the threshold (edit `MAX_PRICE`), ready for a Slack/Gmail node.

1. In n8n: **Workflows → Import from File** and pick `n8n/workflow.json`.
2. Create a **Header Auth** credential named `Apify API token` with name `Authorization` and value `Bearer <your token>`, and select it in the *Run Apify actor* node.
3. Edit the JSON body (your keywords/targets) and activate.

The `run-sync-get-dataset-items` endpoint waits up to 300 s; for bigger runs use `/runs` plus a webhook.

## Use with AI agents (MCP)

Give Claude, ChatGPT, Cursor or any MCP client this actor as a tool:

```
https://mcp.apify.com/?actors=lagenuina_agency/google-hotels-scraper
```

Example config (Claude Desktop, Cursor, VS Code):

```json
{
  "mcpServers": {
    "google-hotels-scraper": {
      "url": "https://mcp.apify.com/?actors=lagenuina_agency/google-hotels-scraper"
    }
  }
}
```

Sign in with Apify OAuth when asked, or send `Authorization: Bearer <APIFY_TOKEN>`.

## Pricing

$3.99 per 1,000 hotels ($0.00399 per hotel, every booking site's price included), no start fee, pay only for results – see [lagenuina_agency/google-hotels-scraper](https://apify.com/lagenuina_agency/google-hotels-scraper).

## Disclaimer

Independent, not affiliated with Google (not endorsed by Google LLC). It reads only publicly available data. Use it in line with the applicable terms and laws.

## License

[MIT](LICENSE) © Quelli di Carne Genuina
