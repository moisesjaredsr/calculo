import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(page_title="Banco de Retos: Integrales", layout="wide")

# --- FUNCIÓN GENERADORA DE GRÁFICOS (ESQUEMAS) ---
def generar_esquema(pd):
    if not pd: return None
    fig = go.Figure()
    
    # Generar 200 puntos en el intervalo especificado
    indep = np.linspace(pd["x"][0], pd["x"][1], 200)
    base_type = pd["type"].replace("_y", "")
    is_y = pd["type"].endswith("_y")
    
    y1 = pd["f1"](indep)
    
    # Renderizado dependiendo del tipo de problema matemático
    if base_type == "area":
        if is_y:
            fig.add_trace(go.Scatter(x=y1, y=indep, fill='tozerox', mode='lines', line=dict(color='#0068c9')))
        else:
            fig.add_trace(go.Scatter(x=indep, y=y1, fill='tozeroy', mode='lines', line=dict(color='#0068c9')))
            
    elif base_type == "area_between":
        y2 = pd["f2"](indep)
        if is_y:
            fig.add_trace(go.Scatter(x=y1, y=indep, mode='lines', line=dict(color='#0068c9')))
            fig.add_trace(go.Scatter(x=y2, y=indep, fill='tonextx', mode='lines', line=dict(color='#ff2b2b')))
        else:
            fig.add_trace(go.Scatter(x=indep, y=y1, mode='lines', line=dict(color='#0068c9')))
            fig.add_trace(go.Scatter(x=indep, y=y2, fill='tonexty', mode='lines', line=dict(color='#ff2b2b')))
            
    # Marcar ejes de revolución si el problema es de sólidos
    if "rev_axis" in pd:
        ax = pd["rev_axis"]
        if ax == "y=0":
            fig.add_hline(y=0, line_dash="dash", line_color="green", annotation_text="Eje de rotación (X)")
        elif ax == "x=0":
            fig.add_vline(x=0, line_dash="dash", line_color="green", annotation_text="Eje de rotación (Y)")
        elif ax == "y=4":
            fig.add_hline(y=4, line_dash="dash", line_color="green", annotation_text="Eje rotación y=4")
            
    fig.update_layout(
        title="Esquema Visual (Representación del Planteamiento)",
        xaxis_title=pd.get("labels", ["Eje X", "Eje Y"])[0],
        yaxis_title=pd.get("labels", ["Eje X", "Eje Y"])[1],
        height=350, showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='rgba(240,240,240,0.4)'
    )
    return fig

