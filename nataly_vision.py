import cv2
import numpy as np

def detectar_personas(ruta_imagen, umbral_confianza=0.5):
    net = cv2.dnn.readNetFromTFLite("yolov8n.tflite")
    
    image = cv2.imread(ruta_imagen)
    if image is None:
        return "Error: No se pudo leer la imagen."
        
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
        
        if confidence > umbral_confianza and class_id == 0:
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)
            
            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            
    indices = cv2.dnn.NMSBoxes(boxes, confidences, umbral_confianza, 0.4)
    
    personas_encontradas = []
    if len(indices) > 0:
        for i in indices.flatten():
            personas_encontradas.append({
                "caja": boxes[i],
                "confianza": confidences[i]
            })
            
    return personas_encontradas
