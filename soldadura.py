import streamlit as st

# --- Configuración de la Página ---
st.set_page_config(layout="wide", page_title="Registro de Soldadura")

# --- Título ---
st.title("Aplicación de Registro de Inspección de Soldadura")
st.markdown("Ingrese los detalles del defecto y los parámetros del proceso de soldadura.")

# --- Sección de Defectos (Usando columnas para mejor layout) ---
st.header("1. Detalles del Defecto")

col1, col2 = st.columns(2)

with col1:
    # id soldadura (alfanumérico)
    id_soldadura = st.text_input("ID de Soldadura", help="Ingrese el identificador alfanumérico de la junta.")

with col2:
    # tipo de defecto (desplegable)
    opciones_defecto = ["Porosidad", "Discontinuidad", "Exceso de material", "Manchas"]
    tipo_defecto = st.selectbox("Tipo de Defecto", options=opciones_defecto)

st.markdown("##### Coordenadas del Defecto (en mm)")
col_x1, col_x2, col_y1, col_y2 = st.columns(4)

with col_x1:
    # xmin (entero)
    xmin = st.number_input("X min", min_value=0, step=1, format="%d")
with col_x2:
    # xmax (entero)
    xmax = st.number_input("X max", min_value=0, step=1, format="%d")
with col_y1:
    # ymin (entero)
    ymin = st.number_input("Y min", min_value=0, step=1, format="%d")
with col_y2:
    # ymax (entero)
    ymax = st.number_input("Y max", min_value=0, step=1, format="%d")

# Confianza (slider de 0 a 1)
conf1, conf2, conf3 = st.columns(3)

with conf1:
    confianza = st.slider("Nivel de Confianza (Probabilidad)", 
                      min_value=0.0, 
                      max_value=1.0, 
                      value=0.75,  # Un default razonable
                      step=0.01)

# multiples defectos (Selector si/no)
multiples_defectos = st.checkbox("¿Existen múltiples defectos en esta ID?", value=False)

st.divider()

# --- Sección de Parámetros de Soldadura ---
st.header("2. Parámetros del Proceso de Soldadura")

col_p1, col_p2, col_p3 = st.columns(3)

with col_p1:
    # tipo gas (desplegable)
    opciones_gas = ["Ar+CO2", "CO2", "Helio", "C2H2", "Propano", "Butano", "Argón Puro"]
    tipo_gas = st.selectbox(
        "Tipo de Gas de Protección/Combustible", 
        options=opciones_gas, 
        index=opciones_gas.index("Ar+CO2")  # Default
    )

    # material base (desplegable)
    opciones_material = ["Acero inoxidable", "Acero al carbono", "Aluminio", "Aleación de níquel", "Titanio"]
    material_base = st.selectbox(
        "Material Base", 
        options=opciones_material,
        index=opciones_material.index("Acero inoxidable")  # Default
    )

with col_p2:
    # flujo de gas (slider)
    flujo_gas = st.slider(
        "Flujo de Gas (l/m)", 
        min_value=0, 
        max_value=30, 
        value=12,  # Default
        step=1
    )

    # junta (desplegable)
    opciones_junta = ["V-groove", "Bevel groove", "Single Bevel", "Square groove", "U-groove", "J-groove"]
    tipo_junta = st.selectbox(
        "Tipo de Junta",
        options=opciones_junta,
        index=opciones_junta.index("V-groove")  # Default
    )

with col_p3:
    # tipo de soldadura (desplegable)
    opciones_tipo_soldadura = ["GMAW", "SMAW", "GTAW (TIG)", "FCAW", "SAW"]
    tipo_soldadura = st.selectbox(
        "Tipo de Soldadura",
        options=opciones_tipo_soldadura,
        index=opciones_tipo_soldadura.index("GMAW")  # Default
    )

st.divider()

# --- (Opcional) Botón para mostrar los datos ---
if st.button("Registrar Datos", type="primary"):
    
    # Recopilar todos los datos en un diccionario
    datos_registro = {
        "ID Soldadura": id_soldadura,
        "Defecto": {
            "Tipo": tipo_defecto,
            "BoundingBox_mm": {
                "xmin": xmin,
                "xmax": xmax,
                "ymin": ymin,
                "ymax": ymax
            },
            "Confianza": confianza,
            "Múltiples Defectos": multiples_defectos
        },
        "Parametros_Proceso": {
            "Tipo de Gas": tipo_gas,
            "Flujo de Gas (l/m)": flujo_gas,
            "Material Base": material_base,
            "Tipo de Junta": tipo_junta,
            "Tipo de Soldadura": tipo_soldadura
        }
    }
    
    # Mostrar los datos recopilados en formato JSON
    st.subheader("Datos Registrados:")
    st.json(datos_registro)
    st.success("¡Registro completado exitosamente!")