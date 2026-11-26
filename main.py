import subprocess
import time
import sys
import os

def iniciar_sistema():
    print("=====================================================")
    print("   🚁 SISTEMA INTEGRADO NATALY VISION - v3.0")
    print("=====================================================")
    
    # 1. Encender el Controlador de Vuelo Virtual
    print("\n[1/3] Iniciando Controlador de Vuelo (Pixhawk Virtual)...")
    dron = subprocess.Popen(["python", "dron_virtual.py"])
    time.sleep(2) # Esperamos un poco para que abra el puerto de comunicación

    # 2. Encender el Servidor Web (Dashboard)
    print("[2/3] Iniciando Dashboard Web (Flask)...")
    # Ocultamos los logs de Flask para que no ensucien la pantalla
    web = subprocess.Popen(["python", "app_web.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)

    # 3. Encender la Visión Artificial
    print("[3/3] Iniciando Visión Artificial y Patrulla...")
    vision = subprocess.Popen(["python", "simulacion_rescate.py"])

    print("\n✅ TODOS LOS SISTEMAS EN LÍNEA.")
    print("👉 Abre tu navegador en: http://localhost:5000")
    print("⚠️  Presiona CTRL+C para apagar el sistema completo.\n")

    # Mantener el programa principal corriendo
    try:
        dron.wait()
        web.wait()
        vision.wait()
    except KeyboardInterrupt:
        print("\n\n[MAIN] Apagando sistema...")
        # Matar los procesos hijos
        dron.terminate()
        web.terminate()
        vision.terminate()
        time.sleep(1)
        # Forzar el cierre si no responden
        dron.kill()
        web.kill()
        vision.kill()
        print("[MAIN] Sistema apagado correctamente.")

if __name__ == "__main__":
    iniciar_sistema()
