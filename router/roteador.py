import socket
import json
import time
import threading
import os
from typing import Dict, Any
from log import Log
from config import Configuracoes
from lsa import LSA

PORTA_LSA = 5000
RTR_IP = os.getenv("ip")
NGH = json.loads(os.getenv("vizinhos"))  # { "R2": ["192.168.0.2", 1], ... }

class Roteador:
    def __init__(self) -> None:
        self.lsdb = {}
        self.thread = threading.Lock()
        Log.log(f"Roteador {RTR_IP} iniciado.")

    def enviar_pacotes(self) -> None:
        sock = self._criar_socket()
        sequencia = 0

        while True:
            sequencia += 1
            pacote = LSA.criar_pacote(sequencia)
            msg = json.dumps(pacote).encode()

            for _, (ip, _) in NGH.items():
                self._enviar_lsa(sock, ip, msg, pacote["seq"])

            with self.thread:
                self.lsdb[RTR_IP] = pacote
                self.salvar_lsdb(self.lsdb)
                Configuracoes.configurar_inter(self.lsdb)

            time.sleep(10)

    def receber_pacotes(self) -> None:
        sock = self._criar_socket()
        sock.bind(("0.0.0.0", PORTA_LSA))

        while True:
            try:
                dado, end = sock.recvfrom(4096)
                lsa = json.loads(dado.decode())
                origem, seq = lsa["id"], lsa["seq"]
                remetente_ip = end[0]

                Log.log(f"LSA seq={seq} recebido de {origem} ({remetente_ip})")

                if origem not in self.lsdb or seq > self.lsdb[origem]["seq"]:
                    for _, (ip, _) in NGH.items():
                        if ip != remetente_ip:
                            self._retransmitir_lsa(sock, ip, dado, origem, seq)

                    with self.thread:
                        self.lsdb[origem] = lsa
                        self.salvar_lsdb(self.lsdb)
                        Configuracoes.configurar_inter(self.lsdb)

            except Exception as error:
                Log.log(f"Erro ao processar LSA: {error}")

    def salvar_lsdb(self, lsdb: Dict[str, Any]) -> None:
        with open("lsdb.json", "w") as f:
            json.dump(lsdb, f, indent=4)

    def _criar_socket(self) -> socket.socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return sock

    def _enviar_lsa(self, sock: socket.socket, ip: str, msg: bytes, seq: int) -> None:
        sock.sendto(msg, (ip, PORTA_LSA))
        Log.log(f"LSA seq={seq} enviado para {ip}")

    def _retransmitir_lsa(self, sock: socket.socket, ip: str, dado: bytes, origem: str, seq: int) -> None:
        sock.sendto(dado, (ip, PORTA_LSA))
        Log.log(f"LSA seq={seq} de {origem} retransmitido para {ip}")
