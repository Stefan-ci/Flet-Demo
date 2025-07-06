from enum import Enum


class Routes(Enum):
    HOME = "/"
    
    # Auth endpoints
    LOGIN = "/login"
    REGISTER = "/register"
    
    # Stack App endpoints
    STOCK_MANAGEMENT = "/stock-management"
    
    # Defaults endpoints (from defaults dir)
    BROWSER = "/browser"
    COUNTER = "/counter"
    TEXT_TO_AUDIO = "/text-to-audio"
    URL_SHORTENER = "/url-shortener"
    
    # Errors endpoints
    PAGE_NOT_FOUND = "/page-not-found"
    ACCESS_DENIED = "/unauthorized"
