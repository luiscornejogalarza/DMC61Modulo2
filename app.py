#Librerias
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Titulo
st.set_page_config(page_title="Primer Proyecto de Portafolio Profesional - EDA - Salud Mental Adolescente", layout="wide")

#Progrmacion orientada a objetos

class DataAnalyzer:
    """Clase para procesar y analizar el dataset de salud mental."""
    def __init__(self, df):
        self.df = df
        
    def get_info_string(self):
        """Captura la salida de df.info() como un string para mostrarlo en Streamlit."""
        buffer = io.StringIO()
        self.df.info(buf=buffer)
        return buffer.getvalue()
        
    def classify_variables(self):
        """Clasifica las variables en numéricas y categóricas."""
        num_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        return num_cols, cat_cols
        
    def get_missing_summary(self):
        """Calcula el conteo y porcentaje de valores nulos."""
        missing = self.df.isnull().sum()
        pct = (missing / len(self.df)) * 100
        return pd.DataFrame({'Valores Nulos': missing, 'Porcentaje (%)': pct})

# SIde Bar

st.sidebar.title("Módulos")
opcion = st.sidebar.selectbox("Seleccione un Módulo:", 
                          ["1. Home", "2. Carga del Dataset", "3. Análisis EDA", "4. Conclusiones"])

# Home

if opcion == "1. Home":
    st.title("🧠 Proyecto Aplicado: Análisis de Salud Mental en Adolescentes")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📋 Descripción del Proyecto")
        st.write("Aplicación interactiva desarrollada para realizar un Análisis Exploratorio de Datos (EDA). El objetivo es identificar patrones entre los hábitos digitales, el descanso, la actividad física y el bienestar de los adolescentes, sin fines de diagnóstico clínico ni modelos predictivos.")
        
        st.subheader("👨‍💻 Datos del Autor")
        st.write("- **Nombre:** Luis Marco Cornejo Galarza")
        st.write("- **Especialización:** Python for Analytics")
        st.write("- **Año:** 2026")
        
    with col2:
        st.subheader("📊 Sobre el Dataset")
        st.write("El conjunto de datos `Teen_Mental_Health_Dataset.csv` cuenta con 1,200 registros y 13 variables, sin valores nulos ni duplicados. Incluye escalas de estrés, ansiedad, dependencia y rendimiento académico de jóvenes entre 13 y 19 años.")
        
        st.subheader("🛠️ Tecnologías Utilizadas")
        st.write("Python, Pandas, NumPy, Matplotlib, Seaborn y Streamlit.")
