"""Turn Overpass JSON exports (one per state) into one tidy CSV of craft shops.

Usage:  python clean_osm.py nsw.json vic.json qld.json sa.json wa.json tas.json nt.json act.json
The state is taken from each file name (nsw.json -> NSW).
Output: craft_shops.csv  (state, shop_type, name, lon, lat)
Source: (c) OpenStreetMap contributors, ODbL. Credit this on the page.
"""
import csv, json, sys
from pathlib import Path

rows, stats = [], {"read": 0, "no_coords": 0, "duplicates": 0}
seen = set()

for path in sys.argv[1:]:
    state = Path(path).stem.upper()
    for el in json.load(open(path, encoding="utf-8")).get("elements", []):
        stats["read"] += 1
        # nodes carry lat/lon; ways/relations carry a centre point ("out center")
        lat = el.get("lat", el.get("center", {}).get("lat"))
        lon = el.get("lon", el.get("center", {}).get("lon"))
        if lat is None or lon is None:
            stats["no_coords"] += 1
            continue
        tags = el.get("tags", {})
        name = tags.get("name", "").strip()
        # same name at (almost) the same spot = the same shop mapped twice
        key = (name.lower(), round(lat, 4), round(lon, 4))
        if key in seen:
            stats["duplicates"] += 1
            continue
        seen.add(key)
        rows.append({"state": state, "shop_type": tags.get("shop", ""),
                     "name": name, "lon": round(lon, 5), "lat": round(lat, 5)})

with open("craft_shops.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["state", "shop_type", "name", "lon", "lat"])
    w.writeheader()
    w.writerows(rows)

print(f"read {stats['read']}, dropped {stats['no_coords']} without coordinates "
      f"and {stats['duplicates']} duplicates, kept {len(rows)}")
for k in sorted({r['state'] for r in rows}):
    print(" ", k, sum(r['state'] == k for r in rows))
for k in sorted({r['shop_type'] for r in rows}):
    print(" ", k or "(none)", sum(r['shop_type'] == k for r in rows))
