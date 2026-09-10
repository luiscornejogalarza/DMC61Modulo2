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
        #Clase para procesar y analizar el dataset de salud mental
    def __init__(self, df):
        self.df = df
        
    def get_info_string(self):
        #Transforma df.info() como un string para mostrarlo en Streamlit
        buffer = io.StringIO()
        self.df.info(buf=buffer)
        return buffer.getvalue()
        
    def classify_variables(self):
        #Clasifica las variables en numéricas y categóricas
        num_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        return num_cols, cat_cols
        
    def get_missing_summary(self):
        #Calcula el conteo y porcentaje de valores nulos.
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
        st.write("Aplicación interactiva desarrollada para realizar un Análisis Exploratorio de Datos (EDA). El objetivo es identificar patrones entre los hábitos de los adolescentes, sin fines de diagnóstico clínico ni modelos predictivos.")
        
        st.subheader("👨‍💻 Datos del Autor")
        st.write("- **Nombre:** Luis Marco Cornejo Galarza")
        st.write("- **Especialización:** Python for Analytics - Modulo 2")
        st.write("- **Año:** 2026")
        
    with col2:
        st.subheader("📊 Sobre el Dataset")
        st.write("El conjunto de datos `Teen_Mental_Health_Dataset.csv` cuenta con 1200 registros y 13 variables, sin valores nulos ni duplicados. Incluye escalas de estrés, ansiedad, dependencia y rendimiento académico de adolecentes.")
        
        st.subheader("🛠️ Tecnologías Utilizadas")
        st.write("Python, Pandas, NumPy, Matplotlib, Seaborn y Streamlit.")

# Carga del Dataset

elif opcion == "2. Carga del Dataset":
    st.title("📂 Carga y Validación de Datos")
    
    # Widget obligatorio para cargar el archivo CSV
    archivo_subido = st.file_uploader("Sube el archivo Teen_Mental_Health_Dataset.csv", type=["csv"])
    
    if archivo_subido is not None:
        try:
            # Lectura del archivo
            df = pd.read_csv(archivo_subido)
            
            # GUARDADO EN EL ESTADO DE LA SESIÓN 
            st.session_state['dataset'] = df
            
            st.success("✅ Archivo cargado y validado correctamente.")
            
            # Division en columnas para mostrar la informacion pedida
            col_prev, col_dim = st.columns([3, 1])
            with col_prev:
                st.subheader("Vista Previa (Head)")
                st.dataframe(df.head())
            with col_dim:
                st.subheader("Dimensiones")
                st.write(f"**Filas:** {df.shape[0]}")
                st.write(f"**Columnas:** {df.shape[1]}")
                
        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")
    else:
        st.warning("⚠️ Esperando la carga del archivo CSV para habilitar el análisis.")

# Analisis Exploratorio de Datos(EDA)

