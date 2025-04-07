import flet as ft
from utils import all_default_views


class HomePage(ft.Column):
    """ Home page of the application. """
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.page.title = f"Flet Demo Apps - Home"
    
    def build(self):
        self.page.update()
        return self.build_content()
    
    def _go_to_linked_page(self, route: str):
        self.page.controls.clear()
        self.page.go(route)
    
    
    def build_content(self):
        self.card_row = ft.ResponsiveRow(
            spacing=10,
            run_spacing=10,
            controls=[
                ft.Column(
                    col={"sm": 12, "md": 4}, # 12/4 = 3 cards per row on medium screens and up
                    controls=[
                        ft.Card(
                            col={"sm": 12, "md": 4},
                            data=view,
                            content=ft.Container(
                                width=400,
                                padding=10,
                                content=ft.Column(
                                    controls=[
                                        ft.ListTile(
                                            leading=ft.Icon(view.get("icon")),
                                            title=ft.Text(value=view.get("title"), weight=ft.FontWeight.BOLD),
                                            subtitle=ft.Text(value=view.get("desc")),
                                        ),
                                        ft.Row(
                                            controls=[
                                                ft.TextButton(
                                                    text="Go to",
                                                    on_click=lambda _, r=view["route"]: self._go_to_linked_page(route=r),
                                                    icon=ft.Icons.ARROW_RIGHT,
                                                    data=view,
                                                ),
                                            ],
                                            alignment=ft.MainAxisAlignment.END,
                                        ),
                                    ]
                                )
                            ), # End Container
                        ) # End Card
                        
                    ]
                )
                for view in all_default_views()
            ]
        )
        
        self.page.add(ft.Container(
            content=ft.Column(
                expand=True,
                scroll=ft.ScrollMode.ALWAYS,
                adaptive=True,
                controls=[
                    ft.Text("Homepage", size=30, weight=ft.FontWeight.BOLD),
                    
                    self.card_row,
                ],
                
            )
        ))
