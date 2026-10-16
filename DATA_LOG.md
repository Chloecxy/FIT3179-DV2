# Data log – "Made by hand" (FIT3179 Data Visualisation 2)

All CSVs in `data/` are produced by `scripts/build_data.py` from the original spreadsheets. Re-run it if a source changes.
Craft-shop data comes from OpenStreetMap via `scripts/clean_osm.py`.

| File | Chart | Source (table, columns) | What was calculated |
|---|---|---|---|
| 01_craft_rate_by_sex.csv | 1 Waffle | ABS 2021–22, Table 4, craft rate, Total column | none (published rates) |
| 02_activity_participants.csv | 2 Lollipop | ABS Table 4, persons counts, Total column | rate = count ÷ 20,390k adults |
| 03_craft_rate_by_age_sex.csv | 3 Butterfly | ABS Table 4, craft rate by age, males and females | none |
| 04_activity_age_ranks.csv | 4 Bump | ABS Table 4, persons counts by age ÷ total persons by age | rate per age group, then rank 1–11 |
| 05_state_participation_rate.csv | 5 Choropleth | ABS Table 1, persons, total participants rate | none |
| 06_state_sex_symbols.csv | 6 Symbols | ABS Table 1 (rate by sex); ABS Table 3 (activity types) | depth = (3 types + 4 or more) ÷ participants; capital coordinates typed in |
| 07_craft_shops.csv | 7 Dot map | OpenStreetMap, shop = craft, fabric, wool, haberdashery, sewing | duplicates removed; two display groups |
| 08_activity_hours.csv | 8 Heatmap | ABS Table 7 | % of participants; cross-checked with ABS's own percentages |
| 09_income_volunteer.csv | 9 Stacked bar and 12 Connected dots (all 11 activities) | ABS Table 5, persons columns | % of participants |
| 10_children_hours.csv | 10 Connected dots | ABS Table 10 (children 5–14) | none (published % and counts) |
| 11_naps_impact_by_sex.csv | 11 Radar | NAPS 2022, Table 13, "Man or male" and "Woman or female" | gap = women − men; `use_in_radar` = false for the two economic statements |

## Checks run
- Craft: 3,099.7k people (15.2%); women 22.9%, men 7.1%.
- Craft income 3.1%, volunteered 8.6% – both match ABS's own percentages.
- Table 7 percentages match ABS's own; the four columns cover 98–102% of participants (rounding in the source).
- NAPS statements: women higher than men on all 10.

## Caveats to state on the page
- State maps (charts 5, 6) cover participation in **all** cultural and creative activities, not craft alone.
- People do several activities, so activity counts overlap and must not be added up.
- NT numbers come from a small sample; margins of error are large.
- Table 1 and Table 3 differ slightly (up to about 1 point): rates come from Table 1, depth from Table 3.
- NAPS combines visual arts and craft in one category.
- OpenStreetMap is volunteer-mapped, so the shop map shows mapped shops, not necessarily every shop.
- Top shop names in the file: Spotlight 98, Kaisercraft 20, Lincraft 18 (136 of 493, 28%).

## Credits
- ABS, *Cultural and creative activities, 2021–22* (Tables 1, 3, 4, 5, 7, 10).
- Creative Australia, *National Arts Participation Survey 2022* (check whether to switch to the 2025 results).
- © OpenStreetMap contributors (ODbL), downloaded <ADD DATE>.
- State boundaries: <ADD SOURCE>.

## Figures on the page that are my own calculations
- "About half of the shops are within 50 km of a state capital": straight-line distance from each OpenStreetMap shop to the nearest of the eight state capitals; 25 km = 41%, 50 km = 52%, 100 km = 61%.
- "Spotlight, Kaisercraft and Lincraft = 136 of 493 (28%)": counts of shop names in `data/07_craft_shops.csv`.
- "3+ kinds of activity, % of participants" (chart 6): (3 types + 4 or more) / (all adults − adults with no activity), ABS Table 3.
- Rank of activities (chart 4): participants / all adults in the age group, ABS Table 4.
