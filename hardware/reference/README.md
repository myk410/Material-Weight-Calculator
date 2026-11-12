# Manufacturer references used for R3

Retrieved 2026-11-12. These are manufacturer-authored documents; their authors retain all rights. Document byte hashes are included in the R3 review manifest.

| Saved document | Source and review focus |
| --- | --- |
| [LTC3440_3440fd.pdf](LTC3440_3440fd.pdf) | [Analog Devices original](https://www.analog.com/media/en/technical-documentation/data-sheets/3440fd.pdf), 22 pages: p1 application, p2 MSOP top-view pinout, p12 layout, p13 input above 4.5 V, p14 compensation, p20 MS drawing |
| [Sumida_CDRH6D38.pdf](Sumida_CDRH6D38.pdf) | [Sumida original](https://products.sumida.com/products/pdf/CDRH6D38.pdf), 4 pages, 2017 revision: p1 7 mm maximum body / 4 mm maximum height / land pattern, p2 10 µH rating. [Current series page](https://products.sumida.com/ProductsInfo/ProductGuide/PowerInductors/TypeDetail.php?type=CDRH6D38) also reviewed. |

Additional manufacturer references reviewed online:

- [Nexperia PMEG2010ER](https://assets.nexperia.com/documents/data-sheet/PMEG2010ER.pdf): p2 pin 1 cathode, pin 2 anode, marking bar; CFP3/SOD123W package. The direct local download returned HTML, so it was not saved as a false PDF.
- [Murata COUT product sheet](https://www.murata.com/en-global/api/pdfdownloadapi?cate=luCeramicCapacitorsSMD&partno=GRM32ER71E226KE15%23) and [SimSurfing](https://ds.murata.com/simsurfing/mlcc.html): GRM32ER71E226KE15L, 22 µF 25 V X7R, 1210. Dynamic DC-bias curve qualification remains open; do not infer effective capacitance from nominal rating.
- [Murata CIN product sheet](https://www.murata.com/en-global/api/pdfdownloadapi?cate=luCeramicCapacitorsSMD&partno=GRM31CR71E106KA12%23): selected GRM31CR71E106KA12L, 10 µF 25 V X7R, 1206. Direct download returned HTML; not bundled. Verify exact current part specification and effective capacitance before release.
- [Microchip AVR128DA datasheet](https://www.microchip.com/content/dam/mchp/documents/MCU08/ProductDocuments/DataSheets/AVR128DA28-32-48-64-Data-Sheet-DS40002183.pdf), 28-pin SPDIP pin map, already documented by R2 audit.
- [onsemi 2N3906](https://www.onsemi.com/pdf/datasheet/2n3906-d.pdf), retained TO-92 EBC part; actual vendor identification remains a physical gate.
- [EastRising series datasheet](https://www.buydisplay.com/download/manual/ERC12864-655_Series_Datasheet.pdf) and [manufacturer-authored hosted copy](https://www.icbanq.com/icdownload/data/ICBShop/Board/ERC12864-655_Series_Datasheet.pdf), pp7–9: existing adapter numbering, dimensions and operating limits. Actual module mating direction remains a physical gate.

Bundled KiCad standard footprints retain the project's [footprint license](../pcb/FOOTPRINT_LICENSE.txt). The custom Sumida footprint is derived from the manufacturer's dimensions with explicitly documented outer toe extensions, not a new manufacturer-recommended land pattern.
