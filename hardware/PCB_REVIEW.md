> **FABRICATION HOLD (2026-11-12):** R2.1 electrical DRC/ERC did not independently prove physical plug orientation. Read [PCB_ORIENTATION_GATE.md](PCB_ORIENTATION_GATE.md) and run `python hardware/source/check_orientation_contract.py` before any board order. LCD front-vs-solder-side mating, keypad ribbon, UPDI Friend header, TO-92 flat-face orientation and battery connector polarity remain unsigned physical checks. The existing Gerbers are NOT released for fabrication. The current board uses an MCP1700 LDO, not the later-discussed buck-boost regulator.

# PCB R2.1 review - November 2, 2026

**The PCB design review is complete for this prototype revision. This is not a bench-tested calculator.** Both boards pass KiCad 9.0.2 ERC, DRC and schematic parity with no exclusions. Firmware is still pending. Use the component/fit checks below before committing to fabrication or assembly; a small prototype run is the next hardware stage, not production release.

## What changed

| Finding | Resolution |
| --- | --- |
| All original schematic pins were passive, limiting ERC usefulness | MCU, regulator, switched supply, source connectors and LCD pins now have application-appropriate electrical types. Explicit VIN power flag documents supply through D1. |
| Local schematic labels had `/` prefixes while PCB nets did not | Global schematic labels now match actual PCB net names. Explicit isolated NC nets and mounting-hole symbols also satisfy native parity checks. |
| Pin/wire endpoints were off grid and project symbols had no matching library | Connections use the 1.27 mm grid. Both projects contain matching `MW.kicad_sym` and `sym-lib-table` files. |
| Power documents contradicted the selected physical slide switch | J2 is explicitly switched battery input. The CYT1107 stays case-mounted; JP1 is an internal service jumper. Switch wiring appears in the schematic and POWER_SWITCH.md. |
| Generic 3 x 1.6 mm ceramic bodies were smaller than the selected 2.2 uF leaded capacitors | Main C1/C2/C5 and adapter C1/C2 now specify TDK FG14X7R1H225KRT00 and a 4.5 x 3.0 mm body footprint. Pad pitch, pad copper and drills are retained. |
| Main regulator output had only nominal 1 uF, the minimum stated by its datasheet | Main C1/C2/C5 increased to 2.2 uF, 50 V X7R. Verify C2 retains at least 1 uF effective capacitance after tolerance, bias and temperature. Adapter flying caps remain 2.2 uF, now rated 50 V. |
| Connector annotation said eight wires | J3 uses seven connected wires and one unused position. Silkscreen and drawings now agree. |

The source refresh preserves all existing track/via geometry and connector/pad positions. Main board remains **82 x 68 mm**; LCD adapter remains **70 x 18 mm**. Both are **two-layer 1.6 mm FR-4 with plated through holes**. No switch hole or switch footprint was added to either PCB.

## Recorded validation

| Check | Main board | Display adapter |
| --- | ---: | ---: |
| Electrical-rule violations, including warnings | 0 | 0 |
| PCB design-rule violations, including warnings | 0 | 0 |
| Unconnected items | 0 | 0 |
| Schematic parity issues | 0 | 0 |
| Actual connected pads matched to schematic/source | 63 | 41 |
| Track segments matched to source | 438 | 227 |
| Vias matched to source | 8 | 1 |

Reports are in `validation/kicad_erc.*`, `kicad_drc.*`, `adapter_erc.*`, `adapter_drc.*` and `pcb_audit.json`. An intentionally merged battery/3.3 V rail in a **temporary copy** produces the expected power-output conflict; `erc_negative_check.json` records that check. No rule exclusions were used to obtain zero violations.

`audit_pcb.py` checks actual saved pad nets, drills, positions, footprint identities, routed segments, vias and outline dimensions against source records. It also checks critical pin assignments against an explicit reference map and reads the PCB mounting-hole coordinates from `build_case.py` without executing a CAD rebuild. The four holes match the case posts at plan (12,67), (84,67), (12,125), (84,125) mm. This is not a populated-component CAD collision simulation.

