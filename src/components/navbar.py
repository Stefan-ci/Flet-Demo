import flet as ft
from utils import Routes, all_default_views


class NavbarComponent(ft.Row):
    """ Navbar component of the application. """
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.padding = 10
        self.scroll = ft.ScrollMode.ALWAYS
        self.adaptive = True
    
    
    def _open_menu(self, e):
        self.page.controls.clear() # clear page to avoid duplication
        self.drawer.open = True
        self.page.open(self.build())
    
    
    def _go_to_selected_page(self, e):
        self.all_routes = [
            control for control in self.drawer.controls
            if isinstance(control, ft.NavigationDrawerDestination)
        ]
        self.selected_route = None
        self.selected_route_index = e.control.selected_index
        
        if 0 <= self.selected_route_index < len(self.all_routes):
            selected_item = self.all_routes[self.selected_route_index]
            
            if selected_item.data:
                self.selected_route = selected_item.data.value
            else:
                self.selected_route = Routes.PAGE_NOT_FOUND.value
        
        if self.selected_route:
            self.drawer.open = False
            self.page.controls.clear()
            self.page.update()
            
            self.page.go(self.selected_route)
            self.page.update()
        else:
            self.page.update()
    
    
    def display_open_drawer_button(self, e):
        self.drawer.open = False
        self.drawer.update()
        self.page.floating_action_button = ft.FloatingActionButton(
            icon=ft.Icons.MENU,
            tooltip="Open Menu",
            on_click=self._open_menu,
            mini=False,
            mouse_cursor=ft.MouseCursor.CLICK,
        )
        self.page.update()
    
    
    def build(self):
        self.nav_items = [
            ft.NavigationDrawerDestination(icon=view.get("icon"), label=view.get("title"), data=view.get("route_data"))
            for view in all_default_views()
        ]
        self.drawer = ft.NavigationDrawer(
            open=True,
            position=ft.NavigationDrawerPosition.START,
            on_change=self._go_to_selected_page,
            on_dismiss=self.display_open_drawer_button,
            controls=[
                ft.NavigationDrawerDestination(icon=ft.Icons.HOME, label="Home", data=Routes.HOME),
                ft.Divider(thickness=2),
                
                *self.nav_items
            ],
        )
        
        return self.drawer
