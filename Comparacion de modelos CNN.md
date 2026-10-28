# Comparación de corridas: clasificador de deportes

## Resumen

La **precisión total** es el porcentaje de fotos de prueba que la red acertó en general.

| Corrida | Qué se cambió | Precisión total | Golf (precisión / recall) | Americano (recall) | f1 (recall) |
|---|---|---|---|---|---|
| Base | Nada, es la referencia | 79.6 % | 59 % / 91 % | 40 % | 36 % |
| 40 épocas | 40 épocas en vez de 20 | 86.5 % | 78 % / 89 % | 75 % | 57 % |
| 64 filtros | 64 filtros en vez de 32 | 82.8 % | 67 % / 86 % | 61 % | 47 % |
| Dropout 0.2 | Dropout de 0.2 en vez de 0.5 | 85.6 % | 75 % / 89 % | 69 % | 60 % |
| Dos bloques de convolución | Una segunda capa de convolución | 69.2 % | 40 % / 93 % | 22 % | 2 % |
| 40 épocas + Dropout 0.2 | Las dos primeras juntas | **90.1 %** | **86 % / 94 %** | **83 %** | **69 %** |

## Corrida por corrida

- **Precisión:** cuando la red dice ese deporte, qué tan seguido acierta.
- **Recall:** de todas las fotos reales de ese deporte, cuántas encuentra.
- **F1:** un solo número que junta precisión y recall. Si uno de los dos es bajo, el F1 también baja.
- **Fotos reales:** cuántas fotos de ese deporte hay en la prueba. Es el mismo número en todos los modelos, porque el reparto de fotos es igual.
- **Exactitud total:** el porcentaje de fotos que la red acertó en general.
- **Promedio simple:** saca el promedio de los 10 deportes sin importar cuántas fotos tiene cada uno.
- **Promedio ponderado:** saca el promedio pero da más peso a los deportes con más fotos.

En la clasificación por deporte, contamos como alto lo que llega a 80 % o más.

### Base

![Gráfica de la corrida base](Imagenes%20comparacion%20CNN/modelo-base-grafica.png)

![Matriz de la corrida base](Imagenes%20comparacion%20CNN/modelo-base-matriz.png)

- La validación se queda en 0.80 y el entrenamiento llega a 0.68 sin terminar de subir. Faltó tiempo: con 20 épocas la red no alcanza a aprender lo suficiente.
- Americano y f1 casi no se detectan. Americano tiene recall de 40 %, así que 714 fotos de americano se fueron a golf.
- Golf encuentra casi todas sus fotos (recall 91 %), pero mete muchas de otros deportes (precisión 59 %).


**Reporte completo**

| Deporte | Precisión | Recall | F1 | Fotos reales |
|---|---|---|---|---|
| americano | 0.58 | 0.40 | 0.47 | 1,888 |
| basket | 0.76 | 0.88 | 0.81 | 1,712 |
| beisbol | 0.80 | 0.73 | 0.76 | 1,515 |
| boxeo | 0.90 | 0.89 | 0.89 | 1,458 |
| ciclismo | 0.96 | 0.99 | 0.97 | 1,544 |
| f1 | 0.77 | 0.36 | 0.49 | 1,019 |
| futbol | 0.89 | 0.82 | 0.85 | 1,522 |
| golf | 0.59 | 0.91 | 0.72 | 1,988 |
| natación | 0.92 | 0.92 | 0.92 | 1,009 |
| tenis | 0.97 | 1.00 | 0.99 | 1,771 |
| **Exactitud total** | | | 0.80 | 15,426 |
| Promedio simple | 0.81 | 0.79 | 0.79 | 15,426 |
| Promedio ponderado | 0.80 | 0.80 | 0.79 | 15,426 |

**Clasificación por deporte:**

- **Alta precisión y alto recall:** boxeo, ciclismo, futbol, natación, tenis
- **Alta precisión y bajo recall:** ninguno
- **Baja precisión y alto recall:** basket, golf
- **Baja precisión y bajo recall:** americano, beisbol, f1


