FROM python:3.12-slim

# Atualize o pip e instale o Bottle
RUN pip install --upgrade pip && \
    pip install bottle eventlet python-socketio

WORKDIR /bmvc

COPY . /bmvc

# Exponha a porta que o aplicativo usa
EXPOSE 8080

# Comando para executar a aplicação
CMD ["python3", "route.py"]
