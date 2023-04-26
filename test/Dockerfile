FROM python:3.11-slim-bullseye

# Upgrade security packages and pip
RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --upgrade pip

# Add non root user
RUN adduser worker
USER worker
WORKDIR /home/worker

# Install requirements
COPY --chown=worker:worker requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && \
    rm requirements.*
ENV PATH="/home/worker/.local/bin:${PATH}"

COPY --chown=worker:worker src ./src
ENV PYTHONUNBUFFERED 1
CMD ["python", "-m", "src.main"]
