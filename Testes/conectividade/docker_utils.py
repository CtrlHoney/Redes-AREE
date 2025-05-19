import os

def pegar_roteadores() -> list:
    """
    Retorna uma lista com os nomes dos containers que contêm 'router' no nome.
    """
    saida = os.popen("docker ps --filter 'name=router' --format '{{.Names}}'").read()
    return sorted(saida.splitlines())

def extrair_roteador_sufixo(nome: str) -> str:
    """
    Extrai o sufixo numérico de um nome de container no formato esperado.
    Exemplo: 'router-1' ou 'lab-router-3_1' -> retorna '3'

    Returns:
        str: sufixo numérico como string
    """
    try:
        prefixo = nome.split('-')[-2]
        return prefixo.split('router')[1]
    except IndexError:
        return "0"
