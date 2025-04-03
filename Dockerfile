# Stage 1: Frontend builder
FROM node:18-alpine as frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json .
RUN npm install
COPY frontend .
RUN npm run build

# Stage 2: Backend builder
FROM python:3.9-slim as backend-builder
WORKDIR /app/backend
COPY backend/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt
COPY backend .

# Final stage
FROM python:3.9-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js for frontend runtime
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && corepack enable

# Copy built frontend
COPY --from=frontend-builder /app/frontend ./frontend
COPY --from=frontend-builder /app/frontend/node_modules ./frontend/node_modules

# Copy backend
COPY --from=backend-builder /app/backend ./backend
COPY --from=backend-builder /root/.local /root/.local

# Environment variables
ENV PATH="/root/.local/bin:${PATH}"
ENV PYTHONPATH=/app/backend

WORKDIR /app
CMD ["sh", "-c", "cd frontend && npm start & cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000"]