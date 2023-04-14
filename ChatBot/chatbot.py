import nltk
import random
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('wordnet')

saludos = ['Hola!', '¡Buen día!', '¡Hola!']
preguntas_rutinas = ['¿Qué tipo de rutina buscas?']
preguntas_dietas = ['¿Qué tipo de dieta buscas?', '¿Quieres una dieta vegetariana o vegana?', '¿Buscas una dieta baja en grasas o en carbohidratos?']
despedidas = ['¡Hasta luego!', '¡Adiós!', '¡Que tengas un buen día!']
ayudas = ['Como puedo ayudarte?', 'Con gusto te ayudare con lo que necesites', 'Cuentame que necesitas']
nombres = ['Como modelo de aprendizaje creado por el grupo 16 aun no tengo un nombre, pero en cuanto lo tenga te lo dire']
sugerencias = ['¿Prefieres entrenamiento cardiovascular o de fuerza?', '¿Buscas una rutina de principiantes o avanzada?']

def procesar_entrada(entrada):
    lematizador = WordNetLemmatizer()
    palabras = nltk.word_tokenize(entrada)
    palabras_lematizadas = [lematizador.lemmatize(palabra) for palabra in palabras]
    
    if 'hola' in palabras_lematizadas:
        respuesta = random.choice(saludos)
    elif 'ayuda' in palabras_lematizadas:
        respuesta = random.choice(ayudas)
    elif 'rutina' in palabras_lematizadas:
        respuesta = random.choice(preguntas_rutinas)
    elif 'dieta' in palabras_lematizadas:
        respuesta = random.choice(preguntas_dietas)
    elif 'adiós' in palabras_lematizadas or 'chao' in palabras_lematizadas:
        respuesta = random.choice(despedidas)
    elif 'nombre' in palabras_lematizadas:
        respuesta = random.choice(nombres)
    elif 'llamar' in palabras_lematizadas:
        respuesta = random.choice(nombres)
    elif 'recomendar' in palabras_lematizadas:
        respuesta = random.choice(sugerencias)
    else:
        respuesta = 'Lo siento, no entiendo lo que quieres decir.'
        
    return respuesta

while True:
    entrada = input('Tú: ')
    respuesta = procesar_entrada(entrada)
    print('Chatbot:', respuesta)
