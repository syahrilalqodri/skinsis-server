FROM python:3.9.2

# Copy local code to the container image
COPY . /app

# Sets the working directory
WORKDIR /app


# Upgrade PIP
RUN pip install --upgrade pip

# Install production dependencies.
RUN pip install Flask gunicorn

#Install python libraries from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set $PORT environment variable
EXPOSE 5000
ENV PORT 5000

# Run the web service on container startup
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
