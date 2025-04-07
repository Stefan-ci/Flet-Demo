from enum import Enum

class Routes(Enum):
    HOME = "/"
    LOGIN = "/login"
    COUNTER = "/counter"
    REGISTER = "/register"
    TEXT_TO_AUDIO = "/text-to-audio"
    URL_SHORTENER = "/url-shortener"
    PAGE_NOT_FOUND = "/page-not-found"
    STOCK_MANAGEMENT = "stock-management"