# --- BASE DE DATOS DE EJERCICIOS (Con 'plot_data' incrustado) ---
ejercicios = {
    "🟢 Fácil": [
        {"tema": "Cinemática (Área)", "pregunta": "Un auto acelera de forma constante y su velocidad está dada por v(t) = 2t (en m/s). Calcula la distancia total recorrida durante los primeros 3 segundos (intervalo [0, 3]).", 
         "latex": r"\text{Distancia} = \int_{0}^{3} 2t \, dt = \left[ t^2 \right]_0^3 = 3^2 - 0^2 = 9", "respuesta": "9 metros",
         "plot": {"f1": lambda x: 2*x, "x": [0, 3], "type": "area", "labels": ["Tiempo t (s)", "Velocidad v (m/s)"]}},
        
        {"tema": "Economía (Costo Marginal)", "pregunta": "El costo marginal de producir un lote de componentes electrónicos aumenta cuadráticamente según C'(x) = x² (en cientos de dólares). ¿Cuál es el costo total acumulado al producir las primeras 2 unidades?", 
         "latex": r"\text{Costo} = \int_{0}^{2} x^2 \, dx = \left[ \frac{x^3}{3} \right]_0^2 = \frac{8}{3} - 0 = 2.66", "respuesta": "8/3 (Aprox. $266 dólares)",
         "plot": {"f1": lambda x: x**2, "x": [0, 2], "type": "area", "labels": ["Unidades x", "Costo Marginal"]}},
        
        {"tema": "Carrera (Área entre curvas)", "pregunta": "Dos corredores inician una carrera. La velocidad del corredor A es v_A(t) = t, y la del B es v_B(t) = t². Calcula la ventaja en distancia (área entre las curvas) que le saca el corredor A al B en el primer minuto (t de 0 a 1).", 
         "latex": r"\Delta d = \int_{0}^{1} (t - t^2) \, dt = \left[ \frac{t^2}{2} - \frac{t^3}{3} \right]_0^1 = \frac{1}{2} - \frac{1}{3} = \frac{1}{6}", "respuesta": "1/6 metros",
         "plot": {"f1": lambda x: x, "f2": lambda x: x**2, "x": [0, 1], "type": "area_between", "labels": ["Tiempo t", "Velocidades"]}},
        
        {"tema": "Ingeniería (Tuberías)", "pregunta": "Se está fabricando una tubería cilíndrica sólida de radio 1 cm y largo 5 cm. Recrea este cilindro girando la función constante f(x) = 1 alrededor del eje X en el intervalo [0, 5] y calcula su volumen.", 
         "latex": r"V = \pi \int_{0}^{5} (1)^2 \, dx = \pi [x]_0^5 = 5\pi", "respuesta": "5π cm³",
         "plot": {"f1": lambda x: x*0 + 1, "x": [0, 5], "type": "area", "rev_axis": "y=0", "labels": ["Longitud x", "Radio"]}},
        
        {"tema": "Acústica (Megáfono)", "pregunta": "Diseñamos un pequeño megáfono cónico cuyo radio de apertura crece según la función r(x) = x. Si la longitud del cono es de 2 cm (de x=0 a x=2), calcula el volumen de aire que cabe en su interior rotándolo sobre el eje X.", 
         "latex": r"V = \pi \int_{0}^{2} (x)^2 \, dx = \pi \left[ \frac{x^3}{3} \right]_0^2 = \frac{8\pi}{3}", "respuesta": "8π/3 cm³",
         "plot": {"f1": lambda x: x, "x": [0, 2], "type": "area", "rev_axis": "y=0", "labels": ["Longitud x", "Radio"]}},
        
        {"tema": "Electricidad (Valor Promedio)", "pregunta": "Un circuito mantiene una corriente eléctrica perfectamente estable de I(t) = 4 Amperios entre las horas t=1 y t=5. Comprueba mediante el Teorema del Valor Medio cuál fue la corriente promedio en ese lapso.", 
         "latex": r"I_{prom} = \frac{1}{5-1} \int_{1}^{5} 4 \, dt = \frac{1}{4} [4t]_1^5 = \frac{1}{4}(20 - 4) = 4", "respuesta": "4 Amperios",
         "plot": {"f1": lambda x: x*0 + 4, "x": [1, 5], "type": "area", "labels": ["Tiempo t", "Corriente I"]}},
        
        {"tema": "Termodinámica (Temperatura)", "pregunta": "La temperatura dentro de un reactor nuclear aumenta linealmente siguiendo la función T(t) = 2t (en °C). Determina la temperatura promedio registrada durante las primeras 4 horas de operación.", 
         "latex": r"T_{prom} = \frac{1}{4-0} \int_{0}^{4} 2t \, dt = \frac{1}{4} [t^2]_0^4 = \frac{1}{4}(16) = 4", "respuesta": "4 °C",
         "plot": {"f1": lambda x: 2*x, "x": [0, 4], "type": "area", "labels": ["Tiempo t", "Temperatura T"]}},
        
        {"tema": "Mecánica (Amortiguadores)", "pregunta": "El resorte de un amortiguador requiere una fuerza descrita por la Ley de Hooke F(x) = 10x (k=10 N/m). ¿Cuánto trabajo mecánico (en Joules) se necesita para estirar este resorte 2 metros desde su posición de reposo?", 
         "latex": r"W = \int_{0}^{2} 10x \, dx = \left[ 5x^2 \right]_0^2 = 5(4) - 0 = 20", "respuesta": "20 Joules",
         "plot": {"f1": lambda x: 10*x, "x": [0, 2], "type": "area", "labels": ["Distancia x", "Fuerza F"]}},
        
        {"tema": "Mecánica (Banda Elástica)", "pregunta": "Una banda elástica gigante industrial tiene una constante de rigidez k = 2 N/m. Calcula el trabajo realizado para estirarla hasta 5 metros de longitud desde su estado natural.", 
         "latex": r"W = \int_{0}^{5} 2x \, dx = \left[ x^2 \right]_0^5 = 25 - 0 = 25", "respuesta": "25 Joules",
         "plot": {"f1": lambda x: 2*x, "x": [0, 5], "type": "area", "labels": ["Distancia x", "Fuerza F"]}},
        
        {"tema": "Hidráulica (Fugas)", "pregunta": "La tasa a la que se fuga el agua de un tanque perforado empeora con el tiempo según R(t) = t³ (en litros por hora). ¿Cuántos litros de agua se habrán perdido en total durante las primeras 2 horas?", 
         "latex": r"\text{Volumen} = \int_{0}^{2} t^3 \, dt = \left[ \frac{t^4}{4} \right]_0^2 = \frac{16}{4} = 4", "respuesta": "4 Litros",
         "plot": {"f1": lambda x: x**3, "x": [0, 2], "type": "area", "labels": ["Tiempo t", "Tasa de Fuga R(t)"]}}
    ],
    "🟡 Medio": [
        {"tema": "Arquitectura (Arcos)", "pregunta": "Se planea construir un puente con un arco parabólico. La altura del arco respecto al suelo (y=0) está dada por y = 4 - x² (en metros). Calcula el área frontal total que ocupará el arco.", 
         "latex": r"\text{Puntos de anclaje: } x = \pm 2. \quad A = \int_{-2}^{2} (4 - x^2) \, dx = \left[ 4x - \frac{x^3}{3} \right]_{-2}^{2} = \frac{32}{3}", "respuesta": "32/3 m²",
         "plot": {"f1": lambda x: 4 - x**2, "x": [-2, 2], "type": "area", "labels": ["Ancho x", "Altura y"]}},
        
        {"tema": "Biología (Poblaciones)", "pregunta": "En un ecosistema, la tasa de natalidad es N(t) = 2t y la de mortalidad es M(t) = t² (en miles de individuos/año). Encuentra cuándo ambas tasas se igualan y calcula el incremento neto de la población (área entre las curvas) en ese periodo.", 
         "latex": r"\text{Intersecciones: } 0, 2. \quad A = \int_{0}^{2} (2t - t^2) \, dt = \left[ t^2 - \frac{t^3}{3} \right]_0^2 = 4 - \frac{8}{3} = \frac{4}{3}", "respuesta": "4/3 (Aprox. 1,333 individuos)",
         "plot": {"f1": lambda x: 2*x, "f2": lambda x: x**2, "x": [0, 2], "type": "area_between", "labels": ["Tiempo t", "Tasas (Natalidad/Mortalidad)"]}},
        
        {"tema": "Impresión 3D (Jarrones)", "pregunta": "Una impresora 3D va a fabricar un jarrón sólido cuyo radio exterior está modelado por y = x² cm. Calcula el volumen de plástico necesario para imprimir la pieza completa si la altura de diseño abarca desde x=0 hasta x=2 cm.", 
         "latex": r"V = \pi \int_{0}^{2} (x^2)^2 \, dx = \pi \int_{0}^{2} x^4 \, dx = \pi \left[ \frac{x^5}{5} \right]_0^2 = \frac{32\pi}{5}", "respuesta": "32π/5 cm³",
         "plot": {"f1": lambda x: x**2, "x": [0, 2], "type": "area", "rev_axis": "y=0", "labels": ["Altura x", "Radio y"]}},
        
        {"tema": "Diseño Industrial (Embudos)", "pregunta": "Para fabricar un embudo hueco en un torno, la pared exterior sigue la recta y = x y la cavidad interior sigue la curva y = x² (en cm). Calcula el volumen del material sólido girando el área comprendida entre estas curvas alrededor del eje X.", 
         "latex": r"V = \pi \int_{0}^{1} \left( (x)^2 - (x^2)^2 \right) \, dx = \pi \int_{0}^{1} (x^2 - x^4) \, dx = \pi \left[ \frac{x^3}{3} - \frac{x^5}{5} \right]_0^1 = \frac{2\pi}{15}", "respuesta": "2π/15 cm³",
         "plot": {"f1": lambda x: x, "f2": lambda x: x**2, "x": [0, 1], "type": "area_between", "rev_axis": "y=0", "labels": ["Longitud x", "Radio y"]}},
        
        {"tema": "Electrónica (Pulsos de Voltaje)", "pregunta": "Un osciloscopio registra un pulso de voltaje de media onda que sigue la función V(t) = sen(t) entre t=0 y t=π milisegundos. Determina el voltaje promedio suministrado al circuito durante ese pulso.", 
         "latex": r"V_{prom} = \frac{1}{\pi - 0} \int_{0}^{\pi} \sin(t) \, dt = \frac{1}{\pi} [-\cos(t)]_0^\pi = \frac{1}{\pi} (1 - (-1)) = \frac{2}{\pi}", "respuesta": "2/π Voltios",
         "plot": {"f1": lambda x: np.sin(x), "x": [0, np.pi], "type": "area", "labels": ["Tiempo t", "Voltaje V"]}},
        
        {"tema": "Microbiología (Cultivos)", "pregunta": "Un cultivo de bacterias crece exponencialmente siguiendo la función P(t) = e^t (en millones). Calcula el tamaño promedio de la población de bacterias durante la primera hora de observación (t de 0 a 1).", 
         "latex": r"P_{prom} = \frac{1}{1-0} \int_{0}^{1} e^t \, dt = \left[ e^t \right]_0^1 = e^1 - e^0 = e - 1", "respuesta": "e - 1 Millones",
         "plot": {"f1": lambda x: np.exp(x), "x": [0, 1], "type": "area", "labels": ["Tiempo t", "Población P"]}},
        
        {"tema": "Ingeniería Mecánica (Resorte Precomprimido)", "pregunta": "Un muelle de suspensión industrial (k=200 N/m) ya se encuentra comprimido 0.1 metros. ¿Cuánto trabajo mecánico adicional se debe ejercer para comprimirlo aún más, hasta alcanzar los 0.3 metros?", 
         "latex": r"W = \int_{0.1}^{0.3} 200x \, dx = \left[ 100x^2 \right]_{0.1}^{0.3} = 100(0.09) - 100(0.01) = 9 - 1 = 8", "respuesta": "8 Joules",
         "plot": {"f1": lambda x: 200*x, "x": [0.1, 0.3], "type": "area", "labels": ["Compresión x", "Fuerza F"]}},
        
        {"tema": "Finanzas (Optimización de Beneficios)", "pregunta": "La tasa de ingresos de una startup es I(t) = √t y la de costos es C(t) = t/2 (en miles de $/mes). Encuentra el periodo en que los ingresos superan a los costos y calcula la ganancia total acumulada (área entre curvas) en esos meses.", 
         "latex": r"\text{Cruce: } 0 \text{ y } 4. \quad G = \int_{0}^{4} \left(\sqrt{t} - \frac{t}{2}\right) \, dt = \left[ \frac{2}{3}t^{3/2} - \frac{t^2}{4} \right]_0^4 = \frac{16}{3} - 4 = \frac{4}{3}", "respuesta": "4/3 (Aprox. $1,333 dólares)",
         "plot": {"f1": lambda x: np.sqrt(x), "f2": lambda x: x/2, "x": [0, 4], "type": "area_between", "labels": ["Tiempo t", "Ingresos/Costos"]}},
        
        {"tema": "Acústica (Trompeta de Torricelli)", "pregunta": "Un pabellón auditivo para un altavoz se modela rotando la curva y = 1/x alrededor del eje X. Para evitar hacerla infinita, fabricaremos la sección que va desde x = 1 hasta x = e. Calcula el volumen de aire que encierra.", 
         "latex": r"V = \pi \int_{1}^{e} \left(\frac{1}{x}\right)^2 \, dx = \pi \left[ -\frac{1}{x} \right]_1^e = \pi \left( -\frac{1}{e} - (-1) \right) = \pi\left(1 - \frac{1}{e}\right)", "respuesta": "π(1 - 1/e) u³",
         "plot": {"f1": lambda x: 1/x, "x": [1, np.e], "type": "area", "rev_axis": "y=0", "labels": ["Longitud x", "Radio y"]}},
        
        {"tema": "Física Clásica (Trabajo contra la Gravedad)", "pregunta": "Una grúa de construcción levanta un balde de cemento de 10 kg desde el suelo hasta un andamio de 5 metros de altura. Considerando que la fuerza de gravedad es constante (F = mg = 98 N), calcula el trabajo realizado.", 
         "latex": r"W = \int_{0}^{5} 98 \, dy = \left[ 98y \right]_0^5 = 490", "respuesta": "490 Joules",
         "plot": {"f1": lambda y: y*0 + 98, "x": [0, 5], "type": "area_y", "labels": ["Fuerza F", "Altura y"]}}
    ],
    "🔴 Difícil": [
        {"tema": "Geografía (Islas Delta)", "pregunta": "En un delta, la acumulación de sedimentos formó una isla acotada por una orilla parabólica x = y² y un canal rectilíneo x = y + 2 (en km). Integra respecto al eje Y para descubrir la superficie total de la isla.", 
         "latex": r"\text{Límites Y: } y^2 = y+2 \rightarrow y \in [-1, 2]. \quad A = \int_{-1}^{2} ((y+2) - y^2) \, dy = \left[ \frac{y^2}{2} + 2y - \frac{y^3}{3} \right]_{-1}^2 = \frac{9}{2}", "respuesta": "9/2 km²",
         "plot": {"f1": lambda y: y + 2, "f2": lambda y: y**2, "x": [-1, 2], "type": "area_between_y", "labels": ["Distancia X", "Distancia Y"]}},
        
        {"tema": "Acústica (Interferencia de Ondas)", "pregunta": "Dos ondas sonoras que interfieren tienen potencias P1(x) = sen(x) y P2(x) = cos(x). Calcula la diferencia absoluta de energía acumulada (el área total entre las curvas) en el intervalo temporal [0, π/2]. ¡Cuidado, las curvas se cruzan!", 
         "latex": r"A = \int_{0}^{\pi/4} (\cos x - \sin x)dx + \int_{\pi/4}^{\pi/2} (\sin x - \cos x)dx = 2\sqrt{2} - 2", "respuesta": "2√2 - 2 Joules",
         "plot": {"f1": lambda x: np.cos(x), "f2": lambda x: np.sin(x), "x": [0, np.pi/2], "type": "area_between", "labels": ["Tiempo t", "Potencias P"]}},
        
        {"tema": "Ingeniería de Alimentos (Tazón Mezclador)", "pregunta": "Diseñaremos un tazón centrífugo. La pared del tazón se forma por el espacio entre las curvas y = x² y x = y². Al girar esta región alrededor del eje Y (el eje del motor), ¿cuál es el volumen de acero inoxidable necesario para la pared del tazón?", 
         "latex": r"\text{En términos de y: } x = \sqrt{y}, x = y^2. \quad V = \pi \int_{0}^{1} ((\sqrt{y})^2 - (y^2)^2) \, dy = \pi \left[ \frac{y^2}{2} - \frac{y^5}{5} \right]_0^1 = \frac{3\pi}{10}", "respuesta": "3π/10 cm³",
         "plot": {"f1": lambda y: np.sqrt(y), "f2": lambda y: y**2, "x": [0, 1], "type": "area_between_y", "rev_axis": "x=0", "labels": ["Radio x", "Altura y"]}},
        
        {"tema": "Aeroespacial (Eje Desplazado)", "pregunta": "El cono frontal de un cohete pequeño se modela tomando la región delimitada por y = x² y el límite plano y = 4, y luego girándola alrededor de un eje central desplazado (la recta y = 4). Calcula el volumen aerodinámico resultante.", 
         "latex": r"V = \pi \int_{-2}^{2} (4 - x^2)^2 \, dx = \pi \int_{-2}^{2} (16 - 8x^2 + x^4) \, dx = \frac{512\pi}{15}", "respuesta": "512π/15 u³",
         "plot": {"f1": lambda x: x*0 + 4, "f2": lambda x: x**2, "x": [-2, 2], "type": "area_between", "rev_axis": "y=4", "labels": ["Radio x", "Altura y"]}},
        
        {"tema": "Mecánica (Potencia de un Péndulo)", "pregunta": "La potencia disipada por un péndulo con fricción durante su primera oscilación sigue la ecuación P(t) = t·sen(t) Watts en el intervalo [0, π]. Usa integración por partes para hallar la potencia promedio en ese lapso.", 
         "latex": r"P_{prom} = \frac{1}{\pi} \int_{0}^{\pi} t\sin(t) \, dt. \text{ (Por partes: } u=t, dv=\sin t dt). \quad \frac{1}{\pi} [ -t\cos t + \sin t ]_0^\pi = \frac{\pi}{\pi} = 1", "respuesta": "1 Watt",
         "plot": {"f1": lambda x: x * np.sin(x), "x": [0, np.pi], "type": "area", "labels": ["Tiempo t", "Potencia P"]}},
        
        {"tema": "Termodinámica (Entropía)", "pregunta": "En un proceso químico, la tasa de generación de entropía aumenta logarítmicamente S'(t) = ln(t) (en J/K·s). ¿Cuál es la tasa promedio de entropía generada en el intervalo de tiempo desde t=1 hasta t=e segundos?", 
         "latex": r"S_{prom} = \frac{1}{e-1} \int_{1}^{e} \ln(t) \, dt = \frac{1}{e-1} [t\ln t - t]_1^e = \frac{1}{e-1} ((e - e) - (0 - 1)) = \frac{1}{e-1}", "respuesta": "1 / (e-1) J/K·s",
         "plot": {"f1": lambda x: np.log(x), "x": [1, np.e], "type": "area", "labels": ["Tiempo t", "Entropía S'"]}},
        
        {"tema": "Ingeniería Civil (Bombeo de Fluidos)", "pregunta": "Un tanque subterráneo cilíndrico (radio 2m, profundidad 5m) está completamente lleno de agua. Calcula el trabajo total requerido por una bomba para extraer toda el agua llevándola hasta el nivel del suelo (y=5). Utiliza el peso específico ρg.", 
         "latex": r"W = \int_{0}^{5} \rho g (\pi r^2) (5-y) \, dy = 4\pi\rho g \left[ 5y - \frac{y^2}{2} \right]_0^5 = 50\pi\rho g \text{ Joules}", "respuesta": "50πρg Joules",
         "plot": {"f1": lambda y: y*0 + 2, "f2": lambda y: y*0 - 2, "x": [0, 5], "type": "area_between_y", "labels": ["Radio (m)", "Profundidad Y (m)"]}},
        
        {"tema": "Sistemas de Izaje (Cadena Pesada)", "pregunta": "Un motor en lo alto de un edificio de 10 m de altura debe izar una cadena pesada de acero de 10 metros que cuelga hasta el suelo. Si la cadena pesa 2 kg por cada metro lineal, calcula el trabajo necesario para subirla por completo (usa g=9.8). ¡Recuerda que la fuerza disminuye a medida que sube!", 
         "latex": r"\text{Fuerza en y: } F = 19.6(10-y). \quad W = \int_{0}^{10} 19.6(10-y) \, dy = 19.6 \left[ 10y - \frac{y^2}{2} \right]_0^{10} = 980", "respuesta": "980 Joules",
         "plot": {"f1": lambda y: 19.6*(10-y), "x": [0, 10], "type": "area_y", "labels": ["Fuerza F (N)", "Altura Y (m)"]}},
        
        {"tema": "Termografía (Choque Térmico)", "pregunta": "Al soldar dos placas metálicas, sus gradientes de temperatura muestran un desajuste modelado por y = e^x (material que se calienta) y y = e^{-x} (material frío). Calcula el área total de choque térmico entre ambas curvas desde el borde x=0 hasta una profundidad de x=1 cm.", 
         "latex": r"A = \int_{0}^{1} (e^x - e^{-x}) \, dx = \left[ e^x + e^{-x} \right]_0^1 = (e + e^{-1}) - (1 + 1) = e + \frac{1}{e} - 2", "respuesta": "e + 1/e - 2 cm²",
         "plot": {"f1": lambda x: np.exp(x), "f2": lambda x: np.exp(-x), "x": [0, 1], "type": "area_between", "labels": ["Profundidad x", "Temperatura y"]}},
        
        {"tema": "Aeronáutica (Cascarones Cilíndricos)", "pregunta": "Un domo de radar o 'radomo' tiene un perfil transversal delimitado por la función y = sen(x) desde x=0 hasta x=π. Aplicando el método de cascarones cilíndricos, calcula el volumen del espacio confinado bajo el domo si esta curva gira sobre el eje Y.", 
         "latex": r"V = 2\pi \int_{0}^{\pi} x\sin(x) \, dx. \text{ Por partes: } 2\pi [ -x\cos x + \sin x ]_0^\pi = 2\pi(\pi) = 2\pi^2", "respuesta": "2π² u³",
         "plot": {"f1": lambda x: np.sin(x), "x": [0, np.pi], "type": "area", "rev_axis": "x=0", "labels": ["Radio x", "Altura y"]}}
    ]
}