### 40 épocas

![Gráfica de la corrida de 40 épocas](Imagenes%20comparacion%20CNN/modelo-40-epocas-grafica.png)

![Matriz de la corrida de 40 épocas](Imagenes%20comparacion%20CNN/modelo-40-epocas-matriz.png)

- Las dos líneas siguen subiendo al final, así que más tiempo sí ayudó. Pasó de 79.6 % a 86.5 %.
- Americano mejoró mucho: su recall subió de 40 % a 75 %. Aun así, 180 fotos de americano siguen cayendo en golf.
- f1 sigue débil, con recall de 57 %.


**Reporte completo**

| Deporte | Precisión | Recall | F1 | Fotos reales |
|---|---|---|---|---|
| americano | 0.68 | 0.75 | 0.71 | 1,888 |
| basket | 0.91 | 0.90 | 0.91 | 1,712 |
| beisbol | 0.81 | 0.77 | 0.79 | 1,515 |
| boxeo | 0.92 | 0.92 | 0.92 | 1,458 |
| ciclismo | 0.98 | 0.99 | 0.98 | 1,544 |
| f1 | 0.76 | 0.57 | 0.65 | 1,019 |
| futbol | 0.94 | 0.85 | 0.89 | 1,522 |
| golf | 0.78 | 0.89 | 0.83 | 1,988 |
| natación | 0.94 | 0.94 | 0.94 | 1,009 |
| tenis | 0.99 | 1.00 | 0.99 | 1,771 |
| **Exactitud total** | | | 0.87 | 15,426 |
| Promedio simple | 0.87 | 0.86 | 0.86 | 15,426 |
| Promedio ponderado | 0.87 | 0.87 | 0.86 | 15,426 |

**Clasificación por deporte:**

- **Alta precisión y alto recall:** basket, boxeo, ciclismo, futbol, natación, tenis
- **Alta precisión y bajo recall:** beisbol
- **Baja precisión y alto recall:** golf
- **Baja precisión y bajo recall:** americano, f1


### 64 filtros

![Gráfica de la corrida de 64 filtros](Imagenes%20comparacion%20CNN/modelo-64-filtros-grafica.png)

![Matriz de la corrida de 64 filtros](Imagenes%20comparacion%20CNN/modelo-64-filtros-matriz.png)

- Casi igual que la base: 82.8 %.
- La confusión americano-golf sigue ahí, con 396 fotos.
- Más filtros no resolvieron el problema y la red tarda más.


**Reporte completo**

| Deporte | Precisión | Recall | F1 | Fotos reales |
|---|---|---|---|---|
| americano | 0.67 | 0.61 | 0.64 | 1,888 |
| basket | 0.82 | 0.83 | 0.83 | 1,712 |
| beisbol | 0.81 | 0.79 | 0.80 | 1,515 |
| boxeo | 0.87 | 0.91 | 0.89 | 1,458 |
| ciclismo | 0.96 | 0.99 | 0.98 | 1,544 |
| f1 | 0.81 | 0.47 | 0.60 | 1,019 |
| futbol | 0.89 | 0.82 | 0.85 | 1,522 |
| golf | 0.67 | 0.86 | 0.75 | 1,988 |
| natación | 0.92 | 0.92 | 0.92 | 1,009 |
| tenis | 0.97 | 1.00 | 0.99 | 1,771 |
| **Exactitud total** | | | 0.83 | 15,426 |
| Promedio simple | 0.84 | 0.82 | 0.82 | 15,426 |
| Promedio ponderado | 0.83 | 0.83 | 0.82 | 15,426 |

**Clasificación por deporte:**

- **Alta precisión y alto recall:** basket, boxeo, ciclismo, futbol, natación, tenis
- **Alta precisión y bajo recall:** beisbol, f1
- **Baja precisión y alto recall:** golf
- **Baja precisión y bajo recall:** americano


### Dropout 0.2

