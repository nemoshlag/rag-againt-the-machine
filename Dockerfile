FROM python:3.10-slim

WORKDIR /app

COPY . .

# pre install tesseract
RUN apt-get update && apt-get install -y tesseract-ocr

# install python dependencies
RUN pip3 install -r requirements.txt

EXPOSE 8501

# HEALTHCHECK --interval=5s --timeout=3s --retries=3 CMD curl --fail http://localhost:8501/_stcore/health || exit 1
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
