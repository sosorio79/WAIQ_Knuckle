"""Port availability check for WAIQ Knuckle."""
import socket

DEFAULT_PORT = 5000


def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    """Return True if the port is in use (something is listening)."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.settimeout(0.5)
            s.connect((host, port))
            return True
        except (socket.error, OSError):
            return False


def is_port_available(port: int, host: str = "127.0.0.1") -> bool:
    """Return True if the port is available to bind (not in use)."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return True
        except (socket.error, OSError):
            return False


def prompt_for_port(default: int = DEFAULT_PORT) -> int:
    """If default port is in use, prompt user for a new port. Return the port to use."""
    if is_port_available(default):
        return default
    print(f"\n[!] Port {default} is already in use.")
    while True:
        try:
            inp = input(f"Enter a different port (or press Enter to try {default} again): ").strip()
            if not inp:
                port = default
            else:
                port = int(inp)
            if port < 1 or port > 65535:
                print("[!] Port must be between 1 and 65535.")
                continue
            if is_port_available(port):
                return port
            print(f"[!] Port {port} is also in use. Try another.")
        except ValueError:
            print("[!] Enter a valid number.")
