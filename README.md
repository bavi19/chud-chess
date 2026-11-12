# Chud Chess V4 — Clean Angular Knight

Sized for the 18 × 18 inch board, with 2.25 inch (57.15 mm) squares.
The knight has been rebuilt with a beveled angular silhouette, sloping face,
cut-in throat, distinct jaw and muzzle, paired pointed ears and narrow mane.
Facial engravings are removed: the eyes, nostrils and mouth grooves are gone.
The other five pieces retain the V2 designs and dimensions.

PRINT AT 100% SCALE IN MILLIMETERS. The enlargement is already included.

## Files

STL contains six unique pieces. Print these quantities in EACH color:
8 pawns, 2 rooks, 2 knights, 2 bishops, 1 queen, 1 king. Total: 32 pieces.
The preview images show the actual generated meshes.

| Piece | Base diameter | Height |
|---|---:|---:|
| Pawn | 30.8 mm | 32.2 mm |
| Rook | 35 mm | 42 mm |
| Knight | 35 mm | Approximately 49 mm |
| Bishop | 35 mm | 50.4 mm |
| Queen | 37.8 mm | 51.8 mm |
| King | 39.2 mm | 57.4 mm |

Exact mesh dimensions and validation results are in mesh_checks.json.

## Printing

All pieces sit base down at Z=0. Start with one knight before making a full set.
For a typical 0.4 mm nozzle: PLA, 0.16–0.20 mm layer height, 3 walls,
4 top/bottom layers, 15–20% infill, and temperatures from your filament profile.
Inspect the knight's muzzle, jaw and ears in the slicer; localized supports
under the muzzle may be needed. The king's crossbar may also need supports.
The angular horse silhouette, muzzle, pointed ears and mane are retained.
These remain unprinted prototypes; slicer preview and a physical test are needed.

## View in Fusion

Extract the ZIP fully. In a new design, Insert Mesh, choose an STL and set
Millimeter. No Cursor or MCP is required. Optional: add Fusion/ChudChess in
Scripts and Add-Ins and run ChudChess to import all six into a new design.
The import script has passed syntax checks but has not been run in Fusion.
Files import as mesh components, not native parametric CAD solids.

## Source

generate_pieces.py and knight.py regenerate the models with Python 3 and numpy.
The SCALE setting is already 1.4. The new knight is a beveled polygon-based
implicit surface, meshed with marching tetrahedra. STL files need no Python.
Mesh checks cover closed edges, consistent winding, positive volume,
Euler characteristic and nondegenerate triangles; they are not physical tests.

## Board and pouch

The playing area is 18 x 18 inches, using 2.25-inch squares. The proposed
cloth pouch is a 32-inch finished circle, with seam and drawstring-channel
allowances added before cutting. Test the pouch capacity before final sewing.

## Regenerate the pieces

Install Python 3, then run:

```sh
python -m pip install -r requirements.txt
python generate_pieces.py
```

No code is needed to print the supplied STL files.
