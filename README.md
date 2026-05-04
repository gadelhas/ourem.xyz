# Piscina Municipal de Ourém - Horário

A static website that displays the swimming pool schedule for Ourém Municipal Pool, showing lane availability by time slot.

## Features

- **Static Data**: PDF is processed once, HTML loads pre-extracted JSON data
- **Fast Loading**: No PDF parsing on client-side
- **Auto-Updates**: GitHub Actions runs daily to update the schedule
- **Responsive Design**: Works on desktop and mobile
- **Interactive Filtering**: Filter by day of the week
- **Lane Availability**: See exactly how many lanes are free at each time slot
- **Activity Legend**: Understand what each activity code means

## How It Works

1. **PDF Storage**: The pool schedule PDF (`MGO-PIscinas-202526-TF.pdf`) is stored in the repository
2. **Data Extraction**: `extract_schedule.py` parses the PDF and generates `schedule.json`
3. **Automation**: GitHub Actions workflow (`.github/workflows/update-schedule.yml`) runs:
   - Daily at 6 AM UTC
   - When the PDF or extraction script is updated
   - Manually via workflow dispatch
4. **Display**: `index.html` loads the JSON and displays it with filtering and interactivity

## Local Development

### Generate Schedule Data

```bash
python3 extract_schedule.py
```

This will create/update `schedule.json` with the latest pool schedule.

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
├── index.html                     # Main website
├── schedule.json                  # Generated schedule data
├── extract_schedule.py            # PDF extraction script
├── MGO-PIscinas-202526-TF.pdf    # Pool schedule PDF
├── .github/
│   └── workflows/
│       └── update-schedule.yml    # Auto-update workflow
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

1. Replace `MGO-PIscinas-202526-TF.pdf` with the new PDF
2. Update the data structure in `extract_schedule.py` if the format changed
3. Run `python3 extract_schedule.py` locally to test
4. Commit and push - GitHub Actions will automatically regenerate the data

## License

This project is for public use. Schedule data belongs to Município de Ourém.
