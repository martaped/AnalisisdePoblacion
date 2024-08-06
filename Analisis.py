import streamlit as st
from streamlit.components.v1 import html
#Streamlit de presentación, con titulo y resumen de proyecto
st.set_page_config(
    page_title="Mi Aplicación Streamlit",
    page_icon=":chart_with_upwards_trend:"
)
# Aplica los colores personalizados
# CSS personalizado para cambiar el color del texto en la barra lateral




st.markdown(
    """
    <style>
    .stApp {
        background-color: #80DEEA;  /* Color de fondo que desees */
    }
    .css-1lcbmhc {
        background-color: #1E88E5;  /* Color de fondo de la sidebar */
    }
    .sidebar .sidebar-content {
        color: #00008b;  /* Azul oscuro */
    }
    </style>
    """,
    unsafe_allow_html=True
)



st.title("Análisis de Población")


st.write("""
Este proyecto tiene como objetivo analizar los datos de la población de América Latina para comprender tendencias y patrones demográficos a lo largo del tiempo. 
Se realizo el respectivo ETL y EDA de los datos preliminares. Utilizamos diversas métricas y Key Performance Indicators (KPIs) para evaluar el crecimiento poblacional, identificar tendencias y tomar decisiones informadas.
""")

from PIL import Image
image = Image.open("data/poblacion.jpg")
st.image(image, caption="Población", use_column_width=True)


st.header("Key Performance Indicators (KPIs)")

st.write("""
- **KPI 1: Tasa de Crecimiento Anual de la Población:** Esta métrica calcula el porcentaje de cambio en la población de un país de un año a otro, lo que nos ayuda a entender la velocidad de crecimiento o decrecimiento de la población.

- **KPI 2: Países con Mayor Crecimiento Poblacional:** Este KPI identifica los países que experimentan el mayor crecimiento poblacional en un período específico. Nos permite identificar las áreas con un crecimiento demográfico significativo.

- **KPI 3: Crecimiento Poblacional Anual Promedio:** Esta métrica calcula el crecimiento promedio de la población de todos los países durante un período determinado, proporcionando una visión general del crecimiento demográfico global.
""")
























#############################################################################

# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import plotly.express as px
# import json


# data = pd.read_csv("data/pais-crecimiento.csv")
# data2 = pd.read_csv("data/poblacion_latam.csv", low_memory=False)
# data3 = pd.read_csv("data/poblacion-mundial-orden1.csv")

# def crecimiento_promedio_anual2(data3):
#     paises = data3['País'].unique()
#     resultados = []
#     for pais in paises:
#         data_pais = data3[data3['País'] == pais]
#         ultimo_año = data_pais['Año'].max()
#         primer_año = data_pais['Año'].min()
#         numero_de_años = ultimo_año - primer_año + 1
#         poblacion_inicial = data_pais[data_pais['Año'] == primer_año]['Población'].sum()
#         poblacion_final = data_pais[data_pais['Año'] == ultimo_año]['Población'].sum()
#         crecimiento_promedio = (poblacion_final - poblacion_inicial) / numero_de_años
#         resultados.append({'País': pais, 'Crecimiento Promedio Anual': crecimiento_promedio})
#     return pd.DataFrame(resultados)

# crecimiento_promedio_por_pais = crecimiento_promedio_anual2(data2)


# with open("data/custom.geojson", "r", encoding="utf-8") as file:
#     geojson_data = json.load(file)


# fig = px.choropleth_mapbox(data, geojson=geojson_data, color='Crecimiento Promedio Anual',
#                            locations='País', featureidkey="properties.name",
#                            mapbox_style="carto-positron", zoom=2, center={"lat": -25, "lon": -60},
#                            opacity=0.5, labels={'Crecimiento Promedio Anual': 'Crecimiento Promedio Anual (%)'})


# fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})


# st.plotly_chart(fig)

# crecimiento_anual_promedio = pd.DataFrame(crecimiento_promedio_por_pais).groupby("País")["Crecimiento Promedio Anual"].mean().reset_index()


# top_crecimiento = crecimiento_anual_promedio.sort_values(by="Crecimiento Promedio Anual", ascending=False).head(5)
# top_decrecimiento = crecimiento_anual_promedio.sort_values(by="Crecimiento Promedio Anual", ascending=True).head(5)



# fig2 = px.bar(top_decrecimiento, x='Crecimiento Promedio Anual', y='País', orientation='h',
#              title='Top 5 Países con Mayor y Menor Crecimiento Promedio Anual',
#              labels={'Crecimiento Promedio Anual': 'Crecimiento Promedio Anual (%)'},
#              color_discrete_sequence=['red'] * len(top_decrecimiento))

# fig2.add_trace(px.bar(top_crecimiento [::-1], x='Crecimiento Promedio Anual', y='País', orientation='h',
#                      color_discrete_sequence=['green'] * len(top_crecimiento)).data[0])





# st.plotly_chart(fig2)


#################################################################################

# # Configuración de página
# st.set_page_config(
#     page_title="Mi Aplicación Streamlit",
#     page_icon=":chart_with_upwards_trend:",
#     layout="wide"
# )

# # Título de la aplicación
# st.title("Análisis de Datos con Streamlit")

# # Sidebar (opcional)
# st.sidebar.header("Configuración")

# # Cargar datos desde un archivo CSV
# file_path = "data/data_label.csv"
# data = pd.read_csv(file_path)

# # Visualización de datos
# st.subheader("Exploración de Datos")

# default_rows_to_show = 5
# rows_to_show = st.number_input("Ingrese la cantidad de filas a mostrar:", min_value=1, max_value=len(data), value=default_rows_to_show)
# st.table(data.head(rows_to_show))


# # Gráfico (ejemplo con gráfico de barras)
# # Gráfico de barras con Pandas
# fig, ax = plt.subplots()
# data.plot.bar(x='Año', y='Población', xlabel='Año', ylabel='Población', title='Población por Año', rot=0, ax=ax)

# st.pyplot(fig)


# # Análisis interactivo (ejemplo con slider)
# st.subheader("Análisis Interactivo")
# selected_column = st.selectbox("Selecciona una columna:", data.columns)
# selected_data = data[selected_column]
# st.line_chart(selected_data)

# # Mapa de calor (ejemplo con seaborn)
# st.subheader("Mapa de Calor")
# correlation_matrix = data.corr()
# st.write(correlation_matrix)
# st.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=.5)

# # Otros elementos y funcionalidades según tus necesidades




