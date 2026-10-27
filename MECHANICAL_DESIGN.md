# Resin enclosure and keypad requirements

Updated October 27, 2026. These requirements capture the user's printing choices and the sixteen-key UI walkthrough. Hardware R2 CAD and STLs now implement these requirements in [hardware/](hardware/README.md). Physical print/actuation tolerances remain untested.

## Printed parts

- Rigid resin: front housing/bezel, rear housing, battery cover, internal board supports, and keypad retaining plate.
- Rubbery/flexible resin: sixteen button caps with underside actuators and retention features. Start with individually replaceable buttons captured by the retaining plate; this avoids committing to a large flexible membrane before testing the resin's feel.
- Button legends must be recessed into the printed top faces. They must be part of the CAD geometry, not raised lettering, decals, or a texture visible only in a render.
- Electronics, display, electrical switches, battery contacts, and fasteners remain conventional components. Printed flexible resin caps press real switches underneath; the caps themselves are not assumed to be electrically conductive.

## Sixteen-key layout

Front view; every cell is one physical key. The 8 and 2 keys also navigate menus.

| Column 1 | Column 2 | Column 3 | Column 4 |
| --- | --- | --- | --- |
| 7 | 8 / ↑ | 9 | MENU |
| 4 | 5 | 6 | BACK |
| 1 | 2 / ↓ | 3 | CLEAR |
| ON / OFF | 0 | . | ENTER / = |

Use two lines where needed, particularly ON/OFF and ENTER/=. Engrave both the digits and the secondary arrows on 8 and 2. MENU replaces the earlier proposed dedicated MAT key and provides material, shape, density, and resume options.

## Button mechanism

Reuse the user-owned DIYmalls 4×4, 16-key, 8-pin membrane keypad as the electrical switch layer. Do not buy sixteen separate switches. Mount the intact pad flat on a rigid backing plate, conceal its original labels behind the front bezel and custom caps, and route its ribbon into the housing. Do not peel apart its laminated switch layers. Match the original key centers; remap logical key functions in firmware to the custom labels.

Each flexible cap should have a broad pressing surface, a broad smooth underside contact pad aligned with its membrane key center, and a captured flange that prevents the cap falling out through the front. A rigid retaining plate locates the buttons relative to the switch board. Validate the actual membrane’s feel and release with the flexible caps; the guide/retainer and any flexible return features must let each cap release reliably. Do not assume the membrane can lift an arbitrarily heavy or stiff cap. Broad contact pads should avoid sharp edges or concentrated pressure on the membrane.

Provide travel stops so excessive pressing loads go into the housing rather than overtraveling the membrane or flexing its backing. Final contact-pad height, travel, stop position, backing supports, and rest gap must follow the actual keypad’s actuation and release behavior. Its short travel does not permit assuming a conventional tact-switch travel distance. There must be no switch preload at rest.

## Initial prototype targets

These are proposed starting dimensions to test, not universal resin printing specifications:

| Feature | Starting target |
| --- | --- |
| Recessed legend depth | 0.4 mm |
| Minimum engraved stroke/channel width | 0.6 mm |
| Main numeral height | 4–5 mm, subject to key size |
| Word legend height | At least 2.5–3 mm where space allows |
| Button-to-bezel clearance | Test 0.25, 0.35, and 0.45 mm per side |

Use a plain, bold sans-serif font with open counters and simple arrows. Recessed labels may optionally be paint-filled after curing for contrast. Paint compatibility and adhesion to the flexible resin must be tested before filling the full set.

Print a small coupon containing a labeled button, its bezel opening, retaining flange, and actuator before printing the full keypad. Check the fully washed and cured parts for legibility, free movement, reliable return, and no accidental adjacent-key presses. Tune clearance and engraving depth for the actual resin and cure process.

Keep supports off the button faces, inside engraved legends, and away from sliding/actuating surfaces where possible. Accessible recesses and internal cavities must allow washing and curing according to the resin manufacturer's process. Do not assume every flexible resin will produce the same stiffness or repeatable button action.

## Enclosure assembly

The housing should provide an accessible AAA compartment and removable rear cover, with board and display mounts independent of the flexible keypad. Use rounded transitions around mounting bosses and avoid relying on thin rigid-resin snap tabs for repeated access. Final outer dimensions and mount locations follow selection of the display, existing membrane keypad, board, battery holder, and fasteners.

Editable CadQuery source, an assembled STEP model, individual STLs, sixteen engraved button caps, and printer-oriented shell sections are now in hardware/. Main joints use M2.5 screws and hex nuts glued into 5.35 mm across-flats pockets. Two bonded shell sections per face fit the Mars 5 Ultra; see hardware/README.md for the complete assembly order and screw lengths.

See [PARTS_LIST.md](PARTS_LIST.md) for the reuse-first prototype and candidate final AAA components.

## R2 display geometry

Selected module: EastRising ERC12864FS-655, no touch panel; 70 × 50 × 5.8 mm maximum body. Body plan origin is (13,7.5) mm. Viewing window is 67 × 37 mm at (14.5,11) mm, following the manufacturer drawing. The unchanged case is 96 × 184 × 31 mm. Four M2.5 screws retain one rear cradle with 0.5 mm foam on opaque support surfaces; R1 edge clamps are removed. Adapter board: 70 × 18 × 1.6 mm, nominal plan origin (13,5.7), lower face Z=13 mm. Keep soldered wire/capacitor heights within the documented envelope. Display glass front Z=27.9 mm, body rear Z=22.1 mm. Check actual pin reach and module alignment on the supplied full-size display template before soldering/printing.
