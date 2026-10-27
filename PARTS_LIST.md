# Parts list — reuse existing parts first

Updated October 27, 2026. The user confirmed owning the DIYmalls 4×4 membrane keypad shown in their screenshot. Relevant purchase records also identify Nano V3 boards, an ELEGOO Uno R3, HiLetgo ESP-WROOM-32 boards, ELEGOO jumper wires, and a five-piece I2C display-module order. Purchases establish prior acquisition, not that unused working spares remain available.

## Reuse for the first working prototype

| Qty | Part | Inventory evidence / use |
| ---: | --- | --- |
| 1 | DIYmalls 4×4, 16-key, 8-pin membrane keypad | Confirmed by user. Keep the entire membrane intact and conceal it under printed buttons. No sixteen-switch purchase needed. |
| 1 | Nano V3 / ATmega328P board | Prior purchase identified (LAFVIN listing B07G99NNXL). Compact controller for a first prototype using the small OLED. Check for a spare. |
| 1 | Small I2C OLED display module | Prior five-piece display-module order identified (B08L7QW7SR). The listing identifier appears to correspond to a 0.91-inch 128×32 SSD1306 OLED; confirm the physical module/controller and supply rating before wiring. Suitable for a compact, one-prompt-at-a-time UI test. |
| 10–14 | Dupont jumper leads | Prior ELEGOO 120-piece wire purchase identified (B01EV70C78). Eight keypad signal wires, two I2C signal wires, plus power/ground as needed. |
| 1 | USB cable matching the Nano | Check existing cables; used for programming and bench power. |
| 1 | Breadboard or temporary mounting board | Check parts bins; not confirmed in this inventory check. |

This prototype can test material selection, pipe/rectangular inputs, errors, button mechanics, and calculations without buying the previously proposed AVR or reflective display. The 128×32 screen requires a compact layout; it cannot show the full graphical simulator screen at once.

The Nano and its OLED are **not yet the final AAA power design**. A normal 5 V / 16 MHz Nano is not a drop-in match for the proposed 3.3 V rail. Do not feed a three-AAA pack into VIN and assume it provides regulated 5 V. A battery-powered Nano version would require a suitable supply and whole-board power measurements; its USB circuitry and LEDs may limit sleep savings.

An owned Uno can substitute on the bench. An owned ESP32 board is another prototype option, especially for the larger memory LCD, but board-level regulator/USB/LED current must be assessed before using it for long battery life. No need to buy another ESP32 for this project.

## Final hardware R1 parts

The exact reference-designator BOM and 22-nut M2.5 fastener list are in [hardware/README.md](hardware/README.md); the machine-readable BOM is [hardware/pcb/bom.csv](hardware/pcb/bom.csv). The following summarizes what to locate or buy for that board.

| Qty | Part | Reuse / purchase status |
| ---: | --- | --- |
| 1 | Existing DIYmalls membrane keypad | Reuse confirmed. |
| 1 | AVR128DA28-I/SP | User is checking this exact 28-pin DIP version; not marked purchased. |
| 1 | 28-pin DIP socket, 7.62 mm row spacing | Check stock. |
| 1 | Adafruit 3502 reflective memory LCD module | Not confirmed owned; reference design target. Verify availability and module revision. |
| 1 | MCP1700-3302E/TO, 3.3 V | Check stock / likely purchase. |
| 1 | 1N5817 diode | Check stock; reverse-battery protection. |
| 1 | 2N3906 PNP transistor | Check stock; display power switching. |
| 1 each | 10 kΩ and 100 kΩ axial resistors | Check stock. |
| 3 | 1 µF ceramic capacitors, at least 10 V, 2.5 mm lead pitch | Check stock. |
| 2 | 100 nF ceramic capacitors, at least 10 V, 2.5 mm lead pitch | Check stock. |
| 1 | Three-AAA holder, nominal 52 × 37 × 13 mm (Pololu 1144 envelope) | Not confirmed owned. |
| 3 | AAA alkaline cells | Check stock. |
| 1 set | 2.54 mm headers: 1×8, 1×9, 1×3, two 1×2; one shunt | Check stock; keypad, display, programmer, battery, master link. |
| 1 set | Existing jumper/hookup wire | Reuse where connectors fit. |
| 1 | Custom two-layer R1 PCB | Fabricate from included Gerbers/drills; PCB source and 1:1 copper artwork supplied. |
| 1 shared tool | 3 V SerialUPDI programmer | Adafruit UPDI Friend 5879 is a verified example. User also showed a generic switchable 3V/5V USB Serial UPDI board; correct type, specific seller's implementation unverified. CANADUINO's ATmega328P bootloader-only tool is incompatible. |
| 22 | M2.5 hex nuts | Glue into printed pockets; check existing stock. |
| 4 / 4 / 14 | M2.5 screws, 16 mm / 8 mm / 6 mm under-head lengths | Use existing matching lengths or obtain/trim as needed. |

