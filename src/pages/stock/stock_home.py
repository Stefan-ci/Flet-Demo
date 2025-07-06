import flet as ft
from components.stock import StockMenuBarComponent

from utils import CustomSizes, Routes
from utils.settings import CURRENT_USER_SESSION_KEY
from utils.decorators.generics import LoginRequiredMixin



class StockHomePage(LoginRequiredMixin, ft.Column):
    """ Homepage of stock """
    
    def __init__(self, page: ft.Page):
        # super().__init__()
        LoginRequiredMixin.__init__(self, page)
        ft.Column.__init__(self)
        
        self.page = page
        self.page.title = f"Flet Demo Apps - Stock App"
        
        self.menu_bar = StockMenuBarComponent(page=page)
    
    def build(self):
        self.page.update()
        return self.build_content()
    
    def build_content(self):
        # Menu bar
        self.page.add(self.menu_bar.build_component())
        
        
        self.page_header = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Stock App", size=CustomSizes.PAGE_TITLE.value, weight=ft.FontWeight.BOLD),
                ]
            )
        )
        
        content = ft.ListView(
            expand=True,
            auto_scroll=True,
            controls=[
                ft.Text(value=f"Test {i}")
                for i in range(100)
            ]
        )
        
        area = ft.Column(
            controls=[self.page_header, content],
            scroll=ft.ScrollMode.ALWAYS,
            expand=True,
            on_scroll_interval=0,
        )
        
        self.page.add(ft.SafeArea(area))
