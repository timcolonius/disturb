# DISTURB website

Website of the ERC Synergy project DISTURB — Digital Simulation Twins for
Turbulence (GA 101307825). Published at https://timcolonius.github.io/disturb/.

- **Home** text and images: `content.py` and `docs/images/`
- **Team, Publications, Positions**: the project Google Sheet (tabs of those
  names). Edit the sheet, then trigger a rebuild (push any commit, or run the
  workflow from the Actions tab).

Local preview: `make serve` → http://localhost:8001

## Google Sheet layout

The sheet must be shared "Anyone with the link → Viewer". Header row names matter
(case-insensitive); column order doesn't. Extra columns are ignored.

| Tab | Columns |
|---|---|
| **Team** | `first`, `last`, `role` (anything containing "PI" gets a large card), `email` (shown as a link for PIs), `homepage`, `institution` (sorted into Experiment / Simulation / Modelling by keyword — Pprime/Poitiers, Sapienza/Roma, Caltech; anything else goes under Collaborators). Optional: `photo` (file in `docs/images/` or a URL), `show` (`no` hides a row). |
| **Publications** | `citation` (one BibTeX entry per cell), `link` (optional; overrides the BibTeX `url`). Grouped by year, newest first. |
| **Positions** | `position`, `location`, `contact` (an email or a URL). Optional: `status` (`filled`/`closed` moves it to a "Filled or closed" list), `deadline`, `type`, `description`. |

The site rebuilds daily at 06:17 UTC; for an immediate update use **Actions → Build and deploy website → Run workflow**.
