import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Nanopanel Solar IA",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡🧠 Simulador IA de Nanopanel Solar Futurista")

st.sidebar.header("Controles del Sistema")

irradiancia = st.sidebar.slider(
    "Irradiancia Solar (W/m²)",
    100,1200,800
)

area = st.sidebar.slider(
    "Área del Nanopanel (m²)",
    0.5,10.0,1.6
)

eficiencia = st.sidebar.slider(
    "Eficiencia Base (%)",
    10.0,50.0,38.0
)

temperatura = st.sidebar.slider(
    "Temperatura (°C)",
    0,80,35
)

nubosidad = st.sidebar.slider(
    "Nubosidad (%)",
    0,100,20
)

angulo = st.sidebar.slider(
    "Ángulo Solar (°)",
    0,90,15
)

degradacion = st.sidebar.slider(
    "Degradación del Material (%)",
    0,30,2
)

horas = st.sidebar.slider(
    "Horas de Operación",
    1,12,6
)

# ---------------------------
# Modelo IA
# ---------------------------

eta = eficiencia/100

beta = 0.0025

eta_temp = eta * (1 - beta*(temperatura-25))

factor_nube = 1 - (nubosidad/100)*0.60

factor_angulo = np.cos(np.radians(angulo))

factor_deg = 1 - degradacion/100

factor_ia = 1 + 0.15*(1 - nubosidad/100)

eta_final = (
    eta_temp
    * factor_nube
    * factor_angulo
    * factor_deg
    * factor_ia
)

potencia = irradiancia * area * eta_final

energia = potencia * horas

perdidas_termicas = (
    (1 - eta_temp/eta)*100
)

# ---------------------------
# IA Predictiva
# ---------------------------

produccion_futura = energia * (
    1 + 0.05*(factor_ia-1)*10
)

# ---------------------------
# Dashboard
# ---------------------------

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "⚡ Potencia",
    f"{potencia:.2f} W"
)

c2.metric(
    "🔋 Energía",
    f"{energia:.2f} Wh"
)

c3.metric(
    "🧬 Eficiencia IA",
    f"{eta_final*100:.2f}%"
)

c4.metric(
    "🤖 Factor IA",
    f"{factor_ia:.3f}"
)

st.markdown("---")

# ---------------------------
# Mensajes Inteligentes
# ---------------------------

if nubosidad < 20:
    st.success(
        "🤖 IA detecta condiciones óptimas."
    )

elif nubosidad < 60:
    st.warning(
        "☁️ IA compensa pérdidas moderadas."
    )
else:
    st.error(
        "🌧️ IA activó modo de optimización extrema."
    )

# ---------------------------
# Potencia vs Irradiancia
# ---------------------------

g = np.linspace(100,1200,100)

p = g * area * eta_final

df1 = pd.DataFrame({
    "Irradiancia": g,
    "Potencia": p
})

fig1 = px.line(
    df1,
    x="Irradiancia",
    y="Potencia",
    title="Potencia vs Irradiancia"
)

# ---------------------------
# Eficiencia vs Temperatura
# ---------------------------

temps = np.arange(0,81)

etas = eta*(1-beta*(temps-25))*100

df2 = pd.DataFrame({
    "Temperatura": temps,
    "Eficiencia": etas
})

fig2 = px.line(
    df2,
    x="Temperatura",
    y="Eficiencia",
    title="Eficiencia vs Temperatura"
)

# ---------------------------
# Producción Día Completo
# ---------------------------

horas_dia = np.arange(6,19)

perfil_sol = np.sin(
    np.linspace(0,np.pi,len(horas_dia))
)

perfil_sol = np.maximum(
    perfil_sol,
    0
)

energia_dia = potencia * perfil_sol

fig3 = go.Figure()

fig3.add_trace(
    go.Scatter(
        x=horas_dia,
        y=energia_dia,
        fill="tozeroy",
        name="Producción"
    )
)

fig3.update_layout(
    title="Producción Energética Diaria"
)

# ---------------------------
# Comparativa Tecnológica
# ---------------------------

panel_conv = irradiancia*area*0.20

panel_nano = potencia

fig4 = go.Figure()

fig4.add_trace(
    go.Bar(
        x=["Convencional"],
        y=[panel_conv]
    )
)

fig4.add_trace(
    go.Bar(
        x=["Nanopanel IA"],
        y=[panel_nano]
    )
)

fig4.update_layout(
    title="Comparación Tecnológica"
)

# ---------------------------
# Mostrar gráficos
# ---------------------------

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

st.markdown("---")

st.subheader(
    "🔮 Predicción IA"
)

st.metric(
    "Producción futura estimada",
    f"{produccion_futura:.2f} Wh"
)

st.info(
    "La IA analiza continuamente "
    "irradiancia, temperatura, "
    "ángulo solar, nubosidad y "
    "degradación para maximizar "
    "la eficiencia del nanopanel."
)

