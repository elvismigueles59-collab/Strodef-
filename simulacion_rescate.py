import os
import time
import subprocess
import cv2
from datetime import datetime
from nataly_vision import detectar_personas, cargar_configuracion
from control_mavlink import ControlDron

config = cargar_configuracion()
tiempo_espera = config.get("tiempo_espera_segundos", 3)
camara = config.get("camara_id", 0)

# Inicializamos el control del dron
dron = ControlDron()

print("=====================================================")
print("   SISTEMA NATALY - v2.0 (TÉRMICO + MAVLINK)")
print("=====================================================")

alerta_enviada = False

try:
    while True:
        print(f"\n[DRON] Patrullando... Tomando foto.")
        
        subprocess.run(["termux-camera-photo", "-c", str(camara), "vuelo.jpg"], 
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # EFECTO TÉRMICO SIMULADO
        imagen_raw = cv2.imread("vuelo.jpg")
        if imagen_raw is not None:
            gris = cv2.cvtColor(imagen_raw, cv2.COLOR_BGR2GRAY)
            imagen_termica = cv2.applyColorMap(gris, cv2.COLORMAP_INFERNO)
            cv2.imwrite("vuelo_termico.jpg", imagen_termica)
        
        # Analizamos la imagen térmica
        resultado = detectar_personas("vuelo_termico.jpg")
        
        if isinstance(resultado, str):
            print("[ERROR]", resultado)
            
        elif len(resultado) > 0:
            if not alerta_enviada:
                hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"\n🚨 ¡OBJETIVO TÉRMICO DETECTADO! ({len(resultado)} personas).")
                
                # --- AQUI USAMOS MAVLINK ---
                dron.enviar_comando_hold()
                dron.enviar_comando_descenso(altitud=15)
                # ---------------------------
                
                with open("registro_vuelo.txt", "a") as log:
                    log.write(f"[{hora_actual}] ALERTA TÉRMICA: {len(resultado)} persona(s) detectada(s).\n")
                
                alerta_enviada = True
                
            # Dibujamos sobre la imagen térmica
            for p in resultado:
                x, y, w, h = p['caja']
                cv2.rectangle(imagen_termica, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.putText(imagen_termica, "Humano", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            cv2.imwrite("evidencia_rescate.jpg", imagen_termica)
            print("📸 Evidencia térmica guardada.")
            
        else:
            print("✅ Zona despejada. Continuando ruta...")
            alerta_enviada = False 
            
        print(f"[DRON] Esperando {tiempo_espera} segundos...")
        time.sleep(tiempo_espera)
        
except KeyboardInterrupt:
    print("\n[DRON] Aterrizando. Misión finalizada.")
