import threading
import os
from core.docker_utils import pegar_hosts, extrair_hosts
from core.utils import ping

MAX_THREADS = os.cpu_count() * 4

def main():
    print("🔍 Buscando containers com nome 'host'...\n")

    hosts = pegar_hosts()
    if not hosts:
        print("[ERRO] Nenhum container 'host' encontrado. Execute `docker compose up --build` primeiro.")
        return

    print(f"✅ {len(hosts)} containers encontrados:\n {', '.join(hosts)}\n")
    
    tarefas = [
        (de, para, f"172.20.{extrair_hosts(para)[0]}.1{extrair_hosts(para)[1]}")
        for de in hosts for para in hosts if de != para
    ]

    resultados = []
    threads = []
    lock = threading.Lock()

    for de, para, ip in tarefas:
        while len(threads) >= MAX_THREADS:
            threads = [t for t in threads if t.is_alive()]
        t = threading.Thread(target=ping, args=(de, para, ip, resultados, lock))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("📊 Testes concluídos. Exibindo resultados:\n")

    sumario = {}
    for de, para, sucesso, tempo in resultados:
        sumario.setdefault(de, []).append((para, sucesso, tempo))

    total = len(resultados)
    total_ok = sum(1 for _, _, ok, _ in resultados if ok)

    for de in sorted(sumario):
        print(f"🧭 Roteador: {de}")
        for para, ok, tempo in sumario[de]:
            status = "✔ SUCESSO" if ok else "❌ FALHA"
            print(f"  {de} → {para}: {tempo:.4f}s [{status}]")
        print()

    print(f"✅ Conexões bem-sucedidas: {total_ok}/{total}")
    print("🏁 Fim da execução.")

if __name__ == "__main__":
    main()
