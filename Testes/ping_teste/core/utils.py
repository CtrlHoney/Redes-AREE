import os
import time
import threading

def ping(de: str, para: str, ip: str, res: list, lock: threading.Lock) -> None:
    """
    Realiza o ping entre dois containers e armazena o resultado.
    """
    ini = time.time()
    comando = f"docker exec {de} ping -c 1 -W 0.1 {ip} > /dev/null 2>&1"
    codigo = os.system(comando)
    fim = time.time()

    tempo = fim - ini
    sucesso = (codigo == 0)

    with lock:
        res.append((de, para, sucesso, tempo))
