from pymavlink import mavutil
import time

print("=====================================================")
print("   CONTROLADOR DE VUELO (PIXHAWK VIRTUAL)")
print("   Escuchando comandos en el puerto 14550...")
print("=====================================================")

# Nos conectamos al puerto donde tu software envía los comandos
master = mavutil.mavlink_connection('udpin:0.0.0.0:14550')

altitud_actual = 50.0 # Empezamos a 50 metros
estado = "PATRULLANDO"

while True:
    try:
        # Escuchar si llega un mensaje del software de visión
        msg = master.recv_match(blocking=False)
        
        if msg:
            tipo = msg.get_type()
            
            # Si el software cambia el modo de vuelo (HOLD)
            if tipo == 'SET_MODE':
                estado = "HOLD (MANTENIENDO POSICIÓN)"
                print(f"[DRON VIRTUAL] Orden recibida: Mantener posición. Altitud: {altitud_actual:.1f}m")
                
            # Si el software envía un comando de misión (DESCENDER)
            elif tipo == 'COMMAND_LONG':
                if msg.command == mavutil.mavlink.MAV_CMD_NAV_WAYPOINT:
                    altitud_objetivo = msg.param7
                    print(f"[DRON VIRTUAL] Orden recibida: Descender a {altitud_objetivo:.1f}m")
                    estado = "DESCENDIENDO"
                    
                    # Simulamos el descenso
                    while altitud_actual > altitud_objetivo:
                        altitud_actual -= 2.5 # Baja 2.5 metros por segundo
                        if altitud_actual < altitud_objetivo:
                            altitud_actual = altitud_objetivo
                        print(f"   -> Descendiendo... Altitud actual: {altitud_actual:.1f}m")
                        time.sleep(1)
                    
                    estado = "EN POSICIÓN (HOLD)"
                    print(f"[DRON VIRTUAL] Descenso completado. Manteniendo {altitud_actual:.1f}m.")

        time.sleep(0.1) # Pequeña pausa para no saturar el procesador

    except KeyboardInterrupt:
        print("\n[DRON VIRTUAL] Apagando sistemas...")
        break
    except Exception as e:
        pass
