from roteadores import listar_roteadores, obter_tabela_roteamento
from utilitarios import exibir_titulo

def main():
    exibir_titulo("Tabela de Roteamento dos Roteadores")

    roteadores = listar_roteadores()
    
    if not roteadores:
        print("Nenhum roteador encontrado. Verifique se o Docker Compose está em execução.")
        return

    for container in roteadores:
        print(f"\nRoteador: {container}")
        print("-" * 60)
        tabela = obter_tabela_roteamento(container)
        print(tabela if tabela else "Nenhuma informação de roteamento disponível.")

if __name__ == "__main__":
    main()