elif opcion == "3. Análisis EDA":
    st.title("📈 Análisis Exploratorio de Datos (EDA)")
    
    # 6.1. Validación de Seguridad (Evitar errores si no hay archivo)
    if 'dataset' not in st.session_state:
        st.error("⚠️ Acceso denegado: Debe cargar el dataset en el 'Módulo 2' antes de iniciar el análisis.")
    else:
        # Recuperamos el dataset de la memoria y creamos el objeto de nuestra clase POO
        df = st.session_state['dataset']
        analyzer = DataAnalyzer(df)
        
        st.write("Bienvenido al panel de análisis. Navegue por las pestañas para explorar los 10 ítems requeridos.")
        
        # 6.2. Creación de las 10 pestañas exigidas por la rúbrica
        tabs = st.tabs([
            "1. Info", "2. Tipos", "3. Estadísticas", "4. Nulos", 
            "5. Dist. Numéricas", "6. Categóricas", "7. Biv(Num/Cat)", 
            "8. Biv(Cat/Cat)", "9. Dinámico", "10. Hallazgos"
        ])
        
        # Ítem 1: Información General
        with tabs[0]:
            st.header("Ítem 1: Información general del dataset")
            st.text(analyzer.get_info_string()) # Uso del método encapsulado POO
            st.info(f"Registros duplicados encontrados: {df.duplicated().sum()}")
            
        # Ítem 2: Clasificación de variables
        with tabs[1]:
            st.header("Ítem 2: Clasificación de variables")
            num_cols, cat_cols = analyzer.classify_variables() # Uso del método encapsulado POO
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Variables Numéricas ({len(num_cols)}):**")
                st.write(num_cols)
            with col2:
                st.write(f"**Variables Categóricas ({len(cat_cols)}):**")
                st.write(cat_cols)
                
        # Ítem 3: Estadísticas descriptivas
        with tabs[2]:
            st.header("Ítem 3: Estadísticas descriptivas")
            st.dataframe(df.describe())
            st.markdown("> **Interpretación técnica:** Analizando los cuartiles (25%, 50%, 75%), podemos evaluar la dispersión central de las horas de sueño y detectar si existen asimetrías importantes o valores atípicos preliminares.")
            
        # Ítem 4: Análisis de valores faltantes
        with tabs[3]:
            st.header("Ítem 4: Análisis de valores faltantes")
            st.dataframe(analyzer.get_missing_summary())
            st.success("Tal como indica el contexto del caso, el dataset tiene una calidad del 100% sin valores nulos, no se necesita aplicar técnicas de procesamiento de datos.")
            
        # Ítem 5: Distribución de variables numéricas
        with tabs[4]:
            st.header("Ítem 5: Distribución de métricas de bienestar")
            st.write("Comparación de escalas (1-10). *Nota: Fines educativos, no constituye diagnóstico clínico*.")
            fig, ax = plt.subplots(1, 3, figsize=(15, 4))
            sns.histplot(df['stress_level'], kde=True, ax=ax[0], color='crimson').set_title('Nivel de Estrés')
            sns.histplot(df['anxiety_level'], kde=True, ax=ax[1], color='darkorange').set_title('Nivel de Ansiedad')
            sns.histplot(df['addiction_level'], kde=True, ax=ax[2], color='indigo').set_title('Nivel de Dependencia')
            st.pyplot(fig)
            
        # Ítem 6: Análisis de variables categóricas
        with tabs[5]:
            st.header("Ítem 6: Análisis de variables categóricas")
            col1, col2 = st.columns(2)
            with col1:
                fig1, ax1 = plt.subplots()
                sns.countplot(data=df, x='gender', palette='Set2', ax=ax1)
                ax1.set_title("Proporción por Género")
                st.pyplot(fig1)
            with col2:
                fig2, ax2 = plt.subplots()
                sns.countplot(data=df, x='platform_usage', palette='Set3', ax=ax2)
                ax2.set_title("Uso de Plataformas")
                st.pyplot(fig2)
                
        # Ítem 7: Análisis bivariado (Numérico vs Categórico)
        with tabs[6]:
            st.header("Ítem 7: Bivariado (Numérico vs Categórico)")
            fig, ax = plt.subplots(1, 3, figsize=(18, 5))
            sns.boxplot(data=df, x='depression_label', y='daily_social_media_hours', palette='pastel', ax=ax[0])
            ax[0].set_title('RRSS vs Depresión')
            sns.boxplot(data=df, x='depression_label', y='sleep_hours', palette='pastel', ax=ax[1])
            ax[1].set_title('Sueño vs Depresión')
            sns.boxplot(data=df, x='depression_label', y='physical_activity', palette='pastel', ax=ax[2])
            ax[2].set_title('Actividad Física vs Depresión')
            st.pyplot(fig)
            
        # Ítem 8: Análisis bivariado (Categórico vs Categórico)
        with tabs[7]:
            st.header("Ítem 8: Bivariado (Categórico vs Categórico)")
            col1, col2 = st.columns(2)
            with col1:
                fig1, ax1 = plt.subplots()
                sns.countplot(data=df, x='platform_usage', hue='depression_label', palette='Set1', ax=ax1)
                ax1.set_title('Plataforma vs Depresión')
                st.pyplot(fig1)
            with col2:
                fig2, ax2 = plt.subplots()
                sns.countplot(data=df, x='social_interaction_level', hue='depression_label', palette='Set1', ax=ax2)
                ax2.set_title('Interacción Social vs Depresión')
                st.pyplot(fig2)
            
        # Ítem 9: Análisis dinámico por parámetros
        with tabs[8]:
            st.header("Ítem 9: Análisis Dinámico Interactivo")
            usar_filtros = st.checkbox("Habilitar Filtros Avanzados (Checkbox)")
            
            if usar_filtros:
                # Widgets obligatorios: slider, multiselect, selectbox
                rango_edad = st.slider("Filtrar por Edad (Slider):", int(df['age'].min()), int(df['age'].max()), (13, 19))
                generos = st.multiselect("Filtrar por Género (Multiselect):", df['gender'].unique(), default=df['gender'].unique())
                
                # Aplicar filtros al DataFrame
                df_filtrado = df[(df['age'] >= rango_edad[0]) & (df['age'] <= rango_edad[1]) & (df['gender'].isin(generos))]
                
                col_x, col_y = st.columns(2)
                with col_x:
                    var_x = st.selectbox("Variable Hábitos (Eje X):", ['daily_social_media_hours', 'screen_time_before_sleep', 'sleep_hours'])
                with col_y:
                    var_y = st.selectbox("Variable Bienestar (Eje Y):", ['stress_level', 'anxiety_level', 'addiction_level'])
                
                fig, ax = plt.subplots()
                sns.scatterplot(data=df_filtrado, x=var_x, y=var_y, hue='depression_label', palette='viridis', ax=ax)
                ax.set_title(f"Dispersión Dinámica ({len(df_filtrado)} registros filtrados)")
                st.pyplot(fig)
            else:
                st.info("👈 Seleccione el checkbox superior para desplegar los filtros.")
                
        # Ítem 10: Hallazgos Clave
        with tabs[9]:
            st.header("Ítem 10: Hallazgos Clave (Matriz de Correlación)")
            num_cols, _ = analyzer.classify_variables()
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.heatmap(df[num_cols].corr(), annot=False, cmap='coolwarm', ax=ax)
            st.pyplot(fig)
            
            st.write("### Insights Principales para Toma de Decisiones")
            st.write("- **Higiene del Sueño:** Se confirma visualmente que a mayor tiempo de pantalla antes de dormir, existe una tendencia a menores horas efectivas de sueño.")
            st.write("- **Métricas Acopladas:** Los niveles de estrés y ansiedad muestran una co-ocurrencia, sugiriendo que intervenciones preventivas deberían abordar ambos frentes.")
