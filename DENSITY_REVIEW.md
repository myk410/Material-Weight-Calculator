# Company density verification

Updated October 27, 2026. The original values came from the company card. At the user’s direction, the calculator now uses published material densities instead. The old card values are retained below only for comparison and are not used by any calculator preset.

Density depends on composition and temperature. The menu now identifies specific grades, with separate choices for LDPE/HDPE, 304/316 stainless, alloys 718/625, and CuNi 90/10 or 70/30. These are explicit material choices, not a claim about which grades the company stocks. Published values are nominal material properties; actual stock may vary. Extra conversion digits do not imply greater precision than the source.

## Active calculator presets

| Preset | Density (lb/ft³, rounded for display) | Published source value | Source |
| --- | ---: | --- | --- |
| Polyethylene — LDPE (0.920 g/cm³) | 57.434 | 0.920 g/cm³ | [1] |
| Polyethylene — HDPE (0.950 g/cm³) | 59.307 | 0.950 g/cm³ | [1] |
| Fresh water (4°C / 39.2°F) | 62.424 | 62.424 lb/ft³ | [2] |
| Aluminum 6061 | 169.344 | 0.098 lb/in³ | [3] |
| Titanium — commercially pure Grade 2 | 281.664 | 0.163 lb/in³ | [4] |
| Carbon steel (7,850 kg/m³) | 490.059 | 7,850 kg/m³ | [5] |
| Stainless steel 304 | 492.480 | 0.285 lb/in³ | [6] |
| Stainless steel 316 | 499.392 | 0.289 lb/in³ | [7] |
| Nickel alloy 718 (Inconel 718) | 511.488 | 0.296 lb/in³ | [8] |
| Nickel alloy 625 (Inconel 625) | 527.040 | 0.305 lb/in³ | [9] |
| Brass — C26000 | 532.224 | 0.308 lb/in³ | [10] |
| CuNi 90/10 — C70600 | 558.144 | 0.323 lb/in³ | [11] |
| CuNi 70/30 — C71500 | 558.144 | 0.323 lb/in³ | [12] |
| NiCu — Monel 400 | 549.504 | 0.318 lb/in³ | [13] |
| Lead | 706.752 | 0.409 lb/in³ | [14] |

## Comparison

All comparison values are in lb/ft³. Conversions use `lb/in³ × 1728` or `kg/m³ ÷ 16.01846337`; figures below are rounded for readability.

| Material | Company value | Published example | Assessment |
| --- | ---: | --- | --- |
| Poly | 57 | LDPE at 0.920 g/cm³ ≈ 57.43; supplier HDPE examples at 0.946–0.960 g/cm³ ≈ 59.06–59.93 [1] | Consistent with some LDPE. Identify the polymer; “Poly” alone does not identify polyethylene, polypropylene, or grade. |
| Water | 62 | Fresh water ≈ 62.4 near its maximum density [2] | Reasonable rounded estimate; temperature and dissolved material affect density. |
| Aluminum | 168 | 6061: 0.098 lb/in³ ≈ 169.34 in the cited supplier table [3] | Close rounded estimating value (about 0.8% below this already-rounded example); exact alloy matters. |
| Titanium | 168 | ATI commercially pure Grade 2: 0.163 lb/in³ ≈ 281.66 [4] | Does not match Grade 2 titanium: about 40.4% below that example. The supplied entry duplicates aluminum; the user directed replacement with the published Grade 2 value. |
| Steel | 490 | SSAB steel plate: 7,850 kg/m³ ≈ 490.06 [5] | Matches typical carbon-steel estimating density very closely. |
| Stainless | 504 | Outokumpu 304: 0.285 lb/in³ ≈ 492.48; 316: 0.289 lb/in³ ≈ 499.39 [6, 7] | About 2.3% / 0.9% above those examples. Reasonable broad estimating factor, but exact verification requires the grade. |
| Inconel | 516 | Alloy 718: 0.296 lb/in³ ≈ 511.49; alloy 625: 0.305 lb/in³ ≈ 527.04 [8, 9] | About 0.9% above 718 or 2.1% below 625. Alloy-specific rather than a universal Inconel density. |
| Brass | 528 | CDA C26000: 0.308 lb/in³ ≈ 532.22 [10] | About 0.8% below this example. Close estimating value; exact alloy required. |
| CuNi | 576 | CDA C70600 and C71500: 0.323 lb/in³ ≈ 558.14 in both cited entries [11, 12] | About 3.2% above these examples. Cannot verify 576 for an unspecified company alloy. |
| NiCu | 576 | Monel 400 example: 0.318 lb/in³ ≈ 549.50 [13] | About 4.8% above this example. NiCu does not uniquely identify Monel 400; confirm alloy and company factor. |
| Lead | 710 | Lead supplier: 0.409 lb/in³ ≈ 706.75 [14] | About 0.5% above this rounded example; close estimating value. |

