# Material Weight Calculator — hardware R1

This package contains real parametric CAD, printable STLs, a routed KiCad PCB, schematic, Gerbers, drills, and actual-scale print templates. It is a **prototype design**, not a physically tested or production-qualified assembly. The device firmware is not included in this hardware release.

## Start here

1. Open `docs/case_front_preview.png` to inspect the actual CAD and recessed legends.
2. Print `docs/keypad_fit_template.pdf` at **100% / Actual Size**. Place the existing DIYmalls pad over the key-center marks. The screenshot identifies the pad type but does not establish its exact pitch. The model currently uses nominal 18 mm key pitch; confirm this fit before printing the full shell. The source has explicit `KEY_X` and `KEY_Y` parameters if the actual pad differs.
3. Print the small fit coupons and one flexible button before the full set. Check legend detail, cap release, nut fit, and actuation with the actual membrane. No claim is made that a particular flexible resin's force or shrinkage has been tested.
4. For the Mars 5 Ultra, use the shell sections in `stl/mars5_ultra_oriented/`. They have been rotated to fit the manufacturer's 153.36 × 77.76 × 165 mm build volume; add supports and a raft in the slicer without exceeding that volume. These are unsliced STLs, not exposure profiles.
5. Use `pcb/gerbers/` for a conventional **two-layer, 1.6 mm copper-clad PCB with plated through holes**. Open the KiCad project to inspect/edit it before ordering.

## Files

| Location | Contents |
| --- | --- |
| `stl/` | Four case sections, battery cover, keypad plates, display cradle and clamps, sixteen individual buttons, full button set, and fit coupons |
| `stl/mars5_ultra_oriented/` | Printer-fitting orientations for the shell sections and larger keypad plates |
| `cad/calculator_assembly.step` | Assembly with parts in their assembled locations; split case sections included |
| `cad/pcb_outline.step` | Board outline and four mounting holes, matching the enclosure |
| `cad/*whole_reference.stl` | Unsplit shell references for a larger printer; do not use these on the Mars 5 Ultra |
| `source/build_case.py` | Editable CadQuery source for case, buttons, nut pockets, and split shells |
| `pcb/material_weight_calculator.kicad_pro` | KiCad 7 project |
| `pcb/material_weight_calculator.kicad_sch` | Editable, embedded-symbol schematic with every used pin/net explicitly named |
| `pcb/material_weight_calculator.kicad_pcb` | Routed two-layer board, 82 × 68 mm |
| `pcb/mw-footprints.pretty/` | Bundled standard footprints; project does not depend on an external footprint-library path |
| `pcb/gerbers/` | Top/bottom copper and masks, top silkscreen, outline, separate plated/non-plated Excellon drills and SVG drill maps |
| `docs/copper_artwork_1to1.pdf` | Exact KiCad copper plots: top reference, top transfer, bottom reference, bottom transfer |
| `docs/drill_template.pdf` | Component-side drill and board outline template |
| `docs/keypad_fit_template.pdf` | Full-scale membrane alignment template and 100 mm scale check |
| `docs/schematic.pdf` | Circuit drawing exported by KiCad |
| `pcb/bom.csv` | Reference-designator BOM |
| `validation/` | CAD, mesh, schematic-net and KiCad design-rule reports |

The STLs are in millimeters, not mirrored. Each individual file is translated to its own positive bounding box. Use STEP for assembly positions. `all_16_buttons.stl` is arranged as **8 × 2 for printing**, while the actual assembled keypad remains **4 × 4**. No support structures are baked into the meshes.

## Case and fasteners

Overall body: 96 × 184 × 31 mm, with button tops at 33 mm. Wall/face thickness is generally 2.6 mm, with internal reinforcement webs. The PCB's lower face is 7 mm from the rear reference plane. The holder pocket targets a Pololu 1144-style 52 × 37 × 13 mm three-AAA holder with leads, allowing clearance around that envelope.

All fastening provisions are **M2.5 with hex nuts**, as requested. Nominal nut pockets are 5.35 mm across flats and about 2.45 mm deep; clearance holes are 2.9 mm. Glue nuts around their outside faces, keeping threads and screw paths clean. On front-facing pocket openings, hold the nut flush to the pocket's open face while the adhesive sets, rather than pushing it deeper into the clearance allowance. Verify actual nut dimensions with the coupon before gluing the full set.

| Joint | Screws | Nuts |
| --- | --- | --- |
| Rear to front shell | 4 × M2.5 × 16 mm | 4, glued into front-shell pockets |
| PCB to rear posts | 4 × M2.5 × 6 mm | 4, glued into rear-post pockets |
| Keypad backing + guide stack to front | 4 × M2.5 × 6 mm | 4, glued into front pockets |
| Display cradle to front | 4 × M2.5 × 6 mm | 4, glued into front pockets |
| Display edge clamps to cradle | 4 × M2.5 × 8 mm | 4, glued into cradle pockets |
| Battery cover | 2 × M2.5 × 6 mm | 2, glued into rear pockets |