![Gráfica de la corrida con Dropout 0.2](Imagenes%20comparacion%20CNN/modelo-dropout-02-grafica.png)

![Matriz de la corrida con Dropout 0.2](Imagenes%20comparacion%20CNN/modelo-dropout-02-matriz.png)

- La distancia entre entrenamiento y validación se hizo más chica (0.79 contra 0.85). Con menos neuronas apagadas, la red aprende más.
- Pasó a 85.6 %. Americano subió a recall de 69 % y f1 a 60 %.
- Todavía hay 252 fotos de americano que caen en golf.


**Reporte completo**

| Deporte | Precisión | Recall | F1 | Fotos reales |
|---|---|---|---|---|
| americano | 0.72 | 0.69 | 0.71 | 1,888 |
| basket | 0.87 | 0.87 | 0.87 | 1,712 |
| beisbol | 0.79 | 0.79 | 0.79 | 1,515 |
| boxeo | 0.92 | 0.91 | 0.92 | 1,458 |
| ciclismo | 0.97 | 0.99 | 0.98 | 1,544 |
| f1 | 0.74 | 0.60 | 0.66 | 1,019 |
| futbol | 0.92 | 0.84 | 0.88 | 1,522 |
| golf | 0.75 | 0.89 | 0.82 | 1,988 |
| natación | 0.93 | 0.92 | 0.92 | 1,009 |
| tenis | 0.99 | 1.00 | 0.99 | 1,771 |
| **Exactitud total** | | | 0.86 | 15,426 |
| Promedio simple | 0.86 | 0.85 | 0.85 | 15,426 |
| Promedio ponderado | 0.86 | 0.86 | 0.86 | 15,426 |

**Clasificación por deporte:**

- **Alta precisión y alto recall:** basket, boxeo, ciclismo, futbol, natación, tenis
- **Alta precisión y bajo recall:** ninguno
- **Baja precisión y alto recall:** golf
- **Baja precisión y bajo recall:** americano, beisbol, f1


### Dos bloques de convolución

![Gráfica de la corrida de dos bloques](Imagenes%20comparacion%20CNN/modelo-dos-bloques-grafica.png)

![Matriz de la corrida de dos bloques](Imagenes%20comparacion%20CNN/modelo-dos-bloques-matriz.png)

- Esta fue la que más me sorprendió: empeoró a 69.2 %.
- f1 casi no se detecta (recall de 2 %). Golf se come muchas fotos de otros deportes: 1,098 de americano, 643 de f1, 516 de beisbol y 347 de futbol.
- Las dos líneas siguen subiendo al final, así que la red no alcanzó a aprender en 20 épocas. Puede que el problema sea el poco tiempo, o que con fotos tan chiquitas, después de dos reducciones, quede muy poca información. Para saberlo hay que probarla con más épocas.


**Reporte completo**

| Deporte | Precisión | Recall | F1 | Fotos reales |
|---|---|---|---|---|
| americano | 0.54 | 0.22 | 0.32 | 1,888 |
| basket | 0.66 | 0.79 | 0.71 | 1,712 |
| beisbol | 0.78 | 0.43 | 0.56 | 1,515 |
| boxeo | 0.93 | 0.82 | 0.87 | 1,458 |
| ciclismo | 0.93 | 0.98 | 0.95 | 1,544 |
| f1 | 0.92 | 0.02 | 0.05 | 1,019 |
| futbol | 0.80 | 0.65 | 0.72 | 1,522 |
| golf | 0.40 | 0.93 | 0.56 | 1,988 |
| natación | 0.90 | 0.91 | 0.90 | 1,009 |
| tenis | 0.91 | 1.00 | 0.95 | 1,771 |
| **Exactitud total** | | | 0.69 | 15,426 |
| Promedio simple | 0.78 | 0.68 | 0.66 | 15,426 |
| Promedio ponderado | 0.75 | 0.69 | 0.66 | 15,426 |

**Clasificación por deporte:**

