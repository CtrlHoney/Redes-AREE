from typing import Dict, Any
import heapq

def dijkstra(origem: str, lsdb: Dict[str, Any]) -> Dict[str, str]:
    grafo = {}
    for roteador, dados in lsdb.items():
        grafo[roteador] = dados["vizinhos"]

    dist = {ip: float('inf') for ip in grafo}
    prev = {}
    dist[origem] = 0
    heap = [(0, origem)]

    while heap:
        atual_dist, atual = heapq.heappop(heap)
        for vizinho, custo in grafo.get(atual, {}).items():
            novo_custo = atual_dist + custo
            if novo_custo < dist.get(vizinho, float('inf')):
                dist[vizinho] = novo_custo
                prev[vizinho] = atual
                heapq.heappush(heap, (novo_custo, vizinho))

    caminhos = {}
    for destino in dist:
        if destino == origem or dist[destino] == float('inf'):
            continue
        anterior = destino
        while prev.get(anterior) != origem:
            anterior = prev.get(anterior)
            if anterior is None:
                break
        if anterior:
            caminhos[destino] = anterior

    return caminhos
