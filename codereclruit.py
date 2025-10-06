import streamlit as st
import pandas as pd
import random
import time

# ====================================================================
# 1. DATOS DEL QUIZ (Simulación de datos alojados en GitHub)
#
# NOTA IMPORTANTE: Para alojar los datos en GitHub, guardarías esta
# estructura en un archivo CSV o JSON y luego usarías su URL RAW
# para cargarla. Ejemplo de cómo cargar un CSV de GitHub:
# DATA_URL = "URL_RAW_DE_TU_ARCHIVO.csv"
# df = pd.read_csv(DATA_URL)
# ====================================================================

# Lista de las 10 preguntas generadas, adaptadas a una estructura de Python.
# 'question': La pregunta.
# 'options': Lista de las 4 opciones.
# 'correct_answer': La opción correcta.

QUIZ_DATA = [
    {
        "question": "¿Cuál es el documento esencial que se debe generar o actualizar antes de iniciar la búsqueda de candidatos, ya que detalla las funciones, responsabilidades y requisitos de la posición?",
        "options": ["El Organigrama de la empresa", "El Plan de Capacitación Anual", "La Descripción y Análisis del Puesto", "El Contrato de Trabajo"],
        "correct_answer": "La Descripción y Análisis del Puesto"
    },
    {
        "question": "Elaborar el Perfil del Candidato Ideal a partir de la Descripción de Puesto se enfoca primordialmente en definir:",
        "options": ["El salario exacto que se ofrecerá y el horario de trabajo", "Las Competencias, Habilidades, Conocimientos y Experiencia (CHKE) requeridas", "Una lista de preguntas para la entrevista", "La lista de posibles empresas competidoras"],
        "correct_answer": "Las Competencias, Habilidades, Conocimientos y Experiencia (CHKE) requeridas"
    },
    {
        "question": "¿Qué tipo de reclutamiento tiene la ventaja principal de ser generalmente más rápido, más económico y aumentar la motivación y lealtad del personal actual?",
        "options": ["Reclutamiento Externo", "Reclutamiento de Referidos", "Reclutamiento Masivo", "Reclutamiento Interno"],
        "correct_answer": "Reclutamiento Interno"
    },
    {
        "question": "El uso de redes sociales profesionales (como LinkedIn) y bolsas de trabajo digitales (Job Boards) para la publicación de una vacante se clasifica como la fase de:",
        "options": ["Análisis de Puestos", "Selección Interna", "Reclutamiento Externo", "Inducción y Onboarding"],
        "correct_answer": "Reclutamiento Externo"
    },
    {
        "question": "Una vez recibidas las solicitudes o currículums, ¿cuál es el primer paso crítico en la fase de preselección o cribado (screening)?",
        "options": ["La entrevista por el gerente de área", "El cribado (filtrado) de Currículums Vitae (CVs) basado en los requisitos obligatorios del perfil", "La aplicación de pruebas psicométricas", "La verificación de referencias laborales"],
        "correct_answer": "El cribado (filtrado) de Currículums Vitae (CVs) basado en los requisitos obligatorios del perfil"
    },
    {
        "question": "El principal objetivo de aplicar pruebas psicométricas en la fase de selección es:",
        "options": ["Medir el nivel de conocimientos técnicos específicos del puesto", "Evaluar la personalidad, el potencial y las aptitudes del candidato", "Determinar el monto salarial que el candidato espera", "Verificar la veracidad de los datos de su currículum"],
        "correct_answer": "Evaluar la personalidad, el potencial y las aptitudes del candidato"
    },
    {
        "question": "Una entrevista estructurada donde el entrevistador pide al candidato describir una Situación, Tarea, Acción y Resultado (método STAR), busca evaluar principalmente:",
        "options": ["El coeficiente intelectual y las habilidades matemáticas del candidato", "Las Competencias conductuales o soft skills del candidato basadas en experiencias pasadas", "La capacidad del candidato para negociar su salario", "Sus conocimientos teóricos sobre la industria"],
        "correct_answer": "Las Competencias conductuales o soft skills del candidato basadas en experiencias pasadas"
    },
    {
        "question": "¿En qué momento del proceso de reclutamiento y selección es más apropiado llevar a cabo la verificación de referencias laborales de los candidatos?",
        "options": ["Antes de publicar la vacante, para validar el perfil", "Después de la(s) entrevista(s) principal(es) y antes de la oferta", "Durante la fase de reclutamiento externo masivo", "Después de que el candidato ha aceptado la oferta de trabajo"],
        "correct_answer": "Después de la(s) entrevista(s) principal(es) y antes de la oferta"
    },
    {
        "question": "¿Cuál es la función principal del Reporte de Candidatos Finalistas que se entrega al gerente que tiene la vacante?",
        "options": ["Servir como borrador del contrato de trabajo del futuro empleado", "Sintetizar la evaluación integral de los mejores candidatos para facilitar la decisión final", "Detallar el plan de capacitación para el candidato elegido", "Justificar por qué se excedió el presupuesto de reclutamiento"],
        "correct_answer": "Sintetizar la evaluación integral de los mejores candidatos para facilitar la decisión final"
    },
    {
        "question": "El indicador clave de rendimiento (KPI) llamado 'Tiempo Promedio para Cubrir la Vacante' (Time-to-Hire) mide la eficiencia de qué parte del proceso:",
        "options": ["La duración de la fase de Inducción y Onboarding", "La diferencia salarial entre lo ofrecido y lo esperado por el candidato", "Desde la aprobación de la vacante hasta que el candidato acepta la oferta (o inicia)", "La efectividad de la fuente de reclutamiento (referidos, job boards, etc.)"],
        "correct_answer": "Desde la aprobación de la vacante hasta que el candidato acepta la oferta (o inicia)"
    }
]

