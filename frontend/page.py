import flet as ft
from frontend import controls
from backend.client_management import ClientManagement
from backend.client import Client
from backend.commands.FileTransfer import sender, receiver

class Page:
    page: ft.Page
    panel: ft.Row

    commands: list[controls.CommandPanel]
    command_grid: ft.ResponsiveRow

    host_list: controls.HostList

    client_management: ClientManagement
    current_client: Client | None

    def __init__(self):
        self.page: ft.Page | None = None
        self.panel: ft.Row | None = None

        self.commands = [controls.FileTransferCommandPanel(send_request=self.send_file_transfer_request),
                         controls.CommandPanel(icon=ft.Icons.PLAY_CIRCLE, name="TEST2", uri="TEST", fields={"first": "first", "second": "second"}, send_request=self.send_request),
                         controls.CommandPanel(icon=ft.Icons.PLAY_CIRCLE, name="TEST3", uri="TEST", fields={"first": "first", "second": "second"}, send_request=self.send_request),
                         controls.CommandPanel(icon=ft.Icons.PLAY_CIRCLE, name="TEST3", uri="TEST", fields={"first": "first", "second": "second"}, send_request=self.send_request)]
        self.command_grid = ft.ResponsiveRow(columns=8, spacing=10, controls=self.commands, expand=True)

        self.host_list = controls.HostList(select_client=self.select_client)

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

        self.panel.controls.extend([ft.Container(content=self.host_list, bgcolor="#1c52a3"), self.command_grid])



        self.page.add(self.panel)

    def select_client(self, ip: str):
        self.current_client = self.client_management.get_client(ip)

    def send_request(self, uri: str, parameters: dict):
        pass

    def send_file_transfer_request(self, uri:str, parameters: dict):
        if self.current_client is None:
            return # update GUI
        if uri == "receive":
            sender.master_send(host=self.current_client, **parameters)
        else:
            receiver.master_receive(host=self.current_client, **parameters)

    def add_client(self, ip: str, port: int):
        self.host_list.add(ip=ip, port=port)
        self.page.update()