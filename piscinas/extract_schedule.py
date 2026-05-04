#!/usr/bin/env python3
"""
Extract swimming pool schedule from PDF and generate JSON data.
This script parses the Ourém Municipal Pool schedule PDF and creates
structured data showing lane availability by time slot.
"""

import json
from datetime import datetime

def extract_schedule_from_pdf(pdf_path):
    """Extract schedule data from the PDF."""

    # Define the schedule structure based on the PDF
    days = ["Segunda-Feira", "Terça-Feira", "Quarta-Feira", "Quinta-Feira", "Sexta-Feira", "Sábado"]

    # Manually structured data based on the PDF content
    # Format: {day: {time: {lane1, lane2, lane3, lane4, lane5, lane6}}}
    schedule = {
        "Segunda-Feira": {
            "15h00-16h00": ["P", "P", "P", "P", "P", "CRIO"],
            "16h00-17h00": ["P", "P", "P", "P", "P", "P"],
            "17h30-18h15": ["P", "P", "P", "P", "AMA+", "P"],
            "18h15-19h00": ["JO", "JO", "P", "Hidro", "JO", "JO"],
            "19h15-20h00": ["JO", "JO", "P", "Hidro", "JO", "JO"],
            "20h00-20h45": ["JO", "JO", "P", "Hidro", "JO", "JO"]
        },
        "Terça-Feira": {
            "15h00-16h00": ["P", "P", "AMA Adultos", "AEO", "P", "P"],
            "16h00-17h00": ["P", "P", "P", "HidroSénior", "AEO", "P"],
            "17h30-18h15": ["P", "P", "P", "P", "P", "AEO"],
            "18h15-19h00": ["P", "JO", "JO", "Hidro", "JO", "JO"],
            "19h15-20h00": ["P", "JO", "JO", "Hidro", "JO", "JO"],
            "20h00-20h45": ["JO", "P", "JO", "Hidro", "JO", "JO"]
        },
        "Quarta-Feira": {
            "15h00-16h00": ["P", "P", "P", "P", "P", "P"],
            "16h00-17h00": ["HidroSénior", "P", "P", "P", "HidroSénior", "P"],
            "17h30-18h15": ["P", "AMA+", "P", "P", "P", "P"],
            "18h15-19h00": ["P", "Hidro", "JO", "JO", "P", "Hidro"],
            "19h15-20h00": ["P", "Hidro", "JO", "JO", "P", "Hidro"],
            "20h00-20h45": ["P", "Hidro", "JO", "JO", "P", "Hidro"]
        },
        "Quinta-Feira": {
            "15h00-16h00": ["P", "P", "P", "P", "AMA Adultos", "P"],
            "16h00-17h00": ["P", "P", "P", "P", "HidroSénior", "P"],
            "17h30-18h15": ["P", "P", "P", "P", "P", "P"],
            "18h15-19h00": ["JO", "JO", "P", "Hidro", "JO", "JO"],
            "19h15-20h00": ["JO", "JO", "P", "Hidro", "JO", "JO"],
            "20h00-20h45": ["JO", "P", "JO", "Hidro", "JO", "JO"]
        },
        "Sexta-Feira": {
            "15h00-16h00": ["P", "P", "P", "P", "P", "P"],
            "16h00-17h00": ["P", "P", "P", "P", "P", "P"],
            "17h30-18h15": ["P", "P", "P", "P", "Hidro", "Aqua Cross Fit"],
            "18h15-19h00": ["P", "JO", "JO", "P", "P", "P"],
            "19h15-20h00": ["P", "JO", "JO", "P", "P", "P"],
            "20h00-20h45": ["P", "JO", "JO", "JO", "P", "P"]
        },
        "Sábado": {
            "09h00-09h45": ["AMA", "P", "P", "P", "", ""],
            "09h45-10h15": ["BEBÉS", "P", "JO", "JO", "", ""],
            "10h30-11h00": ["BEBÉS", "P", "JO", "JO", "", ""],
            "11h00-11h30": ["Hidro", "P", "JO", "JO", "", ""],
            "11h45-12h30": ["Hidro", "P", "JO", "JO", "", ""],
            "12h30-13h15": ["P", "P", "P", "P", "JO", "JO"]
        }
    }

    # Process schedule to add availability info
    processed_schedule = {}

    for day, times in schedule.items():
        processed_schedule[day] = []

        for time_slot, lanes in times.items():
            # Count available lanes (marked with "P" or empty)
            available_lanes = sum(1 for lane in lanes if lane == "P" or lane == "")

            # Get lane details
            lane_details = []
            for i, activity in enumerate(lanes, 1):
                if activity:
                    lane_details.append({
                        "lane": i,
                        "activity": activity,
                        "available": activity == "P"
                    })

            processed_schedule[day].append({
                "time": time_slot,
                "available_lanes": available_lanes,
                "total_lanes": len([l for l in lanes if l]),  # Non-empty lanes
                "lanes": lane_details
            })

    return processed_schedule


def main():
    """Main function to extract and save schedule data."""

    pdf_path = "MGO-PIscinas-202526-TF.pdf"

    print("Extracting schedule from PDF...")
    schedule_data = extract_schedule_from_pdf(pdf_path)

    # Add metadata
    output = {
        "last_updated": datetime.now().isoformat(),
        "season": "2025/2026",
        "pool": "Piscina Municipal de Ourém",
        "legend": {
            "P": "Público/Free Swimming",
            "JO": "Juventude Oureense (Club)",
            "Hidro": "Hidroginástica (Water Aerobics)",
            "HidroSénior": "Senior Water Aerobics",
            "AMA": "Adaptação ao Meio Aquático",
            "AEO": "School",
            "CRIO": "Organization",
            "BEBÉS": "Baby Swimming",
            "Aqua Cross Fit": "Aqua Cross Fit Class"
        },
        "schedule": schedule_data
    }

    # Save to JSON
    output_path = "schedule.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Schedule data saved to {output_path}")

    # Print summary
    print("\nSummary:")
    for day, slots in schedule_data.items():
        print(f"\n{day}:")
        for slot in slots:
            print(f"  {slot['time']}: {slot['available_lanes']} lanes available")


if __name__ == "__main__":
    main()
