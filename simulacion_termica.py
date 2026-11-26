import cv2
import numpy as np
from nataly_vision import detectar_personas

print("=====================================================")
print("   NATALY - MODO VISIÓN TÉRMICA (SIMULADO)")
print("=====================================================")

# 1. Tomamos una foto con la cámara normal
print("[DRON] Tomando foto en modo térmico...")
import subprocess
subprocess.run(["termux-camera-photo", "-c", "0", "termica_raw.jpg"], 
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# 2. Leemos la foto
imagen = cv2.imread("termica_raw.jpg")
if imagen is None:
    print("Error: No se pudo tomar la foto.")
    exit()

# 3. TRUCO TÉRMICO: Convertimos a escala de grises y aplicamos un mapa de calor
# Las cámaras térmicas reales entregan imágenes en escala de grises, donde lo blanco es calor.
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Aplicamos una paleta de colores térmicos (Inferno: negro -> rojo -> amarillo -> blanco)
imagen_termica = cv2.applyColorMap(gris, cv2.COLORMAP_INFERNO)

# Guardamos la imagen térmica para que la veas
cv2.imwrite("termica_efecto.jpg", imagen_termica)
print("📸 Foto con efecto térmico guardada como 'termica_efecto.jpg'")

# 4. Pasamos la imagen térmica por NATALY para detectar personas
print("[NATALY] Analizando imagen térmica...")
resultados = detectar_personas("termica_efecto.jpg")

if len(resultados) > 0:
    print(f"🚨 ¡ALERTA TÉRMICA! Se detectaron {len(resultados)} fuentes de calor humana.")
    # Dibujamos los cuadros en la imagen térmica
    for p in resultados:
        x, y, w, h = p['caja']
        cv2.rectangle(imagen_termica, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.putText(imagen_termica, "Humano", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    cv2.imwrite("evidencia_termica.jpg", imagen_termica)
    print("📸 Evidencia térmica guardada como 'evidencia_termica.jpg'")
else:
    print("✅ No se detectó calor humano en la zona.")