Total: **22 nuts; four 16 mm, four 8 mm, and fourteen 6 mm screws**. Screw lengths are measured under the head. Trial-fit and shorten any screw that bottoms before clamping; do not force a screw into resin. The design does not use heat-set inserts or self-tapping threads.

The long front and rear shells each have an upper/lower **bonded seam** at plan Y=60.25 mm, with locating tongues and mating relief. Bond each upper/lower pair into one shell before final assembly. This printing seam is separate from the removable, screwed front/rear joint. Use an adhesive appropriate for the fully cured rigid resin and test it on a coupon. One-piece references are included if a larger printer is available.

## Assembly order

1. Wash/cure the printed parts according to the actual resin's instructions. Clear supports from recesses and mating faces. Bond the two front sections and the two rear sections using their locating features.
2. Test-fit and glue the M2.5 nuts into their pockets. Allow adhesive to set before applying screw load.
3. From inside the front, insert the sixteen flexible buttons into their corresponding openings. Their larger flanges remain behind the front face. Legends are actual 0.4 mm Boolean recesses, not rendered textures.
4. Install the guide above the membrane and the rigid backing below it. Nominal stack: backing top Z=24.5; 0.8 mm membrane; button contact foot Z=25.45; guide stop top Z=26.6. The initial rest clearance is 0.15 mm and mechanical stop travel 0.5 mm. These targets need a real membrane/resin test. The original labels stay hidden and the membrane stays intact.
5. Route the flexible ribbon through the backing relief; avoid sharp folds or pinching at the enclosure edge. The backing's screw slots allow small translational adjustments, not arbitrary correction of key pitch.
6. Fit the display into its edge cradle, align the active area with the 29 × 27 mm window, and secure the two clamps lightly. The module envelope is based on Adafruit's published approximately 40 × 39 mm board size. The carrier clears rear components and permits small alignment shifts; confirm the actual module revision before tightening. Do not clamp the LCD glass or flexible tail.
7. Assemble the PCB, check power rails with U1/display disconnected, fit the socketed MCU, then connect the keypad, display cable, and battery holder using the wiring below.
8. Install the PCB in the rear tray, secure the battery holder in its pocket, and route leads clear of nut pockets and ribs. Install the battery cover, then join front/rear with the four longer screws.

## PCB circuit and parts

| Ref | Part / function | Quantity |
| --- | --- | ---: |
| U1 | AVR128DA28-I/SP, in 28-pin narrow DIP socket (7.62 mm row spacing) | 1 + socket |
| U2 | MCP1700-3302E/TO, 3.3 V LDO; spread-lead TO-92 footprint | 1 |
| D1 | 1N5817, DO-41, battery reverse-polarity protection | 1 |
| Q1 | 2N3906 PNP, TO-92 spread leads; switches display power | 1 |
| R1 | 10 kΩ, axial, 7.62 mm lead spacing | 1 |
| R2 | 100 kΩ, axial, 7.62 mm lead spacing | 1 |
| C1, C2, C5 | 1 µF, at least 10 V, ceramic, 2.5 mm lead spacing; body within footprint envelope | 3 |
| C3, C4 | 100 nF, at least 10 V, ceramic, 2.5 mm lead spacing | 2 |
| J1 | 1×8, 2.54 mm male header to existing keypad tail | 1 |
| J2 | 1×2, 2.54 mm battery-lead connector; observe polarity | 1 |
| JP1 | 1×2, 2.54 mm header and shunt, normally fitted master/service link | 1 |
| J3 | 1×9, 2.54 mm header to display via cable | 1 |
| J4 | 1×3, 2.54 mm UPDI programming header | 1 |
| External | Existing membrane keypad, Adafruit 3502 display module, three-AAA holder and cells, wiring | 1 set |

No USB interface, radio, indicator LED or charging circuit is on this board. It uses alkaline AAA cells. D1 adds a small forward drop, so regulation ends earlier in battery discharge than with an ideal-diode design. JP1 is an internal service link; the normal ON/OFF button is scanned sleep/wake. Removing one battery through the door provides full power disconnection.

Q1 is off at reset through R2. Firmware must drive U1 PD7 **low** to enable display power and **high** to turn it off. Before removing display power, drive all display signal outputs low to prevent back-powering, then redraw/reinitialize on wake. Maintain the display's required VCOM inversion while active. Disable unused peripherals and configure unused MCU pins appropriately; whole-device sleep current is not yet measured.

### Connector wiring

J1 pins 1–4 are assigned ROW0–ROW3 on PC0–PC3; pins 5–8 are COL0–COL3 on PD0–PD3. Membrane tail row/column ordering varies: establish the actual mapping by continuity test or a key-scan test, then map the eight signal assignments in firmware. Do not assume the photo supplies the electrical pinout.

| J3 pin | Connection at Adafruit display header |
| ---: | --- |
| 1 | VIN, switched LCD power |
| 2 | **No wire** — module regulator output, deliberately unconnected |
| 3 | GND |
| 4 | CLK (U1 PA1) |
| 5 | DI / data (PA2) |
| 6 | CS (PA3) |
| 7 | EXTMODE to GND, selecting serial VCOM control |
| 8 | DISP (PA4) |
| 9 | EXTCOMIN to GND, unused in serial mode |