st.title("🧠 Banco de Retos: Cálculo Integral en la Vida Real")
st.markdown("Pon a prueba tus habilidades. Resuelve problemas aplicados o ponte a prueba en el Quiz conceptual.")

# --- TABS PRINCIPALES ---
tab_retos, tab_quiz = st.tabs(["🚀 Retos Aplicados", "📝 Quiz de Agilidad Mental"])

# ==========================================
# PESTAÑA 1: RETOS APLICADOS
# ==========================================
with tab_retos:
    # --- INTERFAZ LATERAL (SIDEBAR) ---
    st.sidebar.header("⚙️ Configuración")
    nivel_seleccionado = st.sidebar.selectbox("Selecciona la dificultad:", list(ejercicios.keys()))

    lista_ejercicios = ejercicios[nivel_seleccionado]
    nombres_ejercicios = [f"Reto {i+1}: {ej['tema']}" for i, ej in enumerate(lista_ejercicios)]
    ej_seleccionado_idx = st.sidebar.radio("Elige una aplicación:", range(len(nombres_ejercicios)), format_func=lambda x: nombres_ejercicios[x])

    ej_actual = lista_ejercicios[ej_seleccionado_idx]

    # --- CUERPO PRINCIPAL ---
    st.subheader(f"Nivel: {nivel_seleccionado}")
    st.markdown(f"### 📌 Misión: {ej_actual['tema']}")

    # Renderizar el gráfico/esquema si existe
    if "plot" in ej_actual:
        st.plotly_chart(generar_esquema(ej_actual["plot"]), use_container_width=True)

    st.info("**Contexto y Planteamiento del problema:**")
    st.write(ej_actual['pregunta'])

    st.divider()

    st.warning("Toma papel y lápiz ✏️. Intenta plantear la integral y resolverla antes de desplegar la respuesta.")

    with st.expander("Ver Solución Analítica y Procedimiento 🔍"):
        st.success(f"**Respuesta final:** {ej_actual['respuesta']}")
        
        st.markdown("**Desarrollo matemático paso a paso:**")
        st.latex(ej_actual['latex'])
        
        st.divider()
        if "Fácil" in nivel_seleccionado:
            st.write("💡 *Tip de ingeniería: En estos problemas, verifica siempre que las unidades de tu resultado (metros, joules, voltios) concuerden con lo que estás calculando.*")
        elif "Medio" in nivel_seleccionado:
            st.write("💡 *Tip de diseño: Hacer el boceto de las curvas (como el gráfico de arriba) te salva de plantear mal los límites o equivocarte de función superior/inferior.*")
        else:
            st.write("🔥 *¡Excelente nivel! Resolver sistemas como fluidos contra la gravedad o volúmenes complejos es lo que hace un verdadero ingeniero o científico.*")


