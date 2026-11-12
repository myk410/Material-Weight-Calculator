# R3 power redesign — soldering-iron assembly

Updated 2026-11-12. **Implemented in [pcb/r3](pcb/r3/); FABRICATION HOLD pending physical checks.** Read [R3 review](R3_REVIEW.md) and [electrical implementation](source/POWER_R3_IMPLEMENTATION.md).

The selected IC is **LTC3440EMS#PBF in MSOP-10**, with visible 0.5 mm pitch gull-wing leads and no required underside thermal pad. The DFN LTC3440EDD is not interchangeable and must not be fitted. New regulator resistors/compensation/snubber capacitors use 0805 hand-solder lands; CIN uses 1206 and COUT 1210. The Sumida inductor has extended external toes for iron access. The purchased DIP/socket and connector interfaces are retained; all discrete parts on both R3 boards are SMD. See [owned-parts policy](OWNED_PARTS_AND_SMD.md).

The assembly is intended for a regular iron, flux, fine solder, wick and magnification. Solder one corner to align all ten leads before completing the package. Inspect each gap and test for bridges with power disconnected. 0.5 mm pitch remains a precision hand-soldering task; no hot air or oven is required by the chosen regulator package. Never pre-approve an unverified substitute by package name alone.

## MSOP-10 top-view numbering

Looking onto the IC lettering, pin-1 marker at upper left:

| Left, top to bottom | Right, top to bottom |
| --- | --- |
| 1 RT | 10 VC |
| 2 MODE/SYNC | 9 FB |
| 3 SW1 | 8 SHDN/SS |
| 4 SW2 | 7 VIN |
| 5 GND | 6 VOUT |

The F.Cu footprint uses exactly this view. The mirrored underside drawing reverses the columns; it is not the installation view. See the numbered [1:1 main template](docs/r3/main_orientation_1to1.svg) and the [ADI MS package drawing](reference/LTC3440_3440fd.pdf), page 20.

The earlier proposed VC-to-GND compensation was incorrect: actual R3 is **VC → 15 kΩ → 1.5 nF → FB**. The MODE link is to VIN. The circuit includes ADI's protection for possible VIN above 4.5 V. The full selected-part list and current checks are in the review.

No R3 Gerbers, drills or manufacturing ZIP are available until the actual LCD/keypad/cable/programmer/switch orientations, part fits and capacitance qualification are evidenced. Existing R2 fabrication files use MCP1700 and must not be ordered as R3. The assembled supply still requires prototype stability/startup/ripple/current testing.
