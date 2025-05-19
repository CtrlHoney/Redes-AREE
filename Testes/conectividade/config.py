import os

# Número máximo de threads paralelas
CONT_CPU = os.cpu_count()
MAX_THREADS = CONT_CPU * 4 if CONT_CPU else 8
