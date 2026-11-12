# R3 LTC3440 circuit — implemented, physical fabrication hold

Updated 2026-11-12. The new design is in [pcb/r3](../pcb/r3/). Read [R3_REVIEW.md](../R3_REVIEW.md) for full circuit decisions, exact component orientations, native KiCad reports, unresolved real-part checks and reproduction instructions.

The preserved main board one directory above `/r3/` still uses the MCP1700. No old R2 Gerber represents R3. **No R3 Gerbers or drill files have been released.**

## Manufacturer cross-check

Authority: [ADI LTC3440 3440fd](https://www.analog.com/media/en/technical-documentation/data-sheets/3440fd.pdf), bundled in [reference](../reference/LTC3440_3440fd.pdf). Page 1 typical application, page 2 MS package top view, page 12 layout, page 13 high-input protection, page 14 compensation, page 20 MSOP mechanical drawing.

**Correction to the prior draft:** the series 15 kΩ + 1.5 nF network connects **VC to FB**, not to GND. Both the machine-readable reference and actual saved KiCad pads now enforce this. A fault-injection test rejects the old incorrect endpoint.

| MSOP-10 pin | Name | Implemented net / connection |
| ---: | --- | --- |
| 1 | RT | RT → R3 60.4 kΩ → GND |
| 2 | MODE/SYNC | MODE → R8 0 Ω → VIN; Burst Mode |
| 3 | SW1 | L1 terminal 1, D2 anode, R7 snubber input |
| 4 | SW2 | L1 terminal 2 |
| 5 | GND | Ground with bottom plane |
| 6 | VOUT | +3V3, C2 22 µF, R4 340 kΩ upper divider |
| 7 | VIN | Protected switched battery, C1 10 µF, D2 cathode |
| 8 | SHDN/SS | VIN; enabled directly, no RC soft-start fitted |
| 9 | FB | Divider tap, R5 200 kΩ to GND, C6 compensation endpoint |
| 10 | VC | R6 15 kΩ → COMP_NODE → C6 1.5 nF → FB |

D2 PMEG2010ER plus the 2 Ω/1 nF SW1-to-GND series snubber implement the ADI requirement for possible VIN above 4.5 V. D1 SS14 remains series polarity protection; minimum 2.5 V applies **after its voltage drop**, not at the raw pack.

The [actual R3 BOM](../pcb/r3/bom.csv) supersedes the earlier candidate list. New regulator passives use 0805/1206/1210 accessible pads. The purchased MCU/socket and connector interfaces remain unchanged; remaining resistors/capacitors and Q1 are now SMD, including the separate R3 adapter. No DFN, WSON or hidden thermal-pad regulator is used.

## Verified versus still open

Both main and adapter pass native KiCad 9.0.2 ERC/DRC/schematic parity, with zero violations and zero unconnected pads. Every connected schematic XML pin matches actual saved PCB pad nets. Numbered top and mirrored-underside review templates are included. These results are CAD evidence, not a physical mating approval.

LCD soldering-side overlay, keypad contact mapping/dry fit, actual programmer/cable/switch/part identification, populated clearance and capacitance DC-bias checks remain open in [release_gate.json](../pcb/r3/release_gate.json). `export_r3.py --manufacturing` refuses to create files while that evidence is missing. Prototype operation and battery life are unmeasured.