# ==========================================
# PESTAÑA 2: QUIZ CONCEPTUAL
# ==========================================
with tab_quiz:
    st.header("Demuestra tu agilidad mental ⏱️")
    st.markdown("Responde estas 10 preguntas teóricas y de cálculo mental. **¡No necesitas calculadora!**")
    st.divider()

    respuestas = []

    # Preguntas
    q1 = st.radio("1. ¿Cuál es el resultado de la integral definida de 2x evaluada de 0 a 1?", ["A) 0", "B) 1", "C) 2"], index=None)
    respuestas.append(q1 == "B) 1")

    q2 = st.radio("2. Geométricamente, ¿qué representa la integral definida de una función positiva?", ["A) La pendiente de la recta tangente", "B) El volumen de la curva", "C) El área bajo la curva"], index=None)
    respuestas.append(q2 == "C) El área bajo la curva")

    q3 = st.radio("3. Si rotas un rectángulo 360 grados alrededor de uno de sus lados, ¿qué sólido se forma?", ["A) Un cilindro", "B) Una esfera", "C) Un cono"], index=None)
    respuestas.append(q3 == "A) Un cilindro")

    q4 = st.radio("4. ¿Cuál es el valor exacto de la integral de eˣ evaluada desde x=0 hasta x=0?", ["A) e", "B) 1", "C) 0"], index=None)
    respuestas.append(q4 == "C) 0")

    q5 = st.radio("5. Si ejerces una fuerza constante de 10 Newtons, ¿qué trabajo realizas al desplazar un objeto 3 metros?", ["A) 13 Joules", "B) 30 Joules", "C) 3 Joules"], index=None)
    respuestas.append(q5 == "B) 30 Joules")

    q6 = st.radio("6. Según el Teorema Fundamental del Cálculo, ¿cuál es la derivada respecto a 'x' de la integral de f(t)dt desde 'a' hasta 'x'?", ["A) f(x)", "B) f'(x)", "C) 0"], index=None)
    respuestas.append(q6 == "A) f(x)")

    q7 = st.radio("7. ¿Qué método usarías para calcular el volumen de un sólido que posee un hueco interno o cavidad?", ["A) Método de Discos", "B) Método de Arandelas (Washers)", "C) Fracciones Parciales"], index=None)
    respuestas.append(q7 == "B) Método de Arandelas (Washers)")

    q8 = st.radio("8. En la física, si integras la función que describe la velocidad v(t) de un vehículo, ¿qué obtienes?", ["A) La aceleración", "B) La posición o distancia recorrida", "C) La fuerza"], index=None)
    respuestas.append(q8 == "B) La posición o distancia recorrida")

    q9 = st.radio("9. ¿Cuál es el valor de la integral de 1/x (evaluada desde 1 hasta e)?", ["A) 0", "B) 1", "C) e"], index=None)
    respuestas.append(q9 == "B) 1")

    q10 = st.radio("10. ¿Cuál es el valor promedio de la función constante f(x) = 5 en cualquier intervalo [a, b]?", ["A) 5", "B) 0", "C) 2.5"], index=None)
    respuestas.append(q10 == "A) 5")

    st.write("")
    if st.button("Calificar Quiz 🎯", type="primary"):
        # Contar respuestas nulas o vacías
        if None in [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]:
            st.warning("⚠️ Por favor, responde todas las preguntas antes de calificar.")
        else:
            puntuacion = sum(respuestas)
            if puntuacion == 10:
                st.balloons()
                st.success(f"¡PERFECTO! Tu puntuación es {puntuacion} de 10. ¡Dominas la teoría a la perfección! 🏆")
            elif puntuacion >= 7:
                st.success(f"¡Muy bien! Tu puntuación es {puntuacion} de 10. Tienes bases muy sólidas. 👍")
            else:
                st.error(f"Tu puntuación es {puntuacion} de 10. Te sugiero repasar un poco más los conceptos básicos del cálculo. 📚")

