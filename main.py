import sys

# Gestion des importations
try:
    from colorama import Fore, Style, init
    import json
    import os
    import re
    import subprocess
    import tkinter as tk
    import shutil
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    from pathlib import Path
    from tkinter import ttk
    from urllib.parse import unquote, parse_qs
    import psutil
    import webbrowser
    import qrcode
    import socket
    import random
    from PIL import Image
except ImportError as e:
    print(f"Erreur d'importation : {e}. "
          f"Contactez notre support : https://discord.com/channels/1253370383478952007/1306260817775165601")
    import json
    import os
    import re
    import subprocess
    import tkinter as tk
    import shutil
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    from pathlib import Path
    from tkinter import ttk
    from urllib.parse import unquote, parse_qs
    import psutil
    import webbrowser
    import qrcode
    import socket
    import random
    from PIL import Image
    from colorama import Fore, Style, init
    sys.exit(1)

# Variables globales
folder_path = None
init(autoreset=True)
sys.stderr = open(os.devnull, 'w')

def generate_qr_code(ip, port):
    url = f"http://{ip}:{port}"
    print(Fore.BLUE + f"URL : {url}")
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=0,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color=(240, 244, 248))
    logo_path = "System/IcoRetour2.png"
    logo = Image.open(logo_path)
    logo_size = 15
    logo = logo.resize((logo_size, logo_size))

    pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
    img.paste(logo, pos, mask=logo)

    img.save("System/qr_code.png")


def setup_directories():
    global folder_path
    base_path = Path(__file__).resolve().parent
    os.chdir(base_path)
    folder_path = base_path / 'Menu'

    if not folder_path.exists():
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"Dossier créé à : {folder_path}")

    os.chdir(folder_path)
    user_home = Path.home()
    workspace_folder = folder_path / "Espace de Travail"
    appdata_folder = user_home / "AppData/Roaming/FilesNet"

    appdata_folder.mkdir(parents=True, exist_ok=True)

    try:
        for item in appdata_folder.iterdir():
            destination_item = workspace_folder / item.name
            if item.is_dir():
                shutil.copytree(item, destination_item, dirs_exist_ok=True)
            else:
                shutil.copy2(item, destination_item)
    finally:
        pass


def get_metrics():
    disk_usage = psutil.disk_usage('/').percent
    return {'disk': disk_usage}


class FileHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path_mapping = {
            '/': '/System/index.html',
            '/styles.css': '/System/styles.css',
            '/script.js': '/System/scrypt.js',
        }

        if self.path in path_mapping:
            self.path = path_mapping[self.path]
        elif self.path == '/metrics':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            metrics = get_metrics()
            self.wfile.write(json.dumps(metrics).encode())
            return
        elif self.path == '/stop':
            sys.exit()
        elif self.path.startswith('/files'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            query = unquote(self.path.split('?path=')[-1])
            path = Path(query) if query else Path('.')
            if path.is_dir():
                files = [{'name': f.name, 'path': str(f), 'isDirectory': f.is_dir()} for f in path.iterdir()]
                self.wfile.write(json.dumps(files).encode())
            else:
                self.wfile.write(json.dumps([]).encode())
            return
        elif self.path.startswith('/fileinfo'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            query = unquote(self.path.split('?path=')[-1])
            path = Path(query)
            info = {'isDirectory': path.is_dir()}
            self.wfile.write(json.dumps(info).encode())
            return
        elif self.path.startswith('/edit'):
            query = unquote(self.path.split('?path=')[-1])
            path = Path(query)
            if path.exists() and path.is_file():
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                with open(path, 'r', encoding='utf-8') as file:
                    self.wfile.write(file.read().encode())
            else:
                self.send_response(404)
                self.end_headers()
            return
        elif self.path.startswith('/download'):
            download_type = self.path.split('type=')[-1]
            query = unquote(self.path.split('?path=')[-1])
            if re.search("&type=directory", query):
                query = query.replace("&type=directory", "")
            elif re.search("&type=file", query):
                query = query.replace("&type=file", "")
            else:
                print("Erreur dans le nom du Fichier / Dossier.")
            path = Path(query)
            if path.exists():
                if download_type == 'file':
                    self.send_response(200)
                    self.send_header('Content-Disposition', f'attachment; filename="{path.name}"')
                    self.end_headers()
                    with open(path, 'rb') as file:
                        shutil.copyfileobj(file, self.wfile)
                elif download_type == 'directory':
                    zip_path = shutil.make_archive(str(path), 'zip', root_dir=path.parent, base_dir=path.name)
                    self.send_response(200)
                    self.send_header('Content-Disposition', f'attachment; filename="{path.name}.zip"')
                    self.end_headers()
                    with open(zip_path, 'rb') as file:
                        shutil.copyfileobj(file, self.wfile)
                    os.remove(zip_path)
            else:
                self.send_response(404)
                self.end_headers()
            return
        return super().do_GET()

    def do_DELETE(self):
        if self.path.startswith('/delete'):
            query = unquote(self.path.split('?path=')[-1])
            path = Path(query)
            if path.exists():
                if path.is_file():
                    path.unlink()
                else:
                    shutil.rmtree(path)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True}).encode())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False}).encode())
            return

    def do_POST(self):
        if self.path.startswith('/rename'):
            query = parse_qs(unquote(self.path.split('?')[-1]))
            path = Path(query['path'][0])
            new_name = query['newName'][0]
            new_path = path.with_name(new_name)
            if re.search("/", new_name):
                shutil.move(new_path, str(folder_path))
            if path.exists():
                path.rename(new_path)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True}).encode())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False}).encode())
            return
        elif self.path.startswith('/save'):
            query = parse_qs(unquote(self.path.split('?')[-1]))
            path = Path(query['path'][0])
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            if path.exists() and path.is_file():
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(data['content'])
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True}).encode())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False}).encode())
            return
        elif self.path.startswith('/create'):
            query = parse_qs(unquote(self.path.split('?')[-1]))
            item_type = query['type'][0]
            name = query['name'][0]
            path = Path(query.get('path', [''])[0])
            full_path = path / name
            try:
                if item_type == 'fichier':
                    full_path.touch()
                elif item_type == 'dossier':
                    full_path.mkdir(parents=True, exist_ok=True)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode())
            return


