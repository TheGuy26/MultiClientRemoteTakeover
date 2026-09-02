import flet as ft
from frontend import controls

class Page:
    page: ft.Page
    panel: ft.Column

    commands: list[controls.CommandPanel]
    command_grid: ft.ResponsiveRow

    def __init__(self):
        self.page: ft.Page | None = None
        self.panel: ft.Column | None = None

        self.commands = [controls.CommandPanel(icon=ft.Icons.PLAY_CIRCLE, name="TEST1", uri="TEST", fields_titles={"first", "second"}, send_request=self.send_request),
                         controls.CommandPanel(icon=ft.Icons.PLAY_CIRCLE, name="TEST2", uri="TEST", fields_titles={"first", "second"}, send_request=self.send_request),
                         controls.CommandPanel(icon=ft.Icons.PLAY_CIRCLE, name="TEST3", uri="TEST", fields_titles={"first", "second"}, send_request=self.send_request),
                         controls.CommandPanel(icon=ft.Icons.PLAY_CIRCLE, name="TEST3", uri="TEST", fields_titles={"first", "second"}, send_request=self.send_request)]
        self.command_grid = ft.ResponsiveRow(columns=12, spacing=10, controls=self.commands)


        ft.run(main=self.main)


    async def main(self, page: ft.Page):
        self.page: ft.Page = page
        self.page.title = "Multi Client Remote Takeover"
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.panel = ft.Column(alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.START,
                               expand=True)

        self.panel.controls.append(self.command_grid.controls[0])
        self.panel.controls.append(self.command_grid)




        self.page.add(self.panel)

    def send_request(self, uri: str, parameters: dict):
        pass