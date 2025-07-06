import flet as ft
from utils import Routes

from pages.stock import StockHomePage
from pages.converters import TextToAudioPage
from pages.auth import LoginPage, RegisterPage
from pages.defaults import HomePage, UrlShortenerPage, PageNotFoundPage, CounterPage, BrowserPage


def get_page_content_by_route(page: ft.Page, route: str):
    # Homepage
    if route == Routes.HOME.value:
        return HomePage(page=page).build()
    
    # Auth app
    elif route == Routes.LOGIN.value:
        return LoginPage(page=page).build()
    elif route == Routes.REGISTER.value:
        return RegisterPage(page=page).build()
    
    # Defaults app
    elif route == Routes.TEXT_TO_AUDIO.value:
        return TextToAudioPage(page=page).build()
    elif route == Routes.URL_SHORTENER.value:
        return UrlShortenerPage(page=page).build()
    elif route == Routes.COUNTER.value:
        return CounterPage(page=page).build()
    elif route == Routes.BROWSER.value:
        return BrowserPage(page=page).build()
    
    
    # stock app
    elif route == Routes.STOCK_MANAGEMENT.value:
        return StockHomePage(page=page).build()
    
    # Page not found
    else:
        return PageNotFoundPage(page=page).build()
