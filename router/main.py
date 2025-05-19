import threading
from roteador import Roteador

if __name__ == "__main__":
    rtr = Roteador()
    
    t1 = threading.Thread(target=rtr.enviar_pacotes)
    t2 = threading.Thread(target=rtr.receber_pacotes)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
