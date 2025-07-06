import flet as ft
import validators
import flet_webview
from utils import CustomSizes


class BrowserPage(ft.Column):
    """ Browser of stock """
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.page.title = f"Flet Demo Apps - Stock App"
    
    def build(self):
        self.page.update()
        return self.build_content()
    
    def build_content(self):
        HEIGHT = 50
        self.page_header = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Browser simulation", size=CustomSizes.PAGE_TITLE.value, weight=ft.FontWeight.BOLD),
                ]
            )
        )
        
        self.ask_for_url = ft.TextField(
            label="URL or Search Query",
            hint_text="Enter the URL to browse here or the term to search for",
            keyboard_type=ft.KeyboardType.URL,
            autofocus=True,
            expand=True,
            border=ft.InputBorder.NONE,
            content_padding=ft.padding.all(10),
            on_submit=self._browse_or_search_on_google,
            height=HEIGHT,
        )
        
        self.submit_button = ft.ElevatedButton(
            text="Go",
            icon=ft.Icons.SEARCH,
            on_click=self._browse_or_search_on_google,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
            height=HEIGHT,
            # style=ft.ButtonStyle(
            #     shape=ft.RoundedRectangleBorder(radius=0),
            #     padding=ft.padding.symmetric(horizontal=20),
            # ),
        )
        
        self.ask_area = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    border=ft.border.all(0.5),
                    border_radius=ft.border_radius.all(5),
                    padding=0,
                    content=ft.Row(
                        spacing=0,
                        controls=[self.ask_for_url, self.submit_button]
                    )
                )
            ],
        )
        
        
        self.display_area = ft.Column(
            controls=[
                self.page_header,
                ft.Divider(),
                self.ask_area,
            ],
            scroll=ft.ScrollMode.ALWAYS,
            expand=True,
            on_scroll_interval=0,
        )
        
        self.page.add(ft.SafeArea(self.display_area))
    
    
    def _browse_or_search_on_google(self, e):
        # check if not empty string
        search_term = self.ask_for_url.value
        if search_term.strip() == "" or search_term.strip() is None:
            self.page.open(ft.AlertDialog(title=ft.Text("Empty search term"), content=ft.Text("Your search is empty. Please provide either a link or a term to search for.")))
            return
        
        # Either a URL or a search term
        self.url_to_browse = search_term if validators.url(search_term) else f"https://www.google.com/search?q={search_term}"
        self.display_area.controls.append(ft.SafeArea(
                ft.Container(
                    expand=True,
                    adaptive=True,
                    content=flet_webview.WebView(
                        url=self.url_to_browse,
                        expand=True,
                        visible=True
                    ),
                )
            )
        )
        
        self.ask_area.visible = False
        self.display_area.update()
        self.page.update()
