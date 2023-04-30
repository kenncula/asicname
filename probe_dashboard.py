import dash
import dash_bootstrap_components as dbc
import requests
from dash import Input, Output, State, html
import flag
import json
import pycountry

def create_dash_page(probes):

    app = dash.Dash(
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    app.layout = dbc.Alert(
        "Hello, Bootstrap!", className="m-5"
    )

    elems = []

    for probe in probes:
        print(json.dumps(probe, indent=4))
        elems.append(dbc.Button("Probe #" + str(probe['id']), id={'type': "open-probe-info",'index': probe['id']},)),
        elems.append(dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Probe #" + str(probe['id']) + ": " + str(probe['description'])), close_button=True),
                        dbc.ModalBody("Country: " + flag.flag(probe["country_code"]) + "\n"
                        + "Status: " + str(probe['status']['name'])),
                        dbc.ModalFooter(
                            dbc.Button(
                                "Back",
                                id={
                                    'type': "close-probe-info",
                                    'index': probe['id']
                                },
                                className="ms-auto",
                                n_clicks=0,
                            )
                        ),
                    ],
                    id={
                        'type': "modal-probe",
                        'index': probe['id']
                    },
                    centered=True,
                    is_open=False,
        ))


    modals = html.Div(elems)

    app.layout = modals

    for probe in probes:
        @app.callback(
            Output("modal-probe-" + str(probe['id']), "is_open"),
            [Input("open-probe-info-" + str(probe['id']), "n_clicks"), Input("close-cprobe-info-" + str(probe['id']), "n_clicks")],
            [State("modal-probe-" + str(probe['id']), "is_open")],
        )

        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open
    app.run_server()