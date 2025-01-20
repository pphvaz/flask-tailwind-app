# Base image for Python
FROM python:3.10-alpine AS python-base

WORKDIR /app

# Upgrade pip and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Base image for Node.js
FROM node:18-alpine AS node-base

WORKDIR /app

# Install Node.js dependencies and process Tailwind CSS
COPY package.json tailwind.config.js /app/
COPY static/css /app/static/css
COPY templates /app/templates
RUN npm install && \
    npx tailwindcss -i ./static/css/styles.css -o ./static/css/output.css

# Final stage: Combine Python and Node.js outputs
FROM python-base

WORKDIR /app

# Set the Flask environment to production
ENV FLASK_ENV=production

# Copy Python outputs and other necessary files
COPY --from=node-base /app/static/css/output.css /app/static/css/
COPY . /app/

EXPOSE 5000

# Add a non-root user for better security
RUN adduser --disabled-password appuser
USER appuser

# Healthcheck for app health
HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:5000/health || exit 1

# Command to run the app using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]