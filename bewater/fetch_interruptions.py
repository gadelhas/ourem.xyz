#!/usr/bin/env python3
"""
Fetch Bewater water service interruptions and track them historically.
"""

import json
import csv
import re
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

API_URL = "https://ourem-bewater.com.pt/wp-admin/admin-ajax.php"

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent
CSV_FILE = SCRIPT_DIR / "interruptions_history.csv"
JSON_FILE = SCRIPT_DIR / "interruptions.json"

def fetch_interruptions_html():
    """Fetch interruptions HTML from Bewater API."""
    print("Fetching interruptions from Bewater API...")

    data = urllib.parse.urlencode({
        'action': 'update_avarias_widget',
        'order': 'DESC'
    }).encode('utf-8')

    req = urllib.request.Request(API_URL, data=data)
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')

    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        return result.get('html', '')

def parse_interruptions(html):
    """Parse interruption data from HTML."""
    interruptions = []

    # Find all avaria-item divs
    pattern = r'<div class="avaria-item" data-index="(\d+)".*?>(.*?)</div>\s*(?=<div class="avaria-item"|$)'
    matches = re.finditer(pattern, html, re.DOTALL)

    for match in matches:
        item_id = match.group(1)
        content = match.group(2)

        # Extract type
        if 'Avaria Não Programada' in content:
            tipo = 'Não Programada'
        elif 'Avaria Programada' in content:
            tipo = 'Programada'
        else:
            tipo = 'Desconhecida'

        # Extract location (street name)
        location_match = re.search(r'<span class="avaria-street">(.*?)</span>', content)
        location = location_match.group(1).strip() if location_match else 'Desconhecido'

        # Extract start date
        date_match = re.search(r'<span class="avaria-date">(.*?)</span>', content)
        start_date = date_match.group(1).strip() if date_match else ''

        # Extract restoration forecast
        forecast_match = re.search(r'<span class="avaria-forecast">(.*?)</span>', content)
        restoration_date = forecast_match.group(1).strip() if forecast_match else ''

        # Extract last updated
        updated_match = re.search(r'Última atualização: ([\d/\s:]+)', content)
        last_updated = updated_match.group(1).strip() if updated_match else ''

        # Extract affected streets
        streets = []
        street_pattern = r'<p>Rua: (.*?)</p>'
        street_matches = re.finditer(street_pattern, content)
        for sm in street_matches:
            streets.append(sm.group(1).strip())

        # Check for "e ruas adjacentes"
        if 'e ruas adjacentes' in content:
            if streets:
                streets[-1] += ' e ruas adjacentes'
            else:
                streets.append(location + ' e ruas adjacentes')

        affected_streets = '; '.join(streets) if streets else location

        interruptions.append({
            'id': item_id,
            'type': tipo,
            'location': location,
            'start_datetime': start_date,
            'restoration_datetime': restoration_date,
            'last_updated': last_updated,
            'affected_streets': affected_streets
        })

    print(f"Parsed {len(interruptions)} interruptions")
    return interruptions

def parse_datetime(date_str):
    """Parse Portuguese datetime format DD/MM/YYYY HH:MM."""
    try:
        return datetime.strptime(date_str, '%d/%m/%Y %H:%M')
    except:
        return None

def is_active(interruption):
    """Check if interruption is currently active."""
    restoration_dt = parse_datetime(interruption['restoration_datetime'])
    if not restoration_dt:
        return True  # If we can't parse, assume active
    return datetime.now() < restoration_dt

def load_existing_ids():
    """Load existing interruption IDs from CSV to avoid duplicates."""
    csv_path = Path(CSV_FILE)
    if not csv_path.exists():
        return set()

    existing_ids = set()
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_ids.add(row['id'])

    return existing_ids

def append_to_csv(new_interruptions):
    """Append new interruptions to CSV file."""
    csv_path = Path(CSV_FILE)
    file_exists = csv_path.exists()

    fieldnames = ['id', 'type', 'location', 'start_datetime', 'restoration_datetime',
                  'last_updated', 'affected_streets', 'discovered_at']

    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for interruption in new_interruptions:
            interruption['discovered_at'] = datetime.now().strftime('%d/%m/%Y %H:%M')
            writer.writerow(interruption)

    print(f"Appended {len(new_interruptions)} new interruptions to CSV")

def save_active_json(active_interruptions):
    """Save currently active interruptions to JSON for website display."""
    output = {
        'last_updated': datetime.now().isoformat(),
        'count': len(active_interruptions),
        'interruptions': active_interruptions
    }

    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(active_interruptions)} active interruptions to JSON")

def main():
    """Main function."""
    # Fetch data
    html = fetch_interruptions_html()

    # Parse interruptions
    all_interruptions = parse_interruptions(html)

    # Load existing IDs
    existing_ids = load_existing_ids()

    # Find new interruptions
    new_interruptions = [i for i in all_interruptions if i['id'] not in existing_ids]

    if new_interruptions:
        print(f"Found {len(new_interruptions)} new interruptions")
        append_to_csv(new_interruptions)
    else:
        print("No new interruptions found")

    # Filter active interruptions
    active_interruptions = [i for i in all_interruptions if is_active(i)]
    print(f"Currently {len(active_interruptions)} active interruptions")

    # Save active to JSON
    save_active_json(active_interruptions)

    # Print summary
    print("\nSummary:")
    print(f"  Total fetched: {len(all_interruptions)}")
    print(f"  New (added to CSV): {len(new_interruptions)}")
    print(f"  Currently active: {len(active_interruptions)}")

    if active_interruptions:
        print("\nActive interruptions:")
        for i in active_interruptions:
            print(f"  - {i['location']} ({i['type']})")

if __name__ == "__main__":
    main()
