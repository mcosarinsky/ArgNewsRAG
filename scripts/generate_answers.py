import os
from dotenv import load_dotenv
from groq import Groq
import pandas as pd

load_dotenv()


client = Groq(
    # This is the default and can be omitted
    api_key=os.getenv('GROQ_KEY'),
)

articles = pd.read_csv("data/articulos.csv")
questions = pd.read_csv("data/qa_dataset_v2.csv")

prompt = "Dada una pregunta y una serie de artículos donde puedes encontrar su respuesta, responde a la pregunta de forma breve y precisa en a lo sumo una frase.\n"

pregunta = questions['Pregunta'][0]
articulo_1_id = questions['top_1_id'][0]
articulo_2_id = questions['top_2_id'][0]
articulo_3_id = questions['top_3_id'][0]

articulo_1 = articles[articles['id'] == articulo_1_id]
articulo_2 = articles[articles['id'] == articulo_2_id]
articulo_3 = articles[articles['id'] == articulo_3_id]

prompt += f"Pregunta: {pregunta}\n"
prompt += f"Artículo 1:\nDiario:{articulo_1['site']}\nTitulo:{articulo_1['title']}\nFecha: {articulo_1['published date']}\nDescripción: {articulo_1['description']}\nContenido: {articulo_1['text']}"

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "Eres un asistente que responde preguntas basadas en artículos de diarios argentinos."
        },
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="llama-3.2-1b-preview",
)

print(chat_completion.choices[0].message.content)