# ==========================================
# --- NUEVA SECCIÓN: SOLUCIONARIO PASO A PASO (NIVEL DIFÍCIL) ---
# ==========================================
st.divider()
st.header("🔬 Solucionario Detallado: Nivel Difícil")
st.markdown("A continuación, desglosamos el paso a paso matemático de cada uno de los 10 retos del nivel difícil.")

with st.expander("1. Geografía (Islas Delta) - Área respecto al eje Y"):
    st.markdown("1. Identificar las curvas: La función de la derecha es x = y + 2, y la de la izquierda es x = y².")
    st.markdown("2. Encontrar límites igualando: y + 2 = y² resulta en y = -1 y y = 2.")
    st.markdown("3. Plantear la integral y resolver:")
    st.latex(r"A = \int_{-1}^{2} ((y + 2) - y^2) \, dy = \left[ \frac{y^2}{2} + 2y - \frac{y^3}{3} \right]_{-1}^{2} = \frac{9}{2}")

with st.expander("2. Acústica (Interferencia de Ondas) - Área entre curvas"):
    st.markdown("1. Identificar punto de cruce de las potencias P1 y P2: sen(x) = cos(x) ocurre en x = π/4.")
    st.markdown("2. Dividir la integral en dos partes (antes y después del cruce).")
    st.latex(r"A = \int_{0}^{\pi/4} (\cos x - \sin x)dx + \int_{\pi/4}^{\pi/2} (\sin x - \cos x)dx")
    st.markdown("3. Evaluar y sumar ambas áreas:")
    st.latex(r"A = (\sqrt{2} - 1) + (\sqrt{2} - 1) = 2\sqrt{2} - 2")

