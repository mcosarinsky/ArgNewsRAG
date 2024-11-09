""""
Referencias:
- https://ai.google.dev/
- https://ai.google.dev/gemini-api/docs/structured-output?lang=python
"""

import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
from tqdm import tqdm
import os 
import json
import time
import argparse
import typing_extensions as typing

load_dotenv()
api_key = os.getenv('API_KEY')

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

class ResponseSchema(typing.TypedDict):
    Pregunta: str
    Respuesta: str

def generate_query_prompt(sample):
    prompt = "En base al artículo dado a continuación debes generar una pregunta puntual sobre el tema central del artículo junto a su respuesta. La respuesta debe ser breve, precisa y contener a lo sumo una frase que respondan de forma directa a la pregunta. La pregunta puede incluir referencias temporales y al diario que la publicó de ser necesario y debe ser lo suficientemente clara como para que un experto que no haya leído el artículo pueda responderla. La respuesta debe ser precisa y concisa, sin necesidad de elaborar explicaciones largas. Las respuestas deben basarse en el contenido del artículo y reflejar un conocimiento general sobre el tema.\nEl formato de salida debe ser el siguiente: {'Pregunta': [...], 'Respuesta': [...]}"
    query_article = f"\nDiario:{sample['site']}\nTitulo:{sample['title']}\nFecha: {sample['published date']}\nDescripción: {sample['description']}\nContenido: {sample['text']}"
    full_prompt = f"{prompt}\n{query_article}"
    
    return full_prompt

def fetch_responses(df_samples, output_file):
    responses = []
    
    for index, sample in tqdm(df_samples.iterrows(), total=len(df_samples)):
        prompt = generate_query_prompt(sample)

        try:
            # Generate content using the model
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json", 
                    response_schema=ResponseSchema  
                )
            )
            response_text = response.text.strip()
            response_data = json.loads(response_text)
            response_data["id"] = sample["id"]
            
            responses.append(response_data)
        except Exception as e:
            print(f"Error fetching response for index {index}: {e}")
        
        time.sleep(5)  # Adding a pause between API calls to avoid rate limits
    
    df_responses = pd.DataFrame(responses)
    df_responses.to_csv(output_file, index=False, encoding='utf-8')

def main():
    parser = argparse.ArgumentParser(description="Generate Q&A for articles using generative model.")
    parser.add_argument("--input", type=str, default="articulos.csv", help="Input CSV file with articles")
    parser.add_argument("--output", type=str, default="qa_dataset.csv", help="Output csv file for storing responses")
    parser.add_argument("--n_samples", type=int, default=200, help="Number of samples to process")
    
    args = parser.parse_args()

    # Load the dataset and sample N rows
    df = pd.read_csv(args.input)
    df_samples = df.sample(args.n_samples, random_state=1)

    # Fetch responses for the sample and save to file
    fetch_responses(df_samples, args.output)

if __name__ == "__main__":
    main()