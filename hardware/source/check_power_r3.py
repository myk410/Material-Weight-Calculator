"""Validate the frozen LTC3440 MSOP-10 electrical contract; does not DRC copper."""
import json
from pathlib import Path
p = Path(__file__).with_name("power_r3_reference.json")
d = json.loads(p.read_text())
assert d["status"] == "ROUTED_CAD_REVIEW_PHYSICAL_HOLD"
u = d["ic"]
assert u["package"] == "MSOP-10 (MS, no center pad)"
assert u["mounting_side"] == "F.Cu only"
assert u["pins"] == {"1":"RT","2":"MODE","3":"SW1","4":"SW2","5":"GND","6":"+3V3","7":"VIN","8":"VIN","9":"FB","10":"VC"}
parts = {c["ref"]: c["pins"] for c in d["components"]}
assert parts["L1"] == {"1":"SW1","2":"SW2"}
assert parts["RFB_TOP"] == {"1":"+3V3","2":"FB"}
assert parts["RFB_BOTTOM"] == {"1":"FB","2":"GND"}
assert parts["RCOMP"] == {"1":"VC","2":"COMP_NODE"}
assert parts["CCOMP"] == {"1":"COMP_NODE","2":"FB"}
assert parts["CIN"] == {"1":"VIN","2":"GND"}
assert parts["COUT"] == {"1":"+3V3","2":"GND"}
print("PASS: frozen manufacturer LTC3440 10-pin electrical mapping")
print("Reference contract only: run export_r3.py for current native ERC/DRC and actual-board pin checks. Physical/bench gates remain open.")
