// Embeds every Vega-Lite chart. Each chart's JSON lives in vega/ and its data in data/ and geo/.
const CHARTS = [
  ["vis01", "vega/01_waffle.vg.json"],
  ["vis02", "vega/02_lollipop.vg.json"],
  ["vis0304", "vega/0304_linked_age.vg.json"],
  ["vis05", "vega/05_choropleth.vg.json"],
  ["vis06", "vega/06_symbols_by_sex.vg.json"],
  ["vis14", "vega/14_shops_linked.vg.json"],
  ["vis08", "vega/08_heatmap.vg.json"],
  ["vis09", "vega/09_stacked_bar.vg.json"],
  ["vis13", "vega/13_income_volunteer_dots.vg.json"],
  ["vis10", "vega/10_connected_dots.vg.json"],
  ["vis11", "vega/11_radar.vg.json"],
];

// Wait for the web fonts so Vega measures text with the real font, then draw the charts.
const fontsReady = document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve();

Promise.all([fetch("vega/config.json").then(r => r.json()), fontsReady]).then(([config]) => {
  CHARTS.forEach(([id, url]) => {
    vegaEmbed("#" + id, url, {
      config: config,
      renderer: "svg",
      actions: false
    }).catch(error => {
      console.error("Chart failed:", url, error);
      document.getElementById(id).innerHTML = "<p>Sorry, this chart could not be loaded.</p>";
    });
  });
});
