# Ourém - Serviços Municipais Online

A collection of static websites providing information about municipal services in Ourém, Portugal.

## Services

### Piscinas Municipais
Displays the swimming pool schedule for Ourém Municipal Pool, showing lane availability by time slot.

### TUFO - Transportes Urbanos
Displays bus schedules for TUFO (Transportes Urbanos de Fátima e Ourém), including all 5 routes (Amarela, Azul, Verde, Vermelha, Preta) with stops and departure times.

## Features

- **Static Data**: PDF is processed once, HTML loads pre-extracted JSON data
- **Fast Loading**: No PDF parsing on client-side
- **Auto-Updates**: GitHub Actions runs daily to update the schedule
- **Responsive Design**: Works on desktop and mobile
- **Interactive Filtering**: Filter by day of the week
- **Lane Availability**: See exactly how many lanes are free at each time slot
- **Activity Legend**: Understand what each activity code means

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

## Local Development

### Generate Schedule Data

```bash
cd piscinas
python3 extract_schedule.py
```

This will create/update `piscinas/schedule.json` with the latest pool schedule.

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
├── index.html                     # Landing page with service links
├── piscinas/                      # Swimming pool service
│   ├── index.html                 # Pool schedule website
│   ├── schedule.json              # Generated schedule data
│   ├── extract_schedule.py        # PDF extraction script
│   └── MGO-PIscinas-202526-TF.pdf # Pool schedule PDF
├── tufo/                          # Public transport service
│   ├── index.html                 # TUFO schedules website
│   ├── schedules.json             # Generated transport schedules
│   └── fetch_schedules.py         # API fetch script
├── .github/
│   └── workflows/
│       ├── update-schedule.yml    # Pool schedule auto-update
│       └── update-tufo.yml        # TUFO schedules auto-update
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
