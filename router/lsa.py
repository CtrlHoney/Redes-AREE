import os
import json

# IP do roteador atual (definido via variável de ambiente)
RTR_IP = os.getenv("ip")

# Dicionário de vizinhos 
NGH = json.loads(os.getenv("vizinhos"))

class LSA:
    @staticmethod
    def criar_pacote(seq: int) -> dict:
        # Cria um pacote LSA (Link State Advertisement) com:
        pacote = {
            "id": RTR_IP,
            "seq": seq,
            "vizinhos": {}
        }

        for _, (ip, custo) in NGH.items():
            pacote["vizinhos"][ip] = custo

        return pacote
