import nltk
import random
from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
from nltk.stem import WordNetLemmatizer
from flask_cors import CORS

nltk.download('punkt')
nltk.download('wordnet')

app = Flask(__name__)
CORS(app) 

#Entradas
palabras_clave_ayuda = ['ayuda', 'ayudarme', 'ayudame', 'ayudes','sugerencias', 'ayudar', 'consejo', 'aconsejar' 'necesito', 'necesitar', 'duda', 'asistencia', 'auxilio', 'colaboración', 'soporte', 'recomendación', 'orientación', 'asesoramiento', 'guía', 'dirección', 'apoyo', 'auxiliar', 'socorro', 'respaldo', 'alivio', 'favor', 'atención', 'intervención', 'solución', 'resolución', 'necesidad', 'necesitar', 'requerir', 'demanda', 'requerimiento', 'urgencia', 'deseo', 'búsqueda', 'consulta', 'pedir', 'solicitar', 'obtener', 'conseguir', 'alcanzar', 'obtener', 'lograr', 'encontrar', 'localizar', 'descubrir', 'identificar', 'obtener', 'brindar', 'proporcionar', 'suministrar', 'proveer', 'ofrecer', 'entregar', 'compartir', 'facilitar', 'aconsejar', 'orientar', 'dirigir', 'instruir', 'educar', 'informar', 'explicar', 'enseñar']
palabras_clave_rutina = ['rutina', 'ejercicio', 'ejercicios', 'ejercitar','rutinas', 'hábito', 'habitos', 'plan', 'programa', 'horario', 'organización', 'disciplina', 'rutinario', 'regularidad', 'diario', 'semanal', 'mensual', 'diariamente', 'semanalmente', 'mensualmente', 'automatizar', 'eficiencia', 'productividad', 'establecer', 'establecimiento', 'seguir', 'realizar', 'ejecutar', 'practicar', 'implementar', 'desarrollar', 'crear', 'mantener', 'administrar', 'gestionar', 'optimizar', 'mejorar', 'cambiar', 'adaptar', 'ajustar', 'modificar', 'controlar', 'repetir', 'seguimiento']
palabras_clave_principiantes = ['rutina para principiante', 'principiante', 'principiantes','para principiante', 'rutinas para principiantes','para principiantes','principiantes',  'programa para principiante', 'programas para principiantes', 'hábito para principiante', 'hábitos para principiantes', 'plan principiante', 'planes principiantes', 'ejercicio para principiante', 'ejercicios para principiante', 'ejercicios para principiantes', 'entrenamiento para principiante', 'entrenamientos para principiante','entrenamientos para principiantes', 'entrenamiento para principiantes']
palabras_clave_intermedios = ['rutina para intermedio', 'intermedio', 'intermedia', 'intermedias', 'intermedios','para intermedio', 'rutinas para intermedios', 'para intermedios', 'intermedios', 'programa para intermedio', 'programas para intermedios', 'hábito para intermedio', 'hábitos para intermedios', 'plan intermedio', 'planes intermedios', 'ejercicio para intermedio', 'ejercicios para intermedio', 'ejercicios para intermedios', 'entrenamiento para intermedio', 'entrenamientos para intermedio', 'entrenamientos para intermedios', 'entrenamiento para intermedios']
palabras_clave_avanzados = ['rutina para avanzado', 'avanzada', 'avanzadas', 'avanzado', 'avanzados','para avanzado', 'rutinas para avanzados', 'para avanzados', 'avanzados', 'programa para avanzado', 'programas para avanzados', 'hábito para avanzado', 'hábitos para avanzados', 'plan avanzado', 'planes avanzados', 'ejercicio para avanzado', 'ejercicios para avanzado', 'ejercicios para avanzados', 'entrenamiento para avanzado', 'entrenamientos para avanzado', 'entrenamientos para avanzados', 'entrenamiento para avanzados']
palabras_clave_fuerza = [
    'fuerza', 'entrenamiento de fuerza', 'ejercicios de fuerza', 'rutina de fuerza', 'programa de fuerza',
    'entrenamientos de fuerza', 'ejercicios para ganar fuerza', 'rutinas para ganar fuerza', 'programas para ganar fuerza',
    'entrenamiento de fuerza muscular', 'ejercicios de fortalecimiento', 'rutina de fortalecimiento', 'programa de fortalecimiento',
    'entrenamientos de resistencia', 'ejercicios para la fuerza', 'rutinas para la fuerza', 'programas para la fuerza',
    'desarrollo de fuerza', 'aumentar fuerza', 'entrenamiento de fuerza y resistencia', 'rutina de fuerza y resistencia',
    'programa de fuerza y resistencia', 'ejercicios de potencia', 'rutinas de levantamiento de pesas',
    'programas de levantamiento de pesas', 'ejercicios con pesas', 'rutinas con pesas', 'programas con pesas',
    'entrenamiento de fuerza en casa', 'ejercicios de fuerza en casa', 'rutina de fuerza en casa', 'programa de fuerza en casa',
]
palabras_clave_cardio = [
    'cardio', 'entrenamiento cardiovascular', 'ejercicios cardiovasculares', 'rutina de cardio', 'programa de cardio',
    'entrenamientos de cardio', 'ejercicios para quemar grasa', 'rutinas para quemar grasa', 'programas para quemar grasa',
    'entrenamiento de resistencia cardiovascular', 'ejercicios de alta intensidad', 'rutina de alta intensidad',
    'programa de alta intensidad', 'entrenamientos de intervalos', 'ejercicios de intervalos', 'rutinas de intervalos',
    'programas de intervalos', 'entrenamiento aeróbico', 'ejercicios aeróbicos', 'rutina aeróbica', 'programa aeróbico'
]
palabras_clave_otros = ['otras', 'otros', 'que otras', 'alternativas', 'tipo', 'opciones',
                         'mas', 'cosas', 'sobre que', 'que tipo de ayuda', 'con que mas', 
                         'como', 'sabes', 'que mas', 'como me puedes ayudar?','de que manera', 
                         'que mas', 'dime mas', 'dame mas', 'que otras cosas', 'que sabes','que puedes hacer', 
                         'que haces','que sabes hacer']


