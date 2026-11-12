# R3 LTC3440 implementation and fabrication hold

Updated 2026-11-12. **R3 is routed and CAD-validated. Physical mating is NOT approved. No R3 Gerbers, drills or PCB-order ZIP have been released.**

Open [the R3 KiCad project](pcb/r3/material_weight_calculator.kicad_pro). The main PCB under `pcb/` without `/r3/` is the preserved MCP1700 R2.1 design. The SMD [R3 display adapter](pcb/r3/display_adapter/display_adapter.kicad_pro) is included alongside the main board. The older adapter outside `/r3/` is preserved R2.1. Old R2 fabrication archives are historical and must not be used for this redesign.

## What changed

- Replaced the main-board LDO with **LTC3440EMS#PBF, MSOP-10**, externally accessible leads, no exposed center pad. Do not substitute the DFN package.
- 10 µH Sumida CDRH6D38NP-100NC inductor; custom lands preserve the manufacturer's 2 mm inner gap and 7.3 mm land height, extending only the outer toes by 0.65 mm for iron access. Maximum body 7 × 7 × 4 mm. The single winding is not polarity-sensitive.
- New regulator passives are hand-solder footprints: 0805 resistors/compensation/snubber capacitors, 1206 input capacitor, 1210 output capacitor. The purchased DIP/socket and connector interfaces remain through-hole. All discrete components on both current R3 boards are SMD; see [owned-parts policy](OWNED_PARTS_AND_SMD.md).
- C1: 10 µF 25 V X7R, GRM31CR71E106KA12L. C2: 22 µF 25 V X7R, GRM32ER71E226KE15L. Other decouplers and small resistors use 0603 hand-solder pads compatible with suitable owned kit parts. The adapter bulk capacitor is now a nonpolar 1206 ceramic. Named parts and physical footprints are selected; the effective capacitance under DC bias, temperature and tolerance still needs qualification. Nominal capacitance and a 25 V rating alone do not establish this.
- RT 60.4 kΩ gives approximately 1 MHz. FB divider 340 kΩ / 200 kΩ gives **3.294 V nominal**, not an exact 3.300 V. With the datasheet FB limits and 1% resistors, the static arithmetic spans about **3.189–3.402 V**, before dynamic ripple/transients. The LCD's documented 3.0–3.6 V operating range leaves margin for static error, but startup/overshoot must be measured.
- **Corrected the earlier reference error:** the 15 kΩ R6 and 1.5 nF C6 compensation branch goes **VC → R6 → C6 → FB**. It must NOT terminate at ground. This follows ADI's first-page typical application and page 14 compensation circuit.
- The typical 25 µA Burst Mode regulator current plus about 6.1 µA divider current already exceeds the former sub-10-µA automatic-sleep goal. MCU/leakage add to this; hard-off still disconnects the battery. No measured battery-life claim is made.
- MODE is connected through 0 Ω R8 to VIN, enabling Burst Mode without relying on VOUT startup. SHDN/SS is tied to VIN, as in the basic reference. No RC soft-start is fitted; startup and battery sag must be measured.
- Added the datasheet's protection for possible **VIN >4.5 V**: D2 PMEG2010ER (anode SW1, cathode VIN), plus a 2 Ω / 1 nF series SW1-to-ground snubber. Fresh 3-cell alkaline open-circuit voltage must not be assumed to equal 4.5 V.
- D1 is an SMA SS14 series reverse-polarity diode. VIN must remain **at least 2.5 V after D1's drop**, including load sag. This choice sacrifices some end-of-discharge capacity; the assembly is not specified to operate at a 2.5 V raw pack voltage. Use alkaline AAA only; no 3-cell lithium-ion pack.
- Full two-layer rerouting, short front-only U2-to-inductor switch paths, filled B.Cu ground plane, VIN/GND/3V3 test pads, both-side connector labels. Minimum trace width 0.20 mm, clearance 0.15 mm; new vias 0.70/0.35 mm. Switch traces widen to 0.6 mm after lead escape. Two-layer 1.6 mm FR-4 remains the intended construction.
- Retained the 82 × 68 mm outline, four mounting-hole centers, MCU socket and every connector center/numbering. The main enclosure outline still registers; this is not a populated-component collision or cable-fold test.

## Saved evidence

