from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

# Caminho para o banco de dados
DB_PATH = "../data_analysis/coleta_armazenamento/youtube_data.db"

class DatabaseHandler(FileSystemEventHandler):
    """Classe para monitorar mudanças no banco de dados SQLite"""

    def on_modified(self, event):
        if event.src_path.endswith("youtube_data.db"):
            print(f"📢 Banco de dados atualizado: {event.src_path}")
            # Aqui podemos disparar uma ação para atualizar os dados

# Criar o observador
observer = Observer()
event_handler = DatabaseHandler()
observer.schedule(event_handler, path=os.path.dirname(DB_PATH), recursive=False)

# Iniciar o Watchdog
observer.start()
print("👀 Monitorando mudanças no banco de dados...")

try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    observer.stop()
    print("🛑 Monitoramento encerrado.")

observer.join()