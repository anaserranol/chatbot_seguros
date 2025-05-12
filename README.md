# Implementación Chatbot Seguros para Caso III: IA - Caso de negocio aplicación de IA en procesos de negocio de aseguradoras

``Grupo 47: Han Chen, David Martinez Pedroche, Juan José Montoya Lalinde, Dunia Namour Doughani, Ana Serrano Leiva, Jose Luis Sierra Peraza``

___
## Introducción al repositorio
En nuestro proyecto nos enfocamos en el desarrollo de un chatbot para tres casos de usos:
- 1.- **Atención a usuarios web**: cualquier internauta, cliente o no de la aseguradora, que accede a la página web de la aseguradora y quiere utilizar el chatbot para obtener información acerca de los productos que se ofrecen, darse de alta y otros temas relacionados con información general.
- 2.- **Soporte a clientes**: clientes que ya se han identificado en la página web de la aseguradora y que utilizan el chatbot para obtener información sobre sus productos y recomendaciones basadas en su perfil.
- 3.- **Apoyo a los empleados**: empleados de la aseguradora que utilizan el chatbot para agilizar tareas y obtener información y documentación sobre procesos o clientes.
En este repositorio nos centramos en el primer caso de uso: atención a usuarios web.

## Tecnologías utilizadas
Para esta primera aproximación al chatbot hemos utilizado:

- **Flask** (Python)
- **Pandas** para carga y manejo de datos
- **HTML / CSS / JavaScript** para el frontend
- **Ollama** para ejecutar el modelo de lenguaje (Mistral)

## Sobre el contexto y prompt utilizado
Para el contexto, hemos creado dos archivos csv y un txt:
- **seguros.csv**: csv que contiene el nombre, las caracteristicas, el tipo, las modalidades y el link al que redireccionar a los usuarios para que obtengan más información sobre los seguros que tiene nuestra aseguradora.
- **modalidad_seguros.csv**:  csv que se incluye el nombre de las diferentes modalidades que tienen los seguros y una pequeña descripción sobre ellos.
- **info_segurs.txt**: archivo de texto donde se recogen las preguntas frecuentes que pueden hacer los usuarios con sus respuestas.

El prompt que recibe el chatbot es la combinación de la pregunta del usuario y el contexto anterior, tras haber escogido la información más relevante para contestar.

## Flujo y funcionamiento del chatbot
[Usuario] 
   ├─ Introduce una pregunta
   ▼
[Frontend (HTML/JS)]
   ├─ Captura input del usuario
   ├─ Envía pregunta al backend vía AJAX (fetch/POST)
   ▼
[Flask Backend]
   ├─ Crea el contexto basado en los datos del CSV y TXT
   ├─ Prepara el prompt con el contexto
   ├─ Llama a Ollama y le pasa el prompt
   ▼
[Respuesta de Ollama (Mistral)]
   │ 
   ├─ Flask recibe la respuesta y la envía al frontend
   ▼
[Frontend]
   └─ Muestra la respuesta del chatbot en la interfaz

El usuario le realiza una pregunta al chatbot, la cual se envía al servidor Flask. Tras ello, el backend construye un prompt combinando el contexto más relevante de los datos cargados desde archivos CSV y TXT con la pregunta del usuario y se lo pasa al LLM Mistral de Ollama. Una vez Mistral tiene una respuesta, Flask recibe dicha respuesta y la envía de vuelta al navegador para mostrarse al usuario.

## Estructura del repositorio
    .
    ├── data                    # Archivos para el contexto (csv y txt)
    ├── static                  # Archivos JS y CSS
    | ├── script.js                 # Lógica de la interfaz
    | ├── style.js                  # Estilos de la interfaz
    ├── templates               # Archivo HTML
    | ├── script.js                 # Interfaz
    ├── app.py                  # Servidor Flask + lógica
    ├── README.md               # Descripción repositorio
    └── requirements.txt        # Librerías de Python que se necesitan 


## Requisitos e instalación de dependencias
- Python 3.9+
- Ollama instalado y funcionando localmente
- Mistral descargado: `ollama run mistral

```bash
pip install -r requirements.txt
```

## Links
- Mistral: https://ollama.com/library/mistral
- Descarga Ollama: https://ollama.com/download
- Inspiración seguros de Reale Seguros: https://www.reale.es/es/

## Créditos

Desarrollado por Ana Serrano Leiva, Han Chen, David Martinez Pedroche, Juan José Montoya Lalinde, Dunia Namour Doughani y Jose Luis Sierra Peraza. 

Group 47.