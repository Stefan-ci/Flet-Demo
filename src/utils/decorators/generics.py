import flet as ft
from utils import Routes
from utils.settings import CURRENT_USER_SESSION_KEY


def login_required(page: ft.Page, redirect_route: str = Routes.LOGIN.value):
    current_user = page.session.get(CURRENT_USER_SESSION_KEY)
    
    if not current_user:
        page.go(redirect_route)
        return False
    return True


class LoginRequiredMixin:
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_user = self.page.session.get(CURRENT_USER_SESSION_KEY)
        if not self.current_user:
            self.page.clean()
            self.page.go(Routes.LOGIN.value)


class AdminRequiredMixin(LoginRequiredMixin):
    def __init__(self, page: ft.Page):
        super().__init__(page)
        if not self.current_user.get("is_admin", False):
            self.page.go(Routes.ACCESS_DENIED.value)
