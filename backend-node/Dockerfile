# Use a specific, stable version (Alpine is tiny and fast)
FROM node:20-alpine

# Set the folder inside the container
WORKDIR /app

# Copy package files first to speed up future builds
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy everything else from your folder into /app
COPY . .

# Expose the port
EXPOSE 3000

# Run the app directly (more reliable than npm start)
CMD ["node", "index.js"]