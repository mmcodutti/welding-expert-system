# Contenido de: soldadura.py
import streamlit as st
# --- NUEVOS IMPORTS ---
from base import DatosInspeccion, DatosProceso, calcular_tamaño_relativo
from main import ejecutar_sistema_experto # Importamos la función refactorizada
# --- FIN NUEVOS IMPORTS ---

# --- Configuración de la Página ---
st.set_page_config(layout="wide", page_title="Registro de Soldadura")

# --- Título ---
st.title("Aplicación de Registro de Inspección de Soldadura")
st.markdown("Ingrese los detalles del defecto y los parámetros del proceso de soldadura.")

# --- Sección de Defectos (Usando columnas para mejor layout) ---
st.header("1. Detalles del Defecto")

col1, col2 = st.columns(2)

with col1:
    id_soldadura = st.text_input("ID de Soldadura", help="Ingrese el identificador alfanumérico de la junta.")

with col2:
    opciones_defecto = ["Porosidad", "Discontinuidad", "Exceso de material", "Manchas"]
    tipo_defecto = st.selectbox("Tipo de Defecto", options=opciones_defecto)

st.markdown("##### Coordenadas del Defecto (en mm)")
col_x1, col_x2, col_y1, col_y2, col_area = st.columns(5) # Añadida columna para área

with col_x1:
    xmin = st.number_input("X min", min_value=0, step=1, format="%d")
with col_x2:
    xmax = st.number_input("X max", min_value=0, step=1, format="%d")
with col_y1:
    ymin = st.number_input("Y min", min_value=0, step=1, format="%d")
with col_y2:
    ymax = st.number_input("Y max", min_value=0, step=1, format="%d")

# --- CAMPO NUEVO REQUERIDO ---
with col_area:
    area_soldadura = st.number_input("Área Total (mm²)", min_value=1.0, value=10000.0, help="Área total de la soldadura usada para calcular R.")

# Confianza (slider de 0 a 1)
conf1, conf2, conf3 = st.columns(3)

with conf1:
    confianza = st.slider("Nivel de Confianza (Probabilidad)", 
                      min_value=0.0, 
                      max_value=1.0, 
                      value=0.75,
                      step=0.01)

multiples_defectos = st.checkbox("¿Existen múltiples defectos en esta ID?", value=False)

st.divider()

# --- Sección de Parámetros de Soldadura ---
st.header("2. Parámetros del Proceso de Soldadura")

col_p1, col_p2, col_p3 = st.columns(3)

with col_p1:
    opciones_gas = ["Ar+CO2", "CO2", "Helio", "C2H2", "Propano", "Butano", "Argón Puro"]
    tipo_gas = st.selectbox("Tipo de Gas", options=opciones_gas, index=opciones_gas.index("Ar+CO2"))
    
    opciones_material = ["Acero inoxidable", "Acero al carbono", "Aluminio", "Aleación de níquel", "Titanio"]
    material_base = st.selectbox("Material Base", options=opciones_material, index=opciones_material.index("Acero inoxidable"))

with col_p2:
    flujo_gas = st.slider("Flujo de Gas (l/m)", min_value=0, max_value=30, value=12, step=1)
    
    opciones_junta = ["V-groove", "Bevel groove", "Single Bevel", "Square groove", "U-groove", "J-groove"]
    tipo_junta = st.selectbox("Tipo de Junta", options=opciones_junta, index=opciones_junta.index("V-groove"))

with col_p3:
    opciones_tipo_soldadura = ["GMAW", "SMAW", "GTAW (TIG)", "FCAW", "SAW"]
    tipo_soldadura = st.selectbox("Tipo de Soldadura", options=opciones_tipo_soldadura, index=opciones_tipo_soldadura.index("GMAW"))

st.divider()

# --- LÓGICA DEL BOTÓN MODIFICADA ---
if st.button("Ejecutar Diagnóstico", type="primary"):
    
    # 1. Pre-procesar datos de inspección
    try:
        # Usamos los valores del formulario para calcular R
        R = calcular_tamaño_relativo(xmin, ymin, xmax, ymax, area_soldadura)
    except ValueError as e:
        st.error(f"Error al calcular el tamaño del defecto: {e}. Verifique las coordenadas.")
        # Detenemos la ejecución si las coordenadas no son válidas
        st.stop()

    # 2. Crear objetos de datos (como hacía main.py)
    datos_inspeccion = DatosInspeccion(
        tipo_defecto=tipo_defecto.lower(), # Los motores esperan minúsculas
        tamaño_relativo=R,
        confianza=confianza,
        multiples_defectos=multiples_defectos
    )

    datos_proceso = DatosProceso(
        tipo_gas=tipo_gas,
        flujo_gas_l_min=flujo_gas,
        material_base=material_base,
        tipo_junta=tipo_junta,
        metodo_soldadura=tipo_soldadura
    )

    # 3. Llamar al sistema experto
    st.subheader(f"Resultados del Diagnóstico para ID: {id_soldadura}")
    
    # Llamamos a la función importada de main.py
    mensajes, nivel_alcanzado = ejecutar_sistema_experto(datos_inspeccion, datos_proceso)

    # 4. Mostrar los resultados en la interfaz
    if mensajes:
        for m in mensajes:
            # Mostramos cada mensaje con un formato claro
            if "Clasificación:" in m:
                st.write(m)
            elif "Diagnóstico:" in m:
                st.info(m)
            elif "Causa probable:" in m:
                st.warning(m)
            elif "Recomendación:" in m:
                st.success(m)
        
        st.markdown(f"**Nivel de análisis alcanzado: {nivel_alcanzado}**")
    else:
        st.warning("No se identificaron reglas aplicables con los datos ingresados.")