with st.expander("3. Ingeniería de Alimentos (Tazón Mezclador) - Rotación Eje Y"):
    st.markdown("1. Expresar funciones en términos de y: x = √y (exterior) y x = y² (interior).")
    st.markdown("2. Aplicar el método de arandelas respecto al eje Y en el intervalo de 0 a 1.")
    st.latex(r"V = \pi \int_{0}^{1} ((\sqrt{y})^2 - (y^2)^2) \, dy = \pi \int_{0}^{1} (y - y^4) \, dy")
    st.markdown("3. Integrar y evaluar:")
    st.latex(r"V = \pi \left[ \frac{y^2}{2} - \frac{y^5}{5} \right]_0^1 = \frac{3\pi}{10}")

with st.expander("4. Aeroespacial (Eje Desplazado) - Rotación sobre y=4"):
    st.markdown("1. El radio de rotación desde la curva y = x² hasta el eje de giro y = 4 es R = 4 - x².")
    st.markdown("2. Encontrar límites donde la curva corta el eje: x² = 4 resulta en x = -2 y x = 2.")
    st.markdown("3. Aplicar el método de discos:")
    st.latex(r"V = \pi \int_{-2}^{2} (4 - x^2)^2 \, dx = \pi \int_{-2}^{2} (16 - 8x^2 + x^4) \, dx = \frac{512\pi}{15}")

