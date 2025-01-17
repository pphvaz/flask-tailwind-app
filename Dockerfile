# Base image for Python
FROM python:3.13.0-slim AS python-base

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Base image for Node.js
FROM node:18-slim AS node-base

WORKDIR /app

# Copy Tailwind configuration and package files
COPY package.json package-lock.json tailwind.config.js /app/

# Install Node.js dependencies
RUN npm install

# Copy static files for Tailwind processing
COPY static/css /app/static/css
COPY templates /app/templates

# Run Tailwind build
RUN npx tailwindcss -i ./static/css/styles.css -o ./static/css/output.css

# Final stage: Combine Python and Node.js outputs
FROM python-base

WORKDIR /app

# Copy Python and Node.js outputs from earlier stages
COPY --from=node-base /app/static/css/output.css /app/static/css/
COPY . /app/

EXPOSE 5000

# Use gunicorn to run the app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]