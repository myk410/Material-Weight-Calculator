# PCB orientation and physical mating gate — R2.1 audit

**STATUS: FABRICATION HOLD.** The existing KiCad schematic, PCB, and Gerbers are *prototype drafts*. The prior ERC/DRC/netlist audits do not prove that a physically flipped plug or LCD is correctly connected. Do not submit Gerbers until each physical orientation gate below is passed.

## R3 implementation update (2026-11-12)

The LTC3440 supply is now implemented separately in `pcb/r3/`, with native ERC/DRC/parity passing. The regulator, diode and capacitor positions below describe **historical R2.1 only**. Use [R3_REVIEW.md](R3_REVIEW.md), its numbered top/bottom templates and actual-pad audit for current R3 component coordinates. The LCD/keypad/programmer/switch physical gates below remain open; selecting or routing R3 does not clear them.

## Coordinate/view convention

- **KiCad F.Cu view is the PCB component side, looking down onto the top surface.** Board X increases right and Y increases downward in the saved project.
- **B.Cu/underside view is MIRRORED relative to F.Cu.** A pin shown at the left in the top view appears at the right when viewing the board physically from its underside while preserving the same upward direction.
- For every male header, female socket, ribbon, and LCD tail: document whether the connector is approached **from above or below**, and whether the **contact side** or **solder side** is facing the viewer. Never use “leftmost pin” alone without the view definition.
- Use hard silkscreen markings: pad 1 as a square, labeled **1**, and connector key/stripe direction. The round-vs-square pad shape must be checked in actual rendered fabrication layers.
- Test using a printed **1:1 F.Cu** template plus a second **mirrored B.Cu** template. Overlay actual parts before sending the board for manufacture.

## Independent reference pins

AVR128DA28-I/SP, 28-pin SPDIP, **seen from the top of the chip with notch at the upper edge**: pin 1 upper left, pins 1–14 downward on left; 15 lower right to 28 upper right. From Microchip DS40002183E §2.1:
- 14 AVDD = 3.3 V; 15 GND; 19 UPDI; 20 VDD = 3.3 V; 21 GND.
- 23 PA1 LCD_CLK; 24 PA2 LCD_DATA; 25 PA3 LCD_CS; 26 PA4 LCD_CD; 27 PA5 LCD_RST.
- 13 PD7 LCD_PWR_CTRL.
- On **main PCB F.Cu**, U1 pin 1 center (35.00,20.00) mm; pin 28 (42.62,20.00) mm; pin 14 (35.00,53.02) mm; pin 15 (42.62,53.02) mm. MCU must be inserted **from F.Cu** with notch toward the pin 1/28 end. Never install the socket from the underside or rotate MCU 180 degrees.

EastRising ERC12864-655 series manufacturer Rev 1.0 datasheet, **page 7 outline drawing (front/viewing-side drawing), page 8 pin table**:
- 22 contacts, 1.27 mm pitch; center-to-center span 26.67 mm.
- LCD pins: 1 /CS0; 2 RST; 3 CD; 12 D6/SCK; 13 D7/SDA; 14 VDD; 15 VSS; 16–19 bias flying-cap pins; 20 VLCD; 21 BM0; 22 BM1.
- On **adapter PCB F.Cu design plan**, J2 pin 1 center (21.665,3.000) mm, pin 22 center (48.335,3.000) mm, increasing to the right.
- **Physical mating not yet signed off:** establish whether the display's protruding pins will meet the adapter's F.Cu or B.Cu face in the final enclosure, and whether the manufacturer's *front-view* row is being used from the same side as the PCB plan. A flip in the assembly may exchange LCD pin 1 with pad 22 without any DRC warning. Check actual LCD *viewing side*, pin-end faces, adapter component side, and module frame orientation with a paper board before soldering.
- The four long corner pins visible in photos are **mechanical/no-connect** terminals, **not** display signal pin 1 or 22. Do not count them as header contacts.
- Adapter J2 is a **soldered 22-hole interface**, not a socket or added header; verify pin diameter, pitch and available solder length.

## Other interfaces and direction checks