| Check | Result | Evidence |
| --- | --- | --- |
| Main and adapter native KiCad 9.0.2 ERC | PASS, zero violations | [main ERC](validation/r3/main_erc.rpt), [adapter ERC](validation/r3/adapter_erc.rpt) |
| Main and adapter native DRC, including warnings | PASS, zero violations, zero unconnected pads | [main DRC](validation/r3/main_drc.rpt), [adapter DRC](validation/r3/adapter_drc.rpt) |
| Schematic parity | PASS, zero issues on both boards | Same DRC reports |
| All connected schematic XML pins versus actual saved pad nets | PASS | [independent audit](validation/r3/pin_audit.json) |
| Independent ADI / AVR / LCD pin contracts and preserved hole centers | PASS in CAD | Same audit and [verification source](source/verify_r3.py) |
| Top and true mirrored-underside numbering | PASS as a CAD projection | [main 1:1 template](docs/r3/main_orientation_1to1.svg), [adapter 1:1 template](docs/r3/adapter_orientation_1to1.svg), [every pin coordinate/net](validation/r3/orientation_pins.csv) |
| Deliberately rotated regulator/MCU/connectors and wrong compensation endpoint | All detected | [negative checks](validation/r3/negative_checks.json) |
| Attempted manufacturing export with unresolved physical checks | Correctly refused; no output created | Same negative checks |
| Actual component mating, cable order, fit, kit/DC-bias qualification | **OPEN — FABRICATION HOLD** | [release gate](pcb/r3/release_gate.json) |
| Electrical operation, stability, ripple, battery life | **NOT BENCH TESTED** | Prototype procedure below |

[Top copper/silkscreen](docs/r3/main_top.svg) · [true underside copper/silkscreen](docs/r3/main_bottom.svg) · [main schematic](docs/r3/main_schematic.pdf) · [adapter schematic](docs/r3/adapter_schematic.pdf) · [R3 BOM](pcb/r3/bom.csv).

The schematic uses explicit numbered blocks and global net labels. The XML-to-pad check covers every connected terminal; passing ERC does not by itself prove that an analog circuit is correct. No report exclusions or warning suppression were added to make these checks pass.

## Installation and view convention

Every component is installed **from F.Cu**, including DIP socket and male headers. Through-hole soldering is done from B.Cu. SMD parts are soldered on F.Cu. Do not install a connector or socket from B.Cu to make a drawing look convenient.

The underside templates mirror **X about board width**, retaining the same top edge. They show front-side SMD pads as a projection through the board for continuity review; those pads do not exist on B.Cu. Gold marks pad 1. Print at 100% and measure the 50 mm scale before placing any part on the paper.

| Part | F.Cu / package interpretation | Underside interpretation / remaining real-part check |
| --- | --- | --- |
| U1 AVR128DA28-I/SP socket | Notch towards pins 1/28, board top; pin 1 at (35,20), pin 28 at (42.62,20) mm | Pin 1 appears at X47, pin 28 at X39.38 in the mirrored 82 mm board view. Socket and chip both enter from F.Cu. Check actual ED281DT body/lead fit. |
| U2 LTC3440 MSOP-10 | Pin 1 upper left at (22.8875,15); pin 5 lower left (22.8875,17); pin 6 lower right (27.1125,17); pin 10 upper right (27.1125,15). 0.5 mm pitch; pad size 1.625 × 0.35 mm. | Pin 1 moves to right column in the underside projection. Package lettering/dot must match the **top**, never the underside projection. ADI drawing 05-08-1661 Rev F: 3 mm body, 4.9 mm nominal lead span. No underside thermal pad. |
| Q1 onsemi MMBT3906LT1G SOT-23 | Pin 1 B at (56.5,14.05), pin 2 E at (56.5,15.95), pin 3 C at (59.5,15). Accessible hand-solder pads. | Base/emitter move to the right in the mirrored underside projection. This is B/E/C numbering, not the former TO-92 E/B/C. A deliberate B/E swap is rejected by the independent audit. |
| D1 SS14 SMA | Cathode/bar to pad 1 at (12,5), VIN; anode pad 2 at (16,5), VBAT_LINK. | Cathode appears on the right in the underside projection. Match purchased part's package drawing before assembly. |
| D2 PMEG2010ER CFP3 | Rotated 180°: cathode/bar pad 1 at (26.4,22.5), VIN, on the **right** in the top view; anode pad 2 at (23.6,22.5), SW1, left. | Cathode appears left in underside projection. Do not copy D1's apparent stripe direction. |
| L1 | Nonpolar 10 µH winding. Land 1 SW1 above land 2 SW2 after 90° rotation. | Same numbered nets in mirrored projection; ensure the selected 7 mm body and extended lands fit. |
| New ceramic capacitors / resistors | Nonpolar. All SMD regulator parts on F.Cu; see BOM for package/value. | No electrical polarity reversal on rotation; size, terminal access and correct value still matter. |
| Adapter C5 ceramic | Nonpolar 10 µF 25 V X7R 1206. Pad 1 LCD_VCC at (6.4375,7); pad 2 GND at (9.5625,7). | No electrolytic stripe or polarity-sensitive body. Mirrored pin numbering remains in the review CSV. |
| J1 keypad | Male 1×8 2.54 mm header, square pad 1 at (12,22.54), pad 8 at (12,40.32). Ribbon plug is female. | PCB numbering is fixed; the actual female plug's 16-key contact map and cable exit remain unverified. Do not assume ribbon position 1 = ROW0. |
| J2 battery | Pad 1 switched positive; pad 2 GND; F.Cu insertion | Looking into a mating plug reverses the apparent contact order. Check red/black at the actual contact, with batteries disconnected. |
| JP1 | Service shunt VBAT_SW → VBAT_LINK, normally fitted; not the case power switch | A shunt has no electrical polarity; verify its body clears L1 and access remains possible. |
| Main J3 / adapter J1 | Numbered 1→1 … 7→7 wires; pad 8 NC on each. Main row vertical, adapter row horizontal. | Map by contact number and continuity, not colors or apparent left-to-right order. Adapter wire landing is not a tall header stack. |
| Adapter J2 LCD | Direct 22-hole solder interface, 1.27 mm pitch; pin 1 at (21.665,3), pin 22 at (48.335,3), adapter F.Cu plan | Actual LCD viewing side, pin-end face and soldering face must be overlaid. Corner NC pins are not electrical pins. No extra male header/socket here. |
| J4 UPDI | 1 +3V3/VTREF, 2 GND, 3 UPDI, all from F.Cu | Actual UPDI Friend pin label order must be checked from mating face. Use 3.3 V, never 5 V. Remove batteries before externally powering this header. |
| Case slide switch | External CYT1107 SPDT: battery + to measured common, one selected outer to main J2.1; unused outer insulated | No PCB footprint implies no CAD terminal guarantee. Measure actual common and both slider positions. |

