import os
import time
import subprocess
import cv2
from datetime import datetime
from nataly_vision import detectar_personas, cargar_configuracion

config = cargar_configuracion()
tiempo_espera = config.get("tiempo_espera_segundos", 3)
camara = config.get("camara_id", 0)

print("=====================================================")
print("   SISTEMA NATALY - SIMULADOR DE RESCATE AUTÓNOMO")
print(f"   (Configuración cargada: espera de {tiempo_espera}s)")
print("=====================================================")

alerta_enviada = False

try:
    while True:
        print(f"\n[DRON] Patrullando... Tomando foto del terreno.")
        
        subprocess.run(["termux-camera-photo", "-c", str(camara), "vuelo.jpg"], 
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        resultado = detectar_personas("vuelo.jpg")
        
        if isinstance(resultado, str):
            print("[ERROR]", resultado)
            
        elif len(resultado) > 0:
            if not alerta_enviada:
                hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"\n🚨 ¡OBJETIVO DETECTADO! ({len(resultado)} personas).")
                print("📡 ENVIANDO COMANDOS MAVLINK AL CONTROLADOR DE VUELO...")
                print("   > Comando 1: [HOLD] Mantener posición actual.")
                print("   > Comando 2: [SET_ALTITUDE] Descender a 15 metros.")
                print("   > Comando 3: [ALERT] Enviar coordenadas GPS.")
                
                # --- GUARDAR EN EL REGISTRO DE VUELO ---
                with open("registro_vuelo.txt", "a") as log:
                    log.write(f"[{hora_actual}] ALERTA: {len(resultado)} persona(s) detectada(s).\n")
                # --------------------------------------
                
                alerta_enviada = True
                
            imagen = cv2.imread("vuelo.jpg")
            for p in resultado:
                x, y, w, h = p['caja']
                cv2.rectangle(imagen, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.putText(imagen, "Persona", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            cv2.imwrite("evidencia_rescate.jpg", imagen)
            print("📸 Evidencia fotográfica guardada.")
            
        else:
            print("✅ Zona despejada. Continuando ruta de búsqueda...")
            alerta_enviada = False 
            
        print(f"[DRON] Esperando {tiempo_espera} segundos...")
        time.sleep(tiempo_espera)
        
except KeyboardInterrupt:
    print("\n[DRON] Aterrizando. Misión finalizada.")
