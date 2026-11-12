"""Independent frozen pin-orientation regression checks for R2.1.

Run: python hardware/source/check_orientation_contract.py

No external libraries required. Checks saved electrical_design.json pad
coordinates and net identities against independent expected values, rather
than trusting the KiCad footprint generator's pin order.
This does NOT replace actual front/back physical mating inspection.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(file):
    d = json.loads((ROOT / "source" / file).read_text())
    components = {c["ref"]: c for c in d["components"]}
    pads = {(p["ref"], str(p["pin"])): p for p in d["pads"]}
    return components, pads


def pin(components, pads, ref, number, net, xy, tolerance=0.005):
    number = str(number)
    actual_net = components[ref]["pins"][number]
    p = pads[(ref, number)]
    assert actual_net == net, (ref, number, "net", actual_net, net)
    assert abs(p["x"] - xy[0]) <= tolerance, (ref, number, "x", p["x"], xy[0])
    assert abs(p["y"] - xy[1]) <= tolerance, (ref, number, "y", p["y"], xy[1])


def main():
    m, mp = read("electrical_design.json")
    a, ap = read("adapter_electrical_design.json")

    # Independent vendor 28-SPDIP top view: notch at top, pin 1 upper-left.
    for num, net, xy in [
        (1, "", (35, 20)),
        (14, "+3V3", (35, 53.02)),
        (15, "GND", (42.62, 53.02)),
        (19, "UPDI", (42.62, 42.86)),
        (20, "+3V3", (42.62, 40.32)),
        (21, "GND", (42.62, 37.78)),
        (23, "LCD_CLK", (42.62, 32.70)),
        (24, "LCD_DATA", (42.62, 30.16)),
        (25, "LCD_CS", (42.62, 27.62)),
        (26, "LCD_CD", (42.62, 25.08)),
        (27, "LCD_RST", (42.62, 22.54)),
        (28, "", (42.62, 20)),
    ]:
        pin(m, mp, "U1", num, net, xy)

    # EastRising physical 22-pin array: 1.27 mm centers, pin 1 at X21.665
    # *on adapter F.Cu PLAN*. Must still verify actual LCD mating face.
    display_nets = {
        1: "LCD_CS", 2: "LCD_RST", 3: "LCD_CD",
        **{i: "GND" for i in range(4, 12)},
        12: "LCD_CLK", 13: "LCD_DATA",
        14: "LCD_VCC", 15: "GND",
        16: "VB0_PLUS", 17: "VB0_MINUS",
        18: "VB1_MINUS", 19: "VB1_PLUS",
        20: "VLCD", 21: "GND", 22: "GND",
    }
    for n, net in display_nets.items():
        pin(a, ap, "J2", n, net, (21.665 + (n - 1) * 1.27, 3.0))
    assert round(ap["J2", "22"]["x"] - ap["J2", "1"]["x"], 2) == 26.67

    # Distinct *physical* orientations: main cable vertical, adapter horizontal.
    cable = ["LCD_VCC", "GND", "LCD_CLK", "LCD_DATA",
             "LCD_CS", "LCD_CD", "LCD_RST", ""]
    for n, net in enumerate(cable, 1):
        pin(m, mp, "J3", n, net, (70, 16 + (n - 1) * 2.54))
        pin(a, ap, "J1", n, net, (9 + (n - 1) * 2.54, 13))

    for ref, ordered in {
        "J2": [("VBAT_SW", (10, 9)), ("GND", (10, 11.54))],
        "J4": [("+3V3", (55, 46)), ("GND", (55, 48.54)),
               ("UPDI", (55, 51.08))],
        "U2": [("GND", (23, 15)), ("VIN", (25.54, 15)),
               ("+3V3", (28.08, 15))],
        "Q1": [("+3V3", (56, 15)), ("LCD_BASE", (58.54, 15)),
               ("LCD_VCC", (61.08, 15))],
        "D1": [("VIN", (24, 9)), ("VBAT_LINK", (31.62, 9))],
    }.items():
        for n, (net, xy) in enumerate(ordered, 1):
            pin(m, mp, ref, n, net, xy)

    pin(a, ap, "C5", 1, "LCD_VCC", (7, 7))
    pin(a, ap, "C5", 2, "GND", (8.5, 7))

    print("PASS: saved pad numbers, net names, and top-plan coordinates match frozen contract.")
    print("HOLD: LCD actual mating face, keypad cable, programmer header and polarity")
    print("      still require physical orientation verification before fabrication.")


if __name__ == "__main__":
    main()
