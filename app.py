from flask import Flask, request, render_template, jsonify
import pandas as pd
import subprocess
import os
import time

app = Flask(__name__)

df_seguros = pd.read_csv('data/seguros.csv', sep=";")
df_modalidades = pd.read_csv("data/modalidad_seguros.csv", sep=';')
faq_file = "data/info_segurs.txt"

# Crear diccionario: modalidad -> descripción
desc_modalidades = dict(zip(df_modalidades['modalidad'], df_modalidades['descripcion']))

def cargar_faq():
    faqs = {}
    if not os.path.exists(faq_file):
        return faqs
    with open(faq_file, "r", encoding="utf-8") as file:
        content = file.read().strip().split("\n\n")
        for faq in content:
            if "\n" in faq:
                pregunta, respuesta = faq.split("\n", 1)
                faqs[pregunta.strip().lower()] = respuesta.strip()
    return faqs

faq_dict = cargar_faq()

def obtener_respuesta_faq(pregunta):
    if not pregunta:
        return None
    pregunta = pregunta.lower().strip()
    return faq_dict.get(pregunta, None)

def construir_contexto2(pregunta_usuario):
    seguros = ""
    modalidades_texto = ""
    respuesta_faq = ""
    saludos = ["hola", "buenas", "buenos días", "buenas tardes", "buenas noches"]
    respuesta_saludos = ""
    
    # Normalizamos la pregunta del usuario a minúsculas para hacer una comparación más flexible
    pregunta_usuario = pregunta_usuario.lower()
    
    if pregunta_usuario in saludos:
        respuesta_saludos = "Saluda de vuelta y pregunta en cómo podemos ayudar"
    
    # Verificamos si la pregunta está relacionada con los seguros
    if "seguro" in pregunta_usuario or "seguros" in pregunta_usuario:
        # Si la pregunta es sobre los seguros, responder solo con los tipos de seguro
        if "modalidades" not in pregunta_usuario:  # Si no se menciona modalidades
            seguros = "\n".join([f"- {row['seguro']}" for _, row in df_seguros.iterrows()])
        
        # Si la pregunta menciona modalidades, devolver solo las modalidades del seguro mencionado
        elif "modalidades" in pregunta_usuario:
            for _, row in df_seguros.iterrows():
                if row['seguro'].lower() in pregunta_usuario:
                    modalidades = row['modalidades'].split(",")  # Asumimos que las modalidades están separadas por coma
                    modalidades_texto = "\n".join([f"- {modalidad.strip()}" for modalidad in modalidades])
                    break
            else:
                modalidades_texto = "No se ha encontrado el seguro mencionado."

        # Si se menciona un seguro específico, devolver toda la información
        for _, row in df_seguros.iterrows():
            if row['seguro'].lower() in pregunta_usuario:
                modalidades_lista = [m.strip() for m in row['modalidades'].split(',')]
                modalidades_texto = ""
                for modalidad in modalidades_lista:
                    descripcion = desc_modalidades.get(modalidad, "Descripción no disponible.")
                    modalidades_texto += f"\n   - {modalidad}: {descripcion}"
                
                seguros += (
                    f"- {row['seguro']} ({row['tipo']}): {row['caracteristicas']}\n"
                    f"  Modalidades disponibles:{modalidades_texto}\n"
                    f"  Más información: {row['mas_info']}\n\n"
                )
                break  # Si encontramos el seguro, no necesitamos seguir buscando más

    return f"""Responde solo con la siguiente información:

== SEGUROS DISPONIBLES ==
{seguros}

== MODALIDADES DEL SEGURO ==
{modalidades_texto}

== INFORMACIÓN DE LA ASEGURADORA ==
{respuesta_faq}

== SALUDOS ==
{respuesta_saludos}
"""

def construir_contexto(pregunta_usuario):
    """
    Construye el contexto según la pregunta del usuario, devolviendo solo la información relevante.
    """
    saludos = ["hola", "buenas", "buenos días", "buenas tardes", "buenas noches"]
    pregunta_usuario = pregunta_usuario.lower().strip()

    if pregunta_usuario in saludos:
        return f"Saluda de vuelta y pregunta en cómo podemos ayudar"
    # Si el usuario pregunta por los seguros disponibles
    if "seguros" in pregunta_usuario or "qué seguros" in pregunta_usuario:
        # Solo devolvemos los nombres de los seguros
        seguros_lista = [row['seguro'] for _, row in df_seguros.iterrows()]
        return f"Estos son los seguros disponibles: {', '.join(seguros_lista)}."
    
        # Si el usuario pregunta específicamente sobre una modalidad, mostrar la modalidad correspondiente
    if "modalidades" in pregunta_usuario or "modalidad" in pregunta_usuario:
        for _, row in df_seguros.iterrows():
            if row['seguro'].lower() in pregunta_usuario:
                modalidades_lista = [m.strip() for m in row['modalidades'].split(',')]
                modalidades_texto = ""
                for modalidad in modalidades_lista:
                    # Buscar la descripción de cada modalidad en df_modalidades
                    modalidad_desc = df_modalidades[df_modalidades['modalidad'] == modalidad.strip()]
                    if not modalidad_desc.empty:
                        descripcion = modalidad_desc.iloc[0]['descripcion']
                        modalidades_texto += f"\n   - {modalidad}: {descripcion}"
                return f"Las modalidades disponibles para el seguro {row['seguro']} son:{modalidades_texto}"

    # Si el usuario pregunta por modalidades de un seguro específico
    for _, row in df_seguros.iterrows():
        if row['seguro'].lower() in pregunta_usuario:
            modalidades_lista = [m.strip() for m in row['modalidades'].split(',')]
            modalidades_texto = ""
            for modalidad in modalidades_lista:
                # Buscar la descripción de cada modalidad en df_modalidades
                modalidad_desc = df_modalidades[df_modalidades['modalidad'] == modalidad.strip()]
                if not modalidad_desc.empty:
                    descripcion = modalidad_desc.iloc[0]['descripcion']
                    modalidades_texto += f"\n   - {modalidad}: {descripcion}"

            return (f"Seguro: {row['seguro']} ({row['tipo']})\n"
                    f"Características: {row['caracteristicas']}\n"
                    f"Modalidades disponibles:{modalidades_texto}\n"
                    f"Más información: {row['mas_info']}")

    # Si no hay información disponible, devolver un mensaje genérico
    return False


def preguntar_ollama(pregunta, contexto):
    prompt = f"""{contexto}

Pregunta del usuario: {pregunta}
Respuesta:"""

    result = subprocess.run(
        ['ollama', 'run', 'mistral'],
        input=prompt.encode('utf-8'),
        stdout=subprocess.PIPE
    )

    output = result.stdout.decode('utf-8')
    return output.strip()

@app.route('/')
def index():
    return render_template('index.html', saludo="¡Buenas! ¿Cómo podría ayudarte?")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    pregunta = data.get('message')
    
    respuesta = ""
    
    respuesta_faq = obtener_respuesta_faq(pregunta)
    contexto = construir_contexto(pregunta)
    if respuesta_faq:
        time.sleep(4)
        respuesta = respuesta_faq
    
    elif contexto:
        respuesta = preguntar_ollama(pregunta, contexto)
        print(respuesta)
    else:
        time.sleep(4)
        respuesta = """Lo siento, no encontré información relacionada con esa pregunta, 
        pero puedes ponerte en contacto con nosotros a través de seguros-ms@managementsolutions.com o llamarnos al 123 456 789.
        ¿Te puedo ayudar con algo más?"""
    return jsonify({'reply': respuesta})

if __name__ == '__main__':
    app.run(debug=True)