Match signal labels, not a guessed connector orientation. J3 is a cable connection, not a claim of direct mechanical plug compatibility with every display revision. Keep the module's regulator output isolated so it cannot bypass Q1.

J4 pin 1 is +3.3 V / VTREF, pin 2 GND, pin 3 UPDI. A suitable example programmer is **Adafruit UPDI Friend 5879**, set to **3V**. Disconnect the AAA pack when powering the target from the programmer. Do not connect two independent supplies together. The CANADUINO ATmega328P automatic bootloader programmer is not compatible with this MCU.

### Existing pad labels to custom keys

| Original pad row | Custom button functions in the same physical positions |
| --- | --- |
| 1, 2, 3, A | 7, 8/Up, 9, MENU |
| 4, 5, 6, B | 4, 5, 6, BACK |
| 7, 8, 9, C | 1, 2/Down, 3, CLEAR |
| *, 0, #, D | ON/OFF, 0, decimal point, ENTER/= |

## Fabrication and printing

For a PCB manufacturer, use the Gerbers and separate PTH/NPTH drill files, specify **82 × 68 mm, 2 layers, 1.6 mm FR-4**, and retain plated holes. All tracks are 0.4 mm wide; minimum configured clearance is 0.25 mm; the board has eight through vias, 1.0 mm diameter / 0.5 mm drill. Standard footprint holes retain their own drill diameters. The board mounting holes are 2.7 mm nominal; the resin clearance holes are 2.9 mm.

For home etching, the copper PDF includes labeled reference and transfer orientations. Print 100%, verify the 100 mm scale, and register both layers accurately. Home-drilled holes are not automatically plated: every via and any PTH joining layers requires a conductive connection soldered on both sides. DIP sockets and headers can obstruct top-side soldering, so use accessible raised/machined contacts or a professionally plated board. Exact Gerbers are authoritative; the PDFs are for manual processes.

Ordinary printing resin forms the housing and buttons, **not conductive PCB traces**. The PCB files describe copper on an insulating board. No resin-printer exposure file, printer-specific sliced file, or CNC isolation toolpath is supplied because those depend on the actual fabrication process and tools.

The STLs are unsliced. Use rigid resin for housing, cradle and plates; flexible resin for button caps. Keep supports away from label recesses, screw bores, nut pockets, contact feet and mating faces. The raised front face should remain legible after cure; optional compatible paint-fill can improve contrast. Hollow shell cavities must remain accessible for washing and curing; orient them to drain.

## What was verified

- Each individual CAD part is a valid, single solid.
- Each exported STL has a closed two-use edge graph at the mesh-check precision.
- Pairwise assembled-part checks found no positive intersections above 0.02 mm³ (nominal, unloaded geometry).
- Exported schematic pin-to-net connections match the PCB design definition, normalizing the root-sheet prefix on local net names.
- KiCad's final report: **0 DRC violations, 0 unconnected pads, 0 footprint errors**, with local footprints available.
- PCB outline/mount-hole positions and case PCB posts share the same design coordinates.
- These are digital checks. Actual keypad pitch, cured-resin tolerances, membrane actuation, display module revision, soldered component heights, electrical operation and battery runtime still need physical confirmation. Computational DRC is not an electrical bench test or an independent ERC review.

## Rebuilding

Use CadQuery 2.7 / OpenCascade for `python source/build_case.py`. `source/check_and_render.py` also rebuilds the CAD, checks meshes and net mappings, and draws previews. Run `source/build_pcb.py` with KiCad 7's `pcbnew` Python bindings and standard footprints installed, then export its schematic netlist before running the net check. `source/plot_copper.py` uses KiCad's native plot controller for exact copper artwork. `source/make_print_templates.py` requires ReportLab.

## Source references

- [AVR128DA28 datasheet, pinout and SPDIP package](https://ww1.microchip.com/downloads/aemDocuments/documents/MCU08/ProductDocuments/DataSheets/AVR128DA28-32-48-64-Data-Sheet-DS40002183.pdf).
- [MCP1700 datasheet, TO-92 pinout and capacitor requirements](https://ww1.microchip.com/downloads/en/DeviceDoc/MCP1700-Data-Sheet-20001826F.pdf).
- [Adafruit 3502 product dimensions and electrical interface](https://www.adafruit.com/product/3502) and [Sharp breakout reference hardware](https://github.com/adafruit/Adafruit-Sharp-Memory-Display-PCBs). The reference hardware repository also includes older module variants; the final module's printed signal names remain authoritative.
- [Pololu 1144 three-AAA holder envelope](https://www.pololu.com/product/1144).
- [Adafruit UPDI Friend](https://www.adafruit.com/product/5879).
- [ELEGOO Mars 5 Ultra build volume](https://us.elegoo.com/products/mars-5-ultra-9k-7inch-monochrome-lcd-resin-3d-printer).
- Standard footprints copied unchanged from KiCad 7 libraries; see `pcb/FOOTPRINT_LICENSE.txt`.
