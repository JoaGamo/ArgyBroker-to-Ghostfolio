# Broker a Ghostfolio

Este es un proyecto diseñado para importar los datos de tu broker hacia [Ghostfolio](https://github.com/ghostfolio/ghostfolio), un software de código abierto para visualizar tu portfolio.

Por gusto mío, solo soporta importar desde IOL (InvertirOnline), pero puedes agregar un nuevo broker fácilmente.

## Pasos para usar

- Copia el archivo `.env.example` y renómbralo a `.env`

- rellena con los datos necesarios

- Asegúrate de tener instaladas las librerías `requests` y `dotenv` de Python

- Ejecuta el script con `python3 main.py`

Si pusiste un "fecha_desde" muy atrás, el script tardará un tiempo
Al finalizar, te emitirá por consola todos los errores que haya encontrado, si es que hubo, esos datos deberás cargarlos manualmente.

> Nota: Gracias a la API de IOL, este script no exportará tus dividendos.

Debido al estado actual de Ghostfolio, no he continuado este script. [Ver discusión aquí](https://github.com/ghostfolio/ghostfolio/discussions/3666)
