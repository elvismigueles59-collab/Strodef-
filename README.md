# NATALY Vision SDK
**Software de detección de personas para drones de búsqueda y rescate.**

## Descripción
NATALY es un módulo de visión artificial optimizado para dispositivos de bajo costo (como Raspberry Pi o teléfonos Android). Utiliza un modelo YOLOv8 en formato TFLite para detectar personas sin necesidad de conexión a internet.

## Instalación
1. Instalar dependencias: `pkg install python opencv python-numpy`
2. Descargar el modelo: `yolov8n.tflite` (incluido en este paquete)
3. El código principal se encuentra en `nataly_vision.py`

## Uso Básico
Para integrar NATALY en tu dron, importa la función principal:

```python
from nataly_vision import detectar_personas

# Analiza una imagen y devuelve las coordenadas de las personas
resultados = detectar_personas("ruta/a/tu/foto.jpg")
print(resultados)
