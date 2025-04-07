import flet as ft
import validators
from pyshorteners import Shortener


class UrlShortenerPage(ft.Column):
    """ UrlShortener page of the application. """
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.page.title = "Flet Demo Apps - URL Shortener"
    
    
    def build(self):
        self.page.update()
        return self.build_content()
    
    
    def build_content(self):
        # URL input field
        self.url_input = ft.TextField(
            label="Enter the URL here.",
            keyboard_type=ft.KeyboardType.URL,
            autofocus=True,
        )
        
        # Button to submit the URL
        self.shorten_button = ft.ElevatedButton(
            text="Shorten",
            on_click=self._shorten_url,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(padding=10),
        )
        
        # display the shortened URL
        self.result_text = ft.Text(size=18, weight="bold")
        
        
        # button to copy the shortened URL
        self.copy_button = ft.IconButton(
            icon=ft.Icons.COPY,
            on_click=self._copy_to_clipboard,
            visible=False
        )
        
        # alert dialog to show success message
        self.success_copy_alert = ft.AlertDialog(
            modal=True,
            title=ft.Text("Success"),
            content=ft.Text("URL copied succesfully!"),
            actions_alignment=ft.MainAxisAlignment.END,
            actions=[
                ft.TextButton("OK", on_click=self._handle_alert_close),
            ],
        )
        
        self.form_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("URL Shortener", size=30, weight=ft.FontWeight.BOLD),
                    self.url_input,
                    self.shorten_button,
                    self.result_text,
                    self.copy_button,
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ), # End Column,
            padding=30,
            width=600,
            border_radius=15,
            border=ft.border.all(1, ft.Colors.GREY_300),
            shadow=ft.BoxShadow(blur_radius=0, color=ft.Colors.BLACK12),
        )
        
        self.converter_area = ft.Column(
            controls=[self.form_container],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ALWAYS,
            expand=True,
            on_scroll_interval=0,
        )
        
        self.page.add(ft.SafeArea(self.converter_area))
    
    
    def _copy_to_clipboard(self, e):
        self.page.set_clipboard(self.copy_button.data)
        self.page.open(self.success_copy_alert)
        self.page.update()
    
    
    def _handle_alert_close(self, e):
        self.page.close(self.success_copy_alert)
    
    
    def _shorten_url(self, e):
        url = self.url_input.value.strip()
        
        if not url or url == "":
            self.result_text.value = "Please enter a URL"
            self.result_text.color = ft.Colors.RED
            self.result_text.weight = ft.FontWeight.NORMAL
        
        elif not validators.url(url):
            self.result_text.value = "Invalid URL"
            self.result_text.color = ft.Colors.RED
        
        else:
            try:
                short_url = Shortener().tinyurl.short(url)
                self.result_text.value = short_url
                self.result_text.color = ft.Colors.BLUE
                self.result_text.selectable = True
                
                self.copy_button.visible = True
                self.copy_button.data = short_url
            except Exception as e:
                self.result_text.value = f"An error occurred: {e}"
                self.result_text.color = ft.Colors.RED
        
        self.page.update()
