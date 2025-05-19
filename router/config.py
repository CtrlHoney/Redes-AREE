import subprocess
import os
import json
from typing import Dict, Tuple, Any
from dijkstra import dijkstra
from log import Log

RTR_IP = os.getenv("ip")
NGH = json.loads(os.getenv("vizinhos"))

class Configuracoes:
    @staticmethod
    def obter_rotas(rotas: Dict[str, str]) -> Tuple[Dict[str, str], Dict[str, str]]:
        rotas_existentes = {}
        rotas_sistema = {}
        adicionar = {}
        substituir = {}

        try:
            novas_rotas = {}
            for destino, proximo_salto in rotas.items():
                parts = destino.split('.')
                network = f"{'.'.join(parts[:3])}.0/24"
                novas_rotas[network] = proximo_salto

            resultado = subprocess.run(["ip", "route", "show"], capture_output=True, text=True, check=True)

            for linha in resultado.stdout.splitlines():
                partes = linha.split()
                if partes[0] != "default" and partes[1] == "via":
                    rotas_existentes[partes[0]] = partes[2]
                elif partes[1] == 'dev':
                    rotas_sistema[partes[0]] = partes[-1]

            for rede, proximo_salto in novas_rotas.items():
                if rede in rotas_existentes and rotas_existentes[rede] != proximo_salto:
                    substituir[rede] = proximo_salto
                elif rede not in rotas_existentes and rede not in rotas_sistema:
                    adicionar[rede] = proximo_salto

            return adicionar, substituir

        except Exception as e:
            Log.log(f"[ERRO] {RTR_IP} falhou ao obter rotas existentes: {e}")

            return {}, {}

    @staticmethod
    def add_rotas(salto: str, destino: str) -> bool:
        try:
            destino = f"{'.'.join(destino.split('.')[:3])}.0/24"
            comando = f"ip route add {destino} via {salto}"
            subprocess.run(comando.split(), capture_output=True)
            Log.log(f"Rota adicionada por {RTR_IP}: destino={destino}, via={salto}")

            return True
        except Exception as error:
            Log.log(f"Erro ao adicionar rota: {error}")
            return False

    @staticmethod
    def subst_rotas(salto: str, destino: str) -> bool:
        try:
            destino = f"{'.'.join(destino.split('.')[:3])}.0/24"
            comando = f"ip route replace {destino} via {salto}"
            processo = subprocess.run(comando.split(), check=True)
            if processo.returncode == 0:
                Log.log(f"Rota substituída por {RTR_IP}: destino={destino}, via={salto}")

                return True
            else:
                Log.log(f"Problema ao substituir rota.")
        except Exception as error:
            Log.log(f"Erro ao substituir rota: {error}")
        return False

    @staticmethod
    def configurar_inter(lsdb: Dict[str, Any]) -> None:
        rotas = dijkstra(RTR_IP, lsdb)
        caminhos = {}
        for destino, salto in rotas.items():
            for v, ip_custo in NGH.items():
                ip, _ = ip_custo
                if salto == ip:
                    caminhos[destino] = salto
                    break
        add, substituir = Configuracoes.obter_rotas(caminhos)
        for destino, salto in add.items():
            Configuracoes.add_rotas(salto, destino)
        for destino, salto in substituir.items():
            Configuracoes.subst_rotas(salto, destino)
