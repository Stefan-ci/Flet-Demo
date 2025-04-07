import flet as ft
from utils import CustomSizes


class CreateProductPage(ft.Column):
    """ Create product page of the application. """
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.page.title = f"Flet Demo Apps - New Product"
    
    def build(self):
        self.page.update()
        return self.build_content()
    
    def build_content(self):
        self.page_header = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Add a new product", size=CustomSizes.PAGE_TITLE.value, weight=ft.FontWeight.BOLD),
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
