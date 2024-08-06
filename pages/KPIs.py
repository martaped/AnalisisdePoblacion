import pandas as pd
import streamlit as st
import plotly.express as px
import json

# Configuración inicial del layout de la página
st.set_page_config(
    page_title="Mi Aplicación Streamlit",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #80DEEA;  /* Color de fondo que desees */
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Función para calcular la Tasa de Crecimiento Anual de la Población (KPI 1)
def tasa_crecimiento_anual(data):
    data_sorted = data.sort_values(by=['País', 'Año'])
    data_grouped = data_sorted.groupby('País')
    poblacion_inicial = data_grouped['Población'].first()
    poblacion_final = data_grouped['Población'].last()
    crecimiento_por_pais = ((poblacion_final - poblacion_inicial) / poblacion_inicial) * 100
    return crecimiento_por_pais.round(2)

# Función para calcular los Países con Mayor y Menor Crecimiento Poblacional (KPI 2)
def paises_crecimiento_decrecimiento(data):
    data["Crecimiento"] = data.groupby("País")["Población"].pct_change() * 100
    promedios_anuales_por_pais = data.groupby("País")["Crecimiento"].mean().reset_index()
    promedios_anuales_por_pais["Crecimiento"] = promedios_anuales_por_pais["Crecimiento"].round(2)
    return promedios_anuales_por_pais.rename(columns={"País": "País", "Crecimiento": "Crecimiento"})

# Función para calcular el Crecimiento Poblacional Anual Promedio de Cada País (KPI 3)
def crecimiento_promedio_anual(data):
    paises = data['País'].unique()
    resultados = []
    for pais in paises:
        data_pais = data[data['País'] == pais]
        ultimo_año = data_pais['Año'].max()
        primer_año = data_pais['Año'].min()
        numero_de_años = ultimo_año - primer_año + 1
        poblacion_inicial = data_pais[data_pais['Año'] == primer_año]['Población'].sum()
        poblacion_final = data_pais[data_pais['Año'] == ultimo_año]['Población'].sum()
        crecimiento_promedio = (poblacion_final - poblacion_inicial) / numero_de_años
        resultados.append({'País': pais, 'Crecimiento Promedio Anual': crecimiento_promedio})
    return pd.DataFrame(resultados)

# Leer los datos
data = pd.read_csv("data/poblacion-latam.csv", low_memory=False)

# Calcula los KPIs
crecimiento_por_pais = tasa_crecimiento_anual(data)
paises_con_mayor_menor_crecimiento = paises_crecimiento_decrecimiento(data)
crecimiento_promedio_por_pais = crecimiento_promedio_anual(data)

# Crear una aplicación de Streamlit
st.title("Análisis de Población - KPIs")
st.divider()

# Filtrar por países en la barra lateral
opciones_paises = st.sidebar.multiselect("Seleccione uno o varios países", data['País'].unique(), default=["Guatemala", "Honduras", "Panama", "Ecuador", "Bolivia"])

# Filtrar los resultados de los KPIs por países seleccionados
crecimiento_filtrado = crecimiento_por_pais[crecimiento_por_pais.index.isin(opciones_paises)]

# Crear columnas para la presentación de los gráficos
col1, col2, col3 = st.columns([2, 0.2, 2])

# Mostrar el KPI 1: Tasa de Crecimiento Anual de la Población
with col1:
    st.subheader("KPI 1: Tasa de Crecimiento de la Población Porcentual")
    st.bar_chart(crecimiento_filtrado, color="#03045e")
    st.write("**Nota:** Los valores del eje y representan porcentajes.")


with col2:
    st.markdown("&nbsp;")

# Mostrar el KPI 2: Top 5 Países con Mayor y Menor Tasa de Crecimiento Poblacional
with col3:
    top_crecimiento = paises_con_mayor_menor_crecimiento.sort_values(by="Crecimiento", ascending=False).head(5)
    top_decrecimiento = paises_con_mayor_menor_crecimiento.sort_values(by="Crecimiento", ascending=True).head(5)

    st.subheader('KPI 2: Top 5 Países con Mayor y Menor Tasa de Crecimiento Poblacional Porcentual Promedio')
    fig2 = px.bar(top_decrecimiento, x='Crecimiento', y='País', orientation='h',
             labels={'Crecimiento': 'Crecimiento Promedio Anual (%)'},
             color_discrete_sequence=['#48cae4'] * len(top_decrecimiento), height=370)
    fig2.update_layout(xaxis_showgrid=False)

    fig2.add_trace(px.bar(top_crecimiento[::-1], x='Crecimiento', y='País', orientation='h',
                        color_discrete_sequence=['#03045e'] * len(top_crecimiento)).data[0])
    st.plotly_chart(fig2)

# Divisor para separar las secciones
st.divider()

# Crear nuevas columnas para presentar más gráficos
col4, col5, col6 = st.columns([2, 0.2, 2])

# Mostrar el KPI 3: Crecimiento Poblacional Anual Promedio en formato de mapa
with col4:
    # Leer el archivo GeoJSON con información geográfica
    with open("data/custom.geojson", "r", encoding="utf-8") as file:
        geojson_data = json.load(file)

    # Filtrar resultados de KPI 3 por países seleccionados
    crecimiento_filtrado = crecimiento_promedio_por_pais[crecimiento_promedio_por_pais['País'].isin(opciones_paises)]

    st.subheader("KPI 3: Crecimiento Poblacional Anual Promedio")
    fig3 = px.choropleth_mapbox(crecimiento_filtrado, geojson=geojson_data, color='Crecimiento Promedio Anual',
                                locations='País', featureidkey="properties.name", color_continuous_scale="haline",
                                mapbox_style="carto-positron", zoom=1.6, center={"lat": -15, "lon": -70},
                                opacity=0.5, labels={'Crecimiento Promedio Anual': 'CPA'}, height=370)

    fig3.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    st.plotly_chart(fig3)


with col5:
    st.markdown("&nbsp;")

# Mostrar el KPI 3: Crecimiento Poblacional Anual Promedio en formato de gráfico de líneas
with col6:
    # Filtrar datos por países seleccionados
    data_filtrada = data[data['País'].isin(opciones_paises)]

    st.subheader("Crecimiento Poblacional")
    fig = px.line(data_filtrada, x='Año', y='Población', color="País", height=370)

    st.plotly_chart(fig)
