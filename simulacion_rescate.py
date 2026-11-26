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

dron = ControlDron()

print("=====================================================")
print("   SISTEMA NATALY - v2.0 (LÓGICA DE ALTITUD)")
print("=====================================================")

alerta_enviada = False

try:
    while True:
        print(f"\n[DRON] Patrullando... Tomando foto.")
        
        subprocess.run(["termux-camera-photo", "-c", str(camara), "vuelo.jpg"], 
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        imagen_raw = cv2.imread("vuelo.jpg")
        if imagen_raw is None:
            continue
            
        # Efecto térmico
        gris = cv2.cvtColor(imagen_raw, cv2.COLOR_BGR2GRAY)
        imagen_termica = cv2.applyColorMap(gris, cv2.COLORMAP_INFERNO)
        cv2.imwrite("vuelo_termico.jpg", imagen_termica)
        
        # Analizar
        resultado = detectar_personas("vuelo_termico.jpg", modo_larga_distancia=True)
        
        if isinstance(resultado, str):
            print("[ERROR]", resultado)
            
        elif len(resultado) > 0:
            # Calcular el tamaño de la imagen para sacar porcentajes
            alto_img, ancho_img = imagen_termica.shape[:2]
            area_total_img = alto_img * ancho_img
            
            for p in resultado:
                x, y, w, h = p['caja']
                area_persona = w * h
                porcentaje_area = (area_persona / area_total_img) * 100
                
                # Dibujar en pantalla
                cv2.rectangle(imagen_termica, (x, y), (x + w, y + h), (0, 255, 0), 3)
                texto = f"Humano ({porcentaje_area:.1f}%)"
                cv2.putText(imagen_termica, texto, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                print(f"\n🚨 ¡OBJETIVO TÉRMICO DETECTADO! Ocupa el {porcentaje_area:.1f}% de la pantalla.")
                
                # LÓGICA DE ALTITUD
                if porcentaje_area < 2.0:
                    print("   [IA] El objetivo es muy pequeño. El dron está muy alto.")
                    if not alerta_enviada:
                        dron.enviar_comando_descenso(altitud=15) # Bajar
                        alerta_enviada = True
                elif porcentaje_area > 15.0:
                    print("   [IA] El objetivo está muy cerca. El dron debe detenerse.")
                    if not alerta_enviada:
                        dron.enviar_comando_hold() # Mantenerse
                        alerta_enviada = True
                else:
                    print("   [IA] Distancia óptima de rescate. Manteniendo posición.")
                    if not alerta_enviada:
                        dron.enviar_comando_hold()
                        alerta_enviada = True
            
            cv2.imwrite("evidencia_rescate.jpg", imagen_termica)
            
            # Guardar en log
            hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("registro_vuelo.txt", "a") as log:
                log.write(f"[{hora_actual}] ALERTA: {len(resultado)} persona(s). Área: {porcentaje_area:.1f}%\n")
                
        else:
            print("✅ Zona despejada. Continuando ruta...")
            alerta_enviada = False 
            
        print(f"[DRON] Esperando {tiempo_espera} segundos...")
        time.sleep(tiempo_espera)
        
except KeyboardInterrupt:
    print("\n[DRON] Aterrizando. Misión finalizada.")
