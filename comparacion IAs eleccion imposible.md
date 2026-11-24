# Comparación de IAs: La elección imposible

Le di el mismo prompt a cuatro IAs: el expediente completo (las 36 tarjetas) y las 6 preguntas del dictamen. Luego comparé lo que contestó cada una contra la solución del caso.

| IA                  | Dónde corrió      |
| ------------------- | ----------------- |
| gemma4:e4b          | Local, con Ollama |
| phi4-mini           | Local, con Ollama |
| llama3.2:3b         | Local, con Ollama |
| Claude (Sonnet 5.5) |

- Primero probé con qwen3:4b, pero se quedó pensando hasta el límite de tokens y nunca contestó, así que lo cambié por llama3.2:3b.
- Corrí cada IA una sola vez.

## Qué contestó cada una

A cada pregunta le puse 1 punto si estaba bien, 0.5 si quedó a medias y 0 si estaba mal.

### Pregunta 1: ¿Cuántos votos físicos hay y cuánto suman las cinco actas?

**Solución:** 256 votos. Las actas suman Lucía 123, Mateo 119, blancos 7 y nulos 7.

- **gemma4:e4b (bien):** dijo que hay 256 votos físicos. Sumó los totales de las cinco actas (53 + 50 + 58 + 46 + 49 = 256) y lo apoyó con las 256 boletas sacadas de las urnas (E09).
- **phi4-mini (bien):** dijo "hay 256 votos físicos" y lo confirmó con las 256 firmas verificadas (E09). No mostró la suma de las actas.
- **llama3.2:3b (bien):** sumó las boletas de cada mesa y le dio 256.
- **Claude (bien):** 256, con una tabla de las cinco actas con los totales por mesa y por candidato (123, 119, 7 y 7). Además comprobó que los folios van del 001 al 256 sin saltos.

### Pregunta 2: ¿Quién gana con el recuento verificado y por cuántos votos?

**Solución:** Lucía, 123 contra 119, por 4 votos.

- **gemma4:e4b (bien):** sumó mesa por mesa y le salió Lucía 123 y Mateo 119, con diferencia de 4.
- **phi4-mini (a medias):** dijo que Lucía gana con 123, pero lo sacó del resultado anunciado (E07) y de la hoja A17. No dio los votos de Mateo ni el margen.
- **llama3.2:3b (mal):** puso Mateo 141 y Lucía 123, y concluyó que gana Mateo por 18 votos. Usó el número del tablero como si fuera el recuento real.
- **Claude (bien):** Lucía 123 contra 119, por 4 votos. Explicó que el 141 del tablero sale de 119 + 22, y que el total de 278 es 256 + 22.

### Pregunta 3: ¿Qué efecto tiene A17? ¿Qué folios están duplicados?

**Solución:** A17 le suma 22 votos a Mateo, pero son los folios M1-029 a M1-050, que ya estaban contados en la Mesa 1.

- **gemma4:e4b (bien):** dijo que A17 infla a Mateo de 119 a 141. Identificó que los folios M1-029 a M1-050 son los mismos que el acta de la Mesa 1 ya le asigna (E13, E15). Lo llamó "conteo fraudulento".
- **phi4-mini (a medias):** dijo que los 22 votos ya estaban en las actas de la Mesa 1, pero nunca dijo cuáles folios. Citó una lista larga de tarjetas (E13, E15, E16, E18, E20, E21...) sin explicar para qué.
- **llama3.2:3b (a medias):** dijo que A17 trae 22 folios que ya estaban contados y que no agregó nada nuevo, pero habló de "las cinco mesas" (era solo la Mesa 1) y no dio los folios. Además esto choca con lo que contestó en la pregunta 2.
- **Claude (bien):** los 22 folios (M1-029 a M1-050) están duplicados, el 100 %. Lo confirmó con la aclaración de Elisa (E29), el sobre sellado (E30) y el escaneo de las 11:06 (E32). Agregó que A17 no tiene las dos firmas y que el total publicado (278) pasa de las 256 firmas.

### Pregunta 4: Orden por hora oficial

**Solución:** P-43 a las 11:09, P-44 a las 11:14, llegada de A17 a las 11:18 y captura en T a las 11:20. La impresora P va 4 minutos atrasada (se suma 4) y la terminal T va 7 adelantada (se resta 7).

