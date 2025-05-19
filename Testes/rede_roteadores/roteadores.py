import os

def listar_roteadores() -> list:
    """
    Retorna uma lista dos containers Docker que contêm 'router' no nome.
    """
    saida = os.popen("docker ps --filter 'name=router' --format '{{.Names}}'").read()
    roteadores = sorted(saida.strip().splitlines())
    return roteadores

def obter_tabela_roteamento(container: str) -> str:
    """
    Retorna a tabela de roteamento de um container Docker específico.

    Args:
        container (str): Nome do container.

    Returns:
        str: Saída do comando 'ip route'.
    """
    comando = f"docker exec {container} ip route"
    return os.popen(comando).read().strip()
