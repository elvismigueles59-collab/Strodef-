import cv2
import numpy as np
import json
import os

def cargar_configuracion():
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            return json.load(f)
    return {"umbral_confianza": 0.40, "camara_id": 0, "tiempo_espera_segundos": 3}

def procesar_imagen_yolo(net, image, umbral):
    height, width = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 1/255.0, (640, 640), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward()
    output = outputs[0]
    
    boxes = []
    confidences = []
    
    for detection in output.T:
        scores = detection[4:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        
        if confidence > umbral and class_id == 0:
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)
            
            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            
    indices = cv2.dnn.NMSBoxes(boxes, confidences, umbral, 0.4)
    resultados = []
    if len(indices) > 0:
        for i in indices.flatten():
            resultados.append({"caja": boxes[i], "confianza": confidences[i]})
    return resultados

def detectar_personas(ruta_imagen, umbral_confianza=None, modo_larga_distancia=True):
    config = cargar_configuracion()
    if umbral_confianza is None:
        umbral_confianza = config.get("umbral_confianza", 0.40)

    net = cv2.dnn.readNetFromTFLite("yolov8n.tflite")
    image = cv2.imread(ruta_imagen)
    
    if image is None:
        return "Error: No se pudo leer la imagen."

    # --- INICIO DEL ASISTENTE DE VISIÓN ---
    if modo_larga_distancia:
        # 1. Realce de bordes para mejorar la silueta a lo lejos
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        image_enhanced = cv2.filter2D(image, -1, kernel)
        
        height, width = image.shape[:2]
        personas_encontradas = []
        
        # 2. Rebanado (Slicing) 2x2 con superposición (overlap)
        # Esto hace que la IA se enfoque en las 4 esquinas y el centro
        slices = [
            (0, 0, int(width*0.6), int(height*0.6)),                   # Arriba-Izq
            (int(width*0.4), 0, width, int(height*0.6)),               # Arriba-Der
            (0, int(height*0.4), int(width*0.6), height),              # Abajo-Izq
            (int(width*0.4), int(height*0.4), width, height)           # Abajo-Der
        ]
        
        for (x1, y1, x2, y2) in slices:
            recorte = image_enhanced[y1:y2, x1:x2]
            res = procesar_imagen_yolo(net, recorte, umbral_confianza)
            
            # Ajustar coordenadas a la imagen original
            for p in res:
                p['caja'][0] += x1
                p['caja'][1] += y1
                personas_encontradas.append(p)
                
        # 3. Eliminar detecciones duplicadas (si una persona cae en dos rebanadas)
        if len(personas_encontradas) > 0:
            cajas = [p['caja'] for p in personas_encontradas]
            confs = [p['confianza'] for p in personas_encontradas]
            indices = cv2.dnn.NMSBoxes(cajas, confs, umbral_confianza, 0.4)
            
            finales = []
            if len(indices) > 0:
                for i in indices.flatten():
                    finales.append(personas_encontradas[i])
            return finales
            
        return []
    else:
        # Modo normal (rápido, para distancias cortas)
        return procesar_imagen_yolo(net, image, umbral_confianza)
