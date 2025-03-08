# ArgNewsRAG

This repository contains the implementation of a Retrieval-Augmented Generation (RAG) system for answering questions based on Argentine news articles. The system combines dense retrieval with a language model to enhance response accuracy by leveraging external knowledge.

## 📁 Repository Structure

- **data/**: Contains the news articles dataset, FAISS index, and QA datasets.
- **figures/**: Includes visualizations of dataset statistics and evaluation results.
- **notebooks/**: Jupyter notebooks for generating embeddings, running Llama for QA, and evaluating the model.
- **scripts/**: Python scripts for fetching news, generating QA datasets, and producing answers using the RAG model.
- **requirements.txt**: Lists the dependencies needed to run the project.

## 🛠 Tools & Technologies
- **Jina-Embeddings-V3**: Used to generate dense vector embeddings.
- **FAISS**: Efficient similarity search for document retrieval.
- **Llama-3.2-1B-Instruct**: LLM used for answering questions.

## 🚀 Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the news retrieval script:
   ```bash
   python scripts/fetch_news.py
   ```
3. Generate the QA dataset:
   ```bash
   python scripts/generate_qa.py
   ```
4. Generate answers using the RAG model:
   ```bash
   python scripts/generate_answers.py
   ```
5. Evaluate the model using the `evaluation.ipynb` notebook.

## 📊 Evaluation
The system was tested on a manually curated QA dataset. Performance was assessed using:
- **Recall@K**: Measures how often the correct article appears in the top K retrieved results.
- **MRR (Mean Reciprocal Rank)**: Evaluates the ranking quality of the retrieved documents.
- **BLEU & ROUGE-2**: Compare the model's generated responses with reference answers.
- **F1 Score**: Measures the overlap between predicted and reference answers.
- **BERTScore-F1**: Uses transformer embeddings to assess semantic similarity.

## 📌 Future Improvements
- **Improve Retrieval**: Experiment with different embedding models and retrieval strategies.
- **Expand Dataset**: Incorporate more diverse news sources and timeframes.
- **Optimize LLM Performance**: Test larger models or fine-tune on domain-specific data.
