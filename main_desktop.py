import os
import sys
import socket
import threading
import http.server
import time
import subprocess
import webbrowser

# Enable Per-Monitor High-DPI Awareness on Windows
if sys.platform == 'win32':
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

def get_assets_directory():
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller bundled binary
        base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(sys.executable)))
    else:
        # Running from source python script
        base_dir = os.path.dirname(os.path.abspath(__file__))

    sub_dir = os.path.join(base_dir, 'agenda_pc')
    if os.path.isdir(sub_dir) and os.path.isfile(os.path.join(sub_dir, 'index.html')):
        return sub_dir
    return base_dir

def run_server(assets_dir):
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=assets_dir, **kwargs)

        def log_message(self, format, *args):
            pass

        def end_headers(self):
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            super().end_headers()

    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), QuietHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, port

def open_fallback(url):
    """Fallback if WebView2 runtime is missing or fails."""
    edge_candidates = [
        os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%LocalAppData%\Microsoft\Edge\Application\msedge.exe"),
    ]
    edge_exe = None
    for cand in edge_candidates:
        if os.path.isfile(cand):
            edge_exe = cand
            break

    if edge_exe:
        appdata = os.environ.get('APPDATA', os.path.expanduser('~'))
        profile_dir = os.path.join(appdata, 'AgendaOficialPC_EdgeProfile')
        proc = subprocess.Popen([edge_exe, f'--app={url}', f'--user-data-dir={profile_dir}'])
        proc.wait()
    else:
        webbrowser.open(url)
        # Keep alive while browser is open
        while True:
            time.sleep(5)

def main():
    assets_dir = get_assets_directory()
    server, port = run_server(assets_dir)
    url = f'http://127.0.0.1:{port}/index.html'

    # Persistent storage for localStorage, cache and user preferences
    appdata = os.environ.get('APPDATA', os.path.expanduser('~'))
    storage_dir = os.path.join(appdata, 'AgendaOficialPC')
    os.makedirs(storage_dir, exist_ok=True)

    icon_path = os.path.join(assets_dir, 'favicon.ico')
    if not os.path.isfile(icon_path):
        icon_path = None

    try:
        import webview
        window = webview.create_window(
            title='Agenda Oficial PC - Crônica Eclesiástica & Patrimônio',
            url=url,
            width=1366,
            height=820,
            min_size=(1024, 700),
            background_color='#12100e',
            text_select=True,
            zoomable=True
        )

        webview.start(
            gui='edgechromium',
            private_mode=False,
            storage_path=storage_dir,
            icon=icon_path
        )
    except Exception as e:
        print(f"[Aviso] Falha ao iniciar WebView2: {e}. Iniciando modo fallback navegador...")
        open_fallback(url)
    finally:
        try:
            server.shutdown()
        except Exception:
            pass

if __name__ == '__main__':
    main()
