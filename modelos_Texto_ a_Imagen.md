# Modelos que generan imágenes con texto y dataset para LoRA

## Modelos que generan imágenes con texto

| Modelo | Quién lo hizo | ¿Se puede descargar? | ¿Se le puede hacer LoRA? | Lo que se encontró sobre el texto |
|---|---|---|---|---|
| GPT-4o (imágenes) | OpenAI | No | No | OpenAI dice que escribe bien el texto en letreros y menús. Falla más con otros idiomas y con letra pequeña |
| Ideogram | Ideogram | No | No | Su guía pide poner el texto exacto entre comillas y que sea corto. Funciona mejor en inglés |
| FLUX.1 [dev] | Black Forest Labs | Sí, pero solo uso no comercial | Sí | La ficha oficial no menciona el texto. Sale bien en pruebas de terceros |
| Stable Diffusion 3 / 3.5 | Stability AI | Sí, con licencia comunitaria | Sí | Su arquitectura (MMDiT) y sus tres codificadores de texto ayudan a la tipografía, según el paper |
| TextDiffuser | Chen et al., 2023 | Investigación | Investigación | Primero se decide dónde va cada palabra y después se dibuja la imagen |
| GlyphDraw | Ma et al., 2023 | Investigación | Usa fine-tuning ligero | Le da al modelo la forma de las letras y su posición, sobre todo para chino |

Un benchmark de IMG.LY puso a GPT Image y a la familia FLUX entre los mejores en texto. Es una prueba de una sola empresa y no incluye SD3, así que solo sirve de referencia.

## Estructura del dataset

El modelo aprende de pares imagen + descripción. Para que aprenda a escribir texto, la descripción debe llevar el texto exacto que sale en la imagen. Esto es una recomendación que sale de cómo trabajan Ideogram, TextDiffuser y GlyphDraw, no una regla de la herramienta.

Las carpetas siguen el formato ImageFolder de Hugging Face:

```
mi_dataset/
└── train/
    ├── 0001.png
    ├── 0002.png
    ├── 0003.png
    └── metadata.jsonl
```

El `metadata.jsonl` lleva un JSON por línea con dos campos:

| Campo | Qué lleva |
|---|---|
| `file_name` | Nombre de la imagen, relativo a la carpeta donde está el `metadata.jsonl` |
| `text` | La descripción de la imagen, con el texto exacto entre comillas |

Ejemplo:

```json
{"file_name": "0001.png", "text": "un letrero de madera que dice \"Café Luna\" en letras blancas"}
{"file_name": "0002.png", "text": "un cartel de neón que dice \"OPEN\" sobre una pared de ladrillo"}
{"file_name": "0003.png", "text": "una portada de libro con el título \"El Faro\" en letras doradas"}
```

Para cargarlo:

```python
from datasets import load_dataset

dataset = load_dataset("imagefolder", data_dir="mi_dataset", split="train")
# columnas: "image" y "text"
```

## Formato para LoRA

El dataset es el mismo. LoRA no cambia los datos, solo lo que se entrena: se congela el modelo y se entrenan dos matrices pequeñas (A y B) que se suman a los pesos originales (`h = W₀x + BAx`).

Los parámetros que más se mencionan:

- `r` (rank): tamaño de las matrices. Con más rank hay más parámetros por entrenar.
- `lora_alpha`: escala del cambio. Por defecto se usa `lora_alpha / r`.
- `target_modules`: capas donde se aplica. En SD 1.5 con `diffusers` son las de atención (`to_k`, `to_q`, `to_v`, `to_out.0`).

Comando de ejemplo, adaptado de la guía oficial de `diffusers` para SD 1.5:

```bash
accelerate launch --mixed_precision="fp16" train_text_to_image_lora.py \
  --pretrained_model_name_or_path="stable-diffusion-v1-5/stable-diffusion-v1-5" \
  --train_data_dir="mi_dataset" \
  --caption_column="text" \
  --resolution=512 --center_crop --random_flip \
  --train_batch_size=1 --gradient_accumulation_steps=4 \
  --max_train_steps=15000 --learning_rate=1e-04 \
  --output_dir="lora-texto-imagenes"
```

Al terminar se obtiene el archivo `pytorch_lora_weights.safetensors`, que se carga con `pipeline.load_lora_weights(...)`.

También existe DreamBooth LoRA. Ahí no hay una descripción por imagen, sino un solo `--instance_prompt` con un token especial para todas, y sirve para enseñar un sujeto o estilo con pocas imágenes.

Falta verificar que la guía oficial solo muestra el flujo con SD 1.5. Con FLUX o SD 3.5 el dataset sigue la misma idea, pero el script y las opciones cambian.

En resumen: los modelos abiertos (FLUX.1 y SD 3/3.5) se pueden ajustar con LoRA y los comerciales (GPT-4o e Ideogram) no. El dataset es una carpeta de imágenes con un `metadata.jsonl` que tiene `file_name` y `text`, y la descripción debe incluir el texto exacto que aparece en la imagen.

## Fuentes

- OpenAI, [Introducing 4o Image Generation](https://openai.com/index/introducing-4o-image-generation/).
- Ideogram, [Text in images](https://docs.ideogram.ai/prompting/text-in-images).
- Black Forest Labs, [FLUX.1 [dev]](https://huggingface.co/black-forest-labs/FLUX.1-dev) y [repositorio oficial](https://github.com/black-forest-labs/flux).
- Stability AI, [Stable Diffusion 3.5 Large](https://huggingface.co/stabilityai/stable-diffusion-3.5-large).
- Esser et al., [Scaling Rectified Flow Transformers (SD3)](https://arxiv.org/abs/2403.03206).
- Chen et al., [TextDiffuser](https://arxiv.org/abs/2305.10855).
- Ma et al., [GlyphDraw](https://arxiv.org/abs/2303.17870).
- IMG.LY, [GenAI Benchmarks: text reliability](https://img.ly/ai-benchmarks/findings/text-reliability/).
- Hu et al., [LoRA](https://arxiv.org/abs/2106.09685).
- Hugging Face, [PEFT: guía de LoRA](https://huggingface.co/docs/peft/main/en/conceptual_guides/lora).
- Hugging Face, [Create an image dataset](https://huggingface.co/docs/datasets/image_dataset).
- Hugging Face, [Diffusers: Create a dataset for training](https://huggingface.co/docs/diffusers/training/create_dataset), [LoRA](https://huggingface.co/docs/diffusers/training/lora) y [DreamBooth](https://huggingface.co/docs/diffusers/training/dreambooth).
