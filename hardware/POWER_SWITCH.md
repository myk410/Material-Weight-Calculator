# Hardware power switch

The Material Weight Calculator now uses the user-selected CYT1107 / WOWOONE-style 3-pin SPDT slide switch as the primary hard ON/OFF control for battery conservation.

## Selected switch

- Type: SPDT / 1P2T, three pins, two positions.
- Published body envelope: approximately 12.7 × 6.6 × 13.2 mm.
- Published actuator length: approximately 3.5 mm.
- Published terminal pitch: approximately 4.7 mm.
- The enclosure CAD includes a recessed side opening and an internal cradle sized around this envelope.
- Low-cost CYT1107-style switches can vary slightly, so trial-fit an actual switch before final curing/assembly if possible.

## Wiring as a hard power disconnect

Use the SPDT switch as a simple SPST disconnect:

```text
3 × AAA holder (+)
       |
       +---- CENTER / COMMON pin
                    |
                    | switch ON
                    v
             ONE OUTER pin ----> PCB battery-positive input

OTHER OUTER pin: no connection

3 × AAA holder (-) ----------------> PCB ground
```

In the OFF position the common pin is connected to the unused outer pin, so battery positive is physically disconnected from the calculator electronics. This is preferred over relying only on MCU sleep when maximum battery conservation is wanted.

## Enclosure integration

The switch mount is in the upper-right side of the rear shell, above the main PCB zone and away from the AAA compartment. The actuator opening is recessed to reduce accidental switching. Internal end stops/cradle features support the switch body, and local ribs reinforce the side wall around the cutout to limit resin-print warping and flex.

The current CAD opening intentionally has some clearance. Confirm actual knob travel and molded body dimensions on one of the purchased switches before permanently bonding or potting the switch in place.

## Assembly notes

1. Trial-fit the switch in the rear-shell cradle.
2. Confirm both switch positions are reachable without the knob rubbing the resin slot.
3. Identify the center/common pin with a continuity meter if there is any doubt.
4. Solder AAA positive to common and the PCB-positive lead to the chosen outer pin.
5. Leave the other outer pin insulated and unconnected.
6. Route the negative battery lead directly to PCB ground.
7. Add strain relief so wire motion does not load the three solder terminals.
8. Verify OFF gives an open circuit between battery positive and PCB positive before installing cells.
