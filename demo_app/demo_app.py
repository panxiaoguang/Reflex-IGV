
import reflex as rx

from .IGV import igvComponent


class State(rx.State):
    """The app state."""
    genome: str = "hg38"
    loc: str = "chr8:127736588-127739371"
    tracks: list[dict[str, str]] = [
        {
            "name": "HG00103",
            "url": "https://s3.amazonaws.com/1000genomes/data/HG00103/alignment/HG00103.alt_bwamem_GRCh38DH.20150718.GBR.low_coverage.cram",
            "indexURL": "https://s3.amazonaws.com/1000genomes/data/HG00103/alignment/HG00103.alt_bwamem_GRCh38DH.20150718.GBR.low_coverage.cram.crai",
            "format": "cram"
        }]
    location: str
    trackName: str
    trackdata: list[dict[str, str]]

    def change_loc(self):
        self.loc = self.location

    def get_click_info(self, e0: str, e1: list[dict[str, str]]):
        self.trackName = e0
        self.trackdata = [{"name": itm['name'], "value": itm['value']}
                          for itm in e1 if itm['name']]


def data_item(name: str, value: str) -> rx.Component:
    return rx.data_list.item(
        rx.data_list.label(name),
        rx.data_list.value(value)
    )


def data_card(trackdata: list[dict[str, str]]) -> rx.Component:
    return rx.card(
        rx.data_list.root(
            rx.foreach(trackdata, lambda item: data_item(
                item['name'], item['value']))
        )
    )


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.vstack(
            rx.heading("IGV test!", size="9"),
            rx.box(
                igvComponent(genome=State.genome, locus=State.loc,
                             tracks=State.tracks, on_track_click=State.get_click_info),
                width="100%",
            ),
            rx.hstack(
                rx.input(placeholder="Enter location",
                         on_blur=State.set_location,
                         width="40%"),
                rx.button("GoTo!", on_click=State.change_loc),
                width="100%",
                justify="center"
            ),
            rx.divider(),
            rx.cond(
                State.trackName,
                rx.vstack(
                    rx.heading(State.trackName, size="4"),
                    data_card(State.trackdata)
                ),
                rx.heading("No track clicked", size="4")
            ),

            spacing="5",
            justify="center",
            min_height="85vh",
        ),
        rx.logo()
    )


app = rx.App()
app.add_page(index)
