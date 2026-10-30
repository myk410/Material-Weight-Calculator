# Material Weight Calculator — hardware R2

This package contains real parametric CAD, printable STLs, a routed KiCad PCB, schematic, Gerbers, drills, and actual-scale print templates. It is a **prototype design**, not a physically tested or production-qualified assembly. The device firmware is not included in this hardware release; its revised 128 × 64 display and sleep requirements are specified in DISPLAY_INTEGRATION.md. R2 replaces the small Sharp display. R1 files remain in Git history, not in current print/download folders.

Download [complete R2 package](downloads/material_weight_calculator_hardware_r2.zip) or [both PCB fabrication sets](downloads/pcb_fabrication_r2.zip).

## Start here

1. Open `docs/case_front_preview.png` to inspect the actual CAD and recessed legends.
2. Print `docs/keypad_fit_template.pdf` at **100% / Actual Size**. Place the existing DIYmalls pad over the key-center marks. The screenshot identifies the pad type but does not establish its exact pitch. The model currently uses nominal 18 mm key pitch; confirm this fit before printing the full shell. The source has explicit `KEY_X` and `KEY_Y` parameters if the actual pad differs.
3. Print the two-key connected 55A keypad coupon before the full keypad sheet. Check legend detail, independent motion, return, actuator contact, nut fit, and actuation with the actual DIYmalls membrane. No claim is made that the 55A resin's force, shrinkage, or long-term fatigue has been physically validated yet.
4. For the Mars 5 Ultra, use the shell sections in `stl/mars5_ultra_oriented/`. They have been rotated to fit the manufacturer's 153.36 × 77.76 × 165 mm build volume; add supports and a raft in the slicer without exceeding that volume. These are unsliced STLs, not exposure profiles.
5. Use `pcb/gerbers/` for a conventional **two-layer, 1.6 mm copper-clad PCB with plated through holes**. Open the KiCad project to inspect/edit it before ordering.

## Files

| Location | Contents |
| --- | --- |
| `stl/` | Four case sections, battery cover, keypad plates, display cradle, **one-piece 55A flexible keypad sheet**, and fit coupons |
| `stl/mars5_ultra_oriented/` | Printer-fitting orientations for the shell sections and larger keypad plates |
| `cad/calculator_assembly.step` | Assembly with parts in their assembled locations; split case sections included |
| `cad/pcb_outline.step` | Board outline and four mounting holes, matching the enclosure |
| `cad/*whole_reference.stl` | Unsplit shell references for a larger printer; do not use these on the Mars 5 Ultra |
| `source/build_case.py` | Editable CadQuery source for case, one-piece keypad sheet, nut pockets, and split shells |
| `pcb/material_weight_calculator.kicad_pro` | KiCad 7 project |
| `pcb/material_weight_calculator.kicad_sch` | Editable, embedded-symbol schematic with every used pin/net explicitly named |
| `pcb/material_weight_calculator.kicad_pcb` | Routed two-layer board, 82 × 68 mm |
| `pcb/mw-footprints.pretty/` | Bundled standard footprints; project does not depend on an external footprint-library path |
| `pcb/gerbers/` | Top/bottom copper and masks, top silkscreen, outline, separate plated/non-plated Excellon drills and SVG drill maps |
| `docs/copper_artwork_1to1.pdf` | Exact KiCad copper plots: top reference, top transfer, bottom reference, bottom transfer |
| `docs/drill_template.pdf` | Component-side drill and board outline template |
| `docs/keypad_fit_template.pdf` | Full-scale membrane alignment template and 100 mm scale check |
| `docs/schematic.pdf` | Circuit drawing exported by KiCad |
| `pcb/bom.csv` | Main-board BOM |
| `pcb/display_adapter/` | Second KiCad project, schematic, routed 70 × 18 mm adapter and BOM |
| `docs/display_adapter_schematic.pdf` | Adapter circuit, exported by KiCad |
| `docs/display_adapter_copper_1to1.pdf` | Four actual-scale copper reference/transfer pages |
| `docs/display_adapter_drill.pdf` | Adapter drill/outline template at actual size |
| `docs/display_fit_template.pdf` | Full-scale 70 × 50 mm module and pin-center alignment check |
| `DISPLAY_INTEGRATION.md` | Authoritative R2 display pin map, sources and firmware requirements |
| `validation/` | CAD, mesh, schematic-net and KiCad design-rule reports |

