# R3 buck-boost circuit — draft, not yet a routed PCB

**STATUS: DO NOT ORDER PCB FROM EXISTING R2.1 GERBERS.** The existing KiCad design still includes MCP1700 LDO. This revision captures the new exact 3.3 V switching supply circuit and pin mapping for implementation in KiCad.

## Verified manufacturer reference
[Analog Devices LTC3440 PDF](https://www.analog.com/media/en/technical-documentation/data-sheets/3440fd.pdf), **PDF page 1** shows the 3.3 V 600 mA buck-boost application; **page 2** shows the MSOP-10 top-view pinout. The application is originally drawn for 2.7–4.2 V lithium-ion input; our 3-AAA 2.5–5.5 V range must be separately validated.

[Machine-readable reference netlist](power_r3_reference.json) | [preliminary parts BOM](power_r3_bom.csv) | [orientation/pin test](check_power_r3.py).

## LTC3440 MSOP-10 pin map (IC **TOP** view, with pin 1 marker at upper left)
| Pin | Pin name | Proposed PCB net |
|---:|---|---|
| 1 | RT | RT to 60.4 kΩ resistor to GND |
| 2 | MODE/SYNC | MODE, linked to regulated 3.3 V for Burst Mode |
| 3 | SW1 | One end of 10 µH inductor |
| 4 | SW2 | Other end of 10 µH inductor |
| 5 | GND | Ground plane |
| 6 | VOUT | Regulated 3.3 V |
| 7 | VIN | Protected switched battery input |
| 8 | SHDN/SS | Protected switched battery input, enabled when physical switch on |
| 9 | FB | 340 kΩ to 3.3 V and 200 kΩ to ground |
| 10 | VC | Series 15 kΩ + 1.5 nF compensation branch to GND |

Feedback nominal target using datasheet reference: 1.22 V × (1 + 340/200) = 3.294 V. Manufacturer gives 3.3 V nominal.

**The original manufacturer's illustration must remain the authority** for analog compensation placement; a CAD schematic is not complete until all nets are visually compared against the PDF.

## Assembly

- Only **LTC3440EMS#PBF**, MSOP-10 with visible gull-wing legs. **Do not substitute LTC3440EDD** (DFN with hidden underside pad).
- Pin pitch 0.5 mm; use flux, fine solder, wick, magnification, and enlarged solder-mask openings/accessible toe fillets. Verify footprint pad center positions against package drawing; no assumed mirroring.
- Prefer 0805 resistors and 1206/1210 ceramics; verify actual physical footprints, component values and effective capacitance at bias.
- Inductor must be chosen with 10 µH, adequate saturation/current rating and iron-accessible solder joints.
- Keep high-frequency loop SW1/inductor/SW2 very short; place CIN close to VIN/GND and COUT close to VOUT/GND; keep FB node and VC away from switch copper. Follow datasheet layout recommendations.
- Existing 1N5817 protection diode is retained provisionally. Its voltage drop will affect when the unit stops working on discharged batteries; check whether reverse-polarity MOSFET protection is preferable before release.

## Not completed

The old routing and Gerbers are untouched. No new KiCad schematic has been created in this commit. **KiCad isn't installed in the active execution environment**, so native ERC/DRC or finished copper cannot honestly be claimed. Before fabrication, all old U2 footprints and circuit nets must be replaced with this new topology, a new footprint and mechanical review must pass, then first-article power tests must be conducted.

The existing [PCB orientation gate](../PCB_ORIENTATION_GATE.md) remains mandatory for LCD, keypad, programmer and all polarized parts.
