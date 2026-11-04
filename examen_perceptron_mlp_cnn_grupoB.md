# EXAMEN TEÓRICO — PERCEPTRÓN, MLP Y CNN (GRUPO B)

**Eduardo Alcaraz**

---

## 1. Datos del alumno

| Campo  | Dato                         |
| ------ | ---------------------------- |
| Nombre | Cesar Enrique Diaz Maldonado |
| Grupo  | B                            |
| Fecha  | 03/11/2026                   |

---

## Pregunta 1 — Por qué no basta "una sola neurona"

1. Resume el funcionamiento de un perceptrón como "regla de decisión".
2. Explica la noción de _frontera lineal_ sin escribir fórmulas.
3. Da un ejemplo (aunque sea inventado) donde esa frontera _no_ alcanza.

### Respuesta

1. El perceptrón es una neurona simple que recibe varios datos y decide entre dos opciones. Cada dato pesa distinto, se juntan, y según el resultado dice "sí" o "no".

2. La frontera lineal es una línea recta que separa una clase de otra. De un lado queda una y del otro lado queda la otra.

3. No alcanza cuando los grupos están revueltos y una sola recta no los separa. Por ejemplo, si se quiere separar los días "buenos" de los "malos" según la temperatura, los buenos son los de temperatura media. Los malos son los muy fríos y los muy calientes, que quedan a los dos lados, y una sola línea no los separa.

---

## Pregunta 2 — CNN: de píxeles a mapas

1. ¿Qué problema de _estructura espacial_ ignora un MLP si aplana la foto?
2. ¿Qué significa que un mismo filtro se aplique en toda la imagen?
3. Además de clasificación de objetos, cita _dos_ usos donde la CNN encaja bien.

### Respuesta

1. Un MLP, al aplanar la foto, pierde la estructura espacial. Una imagen es una cuadrícula donde importa qué píxeles están juntos, pero al volverla una fila el MLP trata cada píxel como un dato suelto y no sabe cuáles eran vecinos.

2. Que un mismo filtro se aplique en toda la imagen significa que el filtro se va moviendo por toda la foto buscando el mismo patrón, sin importar en qué parte esté. Así se detecta ese patrón en cualquier lado y se usan menos parámetros.

3. Para detectar personas u objetos en video y para reconocimiento facial.

---

## Pregunta 3 — Softmax, clases y decisiones

1. Diferencia un problema _binario_ de uno _multiclase_ en términos de salida de la red.
2. ¿Qué lectura le das a las probabilidades que produce un softmax?
3. Imagina tres carpetas de imágenes (tres riesgos o tres animales): ¿qué arquitectura de _salida_ usarías y por qué?

### Respuesta

1. En un problema binario la salida solo tiene dos opciones posibles, así que basta con una neurona de salida. En uno multiclase hay tres o más opciones y la salida tiene una neurona por cada clase.

2. Las probabilidades del softmax indican qué tan probable cree la red que es cada clase. Todas suman 100%, así que si una sube las demás bajan, y la clase con la probabilidad más alta es la que elige la red. Es una medida de qué tan segura está, no seguro de que acierte.

3. Con tres carpetas usaría una capa de salida con 3 neuronas y softmax, una neurona por carpeta. Softmax da la probabilidad de cada una y se escoge la más alta. Sirve porque cada imagen pertenece a una sola carpeta.

---

## Pregunta 4 — MLP: profundidad con sentido

1. ¿Qué ganas al apilar capas densas con activaciones no lineales?
2. ¿Qué riesgo aparece si la red es _demasiado_ grande para tus datos?
3. Relaciona "capa oculta" con la idea de aprender representaciones intermedias (en palabras simples).

### Respuesta

2. Si la red es demasiado grande para los datos, aparece el sobreajuste: la red se aprende de memoria los ejemplos de entrenamiento en vez de aprender el patrón general. Con los datos que ya vio funciona muy bien, pero con datos nuevos no.

3. La capa oculta es una capa intermedia porque no recibe directamente los datos que se ingresan, sino lo que le pasa la capa anterior. Ahí la red va armando características cada vez más útiles, y esas son las representaciones intermedias que ayudan a tomar la decisión final.

---

## Pregunta 5 — Entrenamiento sin magia

1. Explica qué es una _época_ a nivel intuitivo.
2. ¿Hacia qué "objetivo" se mueven los pesos cuando hablamos de minimizar el error?
3. Si el learning rate es absurdo (muy grande o muy chico), ¿qué síntomas conceptuales esperarías?

### Respuesta

1. Una época es una pasada completa por todos los datos de entrenamiento, o sea, que la red ya vio todos los ejemplos una vez. Se necesitan muchas épocas porque con una sola vuelta no alcanza a aprender bien.

2. Los pesos se van moviendo para que el error sea lo más pequeño posible, es decir, que las predicciones se parezcan cada vez más a las respuestas correctas. Lo ideal es que el error sea bajo también con datos nuevos y no solo con los de entrenamiento.

3. El learning rate es el tamaño del paso con el que se ajustan los pesos. Si es muy grande, los pasos se pasan del punto que queremos. Si es muy chico, el error baja muy lento, tarda muchas épocas y puede quedarse atorado sin llegar a algo bueno. Es como bajar un cerro buscando el punto mas bajo, si vamos despacio con pasos chicos nos tardamos mucho y a veces no llegamos y si vamos muy rapido con pasos grandes, nos podemos pasar

---

## Pregunta 6 — Bloques de una CNN

