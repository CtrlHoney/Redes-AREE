import os

RTR_IP = os.getenv("ip")

class Log:
    @staticmethod
    def log(msg: str) -> None:
        print(f"[ROUTER {RTR_IP}] {msg}", flush=True)