with st.expander("5. Mecánica (Potencia de un Péndulo) - Integración por partes"):
    st.markdown("1. Usar la fórmula de valor promedio en el intervalo de 0 a π.")
    st.latex(r"P_{prom} = \frac{1}{\pi} \int_{0}^{\pi} t\sin(t) \, dt")
    st.markdown("2. Aplicar integración por partes tomando u = t y dv = sen(t)dt.")
    st.latex(r"P_{prom} = \frac{1}{\pi} \left[ -t\cos t + \sin t \right]_0^\pi = \frac{1}{\pi} (\pi) = 1")

with st.expander("6. Termodinámica (Entropía) - Valor Promedio"):
    st.markdown("1. Aplicar teorema de valor medio para integrales en el intervalo de 1 a e.")
    st.latex(r"S_{prom} = \frac{1}{e-1} \int_{1}^{e} \ln(t) \, dt")
    st.markdown("2. La integral de ln(t) conocida es t ln(t) - t.")
    st.latex(r"S_{prom} = \frac{1}{e-1} \left[ t\ln t - t \right]_1^e = \frac{1}{e-1}")

with st.expander("7. Ingeniería Civil (Bombeo de Fluidos) - Trabajo"):
    st.markdown("1. Plantear el diferencial de trabajo dW = Fuerza × Distancia.")
    st.markdown("2. La fuerza es el peso del agua: Densidad × Gravedad × Volumen de una rebanada (π r² dy).")
    st.markdown("3. La distancia que debe subir cada rebanada hacia el nivel y = 5 es (5 - y).")
    st.latex(r"W = \int_{0}^{5} \rho g (\pi (2)^2) (5-y) \, dy = 4\pi\rho g \left[ 5y - \frac{y^2}{2} \right]_0^5 = 50\pi\rho g")