- **Alta precisión y alto recall:** boxeo, ciclismo, natación, tenis
- **Alta precisión y bajo recall:** f1
- **Baja precisión y alto recall:** golf
- **Baja precisión y bajo recall:** americano, basket, beisbol, futbol


### 40 épocas + Dropout 0.2

![Gráfica de la corrida final](Imagenes%20comparacion%20CNN/modelo-40-epocas-dropout-02-grafica.png)

![Matriz de la corrida final](Imagenes%20comparacion%20CNN/modelo-40-epocas-dropout-02-matriz.png)

- Es la mejor: 90.1 %. Las dos líneas suben juntas hasta llegar a 0.86 y 0.90.
- Golf tiene precisión de 86 % y recall de 94 %, así que la red lo maneja bien.
- Americano tiene recall de 83 %, pero precisión de 72 %. Eso quiere decir que f1 (177 fotos) y beisbol (132) se van a americano.
- f1 sigue siendo el más débil, con recall de 69 %. Es también el deporte con menos fotos en el dataset (unas 5 mil contra casi 10 mil de golf), así que ahí puede estar parte del problema.


**Reporte completo**

| Deporte | Precisión | Recall | F1 | Fotos reales |
|---|---|---|---|---|
| americano | 0.72 | 0.83 | 0.77 | 1,888 |
| basket | 0.93 | 0.91 | 0.92 | 1,712 |
| beisbol | 0.88 | 0.82 | 0.85 | 1,515 |
| boxeo | 0.94 | 0.95 | 0.95 | 1,458 |
| ciclismo | 0.99 | 0.99 | 0.99 | 1,544 |
| f1 | 0.85 | 0.69 | 0.76 | 1,019 |
| futbol | 0.95 | 0.87 | 0.91 | 1,522 |
| golf | 0.86 | 0.94 | 0.89 | 1,988 |
| natación | 0.98 | 0.95 | 0.96 | 1,009 |
| tenis | 0.99 | 1.00 | 1.00 | 1,771 |
| **Exactitud total** | | | 0.90 | 15,426 |
| Promedio simple | 0.91 | 0.89 | 0.90 | 15,426 |
| Promedio ponderado | 0.91 | 0.90 | 0.90 | 15,426 |

**Clasificación por deporte:**

- **Alta precisión y alto recall:** basket, beisbol, boxeo, ciclismo, futbol, golf, natación, tenis
- **Alta precisión y bajo recall:** f1
- **Baja precisión y alto recall:** americano
- **Baja precisión y bajo recall:** ninguno


## Comparación: qué mejoró y qué empeoró

- **Más épocas** mejoró casi siempre, porque la red todavía estaba aprendiendo. El costo es que tarda el doble.
- **Menos Dropout** también mejoró, porque la red no apaga tantas neuronas. No probamos qué pasa si lo bajamos mucho más, así que habría que vigilar que no empiece a memorizar.
- **Más filtros** casi no mejoró y tarda más. No vale la pena con estos datos.
- **Dos bloques** empeoró en 20 épocas, y es la peor de todas. Puede que mejore con más tiempo, pero no lo confirmamos.
- **Más épocas y menos Dropout juntos** fueron lo mejor. Se complementan: la red tiene más tiempo para aprender y no se le apagan tantas neuronas.

En resumen: el tiempo de entrenamiento fue lo que más ayudó. Los cambios de arquitectura (más filtros, más capas) no mejoraron nada si no se le da tiempo a la red.

## Qué podemos mejorar

- Probar la corrida de dos bloques con más épocas (60 u 80) para ver si el empeoramiento era solo falta de tiempo.
- Revisar si hay fotos repetidas entre el entrenamiento y la prueba. Un resultado de 90 % puede estar inflado si la misma foto aparece en los dos lados.
- Conseguir más fotos de f1, o equilibrar los deportes, porque es el que tiene menos fotos y el que peor se detecta.
- Usar fotos más grandes. Con 21 × 28 píxeles se pierde mucho detalle.
- Probar aumentar las fotos con giros o recortes, para que la red vea más variedad sin tener que conseguir fotos nuevas.
