#!/bin/bash
# =====================================================
# INSTALADOR AUTOMÁTICO - NATALY VISION SDK
# =====================================================

echo "====================================================="
echo "   🚁 INICIANDO INSTALACIÓN DE NATALY VISION SDK"
echo "====================================================="

# 1. Actualizar repositorios del sistema
echo -e "\n[1/4] Actualizando repositorios del sistema..."
pkg update -y

# 2. Instalar dependencias del sistema operativo (Termux/Linux)
echo -e "\n[2/4] Instalando dependencias del sistema (Python, OpenCV, etc)..."
pkg install python python-pip opencv python-numpy termux-api libxml2 libxslt -y

# 3. Instalar librerías de Python (Flask, etc)
echo -e "\n[3/4] Instalando librerías de Python (requirements.txt)..."
pip install -r requirements.txt

# 4. Instalar MAVLink (Forzando la versión compatible con Android)
echo -e "\n[4/4] Instalando pymavlink (Versión estable para Android)..."
pip install pymavlink==2.4.43

# Dar permisos de ejecución al propio instalador
chmod +x install.sh

echo -e "\n====================================================="
echo "✅ ¡INSTALACIÓN COMPLETADA CON ÉXITO!"
echo "Para iniciar el sistema, ejecuta: python main.py"
echo "====================================================="
