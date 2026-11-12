# EastRising ERC12864FS-655 LCD — hardware reference

Status: manufacturer model identified from purchase listing; physical pin orientation, LCD bias circuitry and backlight connections still require verification before PCB fabrication.

## Manufacturer documentation

- [ERC12864-655 series datasheet (PDF)](https://www.buydisplay.com/download/manual/ERC12864-655_Series_Datasheet.pdf)
- [ERC12864-655 interfacing reference (PDF)](https://www.buydisplay.com/download/interfacing/ERC12864-655_Interfacing.pdf)
- [EastRising / BuyDisplay product page](https://www.buydisplay.com/2-8-inch-128x64-graphic-module-serial-display-spi-lcd-w-optl-touch-screen)

The links point to the manufacturer's original documents. PDF bytes are not bundled here because a verified download is not available in this session.

## Display specifications

- Model ordered: ERC12864FS-655
- 2.8-inch monochrome 128 x 64 graphic LCD, UC1701 controller (per manufacturer listing)
- 70.0 x 50.0 x 5.8 mm module envelope
- 3.3 V typical display logic supply
- SPI serial or parallel interface depending on mode configuration
- 22-pin connection row visible on the physical display
- Separate LED backlight; plan MCU-controlled switching to conserve AAA battery life

## Preliminary series connector reference — VERIFY against original datasheet before wiring

| Pin | Label | Notes |
| --- | --- | --- |
| 1 | /CS0 | Chip select |
| 2 | RST | Reset |
| 3 | CD | Command/data selection |
| 4 | WR0 | Parallel control; defined connection required in SPI mode |
| 5 | WR1 | Parallel control; defined connection required in SPI mode |
| 6–11 | D0–D5 | Parallel data; serial-mode treatment per interfacing drawing |
| 12 | D6 | SPI clock |
| 13 | D7 | SPI data |
| 14 | VDD | Display logic supply |
| 15 | VSS | Ground |
| 16–19 | VB0+, VB0−, VB1−, VB1+ | LCD charge-pump/bias connections; use prescribed capacitors |
| 20 | VLCD | LCD bias node: not an ordinary 3.3-V power pin |
| 21–22 | BM0, BM1 | Interface-mode controls; verify serial-mode straps |

**Important:** This is a working pin-reference transcription, not a fabrication-approved pin map. Confirm datasheet variant, exact connector view, pitch, mode straps, capacitor network, and LED polarity before electrical assembly.

## Material Weight Calculator integration

- MCU: Microchip AVR128DA28-I/SP, 28-pin SPDIP.
- Removable MCU socket: ED281DT, confirmed in DigiKey purchase email.
- UPDI Friend programmer: reserve accessible UPDI/GND/VTG programming header.
- Intended SPI connection from MCU to LCD to conserve GPIO.
- Separate transistor/MOSFET-switched LED backlight, with correct current limiting.
- Proposed pack: 3 AAA alkaline batteries (about 4.5 V nominal fresh), so **do not connect directly to 3.3-V LCD**.
- Add a **regulated 3.3-V supply** to the PCB. Low-quiescent-current buck-boost is preferred if usable cell capacity below 3.3 V is important; a simpler LDO may work but stops regulating earlier. Select an actual device and its required external components before layout.
- Keep the physical slide power switch, snap-fit battery compartment cover and resin case reinforcement ribs.

## Required before PCB sign-off

- [ ] Verify display's exact pin 1 orientation and mechanical footprint from manufacturer drawing.
- [ ] Confirm SPI mode strapping and unused input treatment.
- [ ] Copy reference LCD charge-pump capacitor network (values and voltage ratings).
- [ ] Verify separate backlight pin arrangement, voltage, and current.
- [ ] Choose 3.3-V regulator with appropriate dropout / conversion efficiency / quiescent draw.
- [ ] Bench-test display with current-limited 3.3-V supply before final integration.