Sin matemáticas, di el papel de cada pieza:

1. Kernel / filtro convolucional
2. Función de activación después de conv
3. Max pooling
4. Capa densa + softmax al final de un clasificador

### Respuesta

1. **Kernel / filtro convolucional:** es una ventanita chica que se mueve por toda la foto buscando un patrón, como bordes o formas. Sus valores son los pesos que la red va aprendiendo.

2. **Función de activación después de conv:** hace que la red pueda aprender cosas más complejas y no solo líneas rectas. Por ejemplo, ReLU deja igual los valores positivos y los negativos los vuelve cero.

3. **Max pooling:** hace la imagen más chica y se queda con lo más importante de cada zona, así quedan las características más visibles del objeto.

4. **Capa densa + softmax al final:** la capa densa junta todo lo que detectó la red para decidir. Softmax lo convierte en probabilidades que suman 100%, una por clase, y se escoge la más alta.

---

## Pregunta 7 — XOR y la historia del aprendizaje

1. ¿Por qué XOR se volvió un "contraejemplo" famoso?
2. ¿Qué elemento de un MLP permite patrones que no son una sola línea?
3. ¿En qué tipo de tabla/problema del mundo real seguirías usando algo tan simple como un perceptrón o un modelo lineal?

### Respuesta

1. XOR se volvió un contraejemplo famoso porque es un problema muy simple que el perceptrón no puede aprender. Sus datos no se pueden separar con una sola línea recta, ya que las clases quedan cruzadas, así que el perceptrón nunca converge y se queda dando resultados sin sentido.

2. Lo que permite patrones que no son una sola línea son las capas ocultas con funciones de activación no lineales. Con eso el MLP puede curvar o dividir la frontera de decisión.

3. Seguiría usando un perceptrón o modelo lineal en tablas sencillas con pocas variables numéricas donde los datos sí se pueden separar con una recta, por ejemplo predecir si un cliente compra o no según su edad e ingreso. Es rápido, barato y fácil de explicar.

---

## Pregunta 8 — De lo simple a lo abstracto en visión

1. Contrasta lo que buscan capas tempranas vs capas profundas en una CNN.
2. ¿Qué intuición da eso para _transfer learning_ (aunque no lo hayas programado)?
3. ¿Cuándo sospecharías que tu CNN es "profunda de más" para el dataset del curso?

### Respuesta

1. Las capas tempranas de una CNN buscan cosas simples y generales, como bordes, líneas y esquinas. Las capas profundas juntan esas piezas y detectan cosas más abstractas y completas, como una cara o un auto.

2. Como las primeras capas detectan cosas generales que sirven para casi cualquier imagen, se pueden reutilizar de una red ya entrenada con muchísimas imágenes y solo reentrenar las últimas capas para el problema nuevo. Así se ocupan menos datos y menos tiempo.

3. Es sospechoso cuando le va muy bien con los datos de entrenamiento pero mal con los de validación o datos nuevos osea tiene sobreajuste, o cuando tarda mucho en entrenar sin mejorar.

---

## Pregunta 9 — Análisis: matching problema → modelo

Elige _Perceptrón/lineal_ / _MLP_ / _CNN_ (una opción) y justifica en una frase:

1. Predecir "compra / no compra" con edad, ingreso y visitas a la web (columnas numéricas).
2. Detectar si hay un gato en una foto.
3. Aproximar una frontera "curva" o a trozos en datos 2D tabulares.
4. ¿CNN es la herramienta natural para predecir la siguiente palabra de un párrafo? Justifica y nombra una familia del curso más adecuada (RNN/Transformer a nivel nombre).

### Respuesta

1. **Perceptrón/lineal:** son columnas numéricas y la decisión es de dos opciones (compra o no compra), que se pueden separar con una línea recta.

2. **CNN:** una foto es una cuadrícula de píxeles y la CNN sirve para detectar patrones en imágenes.

3. **MLP:** son datos de una tabla y se necesita una frontera curva, que se logra con capas ocultas.

4. No, la CNN es para imágenes y un texto es una secuencia donde el orden de las palabras importa.

---

## Pregunta 10 — Análisis: auditoría de un equipo

Un equipo entrega un modelo "muy preciso" en su laptop y falla con datos nuevos.

1. ¿Qué diagnósticos conceptuales harías _antes_ de tocar hiperparámetros al azar?
2. Pide _dos_ evidencias que deberían mostrar en la defensa (curvas, separación train/val, ejemplos de error, etc.).
3. Redacta _tres_ preguntas tuyas para comprobar si saben cuándo usar perceptrón, MLP o CNN (distintas a las del Grupo A si las conoces).

### Respuesta

1. Antes de mover hiperparámetros, revisaría si el modelo está sobreajustado, comparando su desempeño con los datos de entrenamiento y con los de validación. Si en entrenamiento es muy alto y en validación bajo, está memorizando. También revisaría que los datos estén bien separados y que el dataset sea variado y suficiente.

2. Les pediría dos evidencias: las curvas de entrenamiento y validación por época, para ver si la validación deja de mejorar mientras el entrenamiento sigue subiendo, y resultados con datos nuevos.

3. Preguntas para el equipo:
   - ¿Por qué usaron una CNN y no un MLP? ¿Qué pasaría si aplanaran las imágenes?
   - ¿En qué caso les bastaría un perceptrón y por qué no sirve para algo como XOR?
   - Si tuvieran tres clases, ¿qué salida usarían y por qué?
