import os
import time
import subprocess
import cv2
from nataly_vision import detectar_personas

print("=====================================================")
print("   SISTEMA NATALY - SIMULADOR DE RESCATE AUTÓNOMO")
print("   (Usando lógica de comandos MAVLink)")
print("=====================================================")

# Variable para saber si ya enviamos la alerta y evitar repetir el comando
alerta_enviada = False

try:
    while True:
        print("\n[DRON] Patrullando... Tomando foto del terreno.")
        
        # 1. Tomar foto
        subprocess.run(["termux-camera-photo", "-c", "0", "vuelo.jpg"], 
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # 2. Analizar con NATALY
        resultado = detectar_personas("vuelo.jpg")
        
        # 3. Tomar decisiones
        if isinstance(resultado, str):
            print("[ERROR]", resultado)
            
        elif len(resultado) > 0:
            if not alerta_enviada:
                print(f"\n🚨 ¡OBJETIVO DETECTADO! ({len(resultado)} personas).")
                print("📡 ENVIANDO COMANDOS MAVLINK AL CONTROLADOR DE VUELO...")
                print("   > Comando 1: [HOLD] Mantener posición actual.")
                print("   > Comando 2: [SET_ALTITUDE] Descender a 15 metros para inspección.")
                print("   > Comando 3: [ALERT] Enviar coordenadas GPS a la estación terrestre.")
                alerta_enviada = True # Evita que el dron entre en bucle de descenso
                
            # Dibujar evidencia
            imagen = cv2.imread("vuelo.jpg")
            for p in resultado:
                x, y, w, h = p['caja']
                cv2.rectangle(imagen, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.putText(imagen, "Persona", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            cv2.imwrite("evidencia_rescate.jpg", imagen)
            print("📸 Evidencia fotográfica guardada.")
            print("[DRON] Manteniendo posición sobre el objetivo...")
            
        else:
            print("✅ Zona despejada. Continuando ruta de búsqueda...")
            # Si la zona está despejada, el dron vuelve a su estado normal
            alerta_enviada = False 
            
        print("[DRON] Esperando 3 segundos...")
        time.sleep(3)
        
except KeyboardInterrupt:
    print("\n[DRON] Aterrizando. Misión finalizada.")