The STLs are in millimeters, not mirrored. Each individual file is translated to its own positive bounding box. Use STEP for assembly positions. The old loose-button aggregate `all_16_buttons.stl` is obsolete; rebuilding the current source deletes it and exports `keypad_sheet_55A.stl` instead. No support structures are baked into the meshes.

## One-piece 55A keypad

The custom visible keypad is now **one connected flexible-resin part**, not sixteen loose buttons. The CAD nominally uses a 72 × 72 × 0.85 mm continuous sheet behind the 4 × 4 button field. Each key has a 14 × 14 mm top rising about 5 mm above that sheet, plus a centered smooth 8 mm-diameter actuator projecting about 1.55 mm below it.

The thin sheet is the flex zone. The thicker key tops remain individual islands geometrically, but they are permanently joined by the 0.85 mm membrane. This should reduce assembly parts, keep the key field aligned, and provide a continuous dust barrier over the original electrical membrane. The dimensions are prototype targets and should be tuned after the first real 55A print.

The existing DIYmalls 4 × 4 pad remains the **electrical switch layer** underneath. The printed 55A part is only the custom mechanical keypad. Do not assume the printed resin is conductive.

## Case and fasteners

Overall body: 96 × 184 × 31 mm, with button tops at about 33 mm. Wall/face thickness is generally 2.6 mm, with internal reinforcement webs. The PCB's lower face is 7 mm from the rear reference plane. The holder pocket targets a Pololu 1144-style 52 × 37 × 13 mm three-AAA holder with leads, allowing clearance around that envelope.

All fastening provisions are **M2.5 with hex nuts**, as requested. Nominal nut pockets are 5.35 mm across flats and about 2.45 mm deep; clearance holes are 2.9 mm. Glue nuts around their outside faces, keeping threads and screw paths clean. On front-facing pocket openings, hold the nut flush to the pocket's open face while the adhesive sets, rather than pushing it deeper into the clearance allowance. Verify actual nut dimensions with the coupon before gluing the full set.

| Joint | Screws | Nuts |
| --- | --- | --- |
| Rear to front shell | 4 × M2.5 × 16 mm | 4, glued into front-shell pockets |
| PCB to rear posts | 4 × M2.5 × 6 mm | 4, glued into rear-post pockets |
| Keypad backing + guide stack to front | 4 × M2.5 × 6 mm | 4, glued into front pockets |
| Display cradle to front | 4 × M2.5 × 6 mm | 4, glued into front pockets |
| Battery cover | 2 × M2.5 × 6 mm | 2, glued into rear pockets |

Total: **18 nuts; four 16 mm and fourteen 6 mm screws**. Screw lengths are measured under the head. Trial-fit and shorten any screw that bottoms before clamping; do not force a screw into resin. The design does not use heat-set inserts or self-tapping threads.

The long front and rear shells each have an upper/lower **bonded seam** at plan Y=60.25 mm, with locating tongues and mating relief. Bond each upper/lower pair into one shell before final assembly. This printing seam is separate from the removable, screwed front/rear joint. Use an adhesive appropriate for the fully cured rigid resin and test it on a coupon. One-piece references are included if a larger printer is available.

## Assembly order

