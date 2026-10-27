# Made by Hand: Who Crafts in Australia

FIT3179 Data Visualisation 2 - Chloe Chan Xin Yi

**Live story:** <https://chloecxy.github.io/FIT3179-DV2/>

A single-page data story about craft in Australia: how many people take part, who they are, where they live, how they buy supplies, why craft stays a hobby and what the next generation is doing.

The page is a static site built with HTML, CSS and JavaScript. The published page was last dated 27 October 2026.

## Story structure

1. **How Big Is The Craft World?** - 3.1 million adults did craft in 2021-22, or 15 in every 100. The gender gap is wide: 23 in 100 women and 7 in 100 men.
2. **Who Crafts?** - Women's participation is more than double men's in every age group. The activities people rank first also change with age: painting and drawing lead under 35, while craft takes first place from 35 onwards.
3. **Creativity Across the States** - A state choropleth and paired Men/Women symbol maps show participation and the breadth of creative activity. A linked shop map then locates 493 craft, fabric and wool shops from OpenStreetMap. Three chains account for 140 of them (28%).
4. **A Hobby, Not A Hustle** - Most crafters spend under 10 hours a week on craft (84%), and only 3.1% earn money from it. A dumbbell chart compares income and volunteering across 11 creative activities.
5. **The Next Generation And Why It Matters** - Children's craft hours are compared with screen-based activity, followed by a radar chart of the eight impacts reported in Creative Australia's National Arts Participation Survey.
6. **So What?** - A closing argument that craft is common, casual, mostly done by women, and usually done for love rather than money.

## Sources

- **Australian Bureau of Statistics**, [Cultural and creative activities, 2021-22](https://www.abs.gov.au/statistics/people/people-and-communities/cultural-and-creative-activities/2021-22), Tables 1, 3, 4, 5, 7 and 10. Used for participation by sex, age and state; breadth of activity; income and volunteering; hours spent; and children aged 5-14.
- **Creative Australia**, [National Arts Participation Survey 2022](https://creative.gov.au/), Table 13. Used for the eight impact measures by sex.
- **OpenStreetMap contributors**, [ODbL licence](https://www.openstreetmap.org/copyright). Used for craft, fabric, wool, haberdashery and sewing shops extracted through the Overpass API.
- **Natural Earth**, [naturalearthdata.com](https://www.naturalearthdata.com/). Used for Australian state boundaries, simplified with mapshaper.

The shop map is a fixed OpenStreetMap extraction, not a live retail census. The published count is 493 shops.

## Interpretation notes

- Northern Territory estimates come from a small sample and should be read with care.
- The radar chart shows shares within each sex, not headcounts; a larger shape means a higher reported rate, not more people.
- The "about half of shops are within 50 km of a state capital" statement is a straight-line calculation from shop and capital coordinates.
- Chain counts treat location-suffixed branches as part of the named chain. Spotlight, Kaisercraft and Lincraft together account for 140 of the 493 shops (28%).
- `vis06` uses fixed label coordinates for its 500 x 400 conicEqualArea maps. Changing the projection requires repositioning the state abbreviations.

## Project layout

- `index.html` - page structure, story copy, key-fact band and source footer.
- `css/styles.css` - layout, typography, colour system, chart sizing and responsive rules.
- `js/main.js` - chart registry, font-ready embedding, error handling and shop-map zoom reset.
- `vega/` - 10 Vega-Lite specifications plus the shared `config.json` theme.
- `data/` - tidy CSVs, one per chart or source table.
- `geo/` - Australian state boundaries as a TopoJSON file.
- `scripts/` - reference scripts for rebuilding the derived data.

