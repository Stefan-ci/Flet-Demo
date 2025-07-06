import flet as ft
from utils import Routes


class StockMenuBarComponent(ft.Row):
    """ StockMenuBar component of the application. """
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
    
    
    def _go_to_home(self, e):
        self.page.clean()
        self.page.go(Routes.HOME.value)
    
    
    def build_component(self):
        self.menu_bar = ft.MenuBar(
            expand=True,
            style=ft.MenuStyle(
                alignment=ft.alignment.top_left,
                bgcolor=ft.Colors.RED_100,
                mouse_cursor={
                    ft.ControlState.HOVERED: ft.MouseCursor.WAIT,
                    ft.ControlState.DEFAULT: ft.MouseCursor.ZOOM_OUT,
                },
            ),
            
            controls=[
                ft.SubmenuButton(
                    content=ft.Text("File"),
                    controls=[
                        ft.MenuItemButton(
                            content=ft.Text("About"),
                            leading=ft.Icon(ft.Icons.INFO),
                            style=ft.ButtonStyle(
                                bgcolor={ft.ControlState.HOVERED: ft.Colors.GREEN_100}
                            ),
                            on_click=self.handle_menu_item_click,
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("Quit"),
                            leading=ft.Icon(ft.Icons.CLOSE),
                            style=ft.ButtonStyle(
                                bgcolor={ft.ControlState.HOVERED: ft.Colors.GREEN_100}
                            ),
                            on_click=self._go_to_home,
                        ),
                    ]
                ),
                
                ft.SubmenuButton(
                    content=ft.Text("Products"),
                    controls=[
                        ft.MenuItemButton(
                            content=ft.Text("New"),
                            leading=ft.Icon(ft.Icons.ADD),
                            style=ft.ButtonStyle(
                                bgcolor={ft.ControlState.HOVERED: ft.Colors.GREEN_100}
                            ),
                            on_click=self.handle_menu_item_click,
                        ),
                        
                        ft.MenuItemButton(
                            content=ft.Text("Table"),
                            leading=ft.Icon(ft.Icons.LIST),
                            style=ft.ButtonStyle(
                                bgcolor={ft.ControlState.HOVERED: ft.Colors.GREEN_100}
                            ),
                            on_click=self.handle_menu_item_click,
                        ),
                    ]
                )
            ]
        )
        
        return ft.Row([self.menu_bar], alignment=ft.MainAxisAlignment.START)
    
    
    def handle_menu_item_click(self, e):
        print(f"{e.control.content.value}.on_click")