1. Wash/cure the printed parts according to the actual resin's instructions. Clear supports from recesses and mating faces. Bond the two front sections and the two rear sections using their locating features.
2. Test-fit and glue the M2.5 nuts into their pockets. Allow adhesive to set before applying screw load.
3. From inside the front, place the **single connected 55A keypad sheet** behind all sixteen bezel openings at once. Align its sixteen button tops with the openings. The 0.85 mm connecting membrane remains behind the bezel and keeps the entire keypad registered as one piece. Legends are actual 0.4 mm Boolean recesses, not rendered textures.
4. Install the rigid guide/backing stack and the existing DIYmalls electrical membrane underneath the printed keypad. The guide acts as registration and a travel-stop layer while the thin printed sheet provides key return. The current actuator projection and rest/stop values are prototype geometry only; verify that the electrical pad is not preloaded at rest and that each key returns without dragging its neighbors.
5. Route the electrical membrane's flexible ribbon through the backing relief; avoid sharp folds or pinching at the enclosure edge. The backing's screw slots allow small translational adjustments, not arbitrary correction of key pitch.
6. Use the ERC12864FS-655 **without touch panel**. Its body fits at plan (13,7.5), 70 × 50 × 5.8 mm maximum. The 67 × 37 mm bezel opening follows the drawing's viewing-area offset: 1.5 mm from the left and 3.5 mm from the top. Place thin 0.5 mm closed-cell foam on opaque perimeter/frame surfaces, between the front shell and module and between the module's backlight frame and rear cradle. Fit the cradle with four M2.5 × 6 mm screws. Tighten only enough to retain it; do not compress LCD glass, the polarizer or the solder tail. No separate printed edge clamps are used in R2.
   Assemble the display adapter before installing the cradle. J2 is a **1×22 row at 1.27 mm pitch**, not 2.54 mm. Solder the module's own pins directly into the adapter holes; do not add another tall header/socket. Keep the adapter at nominal Z=13 to 14.6 mm behind the top tail. Check pin-1 orientation against the manufacturer's front-view drawing. Use short insulated wires at adapter J1 rather than a tall plug. Secure the cable to the cradle side with a soft tie/adhesive anchor, without loading the glass. Capacitor C5 must be ≤4 mm diameter and ≤7 mm high; other adapter parts ≤5 mm high. Confirm actual pin reach before soldering; the fit template provides the 22 pin centers.
7. Assemble the PCB, check power rails with U1/display disconnected, fit the socketed MCU, then connect the keypad, display cable, and battery holder using the wiring below.
8. Install the PCB in the rear tray, secure the battery holder in its pocket, and route leads clear of nut pockets and ribs. Install the battery cover, then join front/rear with the four longer screws.

## PCB circuit and parts

| Ref | Part / function | Quantity |
| --- | --- | ---: |
| U1 | AVR128DA28-I/SP, in 28-pin narrow DIP socket (7.62 mm row spacing) | 1 + socket |
| U2 | MCP1700-3302E/TO, 3.3 V LDO; spread-lead TO-92 footprint | 1 |
| D1 | 1N5817, DO-41, battery reverse-polarity protection | 1 |
| Q1 | onsemi 2N3906 PNP, E-B-C pins 1-2-3, TO-92 spread leads; switches display power | 1 |
| R1 | 10 kΩ, axial, 7.62 mm lead spacing | 1 |
| R2 | 100 kΩ, axial, 7.62 mm lead spacing | 1 |
| C1, C2, C5 | 1 µF, at least 10 V, ceramic, 2.5 mm lead spacing; body within footprint envelope | 3 |
| C3, C4 | 100 nF, at least 10 V, ceramic, 2.5 mm lead spacing | 2 |
| J1 | 1×8, 2.54 mm male header to existing keypad tail | 1 |
| J2 | 1×2, 2.54 mm battery-lead connector; observe polarity | 1 |
| JP1 | 1×2, 2.54 mm header and shunt, normally fitted master/service link | 1 |
| J3 | 1×8, 2.54 mm header to display via cable | 1 |
| J4 | 1×3, 2.54 mm UPDI programming header | 1 |
| External | Existing membrane keypad, ERC12864FS-655 display and R2 adapter, three-AAA holder and cells, wiring | 1 set |

No USB interface, radio, indicator LED or charging circuit is on this board. It uses alkaline AAA cells. D1 adds a small forward drop, so regulation ends earlier in battery discharge than with an ideal-diode design. JP1 is an internal service link; the normal ON/OFF button is scanned sleep/wake. Removing one battery through the door provides full power disconnection.

Q1 is off at reset through R2. Firmware must drive U1 PD7 **low** to enable display power and **high** to turn it off. Before removing display power, drive all display signal outputs low to prevent back-powering, then redraw/reinitialize on wake. UC1701 maintains LCD drive internally while powered; no Sharp-style VCOM servicing is used. Reset and reinitialize the UC1701 after each display power cycle. Use PA4 for command/data and PA5 for active-low LCD reset. Disable unused peripherals and configure unused MCU pins appropriately; whole-device sleep current is not yet measured.

