# ベースイメージの指定
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# バックエンドのコードをコピー
WORKDIR /app/backend
COPY . /app/backend

# バックエンドの依存関係をインストール
RUN pip install -r requirements.txt

EXPOSE 5600

# バックエンドの起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5600"]