"""Build the tidy CSVs for the crafts visualisation from the ABS and NAPS spreadsheets.
Run from the project root:  python scripts/build_data.py <folder with the xlsx files>
Every number is read from the source tables; nothing is typed in by hand.
"""
import csv, sys
from pathlib import Path
from openpyxl import load_workbook

SRC = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
OUT = Path("data"); OUT.mkdir(exist_ok=True)

def sheet(file, name):
    return list(load_workbook(SRC / file, read_only=True)[name].iter_rows(values_only=True))

def write(name, header, rows):
    with open(OUT / name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)
    print(f"{name}: {len(rows)} rows")

T17 = "cultural_and_creative_activities_202122_tables_1_to_7.xlsx"
T813 = "cultural_and_creative_activities_202122_tables_8_to_13.xlsx"
NAPS = "REF_NAPS-2022-Data-Tables.xlsx"

AGES = ["15–24", "25–34", "35–44", "45–54", "55–64", "65+"]
ACT = {  # source label prefix -> plain-English name
    "Performing in a drama": "Acting and performing",
    "Singing or playing": "Singing or playing an instrument",
    "Dancing": "Dancing",
    "Writing song lyrics": "Songwriting and making music",
    "Writing any fiction": "Writing stories, poetry or blogs",
    "Visual art activities, such as": "Painting, drawing and sculpting",
    "Photography": "Photography",
    "Film-making": "Film-making and editing",
    "Craft activities": "Craft",
    "Designing websites": "Designing websites and games",
    "Fashion, interior": "Fashion, interior, graphic design",
}
def short(label):
    for k, v in ACT.items():
        if str(label).startswith(k): return v

# ---------- Table 4: participation by activity, age and sex ----------
t4 = sheet(T17, "Table 4")
def block(rows, start, stop_label):
    out = {}
    for r in rows[start:]:
        if str(r[0]).startswith(stop_label): break
        n = short(r[0])
        if n and isinstance(r[1], (int, float)): out[n] = [float(x) for x in r[1:8]]
    return out
pers_cnt = block(t4, 50, "Total participants")
pop = [float(x) for x in t4[69][1:8]]                       # total persons by age + all
assert t4[69][0] == "Total persons" and abs(pop[6] - 20390) < 1
assert pers_cnt["Craft"][6] == 3099.7 and len(pers_cnt) == 11
rate_m = [float(x) for x in t4[85][1:8]]; rate_f = [float(x) for x in t4[106][1:8]]; rate_p = [float(x) for x in t4[127][1:8]]
assert (rate_m[6], rate_f[6], rate_p[6]) == (7.1, 22.9, 15.2)

# 01 waffle
write("01_craft_rate_by_sex.csv", ["sex", "craft_rate_pct", "per_100_people"],
      [["Women", rate_f[6], round(rate_f[6])], ["Men", rate_m[6], round(rate_m[6])], ["All adults", rate_p[6], round(rate_p[6])]])
# 02 lollipop
write("02_activity_participants.csv", ["activity", "participants_thousand", "rate_pct_of_adults"],
      sorted([[a, v[6], round(100 * v[6] / pop[6], 1)] for a, v in pers_cnt.items()], key=lambda x: -x[1]))
# 03 butterfly
write("03_craft_rate_by_age_sex.csv", ["age_group", "sex", "craft_rate_pct"],
      [[AGES[i], s, r[i]] for s, r in (("Men", rate_m), ("Women", rate_f)) for i in range(6)])
# 04 bump chart: rate and rank of 11 activities within each age group
rows04 = []
for i, age in enumerate(AGES):
    rates = {a: 100 * v[i] / pop[i] for a, v in pers_cnt.items()}
    for rank, a in enumerate(sorted(rates, key=lambda k: -rates[k]), 1):
        rows04.append([a, age, pers_cnt[a][i], pop[i], round(rates[a], 2), rank])
write("04_activity_age_ranks.csv", ["activity", "age_group", "participants_thousand", "adults_thousand", "rate_pct", "rank"], rows04)

# ---------- Table 1 and 3: states ----------
ST = ["New South Wales", "Victoria", "Queensland", "South Australia", "Western Australia", "Tasmania", "Northern Territory", "Australian Capital Territory"]
AB = ["NSW", "Vic", "Qld", "SA", "WA", "Tas", "NT", "ACT"]
t1 = sheet(T17, "Table 1")
assert t1[56][0] == "Total participants" and t1[40][0].startswith("Total male") and t1[48][0].startswith("Total female")
rate_state = {"all": t1[56][1:9], "men": t1[40][1:9], "women": t1[48][1:9]}
part_k = t1[31][1:9]
t3 = sheet(T17, "Table 3")
def depth(none_row, t3_row, t4_row, tot_row):
    d = []
    for i in range(8):
        none, tot = t3[none_row][1 + i], t3[tot_row][1 + i]
        d.append((100 * (t3[t3_row][1 + i] + t3[t4_row][1 + i]) / (tot - none), tot - none))
    return d
dep = {"men": depth(10, 13, 14, 15), "women": depth(18, 21, 22, 23)}
adults_k = [t3[31][1 + i] for i in range(8)]   # persons total, aged 15+
assert abs(sum(adults_k) - 20390) < 5, sum(adults_k)

# 05 choropleth
write("05_state_participation_rate.csv", ["state", "state_abbr", "participation_rate_pct", "participants_thousand", "adults_thousand"],
      [[ST[i], AB[i], rate_state["all"][i], part_k[i], round(adults_k[i], 1)] for i in range(8)])
