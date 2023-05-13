FROM gcr.io/datamechanics/spark:platform-3.2.1-latest

ENV PYSPARK_MAJOR_PYTHON_VERSION=3
WORKDIR /home
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
CMD ["bash"]