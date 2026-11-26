import cv2
import numpy as np
import subprocess
import time
import os
from datetime import datetime

# Parámetros de recolección
UMBRAL_MIN = 0.25  # Si baja de 25%, es basura
UMBRAL_MAX = 0.45  # Si sube de 45%, la IA ya está segura, no nos sirve
CARPETA = "dataset_dificil"

if not os.path.exists(CARPETA):
    os.makedirs(CARPETA)

print("=====================================================")
print("   RECOLECTOR DE DATOS (HARD EXAMPLES)")
print(f"   Guardando fotos con confianza entre {UMBRAL_MIN*100}% y {UMBRAL_MAX*100}%")
print("   Pulsa CTRL+C para detener.")
print("=====================================================")

# Cargamos el modelo directamente
net = cv2.dnn.readNetFromTFLite("yolov8n.tflite")

contador = 1
fotos_guardadas = 0

try:
    while True:
        print(f"\n[Foto #{contador}] Escaneando...")
        
        subprocess.run(["termux-camera-photo", "-c", "0", "temp_recolector.jpg"], 
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        image = cv2.imread("temp_recolector.jpg")
        if image is None:
            time.sleep(2)
            continue
            
        height, width = image.shape[:2]
        blob = cv2.dnn.blobFromImage(image, 1/255.0, (640, 640), swapRB=True, crop=False)
        net.setInput(blob)
        outputs = net.forward()
        
        output = outputs[0]
        guardar_esta_foto = False
        mejor_confianza = 0.0
        
        for detection in output.T:
            scores = detection[4:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            
            # Solo nos interesan las personas (class_id 0) que estén en el rango de duda
            if class_id == 0 and UMBRAL_MIN < confidence < UMBRAL_MAX:
                guardar_esta_foto = True
                if confidence > mejor_confianza:
                    mejor_confianza = confidence
        
        if guardar_esta_foto:
            # Generamos un nombre único con la fecha y hora
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"{CARPETA}/duda_{timestamp}_{mejor_confianza:.2f}.jpg"
            
            # Guardamos la foto original (sin dibujos)
            cv2.imwrite(nombre_archivo, image)
            fotos_guardadas += 1
            print(f" 💾 ¡GUARDADA! La IA dudó (Confianza: {mejor_confianza*100:.1f}%) -> {nombre_archivo}")
        else:
            print("   Zona clara o basura. Descartada.")
            
        contador += 1
        time.sleep(2) # Toma una foto cada 2 segundos

except KeyboardInterrupt:
    print("\n=====================================================")
    print(f" RECOLECCIÓN FINALIZADA. Se guardaron {fotos_guardadas} fotos en '{CARPETA}/'.")
    print("=====================================================")
