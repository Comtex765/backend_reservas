import subprocess

# Comando combinado usando && para ejecutar secuencialmente
command = "cls && black . && uvicorn api.main:app --reload"

# Ejecutar el comando
subprocess.run(command, shell=True)

