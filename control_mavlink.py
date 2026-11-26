from pymavlink import mavutil
import time

class ControlDron:
    def __init__(self, conexion="udpout:127.0.0.1:14550"):
        print(f"[MAVLINK] Iniciando conexión con el controlador de vuelo...")
        self.conectado = False
        try:
            # Esta línea es la que crea la conexión real
            self.master = mavutil.mavlink_connection(conexion)
            self.master.wait_heartbeat(timeout=2)
            print("[MAVLINK] ¡Conexión establecida con el dron!")
            self.conectado = True
        except Exception as e:
            print("[MAVLINK] AVISO: No se detectó dron. Entrando en MODO SIMULACIÓN.")
            self.conectado = False

    def enviar_comando_hold(self):
        """Envía el comando real de mantener posición (LOITER/HOLD)"""
        if not self.conectado:
            print("   -> [SIMULADO] MAV_CMD: HOLD (Mantener posición)")
            return
            
        self.master.mav.set_mode_send(
            self.master.target_system,
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            5) # 5 = LOITER
        print("   -> [REAL] Comando MAVLink enviado: Modo LOITER (HOLD)")

    def enviar_comando_descenso(self, altitud=15):
        """Envía el comando real de descender a una altitud"""
        if not self.conectado:
            print(f"   -> [SIMULADO] MAV_CMD: DESCENDER a {altitud} metros")
            return
            
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
            0, 0, 0, 0, 0, 0, 0, altitud)
        print(f"   -> [REAL] Comando MAVLink enviado: Descender a {altitud}m")
