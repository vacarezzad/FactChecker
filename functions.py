import os

from langchain.chains import LLMCheckerChain
from langchain.memory import SimpleMemory
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

GOOGLE_API_KEY= 'your_google_gemini_api_key'

def set_environment():
    variable_dict = globals().items()
    for key, value in variable_dict:
        if "API" in key or "ID" in key:
            os.environ[key] = value
            
            
set_environment()

class FactChecker:
    def __init__(self, model_name="gemini-1.5-pro", temperature=1):
        """
        Inicializa el FactChecker con el modelo LLM y configuración.
        
        :param model_name: Nombre del modelo LLM a utilizar.
        :param temperature: Controla la creatividad de las respuestas generadas.
        """
        # Configurar el modelo de lenguaje (LLM)
        self.llm = ChatGoogleGenerativeAI(model=model_name, temperature=temperature)

        # Definir el prompt para el chequeo de hechos
        self.template_question = PromptTemplate(
            input_variables=['checked_assertions', 'question'],
            template="""Contesta siempre en español.
                        En base a esta consulta: '{question}', debes realizar el chequeo del siguiente modo.
                        
                        1) Recolección de evidencia:
                           Haz un listado con bullets de toda la evidencia que logres recoger.
                           Idealmente cita cuál es la fuente y el autor de la evidencia.
                           Proporciona todos los detalles.
                           
                        2) Razonamiento:
                        En base a la evidencia recolectada, haz el razonamiento lógico para validar o no el hecho que se desea chequear.
                        
                        3) Respuestas:
                        Contesta en base a la evidencia recolectada y el razonamiento realizado si el hecho es cierto o no.
            """
        )
        # Crear el checker chain utilizando el LLM
        self.checker_chain = LLMCheckerChain(
            llm=self.llm,
            memory=SimpleMemory(),
            verbose=True
        )

    def run_check(self, question):
        """
        Ejecuta el chequeo de hechos con la pregunta dada.
        
        :param question: La pregunta que se desea verificar.
        :return: Resultado del chequeo de hechos.
        """
        # Formatear el prompt con la pregunta específica
        formatted_prompt = self.template_question.format(question=question)
        
        # Ejecutar la cadena de chequeo de hechos con el prompt formateado
        result = self.checker_chain.run(formatted_prompt)
        
        return result

