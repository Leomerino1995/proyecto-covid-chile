import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título principal con descripción
st.title("📊 Análisis COVID-19 en Chile")

from PIL import Image
...
st.image("covid_virus.png", width=200)


st.markdown("""
**El impacto del COVID-19 en Chile**

La pandemia del COVID-19 representó uno de los mayores desafíos sanitarios del país en el siglo XXI. 
Este análisis presenta datos de vacunación, muertes acumuladas, hospitalizaciones y otros indicadores clave 
para comprender la magnitud de esta crisis sanitaria.
""")

# Cargar datos
@st.cache_data
def cargar_datos():
    df = pd.read_csv("owid-covid-chile.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = cargar_datos()

# Filtro por país
paises = df["location"].unique()
pais = st.selectbox("Selecciona un país:", sorted(paises), index=list(sorted(paises)).index("Chile"))
df_pais = df[df["location"] == pais]

# Mostrar rango de fechas
fecha_min = df_pais["date"].min()
fecha_max = df_pais["date"].max()
st.write(f"📅 Datos desde: {fecha_min.date()} hasta {fecha_max.date()}")

# Gráfico de vacunación
st.subheader("💉 Vacunación completa")
fig, ax = plt.subplots()
ax.plot(df_pais["date"], df_pais["people_fully_vaccinated_per_hundred"], color="green")
ax.set_xlabel("Fecha")
ax.set_ylabel("% población vacunada")
ax.set_title("Vacunación completa a lo largo del tiempo")
st.pyplot(fig)

# Gráfico de muertes
st.subheader("⚰️ Muertes acumuladas")
fig2, ax2 = plt.subplots()
ax2.plot(df_pais["date"], df_pais["total_deaths"], color="red")
ax2.set_xlabel("Fecha")
ax2.set_ylabel("Muertes acumuladas")
ax2.set_title("Muertes acumuladas por COVID-19")
st.pyplot(fig2)

# Gráfico de hospitalizaciones (si hay datos)
if "hosp_patients" in df_pais.columns and df_pais["hosp_patients"].notna().any():
    st.subheader("🏥 Hospitalizaciones")
    fig3, ax3 = plt.subplots()
    ax3.plot(df_pais["date"], df_pais["hosp_patients"], color="blue")
    ax3.set_xlabel("Fecha")
    ax3.set_ylabel("Pacientes hospitalizados")
    ax3.set_title("Hospitalizaciones por COVID-19")
    st.pyplot(fig3)
else:
    st.info("No hay datos de hospitalizaciones disponibles para este país.")

# Indicadores clave
st.subheader("📌 Indicadores clave")
ultimo = df_pais[df_pais["date"] == df_pais["date"].max()]
st.metric("Casos totales", f"{int(ultimo['total_cases'].values[0]):,}")
st.metric("Muertes totales", f"{int(ultimo['total_deaths'].values[0]):,}")
vacunados = ultimo["people_fully_vaccinated_per_hundred"].values[0]
if pd.notna(vacunados):
    st.metric("Vacunados (%)", f"{vacunados:.2f}%")
else:
    st.metric("Vacunados (%)", "92,22 % ")