Schematic PDFs were rendered and visually inspected. Updated Gerbers, separate plated/non-plated drills, BOMs and ZIP packages were regenerated from the reviewed board files. The `r2` download filenames are retained so existing links continue to work; the fabrication instructions inside identify **R2.1**.

## Connections checked

- AVR128DA28 **28-pin SPDIP**: AVDD 14, VDD 20, ground 15/21, UPDI 19; PD7 13 controls LCD power. PA1-PA5 are pins 23-27. Do not substitute a 32-pin device or an ATmega328P.
- MCP1700 **TO-92**: 1 GND, 2 VIN, 3 VOUT. Do not substitute the SOT-23 pin order.
- onsemi 2N3906: 1 emitter to 3.3 V, 2 base via R1, 3 collector to LCD_VCC. R2 pulls its base to the emitter at reset. PD7 low turns the display on.
- D1: anode to VBAT_LINK, cathode/banded end to VIN.
- J2: pin 1 switched AAA positive, pin 2 ground. JP1 shunt normally fitted. J4: 1 regulated 3.3 V, 2 ground, 3 UPDI.
- Main J3 and adapter J1: match pins 1-7 directly, leave 8 unwired. The display's own 22-pin row is 1.27 mm pitch and solders directly to adapter J2.
- EastRising LCD supply pins 14/15, serial pins 12/13, control pins 1/2/3, interface straps 21/22 and flying-capacitor pin pairs were checked against the manufacturer's pin table. BM1 low selects SPI; BM0 and unused data/strobe lines are tied low. Separate A/K backlight contacts remain unconnected.

The signal assignments still use software SPI unless firmware explicitly verifies a suitable peripheral route. The printed flexible keypad is mechanical only; retain the existing electrical membrane and establish its ribbon ordering with a scan/continuity test.

## Parts and fit checks before fabrication/assembly

1. Use the two selected EastRising ERC12864FS-655 modules purchased on eBay; confirm the received part and pin-1 orientation against the front-view drawing and `docs/display_fit_template.pdf`. Pin diameter/reach and solder fit have not been physically tested.
2. The five specified TDK 2.2 uF capacitors have a 4.5 mm maximum body length, 3.0 mm thickness, 5.5 mm body height and nominal 2.5 mm lead spacing. Their body envelope is now reserved. The manufacturer's lead-gap tolerance is +/-0.8 mm; adjust leads gently to the board pitch without loading the encapsulation. Include any formed-lead standoff in the installed height.
3. Adapter board top is nominal Z=14.6 mm; the rear LCD frame begins at Z=22.1 mm, leaving 7.5 mm for parts and clearance. A 5.5 mm capacitor body leaves **2.0 mm nominal** before lead standoff. Keep installed height at most **7.0 mm**, including leads, for 0.5 mm clearance. This arithmetic does not validate a physical assembly. Other adapter components must also fit this space.
4. Remaining ceramic footprints (main C3/C4, adapter C3/C4) are generic 3.0 x 1.6 mm bodies at 2.5 mm pitch. Select matching parts or revise these footprints **before ordering**; lead pitch alone is not a sufficient fit check. Adapter C3 must be at least 25 V because it is on VLCD. Adapter C5 must fit the 4 mm-diameter, 1.5 mm-pitch footprint and maximum 7 mm installed height. Confirm the exact socket, headers, diode and transistor/regulator packages as well.
5. The CYT1107 is wired, not board-mounted. Confirm its common terminal and fit in the existing cradle. Battery positive goes to common, one outer goes to J2.1, unused outer is insulated. Do not wire a switch across J2.1/J2.2. The physical switch disconnects the battery; a connected powered programmer can still power the board.
6. Check the existing keypad against its 100% template and test a printed key coupon. This electrical revision does not rebuild or qualify the prior mechanical STLs. The separate connected-keypad export/fit caveats in hardware/README.md still apply.

