import streamlit as st
import pandas as pd
import random
import time

# ====================================================================
# 1. DATOS DEL QUIZ
# ====================================================================

# Lista de las 10 preguntas generadas.
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
if 'answers' not in st.session_state:
    st.session_state.answers = {} # Almacena las respuestas del usuario
    st.session_state.current_index = 0
    st.session_state.quiz_data = QUIZ_DATA[:]
    random.shuffle(st.session_state.quiz_data)

def submit_answer(question_id, user_answer):
    """Guarda la respuesta del usuario, da feedback y avanza."""
    
    # 1. Registrar la respuesta y bloquear el cambio
    if question_id not in st.session_state.answers:
        st.session_state.answers[question_id] = user_answer
        
        # 2. Avanzar el índice
        if st.session_state.current_index < len(st.session_state.quiz_data) - 1:
            st.session_state.current_index += 1
        else:
            # 3. Marcar como terminado
            st.session_state.quiz_finished = True
        
        # Forzar la re-ejecución para mostrar el feedback y la siguiente pregunta
        time.sleep(0.3) 
        st.rerun()

def calculate_score():
    """Calcula el puntaje final basado en las respuestas registradas."""
    score = 0
    total_questions = len(st.session_state.quiz_data)
    
    for idx, data in enumerate(st.session_state.quiz_data):
        question_id = idx # Usamos el índice como ID simple
        if question_id in st.session_state.answers:
            if st.session_state.answers[question_id] == data["correct_answer"]:
                score += 1
    return score, total_questions

# ====================================================================
# 3. INTERFAZ DE STREAMLIT
# ====================================================================

st.set_page_config(
    page_title="Dashboard de Práctica: Reclutamiento",
    layout="centered"
)

st.title("📝 Examen de Práctica: Proceso de Reclutamiento")
st.markdown("---")

if 'quiz_finished' in st.session_state and st.session_state.quiz_finished:
    # ------------------
    # Resultado Final
    # ------------------
    score, total_questions = calculate_score()
    score_percentage = (score / total_questions) * 100
    
    st.success("🎉")
