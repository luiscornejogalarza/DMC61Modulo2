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
