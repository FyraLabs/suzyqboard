# KiKit post-processing script for the SuzyQ panel
import pcbnew
from kikit.units import mm
from shapely.geometry import JOIN_STYLE


def kikitPostprocess(panel, arg):
    # close sub-micron gaps in the substrate. KiKit leaves the vertical backbones
    # ~0.5um short of the top rail, which makes the mill cut them free and
    # confuses gerber viewers (JLC's included)
    eps = float(arg) * mm if arg else 0.005 * mm
    sub = panel.boardSubstrate
    sub.substrates = sub.substrates.buffer(eps, join_style=JOIN_STYLE.mitre) \
                                   .buffer(-eps, join_style=JOIN_STYLE.mitre)

    # keep KiKit's fiducials and tooling holes out of the CPL/BOM so JLC doesn't
    # complain about designators missing from the BOM
    for fp in panel.board.GetFootprints():
        if fp.GetReference().upper().startswith("KIKIT_"):
            fp.SetAttributes(fp.GetAttributes()
                             | pcbnew.FP_EXCLUDE_FROM_POS_FILES
                             | pcbnew.FP_EXCLUDE_FROM_BOM)
