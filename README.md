# Chatbot de reglas para el Avance de Proyecto 1

Chatbot educativo que responde preguntas frecuentes sobre objetivo, alcance,
arquitectura, tecnologías, pruebas y evidencias del Avance de Proyecto 1. Ayuda a
concentrar información básica que normalmente estaría distribuida entre varias
indicaciones del proyecto.

Es un chatbot basado en reglas. No utiliza un modelo de machine learning ni aprende
de las conversaciones.

## Requisitos

- Python 3.10 o superior.
- NLTK 3.9.1.

## Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Ejecución

```bash
python -m asistente
```

Escribe una pregunta sobre el avance o `salir` para terminar.

## Pruebas

```bash
pytest
```

Las pruebas validan normalización, clasificación, fallback y respuestas reproducibles.

## Base de conocimiento

`src/asistente/data/intents.json` contiene las intenciones, los patrones que se
buscan en cada mensaje y las respuestas asociadas. Una palabra coincidente suma un
punto y una frase completa suma tres. Si ninguna regla coincide, el chatbot usa una
respuesta fallback.

## Estructura

```text
src/asistente/                         Motor del chatbot
src/asistente/data/intents.json        Intenciones y respuestas
tests/                                 Pruebas automatizadas
notebooks/chatbot_reglas_colab.ipynb   Ejecución guiada en Colab
.github/workflows/tests.yml             Pruebas en Python 3.10 y 3.12
```
