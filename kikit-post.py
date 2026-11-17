import pcbnew
from kikit.units import mm
from shapely.geometry import JOIN_STYLE

DEFAULT_GAP_TOLERANCE_MM = 0.005
EXCLUDED_FROM_ASSEMBLY = pcbnew.FP_EXCLUDE_FROM_POS_FILES | pcbnew.FP_EXCLUDE_FROM_BOM


def close_substrate_gaps(panel, tolerance):
    substrate = panel.boardSubstrate
    substrate.substrates = (
        substrate.substrates
        .buffer(tolerance, join_style=JOIN_STYLE.mitre)
        .buffer(-tolerance, join_style=JOIN_STYLE.mitre)
    )


def is_kikit_generated(footprint):
    return footprint.GetReference().upper().startswith("KIKIT_")


def exclude_kikit_footprints_from_assembly(panel):
    for footprint in filter(is_kikit_generated, panel.board.GetFootprints()):
        footprint.SetAttributes(footprint.GetAttributes() | EXCLUDED_FROM_ASSEMBLY)


def kikitPostprocess(panel, arg):
    gap_tolerance_mm = float(arg) if arg else DEFAULT_GAP_TOLERANCE_MM
    close_substrate_gaps(panel, gap_tolerance_mm * mm)
    exclude_kikit_footprints_from_assembly(panel)
