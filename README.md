# Made by hand: who crafts in Australia

FIT3179 Data Visualisation 2. A single-page data story built with Vega-Lite.

## Run it locally
Charts load JSON and CSV files, so opening `index.html` by double-clicking will not work.
In VS Code, right-click `index.html` and choose **Open with Live Server**.

## Publish on GitHub Pages
1. Create a **public** repository and upload everything in this folder (`index.html` must be at the top level).
2. Repository **Settings → Pages → Build and deployment**: Source = *Deploy from a branch*, Branch = `main`, folder = `/ (root)`.
3. After a minute your page is at `https://<your-username>.github.io/<repository-name>/`.
4. Open that URL in a private window to confirm it works for the public.

## Before you submit
Search `index.html` for the yellow `[…]` placeholders and fill them in: your name, dates, the OpenStreetMap download date,
the ABS definition of "screen-based activities", and the AI acknowledgement.

## Folders
- `vega/`: one readable Vega-Lite spec per chart, plus `config.json` (shared fonts and styles)
- `data/`: one small CSV per chart (built by `scripts/build_data.py`; see `DATA_LOG.md`)
- `geo/`: Australian state boundaries (Natural Earth, simplified)
- `scripts/`: data preparation (reference only; not needed to run the page)
