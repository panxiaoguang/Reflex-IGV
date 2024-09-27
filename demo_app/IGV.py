import reflex as rx
from typing import List, Dict
from reflex.components.component import NoSSRComponent


class IGV(NoSSRComponent):

    library = "/public/igv"

    tag = "IgvComponent"

    is_default = True

    lib_dependencies: list[str] = [
        "igv@3.0.6"
    ]

    genome: rx.Var[str]
    locus: rx.Var[str]
    tracks: rx.Var[List[Dict[str, str]]]

    on_track_click: rx.EventHandler[lambda e0, e1: [e0, e1]]


igvComponent = IGV.create