saludos = ['Hola! como te ayudo?', '¡Buen día! dime que necesitas', '¡Hola! estoy aqui']
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
periodos_de_ejercicio = {
    'Principiantes': '3-4 veces por semana',
    'Intermedios': '4-5 veces por semana',
    'Avanzados': '5-6 veces por semana'
}

retos = {
    'Livianos': ['Realizar 30 minutos de actividad cardiovascular 3 veces por semana.', 'Realizar 3 series de 10 repeticiones de sentadillas, flexiones de brazos y abdominales 3 veces por semana.', 'Realizar 3 series de 10 repeticiones de sentadillas, flexiones de brazos y abdominales 3 veces por semana.'],
    'Normales': ['Realizar 30 minutos de actividad cardiovascular 4 veces por semana.', 'Realizar 3 series de 10 repeticiones de sentadillas, flexiones de brazos y abdominales 4 veces por semana.', 'Realizar 3 series de 10 repeticiones de sentadillas, flexiones de brazos y abdominales 4 veces por semana.'],
    'Dificiles': ['Realizar 30 minutos de actividad cardiovascular 5 veces por semana.', 'Realizar 3 series de 10 repeticiones de sentadillas, flexiones de brazos y abdominales 5 veces por semana.', 'Realizar 3 series de 10 repeticiones de sentadillas, flexiones de brazos y abdominales 5 veces por semana.'],
    'Extremos': ['Realizar 30 minutos de actividad cardiovascular 6 veces por semana.', 'Realizar 3 series de 10 repeticiones de sentadillas, flexiones de brazos y abdominales 6 veces por semana.', 'Realizar 3 series de 10 repeticiones de sentadillas, flexiones de brazos y abdominales 6 veces por semana.']
}

