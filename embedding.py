# embedding.py：自定义的"中文指纹机"（用硅基流动的 BAAI 中文模型）
import os
import requests
from dotenv import load_dotenv
from chromadb import EmbeddingFunction

load_dotenv()
API_KEY = os.getenv("SILICONFLOW_API_KEY")


class SiliconFlowEmbedding(EmbeddingFunction):
    """把文字变成向量的函数，用的是懂中文的 bge 模型"""

    def __init__(self):
        super().__init__()
        self.url = "https://api.siliconflow.cn/v1/embeddings"
        self.model = "BAAI/bge-large-zh-v1.5"

    def __call__(self, input):
        # 调硅基流动的 API，把一串文字变成一串向量
        resp = requests.post(
            self.url,
            json={"model": self.model, "input": input},
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            timeout=60,
        )
        data = resp.json()

        # 按顺序收集每个向量
        embeddings = []
        for item in data["data"]:
            embeddings.append(item["embedding"])
        return embeddings
