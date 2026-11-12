# R3 power revision — soldering-iron assembly only

**Design constraint confirmed November 12, 2026:** User has a conventional soldering iron, **no hot air, no reflow oven**. Do NOT select WSON/QFN/BGA/underbody-pad regulators for user assembly. Prior TPS63900 proposal is rejected for this build; the TPS63900 has an exposed thermal pad requiring a different assembly process.

## Proposed implementation

Use a **factory-populated 3.3 V buck-boost regulator daughterboard** installed onto a custom through-hole footprint on the main PCB, with ordinary 2.54 mm headers. This retains one unified board assembly in the enclosure, but the switching IC, inductor and tiny SMD parts are already factory soldered to the module. The user only solders accessible through-hole pins.

**Candidate: Pololu S7V8F3, product #2122**:
- [Manufacturer and assembly information](https://www.pololu.com/product/2122)
- [Specifications](https://www.pololu.com/product/2122/specs)
- [Official dimensions, drill guide and schematic](https://www.pololu.com/product/2122/resources)
- VIN 2.7–11.8 V, fixed VOUT 3.3 V.
- Manufacturer lists <0.1 mA enabled, no-load quiescent current. That is **not** the complete calculator sleep current. The preassembled module is less ultra-low-power than the previously considered TPS63900, so measure resulting battery life.
- Four module connections: VIN, GND, VOUT and SHDN. Physical positions must be taken from **Pololu's actual board drawing and hole map**; DO NOT infer order from this prose or from a generic 1×4 header footprint.
- **No integrated reverse-polarity protection.** Design battery protection ahead of VIN and confirm voltage drop / cutoff at three-cell depletion.
- Module dimensions approximately 11 × 17 × 3 mm excluding optional header projections. Final height depends on chosen mounting and solder tail positions.
- It can be mounted with soldered male headers or suitable female sockets depending on clearance; select the exact option before footprint and enclosure checks.
- SHDN may be left open to enable the regulator; for controlled power and reliable bring-up, determine a documented pull configuration and whether a test pad should expose SHDN. User's separate physical battery switch remains upstream.

## Current state

Existing R2.1 design uses MCP1700 LDO and 1N5817 diode, with KiCad routing and Gerbers. **R2.1 is not a buck-boost design. Existing Gerbers remain under fabrication hold.** The R3 redesign must remove the LDO circuit and replace it with the Pololu-module footprint, route power and selected protection, update BOM, 3D mechanical support, netlists, PCB/schematic and Gerbers, followed by independent front/back/mating checks and native ERC/DRC.

### Orientation and assembly requirements

1. Use manufacturer's **actual drill guide** to plot all four module pad coordinates and signal identities. Confirm whether board is oriented components-up or components-down when mounted.
2. Ensure the module does not rotate 180° or get inserted into the wrong face; use an asymmetric mounting scheme, silkscreen VIN/GND/VOUT/SHDN, and a top-and-bottom view.
3. Select header gender and installed height before PCB fabrication. Never mirror a bottom-mounted module as if the mating side were identical to top.
4. Bench-test voltage on VOUT without MCU/display fitted.
5. Re-run all saved KiCad tests and physical 1:1 fit overlays after designing the new board.

**No purchase is needed until the final mating orientation and footprint have been checked.** No statement that the buck-boost copper has been routed or signed off is made here.