- **gemma4:e4b (a medias):** entendió que había que corregir, pero aplicó los minutos al revés. Dejó P-43 a las 11:01, P-44 a las 11:06, la llegada a las 11:22 y la captura a las 11:28. El orden salió bien, las horas no. Para las dos últimas usó la hora de la cámara en lugar de los registros.
- **phi4-mini (a medias):** puso las horas originales (11:05, 11:10, 11:18 y 11:27) y nada más escribió entre paréntesis que la impresora va atrasada. No corrigió ninguna. El orden coincide por casualidad.
- **llama3.2:3b (a medias):** igual, puso 11:05, 11:10, 11:18 y 11:24 sin corregir, y mezcló relojes de la impresora y de la cámara. El orden también coincide por casualidad.
- **Claude (bien):** 11:09, 11:14, 11:18 y 11:20, con la cuenta de cada una. Lo comprobó con la cámara (11:18 de la cámara son las 11:14 oficiales) y con el tiempo que Julia estuvo en la terminal.

### Pregunta 5: ¿Quién envió A17, quién la transcribió y qué no se puede afirmar del beneficiario?

**Solución:** Rebeca la envió e imprimió (credencial R7, cámara y pasillo). Julia la transcribió. No se puede afirmar que Mateo la conociera o la autorizara.

- **gemma4:e4b (bien):** Rebeca por la credencial R7, la cámara y el pasillo. Julia la transcribió sin comprobar folios. De Mateo dijo que no hay evidencia de que supiera (estaba en la asamblea de 11:05 a 11:25). Se pasó al llamar "hecho comprobado" lo de R7, porque una credencial sola no prueba quién estaba ahí.
- **phi4-mini (a medias):** dijo que Rebeca la preparó y Julia la transcribió, pero pegó una lista enorme de tarjetas sin relación. Dijo que "no se puede afirmar con certeza quién se benefició", cuando el beneficiado sí es Mateo. Lo que no se puede probar es que lo supiera.
- **llama3.2:3b (a medias):** dijo que Rebeca la preparó con su credencial R7, pero no contestó quién la transcribió. Dijo que tampoco se puede saber quién se benefició y que no hay evidencia de que alguien usara A17 para alterar los resultados.
- **Claude (bien):** Rebeca imprimió A17 (credencial R7, cámara, pasillo e inicial "R."), aclarando que la credencial sola no lo prueba. Julia la transcribió, porque ella misma lo admite. Descartó a Tomás porque salió a las 11:13. De Mateo dijo que el efecto lo favoreció, pero que no hay evidencia de que supiera de A17.

### Pregunta 6: Dos medidas de control

**Solución:** por ejemplo, no aceptar ajustes sin dos firmas, folios nuevos y comprobación física, y usar credenciales personales con los relojes sincronizados.

- **gemma4:e4b (bien):** doble verificación física de folios con un auditor, y restringir la impresora y la terminal con dos firmas antes de imprimir cualquier ajuste.
- **phi4-mini (a medias):** pedir la firma del auditor en cualquier ajuste (bien) y prohibir usar credenciales para imprimir (muy general).
- **llama3.2:3b (a medias):** verificar que los documentos tengan las dos firmas (bien) y "revisar la lista de votantes antes de permitir que se impriman las boletas", que no tiene sentido para este caso.
- **Claude (bien):** bloquear en el tablero cualquier ajuste sin dos firmas, folios nuevos y comprobación física, y rechazar totales mayores a las firmas verificadas. Además, cuentas personales sin sesiones compartidas, relojes sincronizados y que las actas entren solo por la cadena de custodia.

## Comparación

| Pregunta                   | gemma4:e4b | phi4-mini | llama3.2:3b | Claude |
| -------------------------- | ---------- | --------- | ----------- | ------ |
| 1. Votos y suma de actas   | Bien       | Bien      | Bien        | Bien   |
| 2. Ganador y margen        | Bien       | A medias  | Mal         | Bien   |
| 3. A17 y folios duplicados | Bien       | A medias  | A medias    | Bien   |
| 4. Horas oficiales         | A medias   | A medias  | A medias    | Bien   |
| 5. Quién fue quién         | Bien       | A medias  | A medias    | Bien   |
| 6. Medidas de control      | Bien       | A medias  | A medias    | Bien   |
| **Puntos (de 6)**          | **5.5**    | **3.5**   | **3**       | **6**  |

Lo que noté:

- Las cuatro sacaron bien el 256, que es solo sumar.
- Las horas fueron lo más difícil. Solo Claude las corrigió bien. Gemma sí lo intentó, pero se equivocó en el sentido, y las otras dos ni lo intentaron.
- Llama cayó en la trampa del tablero y dio como ganador a Mateo, aunque en la pregunta 3 dijo que A17 no agregaba folios nuevos, así que se contradijo.
- Phi4-mini citó tarjetas de más sin relación con lo que decía.
