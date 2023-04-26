import nltk
import random
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('wordnet')

saludos = ['Hola!', '¡Buen día!', '¡Hola!', '¡Hola, como estas?', '¡Hola, que tal?', '¡Hola, que tal te va?']
preguntas_rutinas = ['¿Qué tipo de rutina buscas principiantes o avanzados?', '¿Quieres una rutina para principiantes o avanzados?', '¿Buscas una rutina de fuerza o de cardio?', '¿Qué tipo de rutina buscas fuerza o cardio?']
preguntas_dietas = ['¿Qué tipo de dieta buscas?', '¿Quieres una dieta vegetariana o vegana?', '¿Buscas una dieta baja en grasas o en carbohidratos?']
despedidas = ['¡Hasta luego!', '¡Adiós!', '¡Que tengas un buen día!', '¡Hasta pronto!']
ayudas = ['Como puedo ayudarte?', 'Con gusto te ayudare con lo que necesites', 'Cuentame que necesitas', '¿En que te puedo ayudar?']
nombres = ['Como modelo de aprendizaje creado por el grupo 16 aun no tengo un nombre, pero en cuanto lo tenga te lo dire']
sugerencias = ['¿Prefieres entrenamiento cardiovascular o de fuerza?', '¿Buscas una rutina de principiantes o avanzada?', '¿Quieres una rutina de fuerza o de cardio?']
consejos = ['¿Quieres una rutina de fuerza o de cardio?', '¿Quieres una rutina de principiantes o avanzada?', '¿Quieres una rutina de fuerza o de cardio?']
ejercicios = ['¿Quieres una rutina de fuerza o de cardio?', '¿Quieres una rutina de principiantes o avanzada?', '¿Quieres una rutina de fuerza o de cardio?']
rutina_fuerza = ['4 repeticiones de 10 series de sentadillas', '4 repeticiones de 10 series de press de banca', '4 repeticiones de 10 series de press militar', '4 repeticiones de 10 series de remo con barra', '4 repeticiones de 10 series de dominadas', '4 repeticiones de 10 series de press de hombros', '4 repeticiones de 10 series de press de triceps', '4 repeticiones de 10 series de press de biceps', '4 repeticiones de 10 series de press de piernas', '4 repeticiones de 10 series de press de gemelos']
rutina_cardio = {'10 minutos de bicicleta estatica', '10 minutos de caminadora', '10 minutos de eliptica', '10 minutos de remo', '10 minutos de escaladora', '10 minutos de natacion', '10 minutos de saltar la cuerda', '10 minutos de correr', '10 minutos de patinar', '10 minutos de andar en bicicleta'}
rutinas = {
    'Principiantes': ['Calentamiento: 5-10 minutos de actividad cardiovascular como saltar la cuerda, hacer jumping jacks o correr en el lugar para elevar la frecuencia cardíaca y preparar los músculos para el ejercicio.', 'Flexiones de brazos (3 series de 8-10 repeticiones): Colócate en posición de plancha con las manos colocadas a la altura de los hombros y baja el cuerpo hacia el suelo doblando los codos, manteniendo el cuerpo en línea recta, y luego vuelve a subir.', 'Sentadillas (3 series de 10-12 repeticiones): Párate con los pies separados a la altura de los hombros, baja los glúteos hacia el suelo manteniendo los talones en el suelo y el pecho levantado, y luego regresa a la posición inicial.', 'Plank (3 series de 30-60 segundos): Colócate en posición de plancha con los antebrazos apoyados en el suelo y mantén el cuerpo en línea recta, activando los músculos del núcleo y manteniendo la posición el tiempo indicado.', 'Zancadas (3 series de 10-12 repeticiones por pierna): Da un paso adelante con una pierna y baja el cuerpo doblando ambas rodillas, manteniendo el pecho levantado y luego regresa a la posición inicial. Repite con la otra pierna.', 'Abdominales (3 series de 15-20 repeticiones): Acuéstate boca arriba con las rodillas dobladas, coloca las manos detrás de la cabeza y levanta el torso hacia las rodillas, manteniendo los codos abiertos y regresando lentamente a la posición inicial.', 'Enfriamiento: 5-10 minutos de actividad cardiovascular de baja intensidad como caminar o estirar los músculos que trabajaste durante la rutina.'],
    'Intermedios': ['Calentamiento: 5-10 minutos de actividad cardiovascular como correr, saltar la cuerda o hacer bicicleta estática para elevar la frecuencia cardíaca y preparar los músculos para el ejercicio.', 'Levantamiento de pesas (3 series de 8-10 repeticiones): Puedes hacer ejercicios de levantamiento de pesas como press de banca, press de hombros, remo con mancuernas o curls de bíceps. Utiliza pesas que te desafíen pero que te permitan mantener una técnica adecuada.', 'Sentadillas con salto (3 series de 10-12 repeticiones): Párate con los pies separados a la altura de los hombros, realiza una sentadilla y luego salta explosivamente, aterrizando suavemente y repitiendo el movimiento.', 'Pull-ups o dominadas (3 series de 8-10 repeticiones): Si tienes una barra de dominadas disponible, puedes realizar este ejercicio para trabajar la parte superior del cuerpo, específicamente los músculos de la espalda y los brazos. Si no tienes una barra, puedes realizar variaciones de dominadas con bandas elásticas o con TRX.', 'Burpees (3 series de 10-12 repeticiones): Comienza en posición de cuclillas, luego coloca las manos en el suelo y salta con los pies hacia atrás para quedar en posición de plancha, realiza una flexión de brazos, salta con los pies hacia adelante y luego salta explosivamente con los brazos extendidos.', 'Russian twists (3 series de 15-20 repeticiones): Siéntate en el suelo con las piernas dobladas y los pies apoyados en el suelo, sostén una pesa con ambas manos y gira el torso de lado a lado, tocando la pesa en el suelo a cada lado.', 'Enfriamiento: 5-10 minutos de actividad cardiovascular de baja intensidad como caminar o estirar los músculos que trabajaste durante la rutina.'],
    'Avanzados': ['Calentamiento: 5-10 minutos de actividad cardiovascular como correr, saltar la cuerda o hacer bicicleta estática para elevar la frecuencia cardíaca y preparar los músculos para el ejercicio.', 'Levantamiento de pesas compuesto (4 series de 6-8 repeticiones): Puedes realizar ejercicios compuestos que involucren varios grupos musculares como sentadillas con barra, peso muerto, press de banca con barra, y dominadas con peso adicional. Utiliza cargas pesadas que te desafíen y asegúrate de utilizar una técnica adecuada.', 'Entrenamiento en circuito (3-4 rondas de 8-10 repeticiones): Puedes realizar un circuito que incluya ejercicios como burpees, saltos en caja, kettlebell swings, y remo con mancuernas, realizando cada ejercicio uno tras otro sin descanso, y descansando al final de cada ronda.', 'Ejercicios pliométricos (3 series de 8-10 repeticiones): Puedes realizar ejercicios pliométricos como saltos de caja, saltos de longitud, o saltos de altura para trabajar la explosividad y la fuerza de tus piernas.', 'Entrenamiento de core (3 series de 15-20 repeticiones): Puedes realizar ejercicios como rollouts de rueda abdominal, levantamiento de piernas en suspensión, o planchas con variaciones avanzadas para fortalecer los músculos del core.', 'Entrenamiento de alta intensidad (HIIT) (2-3 rondas de 30-45 segundos de trabajo con 15-30 segundos de descanso): Puedes realizar ejercicios de alta intensidad como sprints en intervalos, saltos de tijera, o box jumps para mejorar tu resistencia cardiovascular y quemar calorías.', 'Enfriamiento: 5-10 minutos de actividad cardiovascular de baja intensidad como caminar o estirar los músculos que trabajaste durante la rutina.']
}

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
    elif 'principiante' in palabras_lematizadas:
        respuesta = random.choice(rutinas.get('Principiantes'))
    elif 'intermedio' in palabras_lematizadas:
        respuesta = random.choice(rutinas.get('Intermedios'))
    elif 'avanzado' in palabras_lematizadas:
        respuesta = random.choice(rutinas.get('Avanzados'))
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
