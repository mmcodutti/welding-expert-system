# Contenido de: main.py

# Importamos el nuevo hecho 'ClasificacionFact'
from EngineClasification import Clasificacion, ProcesoFact, InspeccionFact as InspeccionFactClasif, ClasificacionFact
from EngineDiagnosis import MotorDiagnostico, InspeccionFact as InspeccionFactDiag, Diagnostico
from EngineCauses import MotorCausas, DiagnosticoFact, ProcesoFact as ProcesoFactCausa, CausaProbable
# Importamos 'Recomendacion' para poder capturarla
from EngineRecomendations import MotorRecomendaciones, CausaProbableFact, Recomendacion
from base import DatosInspeccion, DatosProceso, Soldadura, calcular_tamaño_relativo

# --- FUNCIÓN PRINCIPAL REFACTORIZADA ---
# Ya no se llama main(), y recibe los datos como parámetros
def ejecutar_sistema_experto(datos_inspeccion: DatosInspeccion, datos_proceso: DatosProceso):
    
    # Extraer datos crudos de los objetos de entrada
    tipo_defecto = datos_inspeccion.tipo_defecto
    R = datos_inspeccion.tamaño_relativo
    confianza = datos_inspeccion.confianza
    multiples_defectos = datos_inspeccion.multiples_defectos
    
    flujo_gas = datos_proceso.flujo_gas_l_min
    material_base = datos_proceso.material_base
    tipo_junta = datos_proceso.tipo_junta

    # --- Lista de mensajes y nivel alcanzado ---
    # En lugar de imprimir, guardamos todo en esta lista
    mensajes = []
    nivel_alcanzado = "Inicio" # Default

    # ----- Nivel 0: Clasificación -----
    motor_clasif = Clasificacion()
    motor_clasif.reset()
    motor_clasif.declare(ProcesoFact(flujo_gas=flujo_gas))
    motor_clasif.declare(InspeccionFactClasif(R=R))
    motor_clasif.run()

    # Modificado: Capturamos los hechos 'ClasificacionFact'
    for fact in motor_clasif.facts.values():
        if isinstance(fact, ClasificacionFact):
            mensajes.append(fact['descripcion'])
            nivel_alcanzado = "Clasificación"

    # ----- Nivel 1: Diagnóstico -----
    motor_diag = MotorDiagnostico()
    motor_diag.reset()
    motor_diag.declare(InspeccionFactDiag(
        tipo_defecto=tipo_defecto,
        R=R,
        confianza=confianza,
        multiples_defectos=multiples_defectos
    ))
    motor_diag.run()

    diag_fact = None
    for fact in motor_diag.facts.values():
        if isinstance(fact, Diagnostico):
            diag_fact = fact
            # Modificado: Usamos .append() en lugar de print()
            mensajes.append(f"Diagnóstico: {fact['descripcion']}")
            nivel_alcanzado = "Diagnóstico"
            break # Asumimos un solo diagnóstico

    # ----- Nivel 2: Causa Probable -----
    causa_fact = None
    if diag_fact:
        motor_causa = MotorCausas()
        motor_causa.reset()
        motor_causa.declare(DiagnosticoFact(descripcion=diag_fact["descripcion"]))
        motor_causa.declare(ProcesoFactCausa(
            flujo_gas=flujo_gas,
            material_base=material_base,
            tipo_junta=tipo_junta
        ))
        motor_causa.run()

        for fact in motor_causa.facts.values():
            if isinstance(fact, CausaProbable):
                causa_fact = fact
                # Modificado: Usamos .append()
                mensajes.append(f"Causa probable: {fact['descripcion']}")
                nivel_alcanzado = "Causa probable"
                break # Asumimos una sola causa

    # ----- Nivel 3: Recomendación de acción -----
    if causa_fact:
        motor_reco = MotorRecomendaciones()
        motor_reco.reset()
        motor_reco.declare(CausaProbableFact(descripcion=causa_fact["descripcion"]))
        motor_reco.run()
        
        # Modificado: Capturamos los hechos 'Recomendacion'
        recomendacion_encontrada = False
        for fact in motor_reco.facts.values():
            if isinstance(fact, Recomendacion):
                mensajes.append(f"Recomendación: {fact['descripcion']}")
                recomendacion_encontrada = True
        
        if recomendacion_encontrada:
            nivel_alcanzado = "Recomendación"

    # --- Resultados finales ---
    # Devolvemos los mensajes y el nivel para que Streamlit los muestre
    return mensajes, nivel_alcanzado


# Eliminamos el bloque 'if __name__ == "__main__":' 
# ya que 'soldadura.py' será ahora el punto de entrada.