# Resin enclosure and keypad requirements

Updated October 30, 2026. These requirements capture the user's printing choices and the sixteen-key UI walkthrough. The keypad is now intentionally designed as one connected flexible-resin sheet rather than sixteen loose caps. Hardware CAD source in [hardware/](hardware/README.md) is being kept consistent with this requirement. Physical print/actuation tolerances remain untested.

## Printed parts

- Rigid resin: front housing/bezel, rear housing, battery cover, internal board supports, keypad guide/backing, and display cradle.
- Rubbery/flexible resin: **one connected sixteen-button keypad sheet printed in 55A flexible resin**. The sixteen button tops, thin connecting membrane, underside actuator pads, and perimeter retention area are one printed part. Do not split the normal production keypad into sixteen loose buttons.
- Button legends must be recessed into the printed top faces. They must be part of the CAD geometry, not raised lettering, decals, or a texture visible only in a render.
- Electronics, display, electrical switch membrane, battery contacts, and fasteners remain conventional components. The printed flexible keypad presses the existing electrical membrane underneath; the 55A resin itself is not assumed to be electrically conductive.

## Sixteen-key layout

Front view; every cell is one physical key. The 8 and 2 keys also navigate menus.

| Column 1 | Column 2 | Column 3 | Column 4 |
| --- | --- | --- | --- |
| 7 | 8 / ↑ | 9 | MENU |
| 4 | 5 | 6 | BACK |
| 1 | 2 / ↓ | 3 | CLEAR |
| ON / OFF | 0 | . | ENTER / = |

Use two lines where needed, particularly ON/OFF and ENTER/=. Engrave both the digits and the secondary arrows on 8 and 2. MENU replaces the earlier proposed dedicated MAT key and provides material, shape, density, and resume options.

## One-piece 55A keypad construction

The custom keypad is a single flexible part, similar in concept to a calculator or remote-control rubber keypad. All sixteen keys are joined by a thin continuous membrane so the entire keypad can be installed and removed as one piece.

Starting geometry for the flexible part:

| Feature | Starting target |
| --- | --- |
| Flexible material | 55A resin |
| Connected sheet footprint | about 72 × 72 mm, centered on the 4 × 4 key field |
| Connecting membrane thickness | 0.8–1.0 mm; CAD nominal 0.85 mm |
| Button top | about 14 × 14 mm |
| Button-top height above membrane | about 5 mm |
| Underside actuator | centered, smooth, about 8 mm diameter |
| Actuator projection below sheet | about 1.5 mm; tune after real keypad test |
| Nominal key pitch | 18 mm |
| Recessed legend depth | 0.4 mm |
| Minimum engraved stroke/channel width | 0.6 mm |
| Main numeral height | 4–5 mm, subject to key size |
| Word legend height | at least 2.5–3 mm where space allows |
| Button-to-bezel clearance | test 0.25, 0.35, and 0.45 mm per side |

The thin sheet provides the flex zone. The button tops must remain substantially thicker than the connecting membrane so pressing one key does not significantly drag neighboring keys. Do not make the entire keypad uniformly several millimeters thick.

The outer membrane should be captured between rigid enclosure features so it cannot shift sideways. The rigid guide/backing stack may provide registration and travel-stop functions, but it must not clamp the active flex zones so tightly that the keys cannot return. The flexible sheet should remain replaceable without destroying the enclosure.

## Button mechanism

Reuse the user-owned DIYmalls 4×4, 16-key, 8-pin membrane keypad as the **electrical switch layer**. Do not buy sixteen separate switches. Mount the intact electrical pad flat on a rigid backing plate, conceal its original labels behind the front bezel and custom 55A keypad sheet, and route its ribbon into the housing. Do not peel apart its laminated switch layers. Match the original key centers; remap logical key functions in firmware to the custom labels.

Each printed key should have a broad pressing surface and a centered smooth underside actuator aligned with its electrical membrane key center. The sixteen printed keys are not separate pieces; they rise from the common thin sheet. Avoid sharp actuator edges or concentrated pressure on the electrical membrane.

Provide travel stops so excessive pressing loads go into the housing/guide rather than overtraveling the membrane or flexing its backing. Final actuator height, travel, stop position, backing supports, and rest gap must follow the actual keypad’s actuation and release behavior. Its short travel does not permit assuming conventional tact-switch travel. There must be no switch preload at rest.

The single-sheet construction should also act as a dust barrier over the button field. Avoid unnecessary through-slots between keys unless later testing proves the continuous sheet is too stiff.

## Prototype and print validation

Use a plain, bold sans-serif font with open counters and simple arrows. Recessed labels may optionally be paint-filled after curing for contrast. Paint compatibility and adhesion to the 55A resin must be tested before filling the full keypad.

Print a small **two-key connected-sheet coupon** before committing to the complete keypad. The coupon should reproduce the real membrane thickness, button-top thickness, actuator projection, bezel clearance, and key pitch. Check the fully washed and cured part for:

- independent motion of adjacent keys;
- reliable return after release;
- no electrical-switch preload at rest;
- no accidental neighboring-key presses;
- legible recessed labels;
- no tearing at the thin membrane around the button bases; and
- enough perimeter stiffness for clean enclosure capture.

Keep supports off the button faces, inside engraved legends, and away from actuator/contact surfaces where possible. The 55A sheet should preferably be oriented so the visible key faces and thin membrane require minimal cleanup. Accessible recesses and internal cavities must allow washing and curing according to the resin manufacturer's process.

## Enclosure assembly

The housing should provide an accessible AAA compartment and removable rear cover, with board and display mounts independent of the flexible keypad. Use rounded transitions around mounting bosses and avoid relying on thin rigid-resin snap tabs for repeated access.

The front bezel presents sixteen individual openings, but from the inside there is only **one custom flexible keypad part**. The sheet is placed behind the bezel, aligned to the sixteen openings, then retained by the guide/backing stack over the original DIYmalls electrical membrane. This eliminates sixteen loose printed parts during assembly.

Editable CadQuery source, an assembled STEP model, individual rigid-part STLs, the one-piece flexible keypad STL, and printer-oriented shell sections belong in hardware/. Main joints use M2.5 screws and hex nuts glued into 5.35 mm across-flats pockets. Two bonded shell sections per face fit the Mars 5 Ultra; see hardware/README.md for the complete assembly order and screw lengths.

See [PARTS_LIST.md](PARTS_LIST.md) for the reuse-first prototype and candidate final AAA components.

## R2 display geometry

Selected module: EastRising ERC12864FS-655, no touch panel; 70 × 50 × 5.8 mm maximum body. Body plan origin is (13,7.5) mm. Viewing window is 67 × 37 mm at (14.5,11) mm, following the manufacturer drawing. The unchanged case is 96 × 184 × 31 mm. Four M2.5 screws retain one rear cradle with 0.5 mm foam on opaque support surfaces; R1 edge clamps are removed. Adapter board: 70 × 18 × 1.6 mm, nominal plan origin (13,5.7), lower face Z=13 mm. Keep soldered wire/capacitor heights within the documented envelope. Display glass front Z=27.9 mm, body rear Z=22.1 mm. Check actual pin reach and module alignment on the supplied full-size display template before soldering/printing.