### Connector wiring

J1 pins 1–4 are assigned ROW0–ROW3 on PC0–PC3; pins 5–8 are COL0–COL3 on PD0–PD3. Membrane tail row/column ordering varies: establish the actual mapping by continuity test or a key-scan test, then map the eight signal assignments in firmware. Do not assume the photo supplies the electrical pinout.

| Main J3 / adapter J1 pin | Function | MCU |
| ---: | --- | --- |
| 1 | Switched 3.3 V LCD_VCC | Q1 collector |
| 2 | GND | Ground |
| 3 | SCK | PA1, DIP pin 23 |
| 4 | SDA | PA2, DIP pin 24 |
| 5 | CS, active low | PA3, DIP pin 25 |
| 6 | CD: low command, high pixels | PA4, DIP pin 26 |
| 7 | RST, active low | PA5, DIP pin 27 |
| 8 | No connection; spare position | No wire |

Connect matching **pin numbers** between main J3 and adapter J1. These are seven wires on an eight-position footprint. No part of this cable is compatible with R1's Sharp wiring. The adapter straps BM1/BM0, WR0/WR1 and unused D0–D5 to ground, and provides the LCD charge-pump capacitors. Leave the separate backlight A/K terminals insulated and unconnected.

Adapter BOM: C1/C2 = 2.2 µF 25 V ceramic (2.5 mm lead pitch, body within footprint), C3 = 330 nF 25 V ceramic, C4 = 100 nF, C5 = 10 µF 16 V low-leakage electrolytic (4 mm diameter, 1.5 mm pitch, ≤7 mm height), R1 = 10 MΩ axial. The two flying capacitors bridge VB0+/VB0− and VB1+/VB1−; C3 and R1 connect VLCD to ground. See the separate adapter schematic, BOM and DISPLAY_INTEGRATION.md.
J4 pin 1 is +3.3 V / VTREF, pin 2 GND, pin 3 UPDI. A suitable example programmer is **Adafruit UPDI Friend 5879**, set to **3V**. Disconnect the AAA pack when powering the target from the programmer. Do not connect two independent supplies together. The CANADUINO ATmega328P automatic bootloader programmer is not compatible with this MCU.

### Existing pad labels to custom keys

| Original pad row | Custom button functions in the same physical positions |
| --- | --- |
| 1, 2, 3, A | 7, 8/Up, 9, MENU |
| 4, 5, 6, B | 4, 5, 6, BACK |
| 7, 8, 9, C | 1, 2/Down, 3, CLEAR |
| *, 0, #, D | ON/OFF, 0, decimal point, ENTER/= |

## Fabrication and printing

For a PCB manufacturer, use the Gerbers and separate PTH/NPTH drill files, specify **82 × 68 mm, 2 layers, 1.6 mm FR-4**, and retain plated holes. Fabricate the **70 × 18 mm adapter** as a separate 2-layer, 1.6 mm FR-4 board from `pcb/display_adapter/gerbers/`. The fabrication ZIP has a separate directory for each board; do not combine their layers. All tracks are 0.4 mm wide; minimum configured clearance is 0.25 mm; both boards use through vias, 1.0 mm diameter / 0.5 mm drill (actual counts in their design JSON files). Standard footprint holes retain their own drill diameters. The board mounting holes are 2.7 mm nominal; the resin clearance holes are 2.9 mm.

For home etching, the copper PDF includes labeled reference and transfer orientations. Print 100%, verify the 100 mm scale, and register both layers accurately. Home-drilled holes are not automatically plated: every via and any PTH joining layers requires a conductive connection soldered on both sides. DIP sockets and headers can obstruct top-side soldering, so use accessible raised/machined contacts or a professionally plated board. Exact Gerbers are authoritative; the PDFs are for manual processes.

Ordinary printing resin forms the housing and keypad, **not conductive PCB traces**. The PCB files describe copper on an insulating board. No resin-printer exposure file, printer-specific sliced file, or CNC isolation toolpath is supplied because those depend on the actual fabrication process and tools.

