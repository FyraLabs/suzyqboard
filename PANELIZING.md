# Panelizing

The panel holds 56 boards (4 × 14) at 140.2 × 237.8 mm, under JLCPCB's 250 × 250 mm
assembly limit.

## Requirements

- KiCad 10
- KiKit 1.8.1 or newer (`sudo dnf install kikit` or `pip3 install --user kikit`)
- [Fabrication Toolkit](https://github.com/bennymeg/Fabrication-Toolkit), from KiCad's Plugin and Content Manager

## Building

```sh
mkdir -p panel
kikit panelize -p kikit-panel.json suzyqboard.kicad_pcb panel/suzyqboard-panel.kicad_pcb
cp fabrication-toolkit-options.json panel/
```

Open `panel/suzyqboard-panel.kicad_pcb` in KiCad and run Fabrication Toolkit. The
output goes to `panel/production/`.

## Ordering

- Upload `SuzyQ_Board_0.zip`, `bom.csv` and `positions.csv` from `panel/production/`.
  They cover the whole panel. Don't mix them with the single-board files in `production/`.
- Set the board and assembly quantities in panels, and mark the board as already panelized.
- Every other column is rotated 180°, so check P1 and J2 rotations in both
  orientations in the placement preview.

## Notes

- Both connectors overhang the board (P1 by ~10.6 mm, J2 by ~1 mm). That's why
  the panel only has top and bottom rails, why columns alternate so the plugs face each other
  across a wide gap (`hevendiff`), and why tabs are only on the long edges.
- Tab positions come from the `KIKIT_TAB1`/`KIKIT_TAB2` footprints in
  `suzyqboard.kicad_pcb`, placed to keep mousebites away from R4. They must sit
  exactly on the board edge.
- `kikit-post.py` closes a ~0.5 µm gap KiKit leaves between the backbones and the top
  rail, and keeps KiKit's fiducials and holes out of the BOM and CPL.
- Keep `rows` even so the rows stay paired around the backbones. 12 rows gives a
  ~204 mm panel with 48 boards.
