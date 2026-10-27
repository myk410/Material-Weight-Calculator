from pathlib import Path
import pcbnew as k
ROOT=Path(__file__).resolve().parents[1]
import os
ADAPTER=os.environ.get('DISPLAY_ADAPTER')=='1'
TMP=ROOT/'validation'/('adapter_plot_intermediates' if ADAPTER else 'plot_intermediates');TMP.mkdir(exist_ok=True)
b=k.LoadBoard(str(ROOT/'pcb'/'display_adapter'/'display_adapter.kicad_pcb' if ADAPTER else ROOT/'pcb'/'material_weight_calculator.kicad_pcb'))
pc=k.PLOT_CONTROLLER(b);o=pc.GetPlotOptions();o.SetOutputDirectory(str(TMP));o.SetPlotFrameRef(False);o.SetAutoScale(False);o.SetScale(1);o.SetBlackAndWhite(True);o.SetPlotReference(False);o.SetPlotValue(False);o.SetDrillMarksType(k.DRILL_MARKS_SMALL_DRILL_SHAPE)
for name,layer,mirror in [('top_reference',k.F_Cu,False),('top_transfer',k.F_Cu,True),('bottom_reference',k.B_Cu,True),('bottom_transfer',k.B_Cu,False)]:
 o.SetMirror(mirror);pc.SetLayer(layer);pc.OpenPlotfile(name,k.PLOT_FORMAT_PDF,name);pc.PlotLayer();pc.ClosePlot()
print('Plotted exact copper with KiCad')
