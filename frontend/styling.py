import flet as ft

page_bg_hex = "#021F28"
panel_bg_hex = "#073642" #"#66BCBC"
white_text_hex = "#FCFCFC"

button_hovered_hex = "#009090"
button_default_hex = "#00B5B5"

page_theme = ft.Theme(
    text_theme=ft.TextTheme( # Change default text color
            body_large=ft.TextStyle(color=white_text_hex),
            body_medium=ft.TextStyle(color=white_text_hex),
            title_large=ft.TextStyle(color=white_text_hex)),
    color_scheme=ft.ColorScheme(
            primary=page_bg_hex,
            on_surface_variant=page_bg_hex)
    )