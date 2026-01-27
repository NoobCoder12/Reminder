FROM python:3.12-slim
# Uyj obrazu python:3.12-slim jako bazę moje kontenera

WORKDIR /app
# Ustalenie Root Dir dla kontenera

COPY requirements.txt .
# Lokalizacja taka sama jak docker-compose, kropka na końcu oznacza lokalizację, będzie po app/ w kontenerze
# Kropka = bieący katalog w kontenerze
# COPY <zrodlo> <cel>

RUN pip install --no-cache-dir -r requirements.txt
# Z --no-cache-dir Docker tworzy mniejszy i czystszy obraz

COPY . .
# Skopiuj wszystko z backendu do app

EXPOSE 8000
# Informacja dla Dockera na jakim porcie nasłuchiwać ma kontener

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# Komenda ma się uruchomić po starcie Dockera
# "uvicorn" - serwer ASI, który odpala backend
# "app.main:app" - ścieka do obiektu FastAPI
# "--host","0.0.0.0" pozwala na dostęp serwera poza kontenerem
# "--port", "8000" - ustala port do nasłuchiwania, zgodnie z EXPOSE