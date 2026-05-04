# Ourém - Serviços Municipais Online

A collection of static websites providing information about municipal services in Ourém, Portugal.

## Services

### Piscinas Municipais
Displays the swimming pool schedule for Ourém Municipal Pool, showing lane availability by time slot.

### TUFO - Transportes Urbanos
Displays bus schedules for TUFO (Transportes Urbanos de Fátima e Ourém), including all 5 routes (Amarela, Azul, Verde, Vermelha, Preta) with stops and departure times.

### Bewater - Water Service Interruptions
Shows active water service interruptions across all parishes in Ourém. Alert banner appears on landing page when there are active interruptions. Maintains historical CSV log of all interruptions for future statistics.

## Features

- **Static Data**: PDFs/APIs are processed server-side, HTML loads pre-extracted JSON data
- **Fast Loading**: No PDF parsing or API calls on client-side
- **Auto-Updates**: GitHub Actions runs hourly (Bewater) or daily (TUFO/Piscinas)
- **Responsive Design**: Works on desktop and mobile
- **Interactive UI**: Filter by day, expand details, color-coded routes/alerts
- **Real-time Alerts**: Water interruption banner appears automatically when issues detected
- **Historical Tracking**: CSV logs for future statistics and trend analysis

## How It Works

### Piscinas (Swimming Pool)

1. **PDF Storage**: The pool schedule PDF (`MGO-PIscinas-202526-TF.pdf`) is stored in the repository
2. **Data Extraction**: `extract_schedule.py` parses the PDF and generates `schedule.json`
3. **Automation**: GitHub Actions workflow runs when the PDF or extraction script is updated
4. **Display**: `index.html` loads the JSON and displays it with filtering and interactivity

### TUFO (Public Transport)

1. **API Fetching**: `fetch_schedules.py` fetches live data from TUFO API
2. **Data Processing**: Organizes routes, circuits, stops, and departure times into `schedules.json`
3. **Automation**: GitHub Actions workflow runs daily at 3 AM UTC to check for updates
4. **Display**: `index.html` loads the JSON and displays routes with color-coded tabs

### Bewater (Water Service)

1. **API Fetching**: `fetch_interruptions.py` fetches interruption data from Bewater API
2. **Data Processing**:
   - Parses HTML response to extract interruption details
   - Maintains `interruptions_history.csv` with ALL interruptions ever detected (for statistics)
   - Generates `interruptions.json` with currently ACTIVE interruptions only
3. **Automation**: GitHub Actions workflow runs every hour to check for new interruptions
4. **Display**: Landing page shows alert banner when active interruptions exist
5. **Historical Tracking**: CSV file logs every interruption with discovery timestamp for future analytics

## Local Development

### Generate Data Files

**Piscinas (Pool):**
```bash
cd piscinas
python3 extract_schedule.py
```

**TUFO (Transport):**
```bash
cd tufo
python3 fetch_schedules.py
```

**Bewater (Water Interruptions):**
```bash
cd bewater
python3 fetch_interruptions.py
```

### Query Historical Interruptions

The CSV file makes it easy to analyze interruption patterns:

```bash
# Count interruptions in May 2026
grep "05/2026" bewater/interruptions_history.csv | wc -l

# Find all interruptions in a specific location
grep "Cavadinha" bewater/interruptions_history.csv

# View most recent 10 interruptions
tail -10 bewater/interruptions_history.csv
```

### View the Website

Simply open `index.html` in your browser:

```bash
open index.html
```

Or serve it with a local server:

```bash
python3 -m http.server 8000
# Then visit http://localhost:8000
```

## Deployment

### GitHub Pages

1. Push the repository to GitHub
2. Go to Settings → Pages
3. Set source to `main` branch, root directory
4. The site will be available at `https://yourusername.github.io/ourem.xyz/`

### Netlify/Vercel

Simply connect your GitHub repository and deploy. The site is fully static.

## File Structure

```
ourem.xyz/
├── index.html                     # Landing page with service links & water alerts
├── piscinas/                      # Swimming pool service
│   ├── index.html                 # Pool schedule website
│   ├── schedule.json              # Generated schedule data
│   ├── extract_schedule.py        # PDF extraction script
│   └── MGO-PIscinas-202526-TF.pdf # Pool schedule PDF
├── tufo/                          # Public transport service
│   ├── index.html                 # TUFO schedules website
│   ├── schedules.json             # Generated transport schedules
│   └── fetch_schedules.py         # API fetch script
├── bewater/                       # Water service interruptions
│   ├── interruptions.json         # Current active interruptions
│   ├── interruptions_history.csv  # Historical log of all interruptions
│   └── fetch_interruptions.py     # API fetch and parse script
├── .github/
│   └── workflows/
│       ├── update-schedule.yml    # Pool schedule auto-update
│       ├── update-tufo.yml        # TUFO schedules auto-update (daily)
│       └── update-bewater.yml     # Water interruptions auto-update (hourly)
└── README.md
```

## Schedule Legend

- **P**: Público/Free Swimming (available lanes)
- **JO**: Juventude Oureense (Club)
- **Hidro**: Hidroginástica (Water Aerobics)
- **HidroSénior**: Senior Water Aerobics
- **AMA**: Adaptação ao Meio Aquático (Water Adaptation)
- **AEO**: School
- **CRIO**: Organization
- **BEBÉS**: Baby Swimming
- **Aqua Cross Fit**: Aqua Cross Fit Class

## Updating the Schedule

When a new schedule PDF is released:

1. Replace `piscinas/MGO-PIscinas-202526-TF.pdf` with the new PDF
2. Update the data structure in `piscinas/extract_schedule.py` if the format changed
3. Run `cd piscinas && python3 extract_schedule.py` locally to test
4. Commit and push - GitHub Actions will automatically regenerate the data

## License

This project is for public use. Schedule data belongs to Município de Ourém.
