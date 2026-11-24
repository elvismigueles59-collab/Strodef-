import cv2
import time
from nataly_vision import detectar_personas

print("=========================================")
print("   NATALY - ANALISIS DE VIDEO (DRON)     ")
print("=========================================")

# 1. Abrir el video de entrada
video_entrada = "people-detection.mp4"
cap = cv2.VideoCapture(video_entrada)

if not cap.isOpened():
    print("Error: No se pudo abrir el video.")
    exit()

# Obtener propiedades del video original
ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps_original = cap.get(cv2.CAP_PROP_FPS)

# 2. Preparar el video de salida (donde guardaremos el resultado)
# Usamos el codec 'mp4v' que es compatible con Termux/Android
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_salida = cv2.VideoWriter("resultado_dron.mp4", fourcc, 10.0, (ancho, alto))

print(f"Video cargado: {ancho}x{alto} a {fps_original} FPS.")
print("Procesando video... (esto puede tardar un poco)")

contador_cuadros = 0
personas_totales = 0

while True:
    # Leer un cuadro del video
    ret, frame = cap.read()
    
    # Si ret es False, significa que el video terminó
    if not ret:
        break
        
    contador_cuadros += 1
    
    # --- OPTIMIZACIÓN ---
    # Para no colapsar el teléfono, solo analizamos 1 de cada 5 cuadros
    if contador_cuadros % 5 == 0:
        # Guardamos el cuadro temporalmente para pasarlo a nuestra función
        cv2.imwrite("temp_frame.jpg", frame)
        
        # Analizamos con nuestro SDK
        resultado = detectar_personas("temp_frame.jpg")
        
        if isinstance(resultado, list) and len(resultado) > 0:
            personas_totales += len(resultado)
            # Dibujar los cuadros verdes en el frame original
            for p in resultado:
                x, y, w, h = p['caja']
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.putText(frame, "Persona", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            print(f" -> Cuadro {contador_cuadros}: ¡{len(resultado)} persona(s) detectada(s)!")

    # Guardar el frame (con o sin dibujos) en el video de salida
    video_salida.write(frame)

# Liberar recursos
cap.release()
video_salida.release()

print("\n=========================================")
print(f"¡Análisis terminado!")
print(f"Cuadros totales procesados: {contador_cuadros}")
print(f"Video guardado como: 'resultado_dron.mp4'")
print("=========================================")