| Part | Top-view PCB pad numbering / electrical contract | Physical orientation task |
|---|---|---|
| Main U1 (socket) | notch at pin 1/28 end; pad 1 x35,y20 | Socket on F.Cu, chip notch aligned; continuity confirm real pins 14,15,19,20,21 to pads |
| Main J1 membrane keypad | 1..8 at x12; y22.54 to 40.32 at 2.54 pitch | Earlier user photo shows a black **female 1x8 termination** on the membrane ribbon, so PCB J1 must be populated with an actual **male 1x8 2.54 mm header** (footprint alone is not a connector). Verify its actual pitch and that the header pins enter all female contacts without bending. Measure ribbon row/column contact order with a meter, and check that the keypad can plug in from the PCB F.Cu side with enough height and correct ribbon exit. The photo alone does NOT prove that connector position 1 is ROW0 |
| Main J2 battery | 1 +switched battery x10,y9; 2 GND x10,y11.54 | Check actual red/black polarity at assembled wire connector, looking into mating plug vs PCB header |
| Main JP1 | 1 switched battery to 2 battery link | Service shunt; not the case slide switch |
| Main J3 LCD cable | 1 VCC, 2 GND, 3 SCK, 4 SDA, 5 CS, 6 CD, 7 RST, 8 NC; y16..33.78 | Cable must be continuity-mapped **by number**, not same-color/left-to-right appearance |
| Adapter J1 LCD cable | identical nets 1..8; x9..26.78 at y13 | J1 is rotated relative to main J3; a straight rigid stacking connection is **not** implied; seven individual wires must be deliberately mapped 1→1 through 7→7 |
| Main J4 UPDI | 1 VTREF/+3V3, 2 GND, 3 UPDI; x55,y46..51.08 | Compare to actual UPDI Friend header labels **as viewed from the connector mating side**, not assume its three pins use the same order |
| Main U2 regulator | MCP1700-3302E/TO TO-92 pins 1 GND, 2 VIN, 3 VOUT | Confirm genuine part's **flat/curved face** and exact manufacturer's footprint drawing; top-view and bottom-view reverse |
| Main Q1 transistor | onsemi 2N3906 TO-92 pins 1 emitter, 2 base, 3 collector | Confirm seller/manufacturer and flat-face orientation; generic 2N3906 variants may not share exact lead assignments |
| Main D1 | 1 cathode VIN; 2 anode battery link | Diode stripe/band must point to **VIN** pad |
| Adapter C5 | 1 positive LCD_VCC; 2 negative GND | Electrolytic stripe is **negative**; test before applying power |
| Slide switch | external case-mounted CYT1107, not a PCB footprint | Identify common terminal by continuity with slider at both positions; common to battery + and chosen outer terminal to J2 pin 1; battery − to J2 pin 2 |

## Reference links

- [EastRising series 20-page PDF, externally hosted](https://www.icbanq.com/icdownload/data/ICBShop/Board/ERC12864-655_Series_Datasheet.pdf) — especially pp. 7–9.
- [Original manufacturer PDF](https://www.buydisplay.com/download/manual/ERC12864-655_Series_Datasheet.pdf) (may return HTTP 403).
- [Microchip AVR128DA datasheet DS40002183E](https://www.microchip.com/content/dam/mchp/documents/MCU08/ProductDocuments/DataSheets/AVR128DA28-32-48-64-Data-Sheet-DS40002183.pdf), p.14.
- [Microchip MCP1700 datasheet](https://www.microchip.com/content/dam/mchp/documents/APID/ProductDocuments/DataSheets/MCP1700-Data-Sheet-20001826F.pdf).
- [onsemi 2N3906](https://www.onsemi.com/pdf/datasheet/2n3906-d.pdf).

## Mandatory go/no-go sequence

- [x] Independently recover saved main/adapter footprint pad numbers, xy positions and net assignments from electrical-design JSON (2026-11-12).
- [x] Compare AVR and LCD *logical* pin assignments to manufacturer pin tables.
- [ ] Verify through-hole mounting direction **F.Cu vs B.Cu** for every installed component; check physical board footprint orientation with manufacturer's *package view*.
- [ ] Physically superimpose LCD pins over 1:1 adapter **from the actual soldering side**; confirm which end is pin 1 (the pin rows MUST NOT be mirror-imaged).
- [ ] Check LCD mechanical NC/corner-pin clearance and adapter rear-side component clearance.
- [ ] Physically map the eight membrane ribbon conductors; no assumed connector pinout.
- [ ] Confirm male/female 2.54 mm connectors, cable exit, and 1-to-1 wire continuity between J3/J1; add polarized keyed solution where possible.
- [ ] Confirm UPDI Friend's exact pin label order against J4, from *mating face*.
- [ ] Verify MCP1700, 2N3906 and switch actual parts/terminal face orientation.
- [ ] Choose between currently implemented MCP1700 LDO/series diode and a revised low-Iq buck-boost regulator. **Current KiCad R2.1 uses MCP1700 LDO, despite the later discussion of buck-boost.** Any regulator change requires rerouting and complete review.
- [ ] Run KiCad ERC and DRC again **after** all board changes, compare netlist vs Gerbers, and have another orientation review from bottom and top.
- [ ] Only then mark fabrication release; first order should be a small prototype run, with current-limited bring-up and continuity testing.

**Engineering rule:** A “0 errors” ERC/DRC only checks the electrical CAD model. It cannot confirm an LCD physically inserted from the opposite face, a reversed removable cable, or a component's wrong package-view interpretation.
