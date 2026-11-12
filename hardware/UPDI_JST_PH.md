# J5 programming connection — user-crimped JST-PH lead

The main R3 PCB includes **J5, a 3-pin 2.0 mm JST-PH top-entry header** for the crimp kit shown by the user. Keep the existing cable plugged into the UPDI Friend. Crimp the 2.0 mm PH contacts onto the cable's loose wire ends and insert them into the mating PH housing for J5. No separate adapter and no soldering to the programmer are required.

The original J4 programming header and the purchased AVR128DA28-I/SP / ED281DT socket are retained.

## Wire by signal

| Calculator J5 cavity/pad | Signal | Existing UPDI Friend cable wire | Existing J4 equivalent | MCU destination |
| ---: | --- | --- | ---: | --- |
| 1 | GND | GND wire (normally black) | 2 | U1 pins 15 and 21 |
| 2 | PWR / +3V3 | PWR wire (normally red), selector **3V** | 1 | U1 AVDD pin 14 / VDD pin 20 |
| 3 | UPDI | UPDI wire (normally white) | 3 | U1 programming pin 19 |

J5 pin 2 supplies the regulated logic rail, **not the raw battery input**. The UPDI Friend PWR pad is a power output. Remove batteries before programmer-powered programming and disconnect USB before attaching or unplugging the lead. Do not connect another power source or a second programmer at the same time. Ordinary 3 V UPDI programming is intended; high-voltage programming is not part of this wiring plan.

**J4 and J5 have different power/ground orders.** Do not make a 1-to-1 numbered harness between those two headers. Identify the existing cable wires by continuity to the UPDI Friend signals shown above, then crimp and insert each contact in its assigned PH cavity. Wire colors are optional identifiers, never proof of contact assignment.

## Connector and orientation

- Board reference: **B3B-PH-K-S(LF)(SN)**, top-entry through-hole header; kit equivalent must match its dimensions. Mating housing reference: **PHR-3**, with matching PH crimp contacts. The board-side header solders to the PCB; the wire-side contacts are crimped into the housing.
- Installed from **F.Cu**, all three hole centers at board Y46 mm. Top view: pad 1 at X63 mm, pad 2 X65 mm, pad 3 X67 mm. Pad 1 is rounded rectangular, marked by the footprint's pin-1 symbol.
- The PH row has **2.00 mm pitch**, 4.00 mm first-to-last span and 0.75 mm PCB drills. The selected footprint's body projection is X61.05–68.95, Y44.3–48.8 mm. The manufacturer defines its PCB layout from the **connector mounting surface**. Match the header's molded pin-1 indication to the board footprint.
- The physical underside view mirrors X about the 82 mm board width: pad 1 becomes X19 mm, pad 2 X17 mm, pad 3 X15 mm; Y remains 46 mm. Do not use this underside view as the installation view.
- A view into the cable housing is different from the PCB top view. Identify each cavity by its mating board pin, then continuity-test it to the corresponding signal on the existing programmer cable after crimping. Do not infer cavity order from an unqualified left/right description.
- Manufacturer nominal mated height is 8 mm above the PCB; actual kit body, cable bend and enclosure clearance still need physical checking. The connector is internal; no external case cutout was added.

[Numbered top/underside template](docs/r3/main_orientation_1to1.svg) · [main top copper/silkscreen](docs/r3/main_top.svg) · [all pad nets/coordinates](validation/r3/orientation_pins.csv).

## Checks and release status

The independent saved-board audit checks J5's footprint, 2 mm pitch, pin order, F.Cu installation, drill size and connections alongside the unchanged J4 and MCU pin contracts. Deliberate 180° rotation and power/ground-swap tests must fail. Native KiCad ERC, DRC and schematic parity must pass after routing.

Actual kit-header fit, crimp retention, existing-cable signal identification, lead continuity and populated enclosure clearance remain physical checks in `pcb/r3/release_gate.json`. No Gerbers are released while these or other outstanding checks remain unresolved.

Sources: [JST PH manufacturer datasheet](https://www.jst-mfg.com/product/pdf/eng/ePH.pdf), pp1/3; [Adafruit UPDI Friend pinouts](https://learn.adafruit.com/adafruit-updi-friend/pinouts), GND/PWR/UPDI breakout connections and voltage selector.