## Physical information still required before manufacturing

The repository contains photographs/descriptions and an electrical connector plan, but **no recorded physical sign-off** for these items. It would be false to mark them as passed remotely.

1. Print both 1:1 templates; photograph the actual LCD with viewing side, electrical pin 1, pin ends and adapter soldering side identified. Overlay the 22 contacts and confirm corner-pin clearances, pin reach, rear-frame insulation and component height. Determine F.Cu versus B.Cu approach before soldering.
2. With no battery/programmer, identify female keypad plug hole numbers from its mating face, dry-fit a spare 2.54 mm male header, measure first-to-last center span (17.78 mm nominal), and record the two closing contact numbers for all sixteen keys.
3. Confirm actual UPDI Friend labels/order, all seven LCD cable continuities, the slide-switch common terminal and switched battery polarity. Check connector/cable bodies against enclosure ribs and available insertion height.
4. Verify genuine U1/MMBT3906 Q1/diode package markings, socket/part fit and capacitor DC-bias data for the chosen MPNs. The board does not authorize unknown substitutes.

Record evidence paths and SHA-256 hashes in `pcb/r3/release_gate.json`, then rerun the native checks. The exporter refuses unresolved checks **before creating any Gerbers, drill files or manufacturing directory**. Approval status is only appropriate after review of that evidence; a CAD pass never edits physical evidence automatically.

## Reproduction

Requires KiCad 9 `kicad-cli` and its `pcbnew` Python, numpy, scipy and shapely for layout regeneration. Use the Python interpreter supplied with the KiCad installation (on this Linux host `/usr/bin/python3`).

```sh
/usr/bin/python3 hardware/source/build_r3.py
/usr/bin/python3 hardware/source/build_r3.py --adapter
/usr/bin/python3 hardware/source/export_r3.py
/usr/bin/python3 hardware/source/render_r3_orientation.py
/usr/bin/python3 hardware/source/test_r3_safety.py
python hardware/source/check_power_r3.py
```

`export_r3.py` produces review files only by default. `--manufacturing` first checks the evidence manifest, then reruns ERC/DRC/parity and the independent actual-pad audit. The current manifest intentionally fails that gate. The old R2 export scripts do not implement the R3 circuit; do not use them for an R3 release.

## First assembled prototype, after physical release

Use a small prototype order. With power removed, check every connector and power-rail continuity, diode bars, U1 notch and adjacent MSOP pins under magnification. Inspect for shorts before installing MCU/LCD. Bring up the supply current-limited with the external battery switch on; confirm regulated output at several light loads while sweeping **VIN at U2** from 2.5 to 5.5 V. Separately test raw 3-AAA pack sag and the D1 drop; do not apply 5.5 V at the battery header and assume the same voltage reaches U2.

Scope VOUT startup, shutdown, ripple and load steps at fresh/depleted pack conditions and LCD wake. Verify no overshoot exceeds the LCD's 3.6 V operating ceiling, no oscillation/ringing, and no abnormal temperature. Characterize minimum VIN, inrush and on/sleep current with actual MCU firmware and LCD. Test regulated-rail load limits gradually; the IC's headline 600 mA rating is not a measured rating of this assembly. Do not deliberately short the first hand-built board without a controlled protection test setup. Only after these tests may runtime, stability and completed-device operation be claimed.
