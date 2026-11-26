import cv2
import subprocess
import time
from nataly_vision import detectar_personas

print("=====================================================")
print("   TEST CONTINUO DE ALCANCE DE YOLO")
print("   (Empieza cerca y camina hacia atrás lentamente)")
print("=====================================================")

contador = 1

try:
    while True:
        print(f"\n--- Foto #{contador} ---")
        
        # 1. Tomar la foto
        subprocess.run(["termux-camera-photo", "-c", "0", "test_distancia.jpg"], 
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 2. Leer la foto
        imagen = cv2.imread("test_distancia.jpg")
        if imagen is None:
            print("Error al leer la imagen.")
            continue

        alto_img, ancho_img = imagen.shape[:2]
        
        # 3. Pasar la foto por YOLO
        resultados = detectar_personas("test_distancia.jpg")

        # 4. Mostrar los resultados del experimento
        if isinstance(resultados, str):
            print("[ERROR]", resultados)
        elif len(resultados) > 0:
            print(f"✅ DETECTADO ({len(resultados)} persona/s):")
            for i, p in enumerate(resultados):
                x, y, w, h = p['caja']
                area = w * h
                porcentaje = (area / (ancho_img * alto_img)) * 100
                print(f"   -> Tamaño: {w}x{h} px | Área: {area} px | Confianza: {p['confianza']*100:.1f}%")
                print(f"   -> Ocupa el {porcentaje:.2f}% de la pantalla.")
        else:
            print("❌ NO DETECTADO: YOLO ha perdido el objetivo a esta distancia.")

        contador += 1
        print("Esperando 2 segundos para la siguiente foto...")
        time.sleep(2)

except KeyboardInterrupt:
    print("\n[TEST] Prueba finalizada por el usuario.")