with st.expander("8. Sistemas de Izaje (Cadena Pesada) - Trabajo Variable"):
    st.markdown("1. Determinar el peso de la cadena por metro lineal: 2 kg/m × 9.8 m/s² = 19.6 N/m.")
    st.markdown("2. La fuerza en cualquier altura y depende de la cantidad de cadena que falta subir (10 - y).")
    st.latex(r"W = \int_{0}^{10} 19.6(10-y) \, dy = 19.6 \left[ 10y - \frac{y^2}{2} \right]_0^{10} = 980")

with st.expander("9. Termografía (Choque Térmico) - Área entre exponenciales"):
    st.markdown("1. La curva superior es e^x y la inferior es e^(-x) en el intervalo de profundidad de 0 a 1.")
    st.markdown("2. Plantear la integral directa.")
    st.latex(r"A = \int_{0}^{1} (e^x - e^{-x}) \, dx")
    st.markdown("3. Integrar y evaluar:")
    st.latex(r"A = \left[ e^x + e^{-x} \right]_0^1 = (e + e^{-1}) - (1 + 1) = e + \frac{1}{e} - 2")

with st.expander("10. Aeronáutica (Cascarones Cilíndricos) - Volumen Y"):
    st.markdown("1. La fórmula general de cascarones cilíndricos es V = 2π ∫ x f(x) dx.")
    st.latex(r"V = 2\pi \int_{0}^{\pi} x\sin(x) \, dx")
    st.markdown("2. Utilizar el mismo resultado de integración por partes del reto 5.")
    st.latex(r"V = 2\pi \left[ -x\cos x + \sin x \right]_0^\pi = 2\pi(\pi) = 2\pi^2")
