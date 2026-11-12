# Keypad J1 connector — physical mating contract (R2.1)

## Hardware on hand

The user's photographed 4×4 membrane keypad has an eight-conductor ribbon ending in a black **female eight-position connector** (holes visible). Typical 4×4 membrane keypads use a Dupont-style 1×8 **2.54 mm (0.1 inch) pitch** female termination, but the exact owned unit has **not yet been measured**.

The PCB design already contains J1: `MW_footprints:PinHeader_1x08_P2.54mm_Vertical`. This is the **board copper/holes for a male 1×8 header**; buying/installing a separate female socket on the PCB is not necessary if the ribbon end is confirmed female.

**Required physical part:** straight or right-angle **1×8, 2.54 mm male through-hole header**, selected for the real case depth and ribbon exit. Existing PCB J1 footprint assumes a straight vertical header; right-angle header needs a revised placement, footprint and case-clearance audit before use. Do not order a 1.0 mm/1.25 mm FFC connector for this pre-terminated cable.

## Top-view PCB J1 map (looking down onto F.Cu, header inserted from above)

J1 has center X=12.00 mm; pad 1 Y=22.54 mm and pad 8 Y=40.32 mm. Pad pitch=2.54 mm. Increasing Y follows increasing pad numbers; this is a PCB top view, **not** necessarily left-to-right ribbon conductor ordering.

| J1 pad | PCB net | MCU physical pin |
|---:|---|---:|
| 1 | ROW0 | 2 |
| 2 | ROW1 | 3 |
| 3 | ROW2 | 4 |
| 4 | ROW3 | 5 |
| 5 | COL0 | 6 |
| 6 | COL1 | 7 |
| 7 | COL2 | 8 |
| 8 | COL3 | 9 |

This is the *desired board-side logical mapping*. The photographed keypad's actual ribbon wire order remains **unverified**. If the ribbon row/column order differs, either remap firmware scan outputs/inputs or intentionally reroute J1, after documenting and testing it. No voltage is applied to an unverified keypad ribbon during continuity testing.

## Orientation gates — required before releasing Gerbers

1. Hold the female plug in the exact intended insertion direction. Make a written front-facing/contact-side diagram of the eight numbered holes as seen **looking into the socket**; do NOT infer that hole order equals keypad-left-to-right order.
2. Confirm with calipers the distance between socket hole 1 and hole 8 should be nominal 17.78 mm for 2.54 mm pitch. Use a dry-fit spare male 1×8 header, **not the PCB**, to check insertion depth and contact fit.
3. With a multimeter in continuity mode and **no battery or programmer attached**, press each membrane key and record which **two plug holes** close for that key. This establishes a full 16-key-to-contact map independent of vendor diagrams.
4. Compare the observed row/column groups with the MCU assignments above. Keep a CSV key map (physical socket hole number as viewed from mating face, board pad, matrix row/column, labeled key).
5. Check whether PCB must present male pins upwards or sideways; check socket body, cable fold radius and exit location in CAD. Never fold the laminated membrane cable sharply at its keypad exit.
6. Put conspicuous `J1-1` and `J1-8` marks on F.SilkS and include a reference photo/assembly drawing with the socket face and board face labeled. Optional keyed shroud only if compatible with actual female plug; an unkeyed header can be installed reversed.
7. Verify no neighboring components, screws or ribs block the installed connector.
8. Re-run electrical and mechanical audits if the header geometry/location changes. Do not fabricate against the existing pin-header footprint until the chosen physical connector is dry-fitted.

## Sources

- [Phipps 4×4 16-Key Matrix Membrane Keypad](https://www.phippselectronics.com/support/4x4-16-key-matrix-membrane-keypad-support-documentation/) (example 2.54 mm female connector, **not** guaranteed to be the exact owned unit).
- [ProtoSupplies membrane keypad](https://protosupplies.com/product/membrane-keypad-4x4-matrix/) (example female 2.54 mm connector).
- Local project: `hardware/source/electrical_design.json`, J1 and U1 pin positions.

**Status: electrical J1 routing identified; real cable contact order and physical mating not signed off.**