# 06 proportional symbols (two panels)
CAP = [("Sydney", 151.21, -33.87), ("Melbourne", 144.96, -37.81), ("Brisbane", 153.03, -27.47), ("Adelaide", 138.60, -34.93),
       ("Perth", 115.86, -31.95), ("Hobart", 147.33, -42.88), ("Darwin", 130.84, -12.46), ("Canberra", 149.13, -35.28)]
rows06 = []
for sex in ("men", "women"):
    for i in range(8):
        rows06.append([ST[i], AB[i], sex.title(), rate_state[sex][i], round(dep[sex][i][0], 1), round(dep[sex][i][1], 1), CAP[i][0], CAP[i][1], CAP[i][2]])
write("06_state_sex_symbols.csv", ["state", "state_abbr", "sex", "participation_rate_pct", "pct_of_participants_doing_3plus_types",
      "participants_thousand_table3", "capital", "capital_lon", "capital_lat"], rows06)

# ---------- 07 craft shops (OpenStreetMap, from craft_shops.csv) ----------
shops = Path("craft_shops.csv")
if not shops.exists(): shops = SRC / "craft_shops.csv"
rows07 = []
for r in csv.DictReader(open(shops, encoding="utf-8")):
    grp = "Craft and art supplies" if r["shop_type"] == "craft" else "Fabric, sewing and yarn"
    rows07.append([r["state"], r["shop_type"], grp, r["name"] or "(unnamed)", r["lon"], r["lat"]])
write("07_craft_shops.csv", ["state", "shop_type", "group", "name", "lon", "lat"], rows07)

# ---------- Table 7: hours heatmap ----------
t7 = sheet(T17, "Table 7")
COLS = ["1–13 weeks, under 10 hours a week", "1–13 weeks, 10+ hours a week", "Over 13 weeks, under 10 hours a week", "Over 13 weeks, 10+ hours a week"]
rows08 = []
abs_pct = {}   # ABS's own percentage block (second occurrence of each activity), used as a cross-check
seen = {}
for r in t7[9:80]:
    n = short(r[0])
    if n and isinstance(r[1], (int, float)):
        seen[n] = seen.get(n, 0) + 1
        if seen[n] == 2: abs_pct[n] = r[1:5]
for r in t7[9:30]:
    n = short(r[0])
    if n and isinstance(r[1], (int, float)):
        tot = r[5]
        gap = tot - sum(r[1:5])          # people the four columns do not account for
        assert abs(gap) / tot < 0.03, (n, r[1:6])
        for c, v, a in zip(COLS, r[1:5], abs_pct[n]):
            assert abs(100 * v / tot - a) < 0.15, (n, c, 100 * v / tot, a)   # matches ABS percentages
            rows08.append([n, c, round(v, 1), round(100 * v / tot, 1)])
        print(f"   {n[:28]:28} four columns cover {100*sum(r[1:5])/tot:.1f}% of participants")
assert [x for x in rows08 if x[0] == "Craft"][0][3] == 45.1
write("08_activity_hours.csv", ["activity", "involvement", "participants_thousand", "pct_of_participants"], rows08)

# ---------- Table 5: income / volunteering (persons = columns 11-15) ----------
t5 = sheet(T17, "Table 5")
rows09 = []
for r in t5[11:26]:   # counts block only (the percentage block starts at row 28)
    n = short(r[0])
    if n and isinstance(r[11], (int, float)):
        tot = r[15]
        rows09.append([n, "Received income", round(r[11], 1), round(100 * r[11] / tot, 1)])
        rows09.append([n, "Worked as a volunteer", round(r[13], 1), round(100 * r[13] / tot, 1)])
craft = {x[1]: x[3] for x in rows09 if x[0] == "Craft"}
print("craft income/volunteer %:", craft)
write("09_income_volunteer.csv", ["activity", "measure", "participants_thousand", "pct_of_participants"], rows09)

# ---------- Table 10: children's hours ----------
t10 = sheet(T813, "Table 10")
BANDS = ["0–2", "3–4", "5–9", "10–19", "20+"]
rows10 = []
for idx, name in ((25, "Arts and crafts"), (29, "Screen-based activities"), (30, "Reading for pleasure")):
    cnt = {25: 13, 29: 17, 30: 18}[idx]
    assert str(t10[idx][0]).startswith(("Art and craft", "Screen", "Reading")) and str(t10[cnt][0]).startswith(("Art and craft", "Screen", "Reading"))
    for b, v, k in zip(BANDS, t10[idx][1:6], t10[cnt][1:6]):
        rows10.append([name, b, round(float(v), 1), round(float(k), 1)])
write("10_children_hours.csv", ["activity", "hours_per_week", "pct_of_children_doing_it", "children_thousand"], rows10)

# ---------- NAPS Table 13: impact statements ----------
t13 = sheet(NAPS, "Table 13")
hdr = [str(c).strip() for c in t13[4]]
print("NAPS T13 header:", [h for h in hdr if h != "None"][:6])
assert hdr[2].lower().startswith("man") and hdr[3].lower().startswith("woman"), hdr[:5]
rows11 = []
for r in t13[5:]:
    if r[0] and isinstance(r[1], float) and not str(r[0]).startswith(("Column", "Unweighted", "Weighted")):
        use = not any(k in str(r[0]).lower() for k in ("customer", "workforce"))
        rows11.append([str(r[0]).strip(), round(100 * r[2], 1), round(100 * r[3], 1), round(100 * (r[3] - r[2]), 1), round(100 * r[1], 1), str(use).lower()])
for x in rows11: print("  ", x)
write("11_naps_impact_by_sex.csv", ["statement", "men_pct", "women_pct", "gap_points", "all_pct", "use_in_radar"], rows11)
