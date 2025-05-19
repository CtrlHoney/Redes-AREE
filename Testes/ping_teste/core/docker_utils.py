import os

def pegar_hosts() -> list:
    """
    Retorna a lista de containers Docker com 'host' no nome.
    """
    saida = os.popen("docker ps --filter 'name=host' --format '{{.Names}}'").read()
    return sorted(saida.splitlines())

def extrair_hosts(nome: str) -> tuple:
    """
    Extrai informações de IP do nome do container.
    """
    try:
        prefixo = nome.split('-')[-2]
        parte = prefixo.split('host')[-1]
        bloco = parte[:-1].split('_')[0]
        sufixo = parte[-1]
        return bloco, sufixo
    except IndexError:
        return None, None
