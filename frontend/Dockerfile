FROM node:20 AS build
WORKDIR /app

ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

# Copy package.json and lock file first for better Docker caching
COPY package.json package-lock.json ./
RUN npm install
# Copy the rest of your frontend source files
COPY . .


RUN npm run build
FROM caddy:2-alpine

# Set the domain at build time (default localhost for local dev)
ARG BACKEND_DOMAIN=http://:80
ENV BACKEND_DOMAIN=${BACKEND_DOMAIN}

COPY --from=build /app/dist /usr/share/caddy
COPY Caddyfile.template /etc/caddy/Caddyfile
