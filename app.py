import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(page_title="Paso a Paso: Sólidos de Revolución", layout="wide")

st.title("De la Superficie al Volumen 🚀")
st.markdown("### Método de Discos: Construcción Paso a Paso")

# Función matemática de ejemplo: f(x) = sqrt(x)
def f(x): return np.sqrt(x)
a, b = 0.0, 4.0

# Controles de la "animación"
paso = st.radio(
    "Selecciona la fase de la explicación:",
    ["1. El área plana (2D)", 
     "2. La rotación (Formando el volumen)", 
     "3. Cortando en rebanadas (Método de discos)", 
     "4. El volumen final (Integral)"],
    horizontal=True
)

st.divider()

col_texto, col_grafica = st.columns([1, 1.5])

with col_texto:
    if paso == "1. El área plana (2D)":
        st.subheader("Paso 1: La superficie original")
        st.markdown("""
        Imagina que tomas el área atrapada entre la función y el eje X.
        Esta es el área plana que acabamos de aprender a calcular.
        """)
        st.latex(r"f(x) = \sqrt{x}")
        st.info("Fíjate bien en la forma plana. Ahora, vamos a prepararla para girar rápidamente alrededor del eje X.")

    elif paso == "2. La rotación (Formando el volumen)":
        st.subheader("Paso 2: Generando el Rastro 3D")
        st.markdown("""
        Al girar nuestra área plana rápidamente alrededor del eje X, **el rastro que deja forma un objeto tridimensional sólido**.
        
        Ejemplos de la vida real: Botellas, copas, pistones de motor, ruedas. Todo lo que se fabrica en un torno industrial es un sólido de revolución.
        """)
        angulo = st.slider("Gira la superficie manualmente (Grados):", 0, 360, 180, 10)

    elif paso == "3. Cortando en rebanadas (Método de discos)":
        st.subheader("Paso 3: Cortando el sólido en rebanadas")
        st.markdown("""
        * Si cortamos nuestro sólido 3D, cada rebanada es un **disco** (un círculo perfecto).
        * El área de un círculo es $\pi r^2$.
        * En nuestro plano, el radio $r$ es exactamente la altura de nuestra función $f(x)$.
        """)
        n_discos = st.slider("Número de discos (rebanadas):", 3, 30, 5)
        st.warning(f"Aquí estamos aproximando el volumen usando {n_discos} cilindros. ¡Mira qué pasa con la forma si aumentas el número de discos!")

    elif paso == "4. El volumen final (Integral)":
        st.subheader("Paso 4: Suma infinita (La Integral)")
        st.markdown("""
        Si hacemos que el grosor de cada disco ($dx$) sea infinitamente pequeño, tendremos una cantidad infinita de discos perfectos.
        
        Por lo tanto, sumamos infinitos discos usando la integral:
        """)
        st.latex(r"V = \pi \int_{a}^{b} [f(x)]^2 \, dx")
        st.success("¡El resultado es el volumen exacto y perfecto de nuestro sólido!")


with col_grafica:
    # Lógica de renderizado según el paso
    if paso == "1. El área plana (2D)":
        x_val = np.linspace(a, b, 100)
        y_val = f(x_val)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_val, y=y_val, fill='tozeroy', mode='lines', line=dict(color='blue', width=3), name="Área plana"))
        fig.update_layout(title="Vista 2D", xaxis_title="Eje X", yaxis_title="Eje Y", yaxis_range=[-2, 3], height=500)
        st.plotly_chart(fig, use_container_width=True)

    elif paso == "2. La rotación (Formando el volumen)":
        x_line = np.linspace(a, b, 50)
        theta = np.linspace(0, np.radians(angulo), 50)
        X, THETA = np.meshgrid(x_line, theta)
        Y = f(X) * np.cos(THETA)
        Z = f(X) * np.sin(THETA)
        
        fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis', opacity=0.9)])
        fig.update_layout(
            title=f"Rotación a {angulo}°",
            scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z',
                       yaxis=dict(range=[-2, 2]), zaxis=dict(range=[-2, 2]),
                       aspectratio=dict(x=1, y=0.5, z=0.5)),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

    elif paso == "3. Cortando en rebanadas (Método de discos)":
        fig = go.Figure()
        dx = (b - a) / n_discos
        x_edges = np.linspace(a, b, n_discos + 1)
        
        # Dibujar cada cilindro (disco)
        for i in range(n_discos):
            x_start = x_edges[i]
            x_end = x_edges[i+1]
            radio = f(x_end) # Usamos el borde derecho para la altura
            
            # Parametrización del cilindro
            xc = np.linspace(x_start, x_end, 2)
            theta_cyl = np.linspace(0, 2*np.pi, 30)
            XC, THETA = np.meshgrid(xc, theta_cyl)
            YC = radio * np.cos(THETA)
            ZC = radio * np.sin(THETA)
            
            # Alternar colores para ver claramente los discos
            color = 'Blues' if i % 2 == 0 else 'Teal'
            fig.add_trace(go.Surface(x=XC, y=YC, z=ZC, colorscale=color, showscale=False, opacity=0.9))

        fig.update_layout(
            title=f"Aproximación con {n_discos} discos",
            scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z',
                       yaxis=dict(range=[-2, 2]), zaxis=dict(range=[-2, 2]),
                       aspectratio=dict(x=1, y=0.5, z=0.5)),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

    elif paso == "4. El volumen final (Integral)":
        x_line = np.linspace(a, b, 50)
        theta = np.linspace(0, 2*np.pi, 50)
        X, THETA = np.meshgrid(x_line, theta)
        Y = f(X) * np.cos(THETA)
        Z = f(X) * np.sin(THETA)
        
        fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Plasma', opacity=1.0)])
        fig.update_layout(
            title="Sólido Perfecto (Discos infinitos)",
            scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z',
                       yaxis=dict(range=[-2, 2]), zaxis=dict(range=[-2, 2]),
                       aspectratio=dict(x=1, y=0.5, z=0.5)),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
