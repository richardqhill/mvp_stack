FROM node:20 AS build
WORKDIR /app

# Copy package.json and lock file first for better Docker caching
COPY package.json package-lock.json ./
RUN npm install
# Copy the rest of your frontend source files
COPY . .


RUN npm run build && ls -l dist
FROM caddy:2-alpine
COPY --from=build /app/dist /usr/share/caddy
COPY Caddyfile.dev /etc/caddy/Caddyfile