The STLs are unsliced. Use rigid resin for housing, cradle and plates; use **55A flexible resin for `keypad_sheet_55A.stl`**. Keep supports away from label recesses, screw bores, nut pockets, actuator faces and mating surfaces. The keypad sheet is only 0.85 mm thick between keys, so avoid support placement or cleanup methods that can tear or permanently distort the flex zones. Optional compatible paint-fill can improve legend contrast. Hollow shell cavities must remain accessible for washing and curing; orient them to drain.

## What was verified

- Each individual CAD part in the prior R2 build was a valid, single solid.
- Each exported STL in the prior R2 build had a closed two-use edge graph at the mesh-check precision.
- Pairwise assembled-part checks in the prior R2 build found no positive intersections above 0.02 mm³ (nominal, unloaded geometry).
- Exported schematic pin-to-net connections match the PCB design definition, normalizing the root-sheet prefix on local net names.
- KiCad's final report: **0 DRC violations, 0 unconnected pads, 0 footprint errors**, with local footprints available.
- PCB outline/mount-hole positions and case PCB posts share the same design coordinates.
- **The new one-piece 55A keypad source has not yet been physically printed or re-validated as an exported mesh in this commit.** Rebuild the CAD and inspect `validation/cad_checks.json` before treating the generated keypad STL as final.
- Actual keypad pitch, cured-resin tolerances, membrane actuation, display pin fit/ambient-light contrast, soldered component heights, electrical operation and battery runtime still need physical confirmation. Computational DRC is not an electrical bench test or an independent ERC review.

## Rebuilding

Use CadQuery 2.7 / OpenCascade for `python source/build_case.py`. The current source exports `stl/keypad_sheet_55A.stl`, a two-key 55A fit coupon, and removes obsolete loose-button STLs from older builds. `source/check_and_render.py` also rebuilds the CAD, checks meshes and net mappings, and draws previews. Run `source/build_pcb.py` and `source/build_display_adapter.py` with KiCad 7's `pcbnew` Python bindings and standard footprints installed, then run `source/export_pcbs.py` with `KICAD_CLI` pointing to KiCad 7 CLI. Run `source/validate_display.py` for the manufacturer pin/capacitor audit. Export both schematic netlists before running the net checks. `source/plot_copper.py` uses KiCad's native plot controller for exact copper artwork. `source/make_print_templates.py` requires ReportLab. Plot main copper with `source/plot_copper.py`, then again with `DISPLAY_ADAPTER=1`; run `source/finish_exports.py` last to assemble labeled PDFs, verify both netlists and package R2 ZIPs.

## Source references

- [AVR128DA28 datasheet, pinout and SPDIP package](https://ww1.microchip.com/downloads/aemDocuments/documents/MCU08/ProductDocuments/DataSheets/AVR128DA28-32-48-64-Data-Sheet-DS40002183.pdf).
- [MCP1700 datasheet, TO-92 pinout and capacitor requirements](https://ww1.microchip.com/downloads/en/DeviceDoc/MCP1700-Data-Sheet-20001826F.pdf).
- [ERC12864FS-655 product](https://www.buydisplay.com/2-8-inch-128x64-graphic-module-serial-display-spi-lcd-w-optl-touch-screen).
- [EastRising module datasheet](https://www.buydisplay.com/download/manual/ERC12864-655_Series_Datasheet.pdf) and [SPI reference circuit](https://www.buydisplay.com/download/interfacing/ERC12864-655_Interfacing.pdf). See DISPLAY_INTEGRATION.md for the drawing and pin audit.
- [Pololu 1144 three-AAA holder envelope](https://www.pololu.com/product/1144).
- [Adafruit UPDI Friend](https://www.adafruit.com/product/5879).
- [ELEGOO Mars 5 Ultra build volume](https://us.elegoo.com/products/mars-5-ultra-9k-7inch-monochrome-lcd-resin-3d-printer).
- Standard footprints copied unchanged from KiCad 7 libraries; see `pcb/FOOTPRINT_LICENSE.txt`.