# ====================================================================
# 2. CONFIGURACIÓN Y FUNCIONES
# ====================================================================

# Inicializar el estado de la sesión si aún no existe
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
    st.session_state.score = 0
    st.session_state.feedback = ""
    st.session_state.quiz_finished = False
    # Mezclamos las preguntas una sola vez al inicio
    st.session_state.quiz_data = QUIZ_DATA[:]
    random.shuffle(st.session_state.quiz_data)

def check_answer(user_answer, correct_answer):
    """Verifica la respuesta del usuario y actualiza el estado."""
    if st.session_state.quiz_finished:
        st.session_state.feedback = "El cuestionario ha finalizado. ¡Revisa tu resultado!"
        return
        
    if user_answer == correct_answer:
        st.session_state.score += 1
        st.session_state.feedback = "¡✅ **Respuesta Correcta!** Pasando a la siguiente pregunta."
        
        # Avanzar al siguiente índice
        if st.session_state.current_question_index < len(st.session_state.quiz_data) - 1:
            st.session_state.current_question_index += 1
        else:
            st.session_state.quiz_finished = True
    else:
        # Aquí se da una retroalimentación más detallada (según tu preferencia)
        st.session_state.feedback = f"❌ **Respuesta Incorrecta.** La respuesta correcta era: **{correct_answer}**. Inténtalo de nuevo."
        
    # La clave 'submitted' se usa para forzar la re-ejecución y mostrar el feedback
    st.session_state.submitted = True

# ====================================================================
# 3. INTERFAZ DE STREAMLIT
# ====================================================================

st.set_page_config(
    page_title="Dashboard de Reclutamiento Interactivo",
    layout="centered"
)

st.title("📚 Quiz Interactivo: Proceso de Reclutamiento")
st.markdown("---")

if st.session_state.quiz_finished:
    # ------------------
    # Resultado Final
    # ------------------
    total_questions = len(st.session_state.quiz_data)
    score_percentage = (st.session_state.score / total_questions) * 100
    
    st.success("🎉 **¡Cuestionario Terminado!** 🎉", icon="🏆")
    st.header(f"Tu Resultado Final:")
    st.balloons()
    
    col1, col2 = st.columns([1, 1])
    col1.metric("Respuestas Correctas", f"{st.session_state.score} / {total_questions}")
    col2.metric("Porcentaje de Acierto", f"{score_percentage:.1f}%")

    if st.button("Reiniciar Quiz"):
        # Reiniciar el estado de la sesión
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

else:
    # ------------------
    # Pregunta Actual
    # ------------------
    
    current_index = st.session_state.current_question_index
    question_data = st.session_state.quiz_data[current_index]
    
    st.subheader(f"Pregunta {current_index + 1} de {len(st.session_state.quiz_data)}")
    st.markdown(f"**{question_data['question']}**")

    # Formulario para manejar la respuesta
    with st.form(key=f"q_form_{current_index}"):
        # Las opciones del quiz
        user_choice = st.radio(
            "Selecciona tu respuesta:",
            options=question_data["options"],
            key=f"q_radio_{current_index}"
        )
        
        submit_button = st.form_submit_button("Responder")
        
        if submit_button:
            # Llamar a la función de verificación
            check_answer(user_choice, question_data["correct_answer"])

    # ------------------
    # Feedback
    # ------------------
    if st.session_state.feedback:
        if "✅" in st.session_state.feedback:
            st.success(st.session_state.feedback)
            # Limpiar el feedback para la siguiente pregunta
            st.session_state.feedback = ""
            time.sleep(0.5)
            st.rerun() # Forzar el avance de la pregunta

        elif "❌" in st.session_state.feedback:
            st.error(st.session_state.feedback)
            # Mantener el feedback hasta que se responda correctamente

    st.markdown("---")
    st.write(f"Puntaje actual: **{st.session_state.score}**")
