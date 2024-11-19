# nginx/Dockerfile

# Use the official Nginx image as the base
FROM nginx:latest

# Ensure the /etc/nginx/ directory exists
RUN mkdir -p /etc/nginx/

# Copy the custom Nginx configuration file into the container
COPY nginx.conf /etc/nginx/
