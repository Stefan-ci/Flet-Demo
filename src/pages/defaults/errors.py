import flet as ft
from utils import CustomSizes


class PageNotFoundPage(ft.Column):
    """ Error 404 page. """
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.page.title = f"Flet Demo Apps - Page not found"
    
    def build(self):
        self.page.update()
        return self.build_content()
    
    def build_content(self):
        self.page_header = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Error 404 - Page Not Found", size=CustomSizes.PAGE_TITLE.value, weight=ft.FontWeight.BOLD),
                ]
            )
        )
        
        area = ft.Column(
            controls=[self.page_header],
            scroll=ft.ScrollMode.ALWAYS,
            expand=True,
            on_scroll_interval=0,
        )
        
        self.page.add(ft.SafeArea(area))
