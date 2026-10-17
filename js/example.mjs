// Cheapest 4-5 star hotels in a city for a stay 30 days ahead.
// Usage: node example.mjs "hotels in Rome"
import { ApifyClient } from 'apify-client';

const token = process.env.APIFY_TOKEN;
if (!token) {
    console.error('Set APIFY_TOKEN first: https://console.apify.com/settings/integrations');
    process.exit(1);
}

const location = process.argv[2] ?? 'hotels in Rome';
const client = new ApifyClient({ token });
const run = await client.actor('lagenuina_agency/google-hotels-scraper').call({
    locations: [location],
    checkInDate: '30 days',
    checkOutDate: '32 days',
    currency: 'EUR',
    hotelClass: ['4', '5'],
    maxResults: 30,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
items.filter((h) => h.pricePerNight != null).sort((a, b) => a.pricePerNight - b.pricePerNight).slice(0, 10)
    .forEach((h) => console.log(`${h.pricePerNight} ${h.currency}  ${h.starRating}*  ${h.hotelName}  (${h.lowestPriceVendor})`));
