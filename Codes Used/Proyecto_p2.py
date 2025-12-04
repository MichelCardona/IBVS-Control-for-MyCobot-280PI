# %% Importar librerias e iniciar matlab.engine
import traceback
import matlab.engine
import numpy as np
import cv2
import time
from Cinematica import cinematica
# from Jacobiano import Jacobiano
from pymycobot import MyCobot280Socket

# --- Inicia el motor de MATLAB ---
eng = matlab.engine.start_matlab()
print("matlab.engine loaded succesfully \n")

#%% --- Iniciar programa ---
# --- Conectar con el robot ---
mc = MyCobot280Socket("192.168.68.119", 9000) # IP del robot
mc.connect_socket()

if mc.is_power_on()  == 1:
    print("MyCobot280 Pi is on")
elif mc.is_power_on() == 0:
    raise RuntimeError("MyCobot280 Pi is off")
elif mc.is_power_on() == -1:
    raise RuntimeError("MyCobot280 Pi is stopped")
    
mc.go_home()
time.sleep(2)
mc.send_angles([0, 50, -70, 20, 0, 0], 30)
time.sleep(2)

mc.set_gripper_value(10, 30)

mc.set_fresh_mode(1)
mc.set_vision_mode(1)
mc.set_tool_reference([-45,0,0,0,0,0])

# mc.send_coords([48.7, -62.3, 400, -91.4, 0.89, -88.7], 35)

# mc.send_angles([0, 0, 0, 0, 0, 0], 35)
# mc.set_vision_mode(0)

# --- Para mover el robot cuando no responda ---
# mc.release_all_servos()
# --- Para volver a encender los motores ---
# mc.focus_all_servos()
# mc.clear_error_information()
#%% 
# --- Iniciar Cámara --- 
cap = cv2.VideoCapture(1) 
if not cap.isOpened():
    raise RuntimeError("Camera could not opened")
else:
    print("Camara loaded succesfully")

# --- Obtener parámetros extrinsecos ---
K = eng.get_params()


# --- Inicialización de gráficos ---
N = 1000
t_plot = np.zeros(N)
coords_plot = np.zeros((6,N))
error_plot = np.zeros((6,N))

# --- Tiempo de simulación ---
S = 30
start_time = time.time()
t0 = time.time()
f = 1

# --- Velocidad deseada 0 - 100 ---
speed = 20
# min_coord = np.array([100, -150, 0])
# max_coord = np.array([400, 150, 400])

# --- Distancia deseada cámara-tag ---
d = 0.2 # metros

# --- Tamaño del tag ---
tagSize = 0.057 # metros

# --- Simulación ---
i = 0
try:
    while time.time() - t0 <= S:
        t = time.time() - t0
        
        ok, I = cap.read()
        
        if not ok:
            f = 0
            break
       
        if cv2.waitKey(1) == 27: # escape para cerrar la cámara
            f = 0
            break
        
        # --- Mostrar cámara ---
        cv2.imshow("Cam", I)
          
        # --- Seguimiento de tag mediante coordenadas ---
        
        q = mc.get_angles()
        if not type(q)==list:
            print("Error al leer ángulos, reintentando...")
            continue
        Kine = cinematica(q)
        
        # if id_ == 0:
        new_coords, flag = eng.readTag(I, K, Kine, tagSize,  matlab.double(d), nargout=2)
    
        NC = np.array(new_coords).flatten().reshape(6, 1)
        
        # time.sleep(0.025)
            
        # --- Enviar coordendas ---
        if flag == 1:
            mc.send_coords(NC.flatten().tolist(), speed)
            # mc.sync_send_coords(NC.flatten().tolist(), speed)
        else:
            NC = 0
            
        cc = mc.get_coords()
        if not type(cc)==list:
            print("Error al leer ángulos, reintentando...")
            continue
        CC = np.array(cc)
        
        # --- Calcular error ---
        Error = CC.flatten().reshape(6, 1) - NC
        
        # --- Para gráficar ---
        if i<=N:
            t_plot[i] = t
            coords_plot[:,i] = CC.flatten()
            error_plot[:,i] = Error.flatten()
            
        print("x:", f"{CC[0]:.2f}",
              "y:", f"{CC[1]:.2f}",
              "z:", f"{CC[2]:.2f}",
              "R:", f"{CC[3]:.2f}",
              "P:", f"{CC[4]:.2f}",
              "Y:", f"{CC[5]:.2f}\n")
        
        # print(Error)
        
        print("t:", f"{t:.2f}\n")
        
        i += 1
        
        time.sleep(0.015)
except: 
    # traceback.print_exc()
    tb_str = traceback.format_exc()
    print("-" * 75)
    print(tb_str)
    print("-" * 75)
    print("\nException occurred program was finished")
    #f = 0
finally:
    cap.release()  
    cv2.destroyWindow("Cam")
    mc.stop()
    mc.set_fresh_mode(0)
    mc.set_vision_mode(0)
    mc.close()
    if f==1:
        # ---------- Graficar en MATLAB ----------
        t_plot_ml = matlab.double(t_plot.tolist())
        v_plot_ml = matlab.double(coords_plot.tolist())
        vp_plot_ml = matlab.double(error_plot.tolist())

        # --- Pasar al workspace de MATLAB ---
        eng.workspace['t_plot'] = t_plot_ml
        eng.workspace['v_plot'] = v_plot_ml
        eng.workspace['vp_plot'] = vp_plot_ml
        eng.workspace['i'] = i
        
        # --- Gráficas ---
        eng.eval("""
        f5 = figure;
        subplot(2,1,1);
        hold on
        grid on
        plot(t_plot(1:i), v_plot(1:3,1:i), "LineStyle","-","LineWidth",1)
        legend('x','y','z')
        title('Coordenadas del MyCobot280')
        ylabel('millimeters')
        
        subplot(2,1,2);
        hold on
        grid on
        plot(t_plot(1:i), v_plot(4:6,1:i), "LineStyle","-","LineWidth",1)
        legend('rx','ry','rz')
        xlabel('tiempo')
        ylabel('degrees')
        
        f7 = figure;
        subplot(2,1,1);
        hold on
        grid on
        plot(t_plot(1:i), vp_plot(1:3,1:i), "LineStyle","-","LineWidth",1)
        legend('Ex','Ey','Ez')
        title('Error coordenadas robot-tag')
        
        subplot(2,1,2);
        hold on
        grid on
        plot(t_plot(1:i), vp_plot(4:6,1:i), "LineStyle","-","LineWidth",1)
        legend('Erx','Ery','Erz')
        xlabel('tiempo')
        """, nargout=0)
    
# --- Ejecutar en la terminal para cerrar Matlab ---


# time.waitKey('q')
# eng.quit()