from typing import Callable, override
import flet as ft

import frontend.styling as styling

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
                 fields: dict[str, str], send_request: Callable):
        self.icon = ft.Icon(icon=icon, size=30)
        self.name = ft.Text(value=name)
        self.header = ft.Column(controls=[self.icon, self.name])
        self.uri = uri
        self.send_request = send_request
        self.send_button = ft.Button(content="Send", on_click=self.send)

        self.set_fields(fields)

        self.fields_container.controls.append(self.send_button)
        super().__init__(title=self.header, col=4,
                         controls=ft.Container(content=self.fields_container, padding=20),
                         bgcolor=styling.button_default_hex, collapsed_bgcolor=styling.button_default_hex,
                         collapsed_shape=ft.RoundedRectangleBorder(radius=5), shape=ft.RoundedRectangleBorder(radius=5))

    def set_fields(self, fields: dict[str, str]): #parameter_name: title
        self.fields = dict()
        for parameter_name, title in fields.items():
            self.fields[parameter_name] = ft.TextField(label=title)
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
            for field in self.fields.values():
                field: ft.TextField
                field.value = ""

            self.send_request(self.uri, parameters)


class FileTransferCommandPanel(CommandPanel):
    swap_container: ft.Column
    body_container: ft.Container
    text_sections: list[ft.Container]
    text_values: list[str]
    swap_button: ft.IconButton

    def __init__(self, send_request: Callable):
        self.text_sections = list()
        self.text_values = ["This PC", "Client's PC"]
        self.set_text()
        self.swap_button = ft.IconButton(icon=ft.Icons.SWAP_VERT_ROUNDED,bgcolor=styling.button_hovered_hex, on_click=self.swap_text,
                                         style=ft.ButtonStyle(color=styling.white_text_hex))

        super().__init__(icon=ft.Icons.DRIVE_FILE_MOVE_ROUNDED, name="File Transfer", uri="receive",
                         fields={"source_path": "source", "destination_path": "destination", "file_name": "name"},
                         send_request=send_request)

        self.swap_container = ft.Column(controls=[self.text_sections[0], self.swap_button, self.text_sections[-1]])
        self.body_container = ft.Container(content=ft.Row(controls=[self.fields_container, self.swap_container],
                                                          alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START),
                                           padding=20)
        self.controls = [self.body_container]

    def set_text(self):  
        for value in self.text_values:
            current_text = ft.Text(value=value)
            text_section = ft.Container(content=current_text, bgcolor=styling.button_hovered_hex, padding=5, border_radius=5)
            self.text_sections.append(text_section)

    def swap_text(self, e):
        self.text_sections[0].content.value, self.text_sections[1].content.value =self.text_sections[1].content.value, self.text_sections[0].content.value

    @override
    def send(self, e, parameters: dict[str: str] = None):
        destination = self.text_sections[1].content.value
        if destination == "Client's PC":
            self.uri = "receive" # uri is the action that the client does
        else:
            self.uri = "send"
        super().send(e)

class HostPanel(ft.Container):
    ip: ft.Text
    port: ft.Text
    status_panel: ft.Row
    status_icon: ft.Icon
    status_text: ft.Text
    fields: ft.Column

    select_client: Callable
    is_clicked: bool

    def __init__(self, ip: str, port: int, select_client: Callable):
        self.ip = ft.Text(value=ip)
        self.port = ft.Text(value=str(port))
        self.status_icon = ft.Icon(icon=ft.Icons.CIRCLE)
        self.status_text = ft.Text()
        self.set_status()
        self.status_panel = ft.Row(controls=[self.status_icon, self.status_text], alignment=ft.MainAxisAlignment.CENTER)
        self.fields = ft.Column(controls=[self.ip,
                                          self.port,
                                          self.status_panel],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        super().__init__(content=self.fields, on_click=self.select, on_hover=self.hover,
                         bgcolor=styling.button_default_hex, border_radius=5,
                         alignment=ft.Alignment.CENTER)

        self.select_client = select_client
        self.is_clicked = False


    def set_status(self):
            self.status_icon.color="#338a4a"
            self.status_text.value="Connected"


    def disable(self):
        self.status_icon.color = "#bd1a1a"
        self.status_text.value = "Disconnected"
        self.disabled = True

    def select(self, e):
        self.select_client(self.ip.value)
        self.bgcolor = styling.button_hovered_hex
        self.is_clicked = True

    def hover(self, e: ft.ControlEvent):
        if self.is_clicked:
            return
        if e.data == "true":
            self.bgcolor = styling.button_hovered_hex
        else:
            self.bgcolor = styling.button_default_hex


class HostList(ft.ListView):
    host_key: set # ip as key
    host_list: list[HostPanel]
    select_client: Callable
    
    def __init__(self, select_client: Callable):
        self.host_key = set()
        self.host_list = list()
        super().__init__(controls=self.host_list, width=200, expand=True)
        self.select_client = select_client

    def add(self, ip: str, port: int):
        if ip not in self.host_key:
            panel = HostPanel(ip=ip, port=port, select_client=self.select_client)
            self.host_list.append(panel)
            self.update()

    def remove(self, ip: str):
        pass

    def update_selected_client(self, ip: str):
        for client in self.host_list:
            if client.ip.value != ip and client.is_clicked:
                client.is_clicked = False
                client.bgcolor = styling.button_default_hex

    def disable_client(self, ip: str):
        for client in self.host_list:
            if client.ip.value == ip:
                client.disable()

class Console(ft.Container):
    text_control: ft.Text
    list_view: ft.ListView

    def __init__(self):
        self.text_control = ft.Text()
        self.list_view = ft.ListView(controls=[self.text_control], expand=True)
        super().__init__(content=self.list_view, height=350, bgcolor=styling.panel_bg_hex, border_radius=5)

    def set_text(self, text: str):
        self.text_control.value = text