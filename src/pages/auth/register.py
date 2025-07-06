import re
import flet as ft
from utils import Routes
from utils.databases.models import UserModel
from utils.databases.interface import DatabaseInterface
from utils.settings import CURRENT_USER_SESSION_KEY, DEFAULT_PASSWORD_LENGTH


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
            on_submit=self._handle_register,
        )
        
        self.email_input = ft.TextField(
            label="Email",
            keyboard_type=ft.KeyboardType.EMAIL,
            on_submit=self._handle_register,
        )
        
        self.first_name_input = ft.TextField(
            label="First name",
            keyboard_type=ft.KeyboardType.TEXT,
            on_submit=self._handle_register,
        )
        
        self.last_name_input = ft.TextField(
            label="Last name",
            keyboard_type=ft.KeyboardType.TEXT,
            on_submit=self._handle_register,
        )
        
        self.password_input = ft.TextField(
            label="Password",
            password=True,
            keyboard_type=ft.KeyboardType.VISIBLE_PASSWORD,
            can_reveal_password=True,
            on_submit=self._handle_register,
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
                    self.email_input,
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
        email = self.email_input.value.strip()
        first_name = self.first_name_input.value
        last_name = self.last_name_input.value
        password = self.password_input.value # can be empty or not, no need to strip it
        
        if not username or username == "":
            self.page.open(ft.AlertDialog(title=ft.Text("Error"), content=ft.Text("Enter a valid username please")))
            self.page.update()
            return
        
        if not last_name.strip() or last_name.strip() == "":
            self.page.open(ft.AlertDialog(title=ft.Text("Error"), content=ft.Text("Enter a valid last name please")))
            self.page.update()
            return
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.page.open(ft.AlertDialog(title="Error", content=ft.Text("Invalid email format!")))
            return
        
        if len(password) < DEFAULT_PASSWORD_LENGTH:
            self.page.open(ft.AlertDialog(title="Error", content=ft.Text("Password too short!")))
            return
        
        with DatabaseInterface() as db:
            self.users_objects = db.users_objects
            
            # check if username is already taken
            if self.users_objects.exists(username=username):
                self.page.open(ft.AlertDialog(title=ft.Text("Warning"), content=ft.Text("Username already taken! Choose a new one.")))
                return
            
            # validation: OK -> Create user
            user: UserModel = self.users_objects.create(
                username=username,
                email=email,
                last_name=last_name,
                first_name=first_name,
                password=password,
            )
            
            # if there were no user and the current user is the first one, give him admin rights
            if self.users_objects.count() <= 1:
                self.users_objects.update(id=user.id, is_admin=True)
            
            
            # user saved
            self.page.controls.clear()
            self.page.open(ft.AlertDialog(title=ft.Text("Success"), content=ft.Text("Account created successfully. Login yet!", color=ft.Colors.GREEN)))
            # Redirect to login
            self.page.go(route=Routes.LOGIN.value)