otros = ['Puedo ayudarte con rutinas intermedias, retos livianos, normales, dificiles, hasta extremos, puedo darte rutinas de cardio o fuerza e incluso recomendarte dietas, si deseas una asesoria sobre lo que comes, aunque sigo en desarrollo ya poseo algo de conocimiento para que me digas que comes y darte algunos consejos, tu solo dime que necesitas', 'También puedo ofrecerte rutinas intermedias, desde retos livianos hasta extremos. Si buscas mejorar tu resistencia o ganar fuerza, puedo ayudarte con eso.',
    'Si estás buscando desafíos, puedo proporcionarte rutinas de diferentes niveles: livianas, normales, difíciles e incluso extremas. Cuéntame qué tipo de entrenamiento te interesa.',
    'Además de las rutinas de fuerza y cardio, también puedo brindarte recomendaciones dietéticas. Si deseas asesoramiento sobre tu alimentación, puedo darte consejos basados en mi conocimiento actual.',
    '¿Necesitas una rutina de entrenamiento? Ya sea que estés buscando una rutina de fuerza o una rutina de cardio, puedo proporcionarte opciones adaptadas a tus necesidades y nivel de habilidad.',
    'Si estás interesado en mejorar tu condición física, puedo ofrecerte rutinas de diferentes intensidades: desde principiante hasta avanzado. Además, puedo darte consejos sobre nutrición para complementar tus objetivos.',
    'No solo puedo ayudarte con rutinas de ejercicios, sino que también puedo brindarte recomendaciones personalizadas en cuanto a tu alimentación. Cuéntame tus necesidades y preferencias, y estaré encantado de ayudarte.',
    '¿Quieres llevar tu entrenamiento al siguiente nivel? Puedo ofrecerte rutinas desafiantes y efectivas, tanto para mejorar tu fuerza como para aumentar tu resistencia cardiovascular.',
    'Si estás buscando rutinas de entrenamiento personalizadas, estás en el lugar correcto. Puedo adaptar las rutinas de cardio y fuerza a tus necesidades y metas específicas.',
    'Además de las rutinas de ejercicios, puedo proporcionarte consejos prácticos sobre cómo llevar una alimentación saludable y equilibrada. Juntos, podemos trabajar en tu bienestar físico y nutricional.',
]

# momentos_de_ejercicio = {
#     'Morning': ['Si haces ejercicio por la mañana, levántate lo suficientemente temprano para terminar el desayuno al menos una hora antes de tu entrenamiento.', '']
# }

def procesar_entrada(entrada):
    lematizador = WordNetLemmatizer()
    palabras = nltk.word_tokenize(entrada)
    palabras_lematizadas = [lematizador.lemmatize(palabra) for palabra in palabras]
    
    if any(palabra in palabras_lematizadas for palabra in palabras_clave_ayuda):
        respuesta = random.choice(ayudas)
    elif 'hola' in palabras_lematizadas:
        respuesta = random.choice(saludos)
    elif any(palabra.startswith('ayud') for palabra in palabras_lematizadas):
        respuesta = random.choice(ayudas)
    elif any(palabra in palabras_lematizadas for palabra in palabras_clave_rutina):
        respuesta = random.choice(preguntas_rutinas)
    elif any(palabra in palabras_lematizadas for palabra in palabras_clave_principiantes):
        respuesta = random.choice(rutinas.get('Principiantes'))
    elif any(palabra in palabras_lematizadas for palabra in palabras_clave_intermedios):
        respuesta = random.choice(rutinas.get('Intermedios'))
    elif any(palabra in palabras_lematizadas for palabra in palabras_clave_avanzados):
        respuesta = random.choice(rutinas.get('Avanzados'))
    elif any(palabra in palabras_lematizadas for palabra in palabras_clave_fuerza):
        respuesta = random.choice(rutina_fuerza)
    elif any(palabra in palabras_lematizadas for palabra in palabras_clave_cardio):
        respuesta = random.choice(list(rutina_cardio))
    elif 'dieta' in palabras_lematizadas:
        respuesta = random.choice(preguntas_dietas)
    elif 'liviano' in palabras_lematizadas:
        respuesta = random.choice(retos.get('Livianos'))
    elif 'retos' in palabras_lematizadas and 'normales' in palabras_lematizadas:
        respuesta = random.choice(retos.get('Normales'))
    elif 'dificiles' in palabras_lematizadas:
        respuesta = random.choice(retos.get('Dificiles'))
    elif 'extremos' in palabras_lematizadas:
        respuesta = random.choice(retos.get('Extremos'))
    elif 'adiós' in palabras_lematizadas or 'chao' in palabras_lematizadas:
        respuesta = random.choice(despedidas)
    elif 'nombre' in palabras_lematizadas:
        respuesta = random.choice(nombres)
    elif any((palabra.startswith('llam') or palabra.startswith('nombr')) for palabra in palabras_lematizadas):
        respuesta = random.choice(nombres)
    elif 'recomendar' in palabras_lematizadas:
        respuesta = random.choice(sugerencias)
    elif any(palabra in palabras_lematizadas for palabra in palabras_clave_otros):
        respuesta = random.choice(otros)    
    else:
        respuesta = 'Perdon :c estoy aprendiendo aun y no entiendo lo que quieres decir, prometo mejorar <3 pero si deseas tambien una asesoria nutricional personalizada puedes escribir "nutricion personal"'
        
    return respuesta

