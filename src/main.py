import flet as ft

# local imports
from components import NavbarComponent
from utils import Routes, get_page_content_by_route


def main(page: ft.Page):
    page.title = "Flet Demo Apps"
    page.adaptive = True
    page.window.maximized = True # using max dimensions of the device's screen
    page.scroll = ft.ScrollMode.AUTO # scroll if necessary
    page.theme_mode = ft.ThemeMode.LIGHT
    
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.drawer = NavbarComponent(page=page).build()
    
    
    # routing
    def change_view(e: ft.RouteChangeEvent):
        route = e.route
        return get_page_content_by_route(page=page, route=route)
    
    page.on_route_change = change_view
    
    # set initial route
    page.clean()
    page.update()
    page.go(Routes.HOME.value)
    
    # open navbar on start
    page.open(NavbarComponent(page=page).build())
    
    print(page.views)



ft.app(target=main)
