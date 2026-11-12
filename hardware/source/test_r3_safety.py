"""Fault injection: actual pads/footprints must fail the independent contracts.
Also require the manufacturing exporter to refuse unresolved physical checks.
"""
from pathlib import Path
import json, subprocess, sys
import pcbnew as k
from verify_r3 import ROOT, FOLDER, actual, contracts
results=[]
def load():
    m=k.LoadBoard(str(FOLDER/'material_weight_calculator.kicad_pcb'))
    a=k.LoadBoard(str(ROOT/'pcb'/'r3'/'display_adapter'/'display_adapter.kicad_pcb'))
    return m,a
for fault in ['rotated_regulator','VC_compensation_to_ground','rotated_MCU','reversed_main_LCD_connector','reversed_adapter_LCD_row','swapped_SOT23_base_emitter','reversed_PH_programming_header','PH_power_ground_swap']:
    m,a=load();mp,ap=actual(m),actual(a)
    if fault=='VC_compensation_to_ground':mp['C6','2'].SetNet(m.FindNet('GND'))
    elif fault=='PH_power_ground_swap':
        mp['J5','1'].SetNet(m.FindNet('+3V3'));mp['J5','2'].SetNet(m.FindNet('GND'))
    elif fault=='swapped_SOT23_base_emitter':
        mp['Q1','1'].SetNet(m.FindNet('+3V3'));mp['Q1','2'].SetNet(m.FindNet('LCD_BASE'))
    else:
        board,ref=(a,'J2') if fault=='reversed_adapter_LCD_row' else (m,{'rotated_regulator':'U2','rotated_MCU':'U1','reversed_main_LCD_connector':'J3','reversed_PH_programming_header':'J5'}[fault])
        f=next(f for f in board.GetFootprints() if f.GetReference()==ref)
        f.SetOrientationDegrees(f.GetOrientationDegrees()+180)
    try:contracts(mp,ap)
    except AssertionError:results.append({'fault':fault,'detected':True})
    else:raise AssertionError('Undetected fault: '+fault)
# Block BEFORE any files are generated, including when native CAD reports are clean.
p=subprocess.run([sys.executable,str(ROOT/'source'/'export_r3.py'),'--manufacturing'],capture_output=True,text=True)
assert p.returncode!=0 and 'FABRICATION HOLD' in p.stderr
assert not (FOLDER/'manufacturing').exists()
results.append({'fault':'unresolved_physical_gate','detected':True,'manufacturing_files_created':False})
(ROOT/'validation'/'r3'/'negative_checks.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
