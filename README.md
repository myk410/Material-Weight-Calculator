# Material Weight Calculator

A standalone pocket calculator for estimating material weight. Select a material, enter length, width, and thickness in inches, and read the result in pounds. Runs entirely on one microcontroller with physical buttons and replaceable AAA batteries.

Status: proposed hardware design, October 27, 2026. The existing HTML example has been reviewed and preserved. Hardware, firmware, wiring, and battery life have not yet been tested.

## Recommended first build

| Part | Proposed choice | Reason |
| --- | --- | --- |
| Controller | Microchip AVR128DA28, preferably the through-hole package for a hand-built prototype | One low-power microcontroller; enough RAM for a graphical display; internal oscillator; no wireless hardware needed |
| Display | Reflective Sharp memory LCD; Adafruit 3502, 1.3-inch 168 × 144 breakout is the reference candidate | Paper-like, daylight-readable screen with fast updates and no backlight |
| Buttons | Passive 4 × 4 matrix keypad, with calculator labels | Sixteen physical keys using eight controller pins; no separate keypad processor |
| Batteries | Three AAA alkaline cells in a replaceable holder | Simple power supply using a low-quiescent-current linear regulator |
| Regulator | MCP1700, 3.0 V output variant | Typical quiescent current of 1.6 µA; common 3 V rail for the controller and display interface |
| Supporting parts | Regulator input/output capacitors, local MCU decoupling, battery protection, switch, programming header | Reliable supply and a way to program the controller without leaving a USB interface powered |
| Housing | Small calculator-style enclosure with accessible battery compartment | Large readable labels and easy battery replacement |

These are design candidates, not a purchase-ready bill of materials. Adafruit's reference display was listed as out of stock when checked. Its viewable area is only about 24.5 × 21 mm: check text readability before committing to this size. A larger reflective display may be better for shop use.

The AVR128DA28 has 16 KB SRAM. The reference display's monochrome framebuffer needs 3,024 bytes, leaving room for the application. An ATmega328P's 2 KB SRAM is too small for this display's standard full-buffer driver. Verify the chosen graphics library and AVR core together during prototyping.

## Why memory LCD instead of e-paper?

| Display | Suitability |
| --- | --- |
| Reflective memory LCD | Recommended for calculator entry: quick digit updates, low power, readable by reflected light. Requires power and periodic display polarity inversion while displaying an image. |
| Black-and-white e-paper | Excellent for holding a result with display power removed. Updates are slower and may show ghosting or occasional full-screen flashes; partial-refresh behavior depends on the exact panel. |
| Reflective character LCD without a backlight | Worth considering if a cheaper, simpler text-only display is preferred. Select a specific low-power module before comparing total current; ordinary hobby modules are not all equally efficient. |

E-paper is compatible with a microcontroller and does not require a Raspberry Pi. For this device, fast keypad feedback makes memory LCD the stronger starting point. Neither unlit option is readable in darkness without external light.

## User operation

1. Press ON to wake the calculator.
2. Press MAT to cycle through named materials; press ENTER to select. Default to the last material during the current powered session.
3. Enter length in inches; press ENTER.
4. Enter width in inches; press ENTER.
5. Enter thickness in inches; press ENTER.
6. Show the material, dimensions, and estimated pounds, with the weight in the largest text.

Key functions: digits 0–9, decimal point, ENTER, MAT, BACK, CLEAR, and ON/OFF. This fits a 16-key matrix. A generic keypad can be relabeled for the prototype; tactile calculator-style keys are preferable for the finished housing.

BACK deletes the last digit; with an empty field it returns to the previous field. CLEAR starts a new calculation while retaining the selected material. ON/OFF puts the calculator to sleep. Do not use long-press combinations for routine entry. Start with decimal inches; fraction entry can be added if needed after testing the controls.

Reject empty fields, zero or negative dimensions, malformed numbers, overflow, and values beyond the supported input range. Display an explicit error instead of a plausible-looking weight. Always label the result as an estimate.

## Calculation and material data

For a solid rectangular piece:

`weight_lb = length_in × width_in × thickness_in × density_lb_per_ft3 / 1728`

Example using the HTML's steel density: `12 × 12 × 1 × 490 / 1728 = 40.8333… lb`, displayed as `40.83 lb`.

The original HTML accepts volume directly. Firmware will calculate volume from the three entered dimensions. Its pounds-to-total-ounces conversion is valid, but pounds should be the primary handheld result.

Three outside dimensions describe a solid rectangular piece. They do not determine the volume of a pipe, hollow section, cylinder, or irregular part. Those need separate shape formulas and additional inputs. Version one should explicitly identify its shape as solid rectangular stock.

