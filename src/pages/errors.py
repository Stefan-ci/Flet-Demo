import flet as ft


class PageNotFoundPage(ft.Column):
    """ Error 404 page. """
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
    
    
    def build_content(self):
        self.controls = [
            ft.Text("PageNotFoundPage", size=30, weight=ft.FontWeight.BOLD),
            ft.ListView(expand=True, controls=[ft.Text(f"Items {i}") for i in range(50)])
        ]
