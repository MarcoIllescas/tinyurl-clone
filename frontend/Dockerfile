# Node to develop
FROM node:18-alpine

# Working directory within the container
WORKDIR /app

# Packages
COPY package.json .

# Install packages
RUN npm install

# Copy code
COPY . .

# Expose port 3000
EXPOSE 3000

# Start-up in development mode
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]