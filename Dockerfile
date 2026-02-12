FROM python:3.10-slim

# Create a user to avoid permission errors
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /home/user/app

# Copy requirements and install
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of your app code
COPY --chown=user . .

# IMPORTANT: Must use port 7860 for Hugging Face Docker
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]