The largest mismatch is titanium. These historical comparisons explain the change; all active defaults now come from the published sources above.

## Original plate-weight column

The original `LBS/1"/ft²` column represents the weight of one square foot of plate, one inch thick. Its exact relationship to volumetric density is `lb/ft³ ÷ 12`.

| Material | Supplied plate factor | Derived from supplied lb/ft³ |
| --- | ---: | ---: |
| Poly | 5 | 4.750 |
| Water | — | 5.167 |
| Aluminum | 14 | 14.000 |
| Titanium | 14 | 14.000 |
| Steel | 41 | 40.833 |
| Stainless | 42 | 42.000 |
| Inconel | 43 | 43.000 |
| Brass | 44 | 44.000 |
| CuNi | 48 | 48.000 |
| NiCu | 48 | 48.000 |
| Lead | 59 | 59.167 |

These columns are consistent with whole-pound rounding. In particular, 5 lb for Poly is a rounded plate factor, not an exact substitute for 57 lb/ft³. The calculator now uses the published grade-specific densities consistently for every shape; neither card column drives calculations.

The original liquid notes were water 8.3 lb/US gal, gasoline 6 lb/US gal, and oil 7.5 lb/US gal. The water note is consistent with the rounded water density. The gasoline and oil notes are approximate factors for unspecified liquids, not independently verified specifications; composition and temperature are needed. These liquid notes are not calculation presets.

## Calculator behavior

- Published grade-specific presets replace the company card values. Select the grade matching the stock.
- Each material displays its source density and grade note. Expand **Density / override** to enter another known density in lb/ft³, or select Custom material.
- An override lasts until another material is selected or the page is reloaded. Results distinguish a published preset from an override. Both apply identically to every shape.
- The calculator now accepts solid rectangular stock, pipe/round tube, or known volume.
- Pipe inputs are length, actual outside diameter, and either wall thickness or inside diameter, all in decimal inches. Nominal pipe size is not the outside diameter; schedule lookup is not implemented.
- For outside diameter D, wall thickness t, and length L, `volume_in3 = π × t × (D − t) × L`.
- For outside diameter D and inside diameter d, `volume_in3 = π/4 × (D − d) × (D + d) × L`.
- Both are equivalent to outer cylinder volume minus inner cylinder volume. Pipe must have `0 < t < D/2` or `0 < d < D` and positive length. Use rectangular/known-volume mode for solid stock.
- `weight_lb = volume_in3 × density_lb_per_ft3 / 1728`. Pipe results cover the wall material only, excluding contents, fittings, weld buildup, insulation, and coatings.

Example: a steel tube with 2-inch actual OD, 0.125-inch wall, and 12-inch length has 8.835729338 in³ of wall material. At the published steel density of 7,850 kg/m³ (about 490.059 lb/ft³), its estimated weight is **2.505806 lb**, displayed as **2.51 lb**. Entering 1.75-inch ID instead gives the same result.

## Sources

1. [Stewart Polymer Solutions — resin grades and densities](https://stewartpolymersolutions.com/products/).
2. [USGS — Water Density](https://www.usgs.gov/water-science-school/science/water-density).
3. [thyssenkrupp Aerospace — aluminum alloy density offerings](https://www.thyssenkrupp-aerospace.com/en/materials/aluminium-plate/alloy-density-offerings).
4. [ATI — commercially pure titanium datasheet](https://www.atimaterials.com/Products/Documents/datasheets/titanium/commerciallypure/ati_cp2_tds_en.pdf).
5. [SSAB — hot-rolled steel plate environmental product declaration](https://www.ssab.com/-/media/files/en/support/certificates/885en-epd-hot-rolled-steel-plates.pdf?m=20200406080301).
6. [Outokumpu — Core range datasheet](https://www.outokumpu.com/en/products/product-ranges/-/media/files/products/core/outokumpu-core-range-datasheet.pdf).
7. [Outokumpu — Supra range datasheet](https://www.outokumpu.com/en/products/product-ranges/-/media/files/products/supra/outokumpu-supra-range-datasheet.pdf).
8. [ATI — alloy 718](https://www.atimaterials.com/Products/ati-718).
9. [Fort Wayne Metals — Inconel alloy 625](https://fwmetals.com/what-we-do/materials/high-performance-alloys/inconel-alloy-625).
10. [Copper Development Association — C26000](https://alloys.copper.org/alloy/C26000).
11. [Copper Development Association — C70600](https://alloys.copper.org/alloy/C70600).
12. [Copper Development Association — C71500](https://alloys.copper.org/alloy/C71500).
13. [Castle Metals — nickel alloys, Monel 400 properties](https://www.castlemetals.com/metals/nickel/c/nickel).
14. [Non-Ferrous Metals — lead properties](https://nfmetals.com/metals/).