def webopen(port):
    webbrowser.open_new_tab(f"http://localhost:{port}")


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    finally:
        s.close()
    return local_ip


def run(server_class=HTTPServer, handler_class=FileHandler, port=1024):
    global folder_path
    if folder_path is None:
        raise ValueError("folder_path is not defined")
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    generate_qr_code(ip, port)
    webopen(port)
    httpd.serve_forever()


def get_html_path():
    current_dir = Path(__file__).resolve().parent
    html_path = current_dir / 'index.html'
    return html_path


def scripts_python():
    global folder_path
    if folder_path is None:
        raise ValueError(Fore.LIGHTRED_EX + "folder_path is not defined")
    repertoire_plugin = folder_path / "Espace de Travail/System/Plugin"
    for fichier in repertoire_plugin.iterdir():
        if fichier.suffix == '.py' and fichier.name != Path(__file__).name:
            print(Fore.LIGHTGREEN_EX + f"Exécution de {fichier.name}...")
            try:
                subprocess.run(['python', fichier], check=True)
            except subprocess.CalledProcessError as e:
                print(Fore.LIGHTRED_EX + f"Erreur lors de l'exécution de {fichier.name}: {e}")

def create_gui():
    root = tk.Tk()
    ttk.Style(root)
    frame1 = ttk.Frame(root, padding=10)
    text2 = tk.Entry(frame1, font="Helvetica 12 bold", bg="peach puff", borderwidth=0, highlightthickness=5, width=20)

    def open_appdata():
        global folder_path
        if os.path.exists(str(folder_path)):
            os.startfile(str(folder_path))
        else:
            print(Fore.LIGHTRED_EX + "AppData indisponible.")
        root.attributes('-topmost', True)

    text3 = tk.Button(frame1, text="ADD FILE", font="Helvetica 18 bold", borderwidth=0, highlightthickness=0, width=10,
                      height=2, bg='moccasin', command=open_appdata)

    def start_server():
        global port
        port = text2.get()
        root.destroy()

    def open_plugin():
        global folder_path
        if folder_path is None:
            raise ValueError(Fore.LIGHTRED_EX + "folder_path is not defined")
        if os.path.exists(folder_path / "Espace de Travail/System/Plugin"):
            os.startfile(folder_path / "Espace de Travail/System/Plugin")
        else:
            print(Fore.LIGHTRED_EX + "Script des Plugins infonctionnel")

    text1 = tk.Button(frame1, text="START", font="Helvetica 18 bold", borderwidth=0, highlightthickness=0,
                      command=start_server, width=10, height=2, bg='moccasin')
    text4 = tk.Button(frame1, text="PLUGIN", font="Helvetica 18 bold", borderwidth=0, highlightthickness=0,
                      command=open_plugin, width=10, height=2, bg='moccasin')

    root.overrideredirect(True)
    root.configure(background="white")
    root.wm_attributes("-transparentcolor", "white")

    frame1.pack(side="top", fill="both", expand=True, padx=20, pady=40)
    text2.pack(fill="both", expand=True)
    text1.pack(fill="both", expand=True)
    text3.pack(fill="both", expand=True)
    text4.pack(fill="both", expand=True)

    html_path = get_html_path()
    if os.path.exists(html_path):
        print(Fore.LIGHTWHITE_EX + f"Le chemin vers index.html est : {html_path}")
        with open(html_path, 'r') as file:
            html_content = file.read()
        print(Fore.LIGHTGREEN_EX + "Chargement de FilesNet effectué !")
        return html_content

    root.mainloop()


if __name__ == "__main__":
    setup_directories()
    create_gui()

    global port
    try:
        port = int(port)
    except ValueError:
        if port == "Admin":
            print(Fore.BLUE + "Mode Administrateur")
            sys.stderr = sys.__stderr__
            port = 49151
        else:
            port = 49151

    if not (1024 <= port <= 49150):
        port = random.randint(1024, 49150)

    ip = get_local_ip()
    if not ip:
        ip = socket.gethostbyname(socket.gethostname())

    scripts_python()
    run(port=port)
