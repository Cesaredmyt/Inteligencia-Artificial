### P1 — ¿Morirá en el siguiente frame?

**Una fila = un frame de una partida.**

#### Variable objetivo (Y)

- **Nombre:** `muere_siguiente`
- **Tipo:** binaria → `1` = muere en el siguiente frame, `0` = no muere.
- **Cómo se obtiene:** no viene tal cual en la telemetría, hay que construirla. La Y del frame *t* es el `died` del frame *t+1*, siempre dentro de la misma sesión.

Ejemplo con la sesión que termina en el frame 82:

| frame | died | muere_siguiente (Y) |
|---|---|---|
| 80 | 0 | 0 |
| 81 | 0 | **1** ← en el 82 muere |
| 82 | 1 | — (no hay frame siguiente, se descarta) |

Nota: La Y habla del **siguiente** frame, no del actual. Si se marcara el frame del choque, el modelo solo aprendería a reconocer un choque que ya pasó.

#### Variables de entrada (X)

Solo entran columnas que se conocen **en ese mismo frame**.

| Variable | Tipo | Por qué se pide |
|---|---|---|
| `dist_obstacle` | numérica | Entre más cerca está el obstáculo, menos margen hay para esquivarlo. |
| `obstacle_type` | categórica | No se esquiva igual un cactus (se salta) que un pájaro (a veces toca agacharse). |
| `speed` | numérica | Con la misma distancia, a más velocidad hay menos tiempo para reaccionar. |
| `dino_state` | categórica | Corriendo, saltando o agachado. Si ya va en el aire, el riesgo cambia. |
| `dino_height` | numérica | Dice si el dino está a la altura del obstáculo o por encima. |
| `reaction_ms` | numérica | El tiempo de reacción o lag del jugador influye en si alcanza a responder. |

#### Granularidad

- Se necesita **cada frame**. A un frame cada 16 ms, son unos **62 frames por segundo** (1000 ÷ 16).
- Un salto dura decenas de frames, y todo se decide en muy poco tiempo.
- Si se guardara un frame de cada 40, muy probablemente se perdería justo el frame antes de morir, que es el que más importa.

#### Tamaño mínimo

El tamaño no se mide en frames, sino en **muertes**: el dino muere una sola vez por partida, así que **cada partida aporta una sola fila con Y = 1**. Por ejemplo, 12 000 frames de 50 partidas son apenas 50 muertes.

**Cálculo paso a paso:**
s
| Paso | Cálculo | Resultado |
|---|---|---|
| 1. Entradas de la neurona | 4 numéricas + 3 columnas 0/1 de `dino_state` + 4 columnas 0/1 de `obstacle_type` | 11 pesos |
| 2. Parámetros a aprender | 11 pesos + 1 bias | **12 parámetros** |
| 3. Muertes para entrenar | Regla práctica: ~10 muertes por parámetro → 10 × 12 | **120 muertes** |
| 4. Partidas totales | Se reserva el 20% para prueba, así que solo entrena el 80% → 120 ÷ 0.8 | **150 partidas** |
| 5. Reparto | 80% entrenamiento / 20% prueba | 120 partidas / 30 partidas |

Notas del cálculo:

- Las variables categóricas entran como **una columna 0/1 por cada valor** (por ejemplo, `es_bird`). Si se codificaran como 0, 1, 2, 3, la neurona entendería que `bird` vale "tres veces" `cactus_small`, y eso no tiene sentido.
- Las partidas de prueba tienen que ser **distintas** a las de entrenamiento. Si no, el modelo parece mejor de lo que es.

**Revisión por tipo de obstáculo:**

- 150 es el **parametro de arranque**, no el número final.
- Hay que revisar cuántas muertes tiene **cada tipo** (`cactus_small`, `cactus_large`, `bird`), tanto en entrenamiento como en prueba.
- Si algún tipo queda corto, se juntan **más partidas reales** hasta completarlo. Copiar filas no sirve, porque el modelo ve los mismos casos repetidos.
- `bird` es el más probable de quedar corto, porque solo aparece en el 11% de los frames.

**Conclusión:** mínimo **150 partidas** (120 para entrenar y 30 para probar), y más si algún tipo de obstáculo tiene pocas muertes.

#### Riesgo si el dataset está mal definido

| Error de diseño | Consecuencia |
|---|---|
| Marcar Y = 1 en el frame **del choque** en vez del anterior | El modelo reconoce choques que ya pasaron, pero no los predice. |
| Usar **una fila por partida** | Se pierde lo que pasa en cada instante (distancia, salto, velocidad) y no hay forma de predecir el siguiente frame. |
