import threading
from docker_utils import pegar_roteadores, extrair_roteador_sufixo
from ping_test import realizar_ping
from config import MAX_THREADS

def montar_tarefas(roteadores):
    tarefas = []
    for origem in roteadores:
        for destino in roteadores:
            if origem != destino:
                sufixo = extrair_roteador_sufixo(destino)
                ip_destino = f"172.20.{sufixo}.3"
                tarefas.append((origem, destino, ip_destino))
    return tarefas

def exibir_resultados(resultados):
    sumario = {}
    total_sucesso = 0

    for origem, destino, sucesso, tempo in resultados:
        sumario.setdefault(origem, []).append((destino, sucesso, tempo))
        if sucesso:
            total_sucesso += 1

    for origem in sorted(sumario):
        print(f"\n[ Roteador: {origem} ]")
        for destino, sucesso, tempo in sumario[origem]:
            status = "SUCESSO ✅" if sucesso else "FALHA ❌"
            print(f"  → Para {destino}: {status} (tempo: {tempo:.2f}s)")

    print("\nResumo final:")
    print(f"Conexões bem-sucedidas: {total_sucesso}/{len(resultados)}")

def main():
    roteadores = pegar_roteadores()
    if not roteadores:
        print("Erro: Nenhum roteador foi encontrado. Execute 'docker compose up --build' antes de iniciar os testes.")
        return

    print("Iniciando testes de conectividade entre roteadores...")

    tarefas = montar_tarefas(roteadores)
    resultados = []
    threads = []
    lock = threading.Lock()

    for origem, destino, ip in tarefas:
        while len(threads) >= MAX_THREADS:
            threads = [t for t in threads if t.is_alive()]
        
        t = threading.Thread(target=realizar_ping, args=(origem, destino, ip, resultados, lock))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    exibir_resultados(resultados)

if __name__ == "__main__":
    main()
