import os
import time
import threading

def realizar_ping(origem: str, destino: str, ip: str, resultados: list, lock: threading.Lock):
    """
    Realiza um ping entre dois containers e registra o tempo e sucesso.

    Args:
        origem (str): container de origem
        destino (str): container de destino
        ip (str): IP do destino
        resultados (list): lista onde os resultados serão armazenados
        lock (threading.Lock): lock de thread para acesso seguro
    """
    inicio = time.time()
    comando = f"docker exec {origem} ping -c 1 -W 0.1 {ip} > /dev/null 2>&1"
    codigo_retorno = os.system(comando)
    fim = time.time()
    sucesso = (codigo_retorno == 0)
    tempo = fim - inicio

    with lock:
        resultados.append((origem, destino, sucesso, tempo))
