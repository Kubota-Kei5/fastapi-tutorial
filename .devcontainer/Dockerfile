FROM python:3.10-bullseye

# Add non-root user
ARG USERNAME=k395599
ARG USER_ID=1000
ARG GROUP_ID=1000

WORKDIR /app

COPY requirements.txt .

RUN groupadd --gid $GROUP_ID $USERNAME
RUN useradd -s /bin/bash --uid $USER_ID --gid $GROUP_ID -m $USERNAME
RUN apt-get update
RUN apt-get install -y sudo git
RUN echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME
RUN chmod 0440 /etc/sudoers.d/$USERNAME
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install --upgrade firebase-admin

COPY static/ static/
COPY app.py .
COPY firestore.py .
COPY env/ env/

# FastAPI アプリを起動
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]