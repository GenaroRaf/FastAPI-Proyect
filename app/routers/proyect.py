from fastapi import APIRouter
from app.schemas import Proyect
import paramiko

router = APIRouter(
    prefix="/proyect",
    tags = ["Proyects"]
)

proyectos = []
status = ""

@router.post('/')
def crear_proyecto(proyect: Proyect):
    proyecto = proyect.dict()
    proyectos.append(proyecto)
    print(proyecto)

    return {"Proyecto creado satisfactoriamente!"}

@router.get('/')
def obtener_proyecto():
    proyecto = proyectos[0]["detail"]
    print("holaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    print(proyecto)
    for key, value in proyecto.items():
        if key == "state":
            status = value
            hola(status)
            configurar_entorno_remoto(status)
    return proyectos

def hola(status:str):
    print("-------------------------------")
    print(status)

def configurar_entorno_remoto(status: str):
    hostname = "192.168.2.27"  
    username = "cliente1"
    password = "1234"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)

    script_content = f"""import os
os.system('echo \"{status}\" > salida.txt')
"""
    script_filename = "Entrada.py" 
    sftp = ssh.open_sftp()

    with open(script_filename, "w") as file:
        file.write(script_content)

    sftp = ssh.open_sftp()
    sftp.put(script_filename, script_filename)
    sftp.close()

    ssh.exec_command(f"chmod +x {script_filename}")
    stdin, stdout, stderr = ssh.exec_command(f"python3 {script_filename}")
    print("Tipo de archivo:", stdout.read().decode())
    print("Permisos del archivo:", stdout.read().decode())
    
    output = stdout.read().decode()
    errors = stderr.read().decode()
    
    print("Salida del script:", output)
    if errors:
        print("Errores:", errors)

    ssh.close()
