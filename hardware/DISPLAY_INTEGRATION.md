# R2 display integration: ERC12864FS-655

This revision selects the **EastRising ERC12864FS-655**, 2.8-inch 128 × 64 positive FSTN monochrome LCD, metal-pin version, **without the optional touch panel**. It replaces Adafruit 3502 throughout the current hardware package. Do not mix an R1 main PCB or cradle with R2 wiring.

The manufacturer's product page lists a 70 × 50 × 5.8 mm maximum body and 67 × 37 mm viewing area. The drawing gives 63.95 × 31.95 mm active pixels (the store's text instead says 31.65 mm high); the CAD uses the **viewing window**, so this discrepancy does not crop the pixel area. The viewing area begins 1.5 mm from the left and 3.5 mm from the top of the module. The 22 electrical pins have **1.27 mm pitch**, 26.67 mm from first to last; the separate corner NC pins/backlight contacts are not the signal header.

## Source audit

- [Product and ordering options](https://www.buydisplay.com/2-8-inch-128x64-graphic-module-serial-display-spi-lcd-w-optl-touch-screen)
- [EastRising series datasheet, Rev 1.0](https://www.buydisplay.com/download/manual/ERC12864-655_Series_Datasheet.pdf): p4 identifies FS as positive FSTN; p6 specifications; p7 mechanical drawing; p8 pin table; p9 electrical limits. A [hosted copy of the same manufacturer document](https://www.icbanq.com/icdownload/data/ICBShop/Board/ERC12864-655_Series_Datasheet.pdf) was used when the manufacturer download returned an access error.
- [EastRising SPI reference circuit, dated 21-Apr-2020](https://www.buydisplay.com/download/interfacing/ERC12864-655_Interfacing.pdf): flying capacitors 2.2 µF, VLCD capacitor 0.33 µF / 25 V with 10 MΩ discharge resistor, supply bypass 100 nF + 10 µF.

These are the manufacturer's own design documents. The earlier similarly named FS-655 one-page drawing from another supplier is not the authority for this PCB. Positive FSTN is not e-paper. The seller lists this variant as sunlight-readable; actual contrast with the backlight disconnected in the intended shop lighting still needs a sample test.

## Electrical connections

Both boards run at regulated 3.3 V. Do not attach the raw AAA pack, a 5 V programmer output, or 5 V logic to this LCD. The module's allowed operating supply is 3.0–3.6 V. Its internal charge pump generates LCD bias; **VLCD is not a 3.3 V power input**.

| LCD pin | Name | R2 connection |
| ---: | --- | --- |
| 1 | /CS0 | Main J3.5, PA3 |
| 2 | RST | Main J3.7, PA5; active low |
| 3 | CD | Main J3.6, PA4; low commands/high pixels |
| 4 | WR0 | Ground |
| 5 | WR1 | Ground |
| 6–11 | D0–D5 | Ground, unused in SPI |
| 12 | D6 / SCK | Main J3.3, PA1 |
| 13 | D7 / SDA | Main J3.4, PA2 |
| 14 | VDD | Switched 3.3 V, main J3.1 |
| 15 | VSS | Ground, main J3.2 |
| 16 | VB0+ | Adapter C1 to pin 17 |
| 17 | VB0− | Adapter C1 to pin 16 |
| 18 | VB1− | Adapter C2 to pin 19 |
| 19 | VB1+ | Adapter C2 to pin 18 |
| 20 | VLCD | Adapter C3 and R1 to ground |
| 21 | BM0 | Ground |
| 22 | BM1 | Ground; selects four-wire SPI |

Adapter J2 uses the manufacturer's pin numbering. Verify pin 1 from the **front-view drawing**, not from an assumed rear-view left/right sequence. Main J3 and adapter J1 have identical pin numbers: 1 VCC, 2 ground, 3 clock, 4 data, 5 /CS, 6 CD, 7 /RST, 8 spare **no connection**. Solder seven insulated wires at the adapter end. Keep wiring short, approximately 50 mm; use slow SPI initially (100 kHz) and inspect the waveform if problems occur. The controller's SPI bus is independent of the keypad scan.

The separate backlight **A/K terminals are left unconnected and insulated**. No backlight drive circuit is included. The manufacturer's LCD current limit is 500 µA at 3.3 V, whereas its backlight alone is listed at approximately 60 mA. This is a display specification, not the assembled calculator's measured current. The PNP switch's base current, MCU, LDO and leakage add consumption. Power off the display during sleep; no runtime claim is made without measurements. The LCD cannot retain a visible result with its power removed.

## Adapter parts and physical assembly

The main PCB stays 82 × 68 mm; the new adapter is 70 × 18 mm. Both are two-layer 1.6 mm FR-4 with plated holes. The LCD's 22 pins solder directly into the adapter's 1.27 mm holes; **do not fit a second male header or socket there**. Board J1 is a 2.54 mm pitch wire landing, not a tall plug in the assembled case.

| Adapter ref | Part | Connection |
| --- | --- | --- |
| C1 | 2.2 µF ceramic, 25 V, 2.5 mm lead pitch | VB0+ to VB0− |
| C2 | 2.2 µF ceramic, 25 V, 2.5 mm lead pitch | VB1+ to VB1− |
| C3 | 330 nF ceramic, 25 V, 2.5 mm lead pitch | VLCD to ground |
| C4 | 100 nF ceramic, 25 V, 2.5 mm lead pitch | VDD to ground |
| C5 | 10 µF low-leakage electrolytic, ≥16 V, 4 mm diameter, 1.5 mm lead pitch | Positive to VDD, negative to ground |
| R1 | 10 MΩ axial, 7.62 mm lead pitch | VLCD to ground |

Ceramic footprints are 3 × 1.6 mm nominal; select parts that fit or revise the footprints before ordering. Do not force a larger capacitor body against an adjacent pad. Keep C5 ≤7 mm high and other adapter parts ≤5 mm high. Adapter plan origin is (13,5.7) mm, with its pin row at Y=8.7 mm. Two 2.1 mm NPTH clearances pass the module’s top NC pins; two rear-cradle reliefs clear the lower NC pins. Adapter lower face is nominal Z=13 mm; LCD body rear Z=22.1 mm. Trim solder leads, insulate exposed tails, and keep at least 0.5 mm between component bodies and the display rear frame. Confirm actual module-pin reach before final soldering. A printed display-fit template shows the pin spacing; direct mating remains physically untested.

Four M2.5 screws hold the rear cradle. Thin 0.5 mm closed-cell foam supports only the opaque front perimeter and rear frame. No adhesive on the polarizer, no hard screw load through glass, no support against the flex/COG area. Cable strain relief attaches to a cradle side rail. The adapter is located by its 22 soldered module pins; its cable must carry no external load. The original 16 custom flexible caps and all keypad functions remain the same.

## Firmware/display UI contract

Device firmware remains pending. R2 is a hardware and interface revision, not a flashed working calculator. Implement these requirements before powering a populated assembly for normal use:

1. Configure PA1/PA2 for clock/data, PA3 chip-select, PA4 command/data, PA5 reset. The current routed pins assume software SPI or an explicitly verified peripheral pin route, not an assumed default Arduino SPI mapping. PA1/2/3/4/5 correspond to DIP pins 23/24/25/26/27.
2. Keep LCD signal outputs low while Q1 is off to avoid backfeeding. PD7 low enables Q1, high disables it; R2 holds Q1 off during MCU reset.
3. At wake, enable power, allow the rail to settle, apply the UC1701 hardware reset and initialization per the controller/module example, set contrast/bias, clear RAM and draw the screen. Verify segment/COM orientation and column offset on the actual panel using a border and corner labels. Do not reuse a Sharp memory-LCD driver, its pixel format, or VCOM task.
4. Use a 1,024-byte 128 × 64 monochrome framebuffer, or equivalent page rendering. A 6 × 8 font gives 21 characters × 8 lines. Long material names scroll or abbreviate while retaining an unambiguous grade in the material-selection page.
5. Input page: title, material, shape, field prompt, entered value in inches, validation/status, and navigation hint. Show one editable dimension at a time. Pipe prompts are length, outside diameter and wall thickness, with inside-diameter mode selectable in the menu.
6. Result page: abbreviated material and shape at top, weight in a large approximately 16-pixel font with `lb`, then ounces/entered dimensions and `ENTER new / BACK edit`. Show errors as text; never present a stale result after editing an input.
7. All sixteen keys retain the documented layout. MENU contains Material, Shape, Density and Resume. 8/2 navigate; ENTER chooses; BACK returns or deletes; CLEAR clears the field. ON/OFF enters sleep. After the inactivity timeout, shut down the display; the first key wakes and is consumed.
8. Save transient calculation state in MCU RAM for sleep/wake. Redraw on wake. Disable unused peripherals and measure sleep/active current on the completed assembly before estimating battery life. Three alkaline AAA cells remain the supply; the 3.3 V LDO plus protection diode impose an early end-of-discharge limit.

## Prototype acceptance checks

Print the two alignment templates and one key coupon. Check display corners, 22-pin centers and actual solder-pin reach; verify the cured cradle and foam do not bow the glass. With the LCD disconnected, check main-board 3.3 V and Q1 switching. With current-limited power, verify adapter pin 14 supply and pin 15 ground, BM1 low, both flying capacitors and VLCD components, and C5 polarity. Bring up border/corner labels, then the calculator UI. Check ambient-light contrast with A/K disconnected, repeated sleep/wake, display power-off leakage, all keys and pipe input. Digital DRC/net checks do not replace these tests.
