import torch
import pandas as pd
from sentence_transformers import SentenceTransformer, util

class SemanticSearch:
    # def __init__(self, path):
    #     self.df = pd.read_csv(path)
    #     self.model = SentenceTransformer('cointegrated/rubert-tiny2')

    def __init__(self, path):
        print(f"Загружаю датасет из: {path}")
        self.df = pd.read_csv(path)
        print(f"Загружено {len(self.df)} строк")

        if self.df.empty:
            print("DataFrame пуст!")
        else:
            print(f"Пример вопроса: {self.df.iloc[0]['question']}")

        self.model = SentenceTransformer('cointegrated/rubert-tiny2')

    def search(self, user_question, category=None, top_k=2):
        query_embedding = self.model.encode(user_question, convert_to_tensor=True)

        # Фильтрация по категории
        if category:
            filtered_df = self.df[self.df['category'] == category.capitalize()].copy()
        else:
            filtered_df = self.df.copy()

        # Проверка на пустую выборку
        if filtered_df.empty:
            print(f"[INFO] Нет данных по категории '{category}'")
            return []

        # Пересчёт эмбеддингов для отфильтрованных вопросов
        filtered_questions = filtered_df['question'].tolist()
        embeddings = self.model.encode(filtered_questions, convert_to_tensor=True)

        # Расчёт косинусной близости
        scores = util.pytorch_cos_sim(query_embedding, embeddings)[0]

        # Получение индексов top_k самых похожих вопросов
        top_results = torch.topk(scores, k=min(top_k, len(scores)))  # защита от выхода за границы

        results = []
        for idx, score in zip(top_results.indices, top_results.values):
            match = filtered_df.iloc[idx.item()]
            results.append({
                'question': match['question'],
                'answer': match['answer'],
                'score': round(score.item(), 4)
            })

        return results