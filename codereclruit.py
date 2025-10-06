import streamlit as st
import pandas as pd
import random
import time

# ====================================================================
# 1. DATOS DEL QUIZ (Simulación de datos alojados en GitHub)
# NOTA: En un caso real, cargarías estos datos desde un CSV/JSON de GitHub.
# ====================================================================

QUIZ_DATA = [
    {
        "id": 1,
        "question": "¿Cuál es el documento esencial que se debe generar o actualizar antes de iniciar la búsqueda de candidatos, ya que detalla las funciones, responsabilidades y requisitos de la posición?",
        "options": ["El Organigrama de la empresa", "El Plan de Capacitación Anual", "La Descripción y Análisis del Puesto", "El Contrato de Trabajo"],
        "correct_answer": "La Descripción y Análisis del Puesto"
    },
    {
        "id": 2,
        "question": "Elaborar el Perfil del Candidato Ideal a partir de la Descripción de Puesto se enfoca primordialmente en definir:",
        "options": ["El salario exacto que se ofrecerá y el horario de trabajo", "Las Competencias, Habilidades, Conocimientos y Experiencia (CHKE) requeridas", "Una lista de preguntas para la entrevista", "La lista de posibles empresas competidoras"],
        "correct_answer": "Las Competencias, Habilidades, Conocimientos y Experiencia (CHKE) requeridas"
    },
    {
        "id": 3,
        "question": "¿Qué tipo de reclutamiento tiene la ventaja principal de ser generalmente más rápido, más económico y aumentar la motivación y lealtad del personal actual?",
        "options": ["Reclutamiento Externo", "Reclutamiento de Referidos", "Reclutamiento Masivo", "Reclutamiento Interno"],
        "correct_answer": "Reclutamiento Interno"
    },
    {
        "id": 4,
        "question": "El uso de redes sociales profesionales (como LinkedIn) y bolsas de trabajo digitales (Job Boards) para la publicación de una vacante se clasifica como la fase de:",
        "options": ["Análisis de Puestos", "Selección Interna", "Reclutamiento Externo", "Inducción y Onboarding"],
        "correct_answer": "Reclutamiento Externo"
    },
    {
        "id": 5,
        "question": "Una vez recibidas las solicitudes o currículums, ¿cuál es el primer paso crítico en la fase de preselección o cribado (screening)?",
        "options": ["La entrevista por el gerente de área", "El cribado (filtrado) de Currículums Vitae (CVs) basado en los requisitos obligatorios del perfil", "La aplicación de pruebas psicométricas", "La verificación de referencias laborales"],
        "correct_answer": "El cribado (filtrado) de Currículums Vitae (CVs) basado en los requisitos obligatorios del perfil"
    },
    {
        "id": 6,
        "question": "El principal objetivo de aplicar pruebas psicométricas en la fase de selección es:",
        "options": ["Medir el nivel de conocimientos técnicos específicos del puesto", "Evaluar la personalidad, el potencial y las aptitudes del candidato", "Determinar el monto salarial que el candidato espera", "Verificar la veracidad de los datos de su currículum"],
        "correct_answer": "Evaluar la personalidad, el potencial y las aptitudes del candidato"
    },
    {
        "id": 7,
        "question": "Una entrevista estructurada donde el entrevistador pide al candidato describir una Situación, Tarea, Acción y Resultado (método STAR), busca evaluar principalmente:",
        "options": ["El coeficiente intelectual y las habilidades matemáticas del candidato", "Las Competencias conductuales o soft skills del candidato basadas en experiencias pasadas", "La capacidad del candidato para negociar su salario", "Sus conocimientos teóricos sobre la industria"],
        "correct_answer": "Las Competencias conductuales o soft skills del candidato basadas en experiencias pasadas"
    },
    {
        "id": 8,
        "question": "¿En qué momento del proceso de reclutamiento y selección es más apropiado llevar a cabo la verificación de referencias laborales de los candidatos?",
        "options": ["Antes de publicar la vacante, para validar el perfil", "Después de la(s) entrevista(s) principal(es) y antes de la oferta", "Durante la fase de reclutamiento externo masivo", "Después de que el candidato ha aceptado la oferta de trabajo"],
        "correct_answer": "Después de la(s) entrevista(s) principal(es) y antes de la oferta"
    },
    {
        "id": 9,
        "question": "¿Cuál es la función principal del Reporte de Candidatos Finalistas que se entrega al gerente que tiene la vacante?",
        "options": ["Servir como borrador del contrato de trabajo del futuro empleado", "Sintetizar la evaluación integral de los mejores candidatos para facilitar la decisión final", "Detallar el plan de capacitación para el candidato elegido", "Justificar por qué se excedió el presupuesto de reclutamiento"],
        "correct_answer": "Sintetizar la evaluación integral de los mejores candidatos para facilitar la decisión final"
    },
    {
        "id": 10,
        "question": "El indicador clave de rendimiento (KPI) llamado 'Tiempo Promedio para Cubrir la Vacante' (Time-to-Hire) mide la eficiencia de qué parte del proceso:",
        "options": ["La duración de la fase de Inducción y Onboarding", "La diferencia salarial entre lo ofrecido y lo esperado por el candidato", "Desde la aprobación de la vacante hasta que el candidato acepta la oferta (o inicia)", "La efectividad de la fuente de reclutamiento (referidos, job boards, etc.)"],
        "correct_answer": "Desde la aprobación de la vacante hasta que el candidato acepta la oferta (o inicia)"
    }
]

