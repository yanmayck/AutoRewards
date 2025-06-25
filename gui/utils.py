# gui/utils.py

import queue

class QueueHandler(queue.Queue):
    """Redireciona o stdout para uma fila para ser lido pela UI."""
    def write(self, msg):
        # Ignora mensagens de erro internas do Tkinter ao fechar a janela
        if 'PY_SSIZE_T_CLEAN' not in msg:
            self.put(msg)

    def flush(self):
        pass