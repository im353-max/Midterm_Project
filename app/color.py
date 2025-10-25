from colorama import Fore, Style

class Colors:
    INFO = Fore.CYAN
    SUCCESS = Fore.GREEN
    WARNING = Fore.YELLOW
    ERROR = Fore.RED
    RESET = Style.RESET_ALL

def print_info(message: str):
    print(f"{Colors.INFO}{message}{Colors.RESET}")

def print_success(message: str):
    print(f"{Colors.SUCCESS}{message}{Colors.RESET}")

def print_warning(message: str):
    print(f"{Colors.WARNING}{message}{Colors.RESET}")

def print_error(message: str):
    print(f"{Colors.ERROR}{message}{Colors.RESET}")