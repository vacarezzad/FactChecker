
import streamlit as st

from functions import FactChecker


def main():
    st.set_page_config(page_title="Chat de Chequeo de Hechos", page_icon="🔍")

    if 'history' not in st.session_state:
        st.session_state.history = []



    st.title("Chat de Chequeo de Hechos")
    st.markdown("""
    Bienvenido al **Chat de Chequeo de Hechos**. Aquí puedes verificar la veracidad de afirmaciones 
    ingresando una pregunta y ajustando la temperatura del modelo.
    """)

    # Botón para limpiar el historial en la parte superior
    if st.button("Limpiar Historial"):
        st.session_state.history = []
        st.experimental_rerun()

    # Crear una barra lateral para ajustar la temperatura
    temperature = st.sidebar.slider(
        "Selecciona la temperatura del modelo:",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.1
    )
    
    # Área de entrada de texto para la pregunta
    question = st.text_input(
        "Introduce tu pregunta aquí:", 
        placeholder="¿Cuál es la capital de Francia?"
    )

    # Botón para ejecutar el chequeo de hechos
    if st.button("Chequear Hecho"):
        if question:
            # Mostrar la barra de progreso
            progress_bar = st.progress(0)
            
            # Actualizar la barra de progreso mientras se realiza el chequeo
            with st.spinner('Chequeando...'):
                # Crear una instancia de FactChecker con la temperatura seleccionada
                fact_checker = FactChecker(temperature=temperature)
                
                # Simular progreso
                for percent_complete in range(0, 100, 10):
                    progress_bar.progress(percent_complete)
                
                # Ejecutar el chequeo de hechos
                result = fact_checker.run_check(question)
                
                # Actualizar la barra de progreso al 100%
                progress_bar.progress(100)
                
                # Guardar la pregunta y el resultado en el historial
                st.session_state.history.append({"question": question, "result": result})

    # Mostrar el historial de chat
    if st.session_state.history:
        st.markdown("### Historial de Consultas:")
        for entry in st.session_state.history:
            st.write(f"**Pregunta:** {entry['question']}")
            st.write(f"**Resultado:** {entry['result']}")
            st.write("---")

if __name__ == "__main__":
    main()