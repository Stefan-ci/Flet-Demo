import flet as ft
from utils import Routes
from utils.database import DatabaseQuery


class RegisterPage(ft.Column):
    """ Register page of the application. """
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.adaptive = True
        self.page.title = f"Flet Demo Apps - Register"
    
    def build(self):
        return self.build_content()
    
    def build_content(self):
        self.username_input = ft.TextField(
            label="Username",
            keyboard_type=ft.KeyboardType.TEXT,
        )
        
        self.username_input = ft.TextField(
            label="Username",
            keyboard_type=ft.KeyboardType.TEXT,
        )
        
        self.first_name_input = ft.TextField(
            label="First name",
            keyboard_type=ft.KeyboardType.TEXT,
        )
        
        self.last_name_input = ft.TextField(
            label="Last name",
            keyboard_type=ft.KeyboardType.TEXT,
        )
        
        self.password_input = ft.TextField(
            label="Password",
            password=True,
            keyboard_type=ft.KeyboardType.VISIBLE_PASSWORD,
            can_reveal_password=True,
        )
        
        self.submit_button = ft.ElevatedButton(
            text="Register",
            icon=ft.Icons.LOGIN,
            on_click=self._handle_register,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(padding=10),
        )
        
        self.form_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Create Your Account", size=30, weight=ft.FontWeight.BOLD),
                    self.username_input,
                    self.first_name_input,
                    self.last_name_input,
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
    
    
    
    def _handle_register(self, e):
        username = self.username_input.value.strip()
        first_name = self.first_name_input.value
        last_name = self.last_name_input.value
        password = self.password_input.value # can be empty or not, no need to strip it
        
        if not username or username == "":
            self.page.open(ft.AlertDialog(title=ft.Text("Error"), content=ft.Text("Enter a valid username please")))
            self.page.update()
            return
        
        if not last_name or last_name == "":
            self.page.open(ft.AlertDialog(title=ft.Text("Error"), content=ft.Text("Enter a valid last name please")))
            self.page.update()
            return
        
        db_instance = DatabaseQuery()
        db_instance._create_tables()
        
        # check if user is available
        if db_instance._check_user_exists(username=username):
            alert = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text("Username already exist. Choose a new one."))
            self.page.open(alert)
            return
        
        # user exists
        if db_instance.register_user(last_name=last_name, username=username, password=password, first_name=first_name):
            self.page.controls.clear()
            
            self.page.open(ft.AlertDialog(title=ft.Text("Success"), content=ft.Text("Account created successfully. Login yet!", color=ft.Colors.GREEN)))
            
            # Redirect to login
            self.page.go(route=Routes.LOGIN.value)
        else:
            self.page.add(ft.Text("Registration failed. Check your data", color="red"))
            return
