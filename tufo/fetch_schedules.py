#!/usr/bin/env python3
"""
Fetch TUFO transport schedules from API and generate JSON data.
TUFO is the urban transport service in Ourém/Fátima.
"""

import json
import urllib.request
from datetime import datetime
from collections import defaultdict

API_URL = "https://servicos.ourem.pt/api/index.php?service=tufo"

def fetch_tufo_schedules():
    """Fetch schedule data from TUFO API."""
    print("Fetching TUFO schedules from API...")

    with urllib.request.urlopen(API_URL) as response:
        data = json.loads(response.read().decode('utf-8'))

    print(f"Fetched {len(data)} schedule entries")
    return data

def process_schedules(raw_data):
    """Process raw API data into organized route schedules."""

    # Organize by route (linha)
    routes = defaultdict(lambda: {
        'name': '',
        'color': '',
        'circuits': defaultdict(list)
    })

    for entry in raw_data:
        linha = entry.get('linha', 'Unknown')
        circuito = entry.get('circuito', 'Unknown')
        paragem = entry.get('paragem', 'Unknown')

        # Extract all departure times
        times = []
        for i in range(1, 9):  # horario_1 to horario_8
            time = entry.get(f'horario_{i}')
            if time and time.strip():
                times.append(time.strip())

        # Store route metadata
        routes[linha]['name'] = linha
        routes[linha]['color'] = get_route_color(linha)

        # Add stop with its times
        routes[linha]['circuits'][circuito].append({
            'stop': paragem,
            'times': times
        })

    return routes

def get_route_color(linha):
    """Map route name to color."""
    color_map = {
        'Amarela': '#FFC107',
        'Azul': '#2196F3',
        'Verde': '#4CAF50',
        'Vermelha': '#F44336',
        'Preta': '#424242'
    }
    return color_map.get(linha, '#9E9E9E')

def main():
    """Main function to fetch and save TUFO schedules."""

    # Fetch data from API
    raw_data = fetch_tufo_schedules()

    # Process into organized structure
    processed_routes = process_schedules(raw_data)

    # Convert to regular dict for JSON serialization
    output = {
        "last_updated": datetime.now().isoformat(),
        "source": "TUFO - Transportes Urbanos de Fátima e Ourém",
        "api_url": API_URL,
        "routes": {}
    }

    for route_name, route_data in processed_routes.items():
        output['routes'][route_name] = {
            'name': route_data['name'],
            'color': route_data['color'],
            'circuits': {
                circuit: stops for circuit, stops in route_data['circuits'].items()
            }
        }

    # Save to JSON
    output_path = "schedules.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nSchedules saved to {output_path}")

    # Print summary
    print("\nSummary:")
    for route_name, route_data in output['routes'].items():
        circuit_count = len(route_data['circuits'])
        total_stops = sum(len(stops) for stops in route_data['circuits'].values())
        print(f"  {route_name}: {circuit_count} circuits, {total_stops} stops")

if __name__ == "__main__":
    main()
