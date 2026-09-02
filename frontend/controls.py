from dataclasses import field
from typing import Callable

import flet as ft

from backend.endpoint import Endpoint

class CommandPanel(ft.ExpansionTile):
    icon: ft.Icon
    name: ft.Text
    header: ft.Column

    uri: str

    fields: dict[str, ft.TextField]
    fields_container: ft.Column

    send_button: ft.Button
    send_request: Callable

    def __init__(self, icon: ft.IconData, name: str, uri: str,
                 fields_titles: set[str], send_request: Callable):
        self.icon = ft.Icon(icon=icon, size=30)
        self.name = ft.Text(value=name)
        self.header = ft.Column(controls=[self.icon, self.name])
        self.uri = uri
        self.send_request = send_request
        self.send_button = ft.Button(content="Send", on_click=self.send)

        self.set_fields(fields_titles)

        self.fields_container.controls.append(self.send_button)
        super().__init__(title=self.header, controls=self.fields_container, col=4)

    def set_fields(self,  fields_titles: set[str]):
        self.fields = dict()
        for title in fields_titles:
            self.fields[title] = ft.TextField(label=title)
        self.fields_container = ft.Column(controls=list(self.fields.values()))

    def send(self, e):
        empty_field = False
        parameters = dict()
        for parameter, field in self.fields.items():
            field: ft.TextField
            if not field.value.strip():
                field.error = "Required"
                empty_field = True
            else:
                field.error = None
                parameters[parameter] = field.value

        if not empty_field:
            self.send_request(self.uri, parameters)

            for field in self.fields.values():
                field: ft.TextField
                field.value = ""