# ====================================================================
# 2. CONFIGURACIÓN Y FUNCIONES
# ====================================================================

# Inicializar el estado de la sesión
if 'answers' not in st.session_state:
    st.session_state.answers = {}         # Almacena {pregunta_id: respuesta_usuario}
    st.session_state.current_index = 0    # Índice de la pregunta actual
    st.session_state.quiz_data = QUIZ_DATA[:]
    random.shuffle(st.session_state.quiz_data)
    st.session_state.answered_this_turn = False # Controla si el usuario ya respondió el ítem actual

def calculate_score():
    """Calcula el puntaje final basado en las respuestas registradas."""
    score = 0
    total_questions = len(st.session_state.quiz_data)
    
    for data in st.session_state.quiz_data:
        q_id = data["id"]
        if q_id in st.session_state.answers:
            if st.session_state.answers[q_id] == data["correct_answer"]:
                score += 1
    return score, total_questions

def handle_submit(question_id, user_answer):
    """Guarda la respuesta y marca el ítem como respondido en este turno."""
    if question_id not in st.session_state.answers:
        st.session_state.answers[question_id] = user_answer
        st.session_state.answered_this_turn = True
        st.rerun() # Forzar la re-ejecución para mostrar el feedback

def handle_advance():
    """Avanza a la siguiente pregunta o termina el quiz."""
    current_index = st.session_state.current_index
    total_questions = len(st.session_state.quiz_data)
    
    if current_index < total_questions - 1:
        st.session_state.current_index += 1
        st.session_state.answered_this_turn = False # Restablecer para la nueva pregunta
    else:
        st.session_state.quiz_finished = True
        
    st.rerun()

# ====================================================================
# 3. INTERFAZ DE STREAMLIT
# ====================================================================

st.set_page_config(
    page_title="Dashboard de Práctica: Reclutamiento",
    layout="centered"
)

st.title("📝 Examen de Práctica: Proceso de Reclutamiento")
st.markdown("---")

total_questions = len(st.session_state.quiz_data)

# Condición de Finalización
if st.session_state.current_index >= total_questions:
    st.session_state.quiz_finished = True

if 'quiz_finished' in st.session_state and st.session_state.quiz_finished:
    # ------------------
    # Resultado Final
    # ------------------
    score, total_questions = calculate_score()
    score_percentage = (score / total_questions) * 100
    
    st.success("🎉 **¡Examen de Práctica Terminado!** 🎉", icon="🏆")
    st.header(f"Tu Resultado Final:")
    st.balloons()
    
    col1, col2 = st.columns([1, 1])
    col1.metric("Respuestas Correctas", f"{score} / {total_questions}")
    col2.metric("Porcentaje de Acierto", f"{score_percentage:.1f}%")

    if st.button("Reiniciar Examen"):
        # Reiniciar el estado de la sesión
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

else:
    # ------------------
    # Pregunta Actual
    # ------------------
    
    current_index = st.session_state.current_index
    question_data = st.session_state.quiz_data[current_index]
    question_id = question_data["id"]
    
    answered = question_id in st.session_state.answers
    user_selection = st.session_state.answers.get(question_id, None)

    st.subheader(f"Pregunta {current_index + 1} de {total_questions}")
    st.markdown(f"**{question_data['question']}**")

    # Mostrar opciones (Radio Buttons)
    # Se usa 'user_selection' como valor predeterminado si ya respondió para que se mantenga marcado.
    # El índice 'index' se ajusta si ya respondió. Si no ha respondido, es 0 por defecto (o None para no seleccionar nada).
    selected_option = st.radio(
        "Selecciona tu respuesta:",
        options=question_data["options"],
        index=question_data["options"].index(user_selection) if user_selection else None, 
        disabled=answered, 
        key=f"q_radio_{current_index}"
    )

    
    # ------------------
    # Botones y Feedback
    # ------------------

    # Columna para el botón de Responder
    col_submit, col_advance = st.columns([1, 1])
    
    if not answered:
        # Mostrar botón de Responder si no ha respondido
        with col_submit:
            if st.button("Responder", key=f"submit_{current_index}", disabled=not selected_option):
                handle_submit(question_id, selected_option)
    
    if answered:
        # Mostrar Feedback y Botón de Avanzar si ya respondió
        
        # Retroalimentación
        is_correct = user_selection == question_data["correct_answer"]
        if is_correct:
            st.success(f"✅ ¡Correcto! La respuesta es: **{user_selection}**.")
        else:
            st.error(f"❌ Incorrecto. Tu respuesta fue: **{user_selection}**.")
            st.info(f"La respuesta correcta era: **{question_data['correct_answer']}**.")

        # Botón Avanzar
        with col_advance:
            advance_text = "Finalizar Examen" if current_index == total_questions - 1 else "Avanzar a la Siguiente Pregunta"
            if st.button(advance_text, key=f"advance_{current_index}"):
                handle_advance()

    st.markdown("---")
    st.write(f"Progreso: **{len(st.session_state.answers)} / {total_questions}** respondidas")
