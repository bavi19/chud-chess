"""Import the six supplied STL pieces into a new Fusion design, in millimeters.
This creates mesh components, not parametric solid features. No MCP required.
"""
import adsk.core, adsk.fusion, traceback
from pathlib import Path

def run(context):
    app=adsk.core.Application.get()
    ui=app.userInterface
    try:
        folder=Path(__file__).resolve().parents[2]/'STL'
        names=['Pawn','Rook','Knight','Bishop','Queen','King']
        missing=[str(folder/f'ChudChess_{name}.stl') for name in names if not (folder/f'ChudChess_{name}.stl').is_file()]
        if missing:
            ui.messageBox('Keep the extracted ChudChess folder together. Missing:\n'+'\n'.join(missing));return
        doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        doc.name='Chud Chess v4 - 18 inch board'
        design=adsk.fusion.Design.cast(app.activeProduct)
        design.designType=adsk.fusion.DesignTypes.DirectDesignType
        root=design.rootComponent
        for i,name in enumerate(names):
            transform=adsk.core.Matrix3D.create()
            transform.translation=adsk.core.Vector3D.create(i*5.0,0,0) # Fusion internal units: cm
            occ=root.occurrences.addNewComponent(transform)
            comp=occ.component
            comp.name='Chud Chess '+name
            bodies=comp.meshBodies.add(str(folder/f'ChudChess_{name}.stl'),adsk.fusion.MeshUnits.MillimeterMeshUnit)
            if not bodies or bodies.count==0:raise RuntimeError('Import failed for '+name)
            bodies.item(0).name=name
        app.activeViewport.fit()
        ui.messageBox('Chud Chess imported: six mesh components.\nSave the design if you want to keep it.\nFor printing, use the supplied STL files at 100% scale in millimeters.')
    except:
        ui.messageBox(traceback.format_exc())