The final R1 board uses a master shunt link instead of the earlier proposed external slide switch. Ordinary ON/OFF is keypad sleep/wake; removing a battery fully disconnects it. The discrete PNP transistor and two resistors implement the display switch, so no separate load-switch module is needed.

The standard driver for the 168×144 Sharp display requires a 3,024-byte framebuffer. A classic Nano/Uno has only 2 KB SRAM, so it cannot simply replace the AVR128DA28 in that configuration. A custom line-buffer driver would be a separate implementation choice, not assumed here.

Do not connect three fresh AAA cells directly to a bare 3 V display. Final power wiring must follow the selected module's voltage limits. Battery runtime remains unmeasured; the MCU's sleep specification alone is not the assembly's sleep current.

## Resin-printed parts

| Qty | Printed part | Material |
| ---: | --- | --- |
| 2 | Front shell sections with display bezel and sixteen button openings | Rigid resin |
| 2 | Rear shell sections | Rigid resin |
| 1 | Battery access cover | Rigid resin |
| 1 | Flat membrane-keypad backing plate | Rigid resin |
| 1 | Button guide/retainer | Rigid resin |
| 16 | Custom button caps, recessed labels and broad underside contact pads | Rubbery resin |
| As needed | Internal brackets/spacers | Rigid resin |

Use the already-established key layout from [MECHANICAL_DESIGN.md](MECHANICAL_DESIGN.md). Keep the buttons aligned over the existing membrane's key centers and remap their electrical positions in firmware. No need to expose the membrane's original printed labels.

## Suggested purchase order

1. Locate one spare Nano, one matching OLED, existing leads, and the confirmed keypad. Test the UI and printed button coupon using USB power.
2. Check stock for the small passive parts, AAA holder, connectors, and screws.
3. Source the final reflective display and low-power MCU only after choosing the display size. Complete the final power schematic and programmer choice before ordering the remaining electrical parts.

## Technical references

- [Arduino classic Nano specifications](https://store.arduino.cc/products/arduino-nano): 5 V operation and 2 KB SRAM. The user's clone requires confirmation against its actual board.
- [Microchip AVR128DA28 datasheet](https://ww1.microchip.com/downloads/aemDocuments/documents/MCU08/ProductDocuments/DataSheets/AVR128DA28-32-48-64-Data-Sheet-DS40002183.pdf): memory, packages, voltage limits, and programming.
- [Adafruit Sharp memory display 3502](https://www.adafruit.com/product/3502): interface, RAM needs, module supply, and size.
- [Microchip MCP1700 datasheet](https://www.microchip.com/content/dam/mchp/documents/APID/ProductDocuments/DataSheets/MCP1700-Data-Sheet-20001826F.pdf): regulator options, package pinouts, and required capacitors.
- [Parallax membrane keypad reference](https://www.parallax.com/products/4x4-matrix-membrane-keypad): similar 8-pin matrix construction. Its dimensions and pinout are not a verified drawing for the user's DIYmalls pad.

Exact key pitch, active contact centers, ribbon exit, connector pinout, display variant, and mounting geometry must be established from the actual selected parts or their matching drawings before final CAD. The screenshot is sufficient to identify the keypad type, not its fabrication dimensions.
