# Purchased parts retained; discrete parts use SMD

Updated 2026-11-12 after the user's clarification: **keep the socket and bought parts; use hand-solderable SMD for the booster, resistors, capacitors and similar components.** This supersedes the mixed through-hole/SMD interpretation in the first R3 commit.

## Retained hardware

- AVR128DA28-I/SP chips and ED281DT DIP sockets: purchase-confirmed, five of each. U1 remains a removable 28-pin DIP; no new surface-mount MCU is required. The socket, notch direction and every pad center remain unchanged.
- The two purchased EastRising ERC12864FS-655 displays, selected DIYmalls membrane keypad, existing UPDI programming hardware, case slide switch and wiring/connector plan remain in use. No alternate display, keypad or programmer is introduced.
- Existing 0603 resistor/capacitor kits remain usable stock. Board footprints now accommodate 0603 small passives with extended hand-solder lands. Reuse a kit part when its value, tolerance, voltage rating, dielectric, effective capacitance and body dimensions meet the specific BOM line; do not purchase an equivalent unnecessarily. Unknown kit voltage/dielectric is **not** proof of suitability.
- Owned 2N7002 SOT-23 MOSFETs remain useful stock, but cannot replace the PNP high-side display switch by matching package shape. Q1 requires MMBT3906LT1G (PNP), not 2N7002 (N-channel MOSFET). No owned component is discarded.

## Current board implementation

| Group | Main R3 | R3 display adapter |
| --- | --- | --- |
| Controller | Purchased DIP chip in purchased socket | Purchased LCD solder-pin landing |
| Connectors | Existing through-hole male headers / service link | Same LCD and cable contact coordinates as before |
| Small existing-function resistors | R1/R2: 0603, 10 kΩ / 100 kΩ | R1: 0603, 10 MΩ |
| Small decoupling / bypass | C3/C4: 0603 100 nF; C5: 0603 2.2 µF | C1/C2: 0603 2.2 µF; C3: 0603 330 nF; C4: 0603 100 nF |
| Converter precision / compensation | Hand-solder 0805; unchanged LTC3440 circuit | Not applicable |
| Power bulk capacitors | C1 10 µF: 1206; C2 22 µF: 1210 | C5 10 µF: 1206 ceramic, nonpolar |
| Display switch | Q1: MMBT3906LT1G, hand-solder SOT-23 | Not applicable |
| Converter, inductor, diodes | LTC3440 MSOP-10, accessible inductor lands, SMA / CFP3 diodes | Not applicable |

**All resistors, capacitors, diodes, transistors and inductors on both current R3 boards are SMD.** The independent saved-board audit enforces this, while explicitly retaining DIP U1 and through-hole connector interfaces.

Main and adapter 2.2 µF 0603 parts have selected 25 V X5R reference MPN GRM188R61E225KA12D. Their nominal value and voltage rating alone do not establish effective capacitance. Flying-capacitor performance, VLCD ripple, LCD startup and contrast still require qualification. Use a kit part only if those requirements are met; the larger 1206/1210 converter capacitors must not be replaced by unidentified 0603 stock.

The adapter's former polarized electrolytic C5 is now a nonpolar 10 µF ceramic. The current adapter is [pcb/r3/display_adapter](pcb/r3/display_adapter/display_adapter.kicad_pro). The old adapter under `pcb/display_adapter` is preserved historical R2.1, not the SMD board.

## Q1 orientation: do not copy the old pin numbers

Manufacturer [onsemi MMBT3906 datasheet](https://www.onsemi.com/pdf/datasheet/mmbt3906lt1-d.pdf), case 318 style 6, specifies **1 base, 2 emitter, 3 collector**. The old through-hole 2N3906 footprint used E/B/C numbering instead.

The new footprint is installed from **F.Cu**, center (58,15) mm. Top-view pads: 1 B at (56.5,14.05), 2 E at (56.5,15.95), 3 C at (59.5,15). Looking from the physical underside mirrors X: base/emitter appear on the right and collector on the left. This projected underside image is not the installation side. The independent audit and a deliberate B/E-swap negative test enforce the new mapping.

Gerbers remain withheld while the existing physical mating, kit/component qualification and populated-fit checks are unresolved. See [R3_REVIEW.md](R3_REVIEW.md).
