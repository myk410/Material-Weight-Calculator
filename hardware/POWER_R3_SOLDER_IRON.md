# R3 power redesign — hand-solderable SMD preference

**Updated 2026-11-12. Status: design candidate only, NOT schematic/PCB release.**

## Assembly requirements
User **prefers SMD/SMT** components soldered directly onto the main PCB, using a **regular soldering iron only**, no hot air or oven. Prefer externally accessible gull-wing leads, generously extended pads, flux and drag soldering. Reject QFN/WSON/DFN parts with hidden pads. The previously explored factory-assembled Pololu S7V8F3 module is now a fallback, **not** the preferred solution.

## Preferred IC candidate: Analog Devices LTC3440EMS#PBF (MSOP-10)

- [Official product page](https://www.analog.com/en/products/ltc3440.html)
- [Manufacturer full datasheet PDF](https://www.analog.com/media/en/technical-documentation/data-sheets/3440fd.pdf)
- [MSOP-10 manufacturer package drawing](https://www.analog.com/en/products/ltc3440.html) (choose the **MS** package, not **DD/DFN**).
- Input range 2.5–5.5 V; output adjusted to 3.3 V by feedback divider. Appropriate for 3 alkaline AAA cells over 2.5–5.5 V, subject to battery sag.
- 25 µA typical quiescent current in Burst Mode; under 1 µA specified shutdown current. Complete assembled system consumption remains unmeasured.
- Manufacturer claims up to 96% efficiency and up to 600 mA output under specified conditions; do not assume either at very light actual loads.
- MSOP-10 has **visible side leads at 0.5 mm pitch** and manufacturer's top-view pin diagram without a mandatory exposed underside pad. The **DFN** variant has an exposed pad that must be soldered and is NOT acceptable.
- 0.5 mm lead pitch is challenging but hand-solderable with a suitable tip, plenty of flux, solder wick, magnification and practice. Confirm the user's comfort before ordering.

### Independent TOP-view orientation (MSOP-10, looking at lettering from ABOVE, with pin-1 marker at upper-left)

```
          LTC3440EMS#PBF
     RT  1 |             | 10 VC
   MODE  2 |             |  9 FB
    SW1  3 |             |  8 SHDN/SS
    SW2  4 |             |  7 VIN
    GND  5 |_____________|  6 VOUT
```

This is an **IC package top view**, NOT a PCB underside view. The PCB F.Cu pads must mirror neither column. Place pin-1 dot and visual flat-edge marker on silkscreen. The footprint must be checked against Analog Devices MSOP drawing, and Gerber F.Cu/B.Cu rendered separately for orientation review.

### Circuit tasks (not yet implemented)

1. Copy the manufacturer's **3.3V typical application** as the starting point; select and verify the 10 µH inductor, input/output ceramic capacitors, RT resistor, FB upper/lower divider, VC compensation and shutdown soft-start circuitry from datasheet. Prefer 0805/1206 passives or leaded alternatives where electrically valid; ensure the required capacitance under DC bias.
2. Set MODE/SYNC high for low-Iq Burst Mode when suitable; verify behavior/noise at expected LCD current.
3. Retain the 3-AAA battery holder and physical switch. Determine polarity protection approach with low enough voltage drop to retain useful battery capacity; assess any leakage.
4. Verify power-up with batteries fresh (including open-circuit voltage), battery depletion, current transients during LCD startup and high-frequency ripple, using the actual LCD adapter and MCU.
5. Regenerate main PCB KiCad schematic/layout/netlist/BOM/Gerbers to replace MCP1700 power supply only after full circuit selection, then run independent pin-map, physical top/bottom, DRC/ERC, and prototype bring-up checks.
6. The power redesign must preserve the LCD 22-pin orientation gate, AVR socket notch, keypad J1 contact ordering and programmer J4 mating checks.

**Warning:** Existing KiCad R2.1 files and all previously generated Gerbers **still use the MCP1700 LDO**. Merely selecting this IC does not update copper. They remain on FABRICATION HOLD.

## Previous candidates

- TPS63900: electrically attractive but WSON with hidden pad; reject for user's soldering setup.
- Pololu S7V8F3: manufacturer-assembled buck-boost module with through-hole leads; retain only as fallback if MSOP-10 soldering is too fine.