def calcular_grasas_totales(entrada):
    alimentos = {
    'hamburguesa': 20,
    'hotdog': 15,
    'ensalada': 5,
    'papasfritas': 10,
    'pizza': 12,
    'pollofrito': 25,
    'alitasdepollo': 18,
    'sushi': 8,
    'tacos': 15,
    'chilesrellenos': 14,
    'pastel': 30,
    'helado': 10,
    'donas': 8,
    'chocolate': 15,
    'chips': 12,
    'pancakes': 10,
    'cereal': 5,
    'galletas': 7,
    'lasaña': 22,
    'polloalhorno': 8,
    'queso': 10,
    'churros': 15,
    'papasalacarta': 9,
    'pescado': 7,
    'sopa': 6,
    'sandwich': 8,
    'empanadas': 15,
    'burritos': 18,
    'tortillaespañola': 20,
    'salmón': 12,
    'arrozfrito': 14,
    'camarones': 10,
    'nachos': 15,
    'pasta': 10,
    'costillasdecerdo': 30,
    'cebiche': 5,
    'polloasado': 7,
    'ceviche': 6,
    'tamales': 15,
    'filetemignon': 20,
    'lentejas': 2,
    'guisantes': 2,
    'champiñones': 0.5,
    'sopaipillas': 12,
    'quinoa': 6,
    'ceviche': 6,
    'sopaipillas': 12,
    'gazpacho': 2,
    'ensaladilla': 5,
    'mariscos': 10,
    'tortillafrancesa': 10,
    'canelones': 15,
    'revuelto': 8,
    'carne': 10,
    'fajitas': 15,
    'mejillones': 6,
    'lomo': 12,
    'codillo': 30,
    'chorizo': 15,
    'pollo': 8,
    'solomillo': 10,
    'almejas': 7,
    'embutidos': 20,
    'morcilla': 15,
    'jamón': 15,
    'pulpo': 8,
    'bacalao': 10,
    'huevo': 5,
    'pavo': 8,
    'salchichón': 15,
    'salchicha': 12,
    'butifarra': 10,
    'conejo': 8,
    'cerdo': 20,
    'pierna': 12,
    'calamares': 10,
    'sepia': 8,
    'pulpo': 8,
    'calamar': 8,
    'espinacas': 2,
    'berenjena': 1,
    'tomate': 0.5,
    'patatas': 1,
    'zanahorias': 1,
    'calabaza': 1,
    'pepinos': 0.5,
    'lechuga': 0.5,
    'repollo': 0.5,
    'espárragos': 1,
    'pimiento': 0.5,
    'remolacha': 0.5,
    'puerro': 0.5,
    'apio': 0.5,
    'nabo': 0.5,
    'coliflor': 0.5,
    'perejil': 0.5,
    'ajo': 0.5,
    'cebolla': 0.5,
    'limón': 0.5,
    'naranja': 0.5,
    'mandarina': 0.5,
    'pera': 0.5,
    'manzana': 0.5,
    'plátano': 0.5,
    'uvas': 0.5,
    'fresas': 0.5,
    'cerezas': 0.5,
    'sandía': 0.5,
    'melón': 0.5,
    'piña': 0.5,
    'kiwi': 0.5,
    'melocotón': 0.5,
    'albaricoque': 0.5,
    'ciruela': 0.5,
    'caqui': 0.5,
    'mango': 0.5,
    'frambuesas': 0.5,
    'arándanos': 0.5,
    'granada': 0.5,
    'aceitunas': 10,
    'aguacate': 20,
    'aceite': 20,
    'mantequilla': 15,
    'mayonesa': 10,
    'salsa': 8,
    'ketchup': 5,
    'mostaza': 2,
    'azúcar': 0.5,
    'sal': 0.5,
    'harina': 0.5,
    'arroz': 0.5,
    'pan': 1,
    'avena': 1,
    'pasta': 2,
    'queso': 5,
    'yogur': 2,
    'leche': 2,
    'chocolate': 10,
    'mermelada': 5,
    'miel': 5,
    'chicle': 0.5,
    'helado': 10,
    'galletas': 5,
    'caramelos': 2,
    'refresco': 5,
    'café': 0.5,
    'té': 0.5,
    'cerveza': 5,
    'vino': 1,
    'whisky': 0.5,
    'ron': 0.5,
    'vodka': 0.5,
    'tequila': 0.5,
    'vermouth': 1,
    'sidra': 2,
    'brandy': 0.5,
    'licor': 5,
    'ginebra': 0.5,
    'campari': 0.5,
    'absenta': 0.5,
    'champagne': 1,
    'cava': 1,
    'coñac': 0.5,
    'pacharán': 0.5,
    'mezcal': 0.5,
    'orujos': 0.5,
    'tekila': 0.5,
    'aguardiente': 0.5,
    'brandy': 0.5,
    'limonada': 0.5,
    'pisco': 0.5,
    'ponche': 2,
    'sangría': 5,
    'anís': 0.5,
    'polvorones': 5,
    'tarta': 30,
    'churros': 10,
    'rosquillas': 10,
    'flan': 10,
    'natillas': 10,
    'pastel': 30,
    'bizcocho': 10,
    'chocolate': 15,
    'turrón': 10,
    'mantecados': 5,
    'goxua': 15,
    'barquillo': 5,
    'caramelos': 2,
    'gominolas': 2,
    'helado': 10,
    'galletas': 5,
    'chocolate': 10,
    'caramelos': 2,
    'pastelitos': 10,
    'polvorones': 10,
    'donuts': 8,
    'magdalenas': 8,
    'churros': 15,
    'gofres': 10,
    'rosquillas': 10,
    'tarta': 30,
    'brownie': 15,
    'muffin': 10,
    'cookies': 8,
    'cupcake': 12,
    'cheesecake': 20,
    'chocolate': 15,
    'tiramisú': 18,
    'crema': 10,
    'croissant': 8,
    'cronut': 15,
    'profiteroles': 12,
    'buñuelos': 15,
    'brazo': 12,
    'sopa': 2,
    'consomé': 2,
    'puré': 5,
    'crema': 5,
    'sopa': 2,
    'cocido': 20,
    'garbanzos': 2,
    'puchero': 18,
    'cocido': 20,
    'fabada': 18,
    'paella': 12,
    'arroz': 2,
    'pisto': 5,
    'guacamole': 10,
    'paté': 15,
    'foie': 20,
    'salmorejo': 5,
    'gazpacho': 5,
    'hummus': 8,
    'baba': 8,
    'tapenade': 5,
    'crema': 10,
    'escalivada': 5,
    'mermelada': 5,
    'aceitunas': 2,
    'salsa': 5,
    'mostaza': 2,
    'ketchup': 5,
    'mayonesa': 5,
    'tabasco': 2,
    'aji': 2,
    'salsa': 5,
    'tahini': 8,
    'salsa': 5,
    'ají': 2,
    'barbacoa': 15,
    'parrilla': 15,
    'asado': 15,
    'frito': 10,
    'cocido': 20,
    'marinado': 8,
    'horneado': 5,
    'plancha': 5,
    'gulash': 20,
    'vapor': 2,
    'a la': 0.5,
    'tandoori': 8,
    'tempura': 8,
    'wok': 5,
    'glaseado': 5,
    'ahumado': 10,
    'al': 0.5,
    'en': 0.5,
    'a': 0.5,
    'de': 0.5,
    'con': 0.5,
    'sin': 0.5,
    'y': 0.5,
    'para': 0.5,
    'sobre': 0.5,
    'entre': 0.5,
    'bajo': 0.5,
    'a': 0.5,
    'la': 0.5,
    'las': 0.5,
    'lo': 0.5,
    'los': 0.5,
    'un': 0.5,
    'una': 0.5,
    'uno': 0.5,
    'unos': 0.5,
    'unas': 0.5,
}
    
    grasas_totales = 0
    
    # Limpiar y normalizar la entrada
    entrada_procesada = entrada.lower().replace(" ", "")
    
    # Buscar palabras clave y sumar las grasas correspondientes
    for alimento, grasa in alimentos.items():
        if alimento in entrada_procesada:
            grasas_totales += grasa
    
     # Realizar la validación y proporcionar una recomendación
    if grasas_totales > 30:
        recomendacion = "Estás consumiendo demasiada grasa. Deberías moderar tu ingesta."
    elif grasas_totales < 10:
        recomendacion = "Tu ingesta de grasas está un poco baja. Considera agregar alimentos más nutritivos."
    else:
        recomendacion = "Tu ingesta de grasas está dentro de un rango saludable. ¡Sigue así!"
    
    return recomendacion

@app.route('/chatbot', methods=['POST'])
def chatbot_post():
    entrada = request.json['entrada']
    respuesta = procesar_entrada(entrada.lower())
    return jsonify({'respuesta': respuesta})

if __name__ == '__main__':
    # Obtén el número de puerto desde una variable de entorno o usa un valor predeterminado
    port = int(os.environ.get('PORT', 8085))
    # Ejecuta la aplicación en el puerto especificado
    app.run(host='0.0.0.0', port=port)