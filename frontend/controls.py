from dataclasses import field
from typing import Callable, override

import flet
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
                 fields_titles: list[str], send_request: Callable):
        self.icon = ft.Icon(icon=icon, size=30)
        self.name = ft.Text(value=name)
        self.header = ft.Column(controls=[self.icon, self.name])
        self.uri = uri
        self.send_request = send_request
        self.send_button = ft.Button(content="Send", on_click=self.send)

        self.set_fields(fields_titles)

        self.fields_container.controls.append(self.send_button)
        super().__init__(title=self.header, controls=self.fields_container, col=4)

    def set_fields(self,  fields_titles: list[str]):
        self.fields = dict()
        for title in fields_titles:
            self.fields[title] = ft.TextField(label=title)
        self.fields_container = ft.Column(controls=list(self.fields.values()))

    def send(self, e, parameters: dict[str: str] = None):
        if parameters is None:
            parameters = dict()

        empty_field = False
        for parameter, field in self.fields.items():
            field: ft.TextField
            if not field.value.strip(): # Field is empty
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

class FileTransferCommandPanel(CommandPanel):
    swap_container: ft.Column
    body_container: ft.Row
    text_sections: list[ft.Container]
    text_values: list[str]
    swap_button: ft.IconButton

    def __init__(self, send_request: Callable):
        self.text_sections = list()
        self.text_values = ["This PC", "Client's PC"]
        self.set_text()
        self.swap_button = ft.IconButton(icon=ft.Icons.SWAP_VERT_ROUNDED, bgcolor="#5ce07f", on_click=self.swap_text)

        super().__init__(icon=ft.Icons.DRIVE_FILE_MOVE_ROUNDED, name="File Transfer", uri="transfer",
                         fields_titles=["source", "destination"], send_request=send_request)

        self.swap_container = ft.Column(controls=[self.text_sections[0], self.swap_button, self.text_sections[-1]])
        self.body_container = ft.Row(controls=[self.fields_container, self.swap_container], vertical_alignment=ft.CrossAxisAlignment.START)
        self.controls = [self.body_container]

    def set_text(self):  
        for value in self.text_values:
            current_text = ft.Text(value=value)
            text_section = ft.Container(content=current_text, bgcolor="#5ce07f", padding=5, border_radius = 5)
            self.text_sections.append(text_section)

    def swap_text(self, e):
        self.text_sections[0].content.value, self.text_sections[1].content.value =self.text_sections[1].content.value, self.text_sections[0].content.value

    @override
    def send(self, e, parameters: dict[str: str] = None):
        source = self.text_sections[0].content.value
        parameters = {"source": source}
        super().send(e, parameters)