## Prototype bring-up

1. With no cells/programmer, inspect soldering and check polarity/shorts. Fit JP1. Leave the MCU and display disconnected for initial power checks.
2. Feed main J2 from a current-limited bench source emulating three alkaline AAA cells. Verify VIN and regulated 3.3 V, correct polarity and no abnormal current/heating. Never feed the raw pack into the LCD.
3. Fit/program the AVR with a 3 V UPDI tool. Remove cells before programmer-powered use. Confirm PD7 high/off and low/on operation and measure LCD_VCC at both boards. Initial display charge-pump inrush and settling are unmeasured.
4. Start LCD software SPI slowly, display a border/corner test, then verify all keys and sleep/wake. Keep LCD signals low before switching its supply off. Check that no signal backfeeds the unpowered panel.
5. Implement the calculator firmware and its brownout/clock settings before normal use. Verify matrix wake behavior on the assigned AVR port pins rather than assuming every interrupt mode wakes from every sleep state. Hard OFF loses RAM state.
6. Measure active/sleep current and operation over the usable battery range. The series diode plus 3.3 V LDO means some cell capacity is unusable at dropout. Readability, runtime and low-battery behavior are not established by these checks.

## Reproduce the electrical review

Use Python with KiCad 9 `pcbnew` bindings for refresh/audit/plot/export, and Python with `pypdf` and `reportlab` for packaging. For example, on the reviewed Linux environment:

```bash
/usr/bin/python3 hardware/source/refresh_schematics.py
/usr/bin/python3 hardware/source/export_pcbs.py
/usr/bin/python3 hardware/source/audit_pcb.py
python hardware/source/validate_display.py
/usr/bin/python3 hardware/source/plot_copper.py
DISPLAY_ADAPTER=1 /usr/bin/python3 hardware/source/plot_copper.py
python hardware/source/finish_exports.py
```

The original routing generators build a new layout from scratch; do not confuse that with refreshing the reviewed layout. Re-run all checks if copper, footprints, parts or the enclosure change. Kept track widths are 0.4 mm, minimum clearance 0.25 mm, vias 1.0 mm with 0.5 mm drills.

## References checked during this review

- [Microchip AVR128DA28/32/48/64(S), DS40002183E](https://www.microchip.com/content/dam/mchp/documents/MCU08/ProductDocuments/DataSheets/AVR128DA28-32-48-64-Data-Sheet-DS40002183.pdf): 28-pin SPDIP pinout, page 14.
- [Microchip MCP1700, DS20001826F](https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/MCP1700-Data-Sheet-20001826F.pdf): TO-92 pin table and minimum output capacitor.
- [onsemi 2N3906](https://www.onsemi.com/pdf/datasheet/2n3906-d.pdf): E-B-C pinout.
- [TDK FG14X7R1H225KRT00](https://product.tdk.com/en/search/capacitor/ceramic/lead-mlcc/info?part_no=FG14X7R1H225KRT00): capacitor value, voltage, dimensions and lead spacing.
- [EastRising product](https://www.buydisplay.com/2-8-inch-128x64-graphic-module-serial-display-spi-lcd-w-optl-touch-screen) and [manufacturer datasheet hosted by ICBanQ](https://www.icbanq.com/icdownload/data/ICBShop/Board/ERC12864-655_Series_Datasheet.pdf): mechanical envelope, pin table, supply limits and SPI straps.

The manufacturer's separate SPI reference PDF returned HTTP 403 during this review. Its capacitor topology/values documented in the existing DISPLAY_INTEGRATION.md were retained; that document was not independently re-downloaded this time. The manufacturer datasheet pin table was accessible. ERC verifies connectivity/type rules, not charge-pump operation, contrast or transient stability; those remain bench tests.
