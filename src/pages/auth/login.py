import time
import flet as ft
from utils import Routes
from utils.database import DatabaseQuery

class LoginPage(ft.Column):
    """ Login page of the application. """
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.adaptive = True
        self.page.title = f"Flet Demo Apps - Login"
    
    def build(self):
        return self.build_content()
    
    def build_content(self):
        self.username_input = ft.TextField(
            label="Username",
            keyboard_type=ft.KeyboardType.TEXT,
        )
        
        self.password_input = ft.TextField(
            label="Password",
            password=True,
            keyboard_type=ft.KeyboardType.VISIBLE_PASSWORD,
            can_reveal_password=True,
        )
        
        self.submit_button = ft.ElevatedButton(
            text="Sign In",
            icon=ft.Icons.JOIN_LEFT,
            on_click=self._handle_login,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(padding=10),
        )
        
        self.form_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Login to Your Account", size=30, weight=ft.FontWeight.BOLD),
                    self.username_input,
                    self.password_input,
                    self.submit_button,
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
        
        
        self.display_area = ft.Column(
            controls=[self.form_container],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ALWAYS,
            expand=True,
            on_scroll_interval=0,
        )
        
        self.page.add(ft.SafeArea(self.display_area))
    
    
    def _handle_login(self, e):
        global current_user
        
        username = self.username_input.value.strip()
        password = self.password_input.value # can be empty or not, no need to strip it
        
        if not username or username == "":
            self.page.open(ft.AlertDialog(title=ft.Text("Error"), content=ft.Text("Enter a valid username please")))
            self.page.update()
            return
        
        db_instance = DatabaseQuery()
        db_instance._create_tables()
        
        # check if user is available, if not redirect to register
        if not db_instance._check_user_exists(username=username):
            alert = ft.AlertDialog(title=ft.Text("Warning"), content=ft.Text("You haven't an account yet. Register a new one!"))
            self.page.open(alert)
            
            # visual stuffs
            time.sleep(1)
            
            self.page.close(alert)
            
            # redirect
            self.page.clean()
            self.page.go(route=Routes.REGISTER.value)
            return
        
        # user exists
        if db_instance.login_user(username, password):
            current_user = username
            self.page.controls.clear()
            
            # Add welcome message
            self.page.add(self.show_dashboard_after_login())
        else:
            self.page.add(ft.Text("Login failed. Check your data", color="red"))
            return
    
    
    def show_dashboard_after_login(self):
        self.dashboard = ft.Text(weight=ft.FontWeight.BOLD, size=40, value=f"Welcome, {current_user}", color=ft.Colors.BLACK)
        return ft.SafeArea(self.dashboard)
