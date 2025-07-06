import flet as ft
from utils import Routes


def all_default_views():
    """
    Utility to host all available views (including URLs, titles, descriptions, icons, …).
    These are main views, like homepages, list pages, read data page, …
    """
    
    views = [
        # Login
        {
            "route": Routes.LOGIN.value,
            "title": "Login",
            "desc": "Login page simulation",
            "icon": ft.Icons.LOGIN,
            "route_data": Routes.LOGIN,
        },
        
        # Register
        {
            "route": Routes.REGISTER.value,
            "title": "Register",
            "desc": "Register page simulation",
            "icon": ft.Icons.JOIN_LEFT,
            "route_data": Routes.REGISTER,
        },
        
        # URL Shortener
        {
            "route": Routes.URL_SHORTENER.value,
            "title": "Shorten URL",
            "desc": "An App to shorten URLs (using the 'tiny' mechanism)",
            "icon": ft.Icons.LINK,
            "route_data": Routes.URL_SHORTENER,
        },
        
        # Text to audio
        {
            "route": Routes.TEXT_TO_AUDIO.value,
            "title": "Text To Audio",
            "desc": "An App to convert a text into an audio (using Murf AI)",
            "icon": ft.Icons.AUDIOTRACK,
            "route_data": Routes.TEXT_TO_AUDIO,
        },
        
        # Counter
        {
            "route": Routes.COUNTER.value,
            "title": "Counter",
            "desc": "The default counter app (just modified for purpose)",
            "icon": ft.Icons.COUNTERTOPS_ROUNDED,
            "route_data": Routes.COUNTER,
        },
        
        # Stock App
        {
            "route": Routes.STOCK_MANAGEMENT.value,
            "title": "Stock Management",
            "desc": "An application to imitate a product stock app",
            "icon": ft.Icons.PRODUCTION_QUANTITY_LIMITS,
            "route_data": Routes.STOCK_MANAGEMENT,
        },
        
        # Browser
        {
            "route": Routes.BROWSER.value,
            "title": "Tiny Browser",
            "desc": "A custom built-in browser",
            "icon": ft.Icons.SEARCH,
            "route_data": Routes.BROWSER,
        },
    ]
    
    return views
