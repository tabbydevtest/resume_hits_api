# Use the Nginx image from Docker Hub
FROM nginx:alpine

# Remove the default Nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Copy the configuration file from the current directory to the Nginx directory
COPY nginx.conf /etc/nginx/conf.d

# Expose ports
EXPOSE 80

# Start Nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]