# Pull node.js image from Docker Officail Images
FROM node:15.1.0-alpine3.10

# Install expo-cli globally
RUN npm i --unsafe-perm -g expo-cli@3.28.5

# Set working directory and path to node modules
WORKDIR /app_frontend
ENV PATH /app_frontend/node_modules/.bin:$PATH


# Install app dependencies
COPY package*.json ./
RUN npm install

# Copies everything over to the Docker environment
COPY . .

# Make port 19006 available for the app
EXPOSE 19006

# Start app
ENTRYPOINT ["npm", "run"]
CMD ["web"]
