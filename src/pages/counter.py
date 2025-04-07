import flet as ft


class CounterPage(ft.Column):
    """ Counter page of the application. """
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.page.title = f"Flet Demo Apps - Counter"
    
    def build(self):
        self.page.update()
        return self.build_content()
    
    def build_content(self):
        self.counter = ft.Text("0", size=50, data=0)
        
        self.counter_button = ft.ElevatedButton(
            icon=ft.Icons.ADD_CIRCLE,
            on_click=self.increment_click,
            tooltip="Click to increment the counter",
            text="Increment",
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(padding=10),
        )
        
        container = ft.Container(
            content=ft.Column(
                controls=[
                    self.counter,
                    self.counter_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ), # End Column,
            padding=30,
            width=600,
            border_radius=15,
            border=ft.border.all(1, ft.Colors.GREY_300),
            shadow=ft.BoxShadow(blur_radius=0, color=ft.Colors.BLACK12),
        )
        
        
        area = ft.Column(
            controls=[container],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ALWAYS,
            expand=True,
            on_scroll_interval=0,
        )
        
        self.page.add(ft.SafeArea(area))
    
    
    def increment_click(self, e):
        self.counter.data += 1
        self.counter.value = str(self.counter.data)
        self.counter.update()