The original material list contains Poly, Water, Aluminum, Titanium, Steel, Stainless, Inconel, Brass, CuNi, NiCu, and Lead. It is a useful starting point, but the entries need a density review before firmware release:

- Titanium is currently assigned 168 lb/ft³, identical to aluminum. ATI lists commercially pure Grade 2 titanium at 0.163 lb/in³, equivalent to 281.664 lb/ft³. This correction must identify the grade; it is not a universal value for every titanium alloy.
- Names such as Poly, Stainless, Inconel, CuNi, and NiCu describe families. Specify the actual polymer/alloy or clearly mark a default as approximate.
- Store one canonical density value per material. Derive any other density units from it instead of copying inconsistent rounded reference columns.
- Include a Custom Density option in lb/ft³ for materials outside the preset list. The user must supply a known density; dimensions and a material name alone cannot identify every material's density.

Do not silently carry the original density table into production firmware. The original HTML remains unchanged as the supplied reference.

## Battery and sleep design

Use three AAA alkaline cells through a 3.0 V MCP1700 regulator. Check the regulator's selected ordering code, input rating, dropout at the actual load, capacitor requirements, and the exact display breakout's regulator path before finalizing the schematic. A 3.0 V source feeding a breakout's onboard regulator may reduce its output; confirm adequate display voltage rather than assuming the breakout has no dropout.

Two AAA cells are possible, but a regulated 3 V display supply would require a boost or buck-boost converter as the cells discharge. Three cells with an LDO are the proposed simpler circuit. The LDO will leave some battery capacity unused near the end of discharge.

- While active, scan/debounce keys and update changed content. Keep required memory-LCD polarity inversion running at the panel's specified interval; the Adafruit example calls for servicing at least once per second.
- After about two minutes without input, save current state in RAM, blank the display, shut the display down according to its documentation, disable unused peripherals, and enter MCU power-down mode.
- If display power is switched off, put connected signal pins in a safe state to prevent back-powering. Reinitialize and redraw on wake.
- Wake from a keypad interrupt. In sleep, drive matrix columns low and use pulled-up interrupt-capable row inputs. Confirm exact AVR pin wake behavior before assigning pins. Consume the wake press so it does not enter a stray digit. Wait for key release before accepting another entry.
- Avoid continuous keypad polling during sleep, always-on LEDs, powered USB adapters, and continuously connected battery-sense resistor dividers.
- Use a mechanical master switch for complete battery disconnection. Normal ON/OFF is sleep; RAM state is lost after battery removal or master power-off.

Battery-life goals must use measured current for the entire assembly, including display breakout and regulator. Initial targets are below 10 µA in automatic sleep and a few mA while actively used; these are goals, not verified specifications.

Illustrative budget only: at 5 mA for 20 minutes per day plus 10 µA for the rest of the day, consumption is about 1.90 mAh/day. An assumed usable pack capacity of 800 mAh gives about 420 days arithmetically. Real runtime will depend on cutoff voltage, cell type, regulator dropout, temperature, leakage, and usage. Series-connected AAA cells raise voltage; their mAh capacities do not add.

## Build sequence

1. Confirm a readable display size and source the exact module.
2. Prototype the controller, display, and relabeled keypad. Use a detachable UPDI programmer; it is a setup tool, not part of the running device.
3. Implement the material menu, three input fields, calculation, and input validation. Check known rectangular-stock examples and custom density.
4. Implement keypad wake and display shutdown. Measure whole-device active and sleep current from the battery input.
5. Validate operation over the usable battery voltage range, including low-battery indication and clean handling of power loss.
6. Finalize the schematic, component list, firmware build instructions, and enclosure after these checks.

## Manufacturer references

- [Microchip AVR128DA28](https://www.microchip.com/en-us/product/AVR128DA28) and its linked datasheet: voltage limits, memory, sleep behavior, pin functions, and programming.
- [Microchip MCP1700](https://www.microchip.com/en-us/product/MCP1700) and its linked datasheet: quiescent current, voltage options, dropout, and capacitors.
- [Adafruit 3502 Sharp memory LCD](https://www.adafruit.com/product/3502): module dimensions, interface, framebuffer requirements, and display characteristics.
- [Adafruit Sharp display example](https://github.com/adafruit/Adafruit_SHARP_Memory_Display/blob/master/examples/sharpmemtest/sharpmemtest.ino): periodic display servicing.
- [Waveshare e-paper manual](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT_Manual): refresh and standby considerations for an alternative display.
- [ATI corrosion-resistant titanium datasheet](https://www.atimaterials.com/Products/Documents/datasheets/titanium/alloyed/ati_corrosion_resistant_titanium%20_alloys_tds_en5_v1.pdf): grade-specific titanium density.
