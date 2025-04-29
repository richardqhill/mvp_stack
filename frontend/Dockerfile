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

COPY --from=build /app/dist /usr/share/caddy
COPY Caddyfile.template /etc/caddy/Caddyfile

EXPOSE 80
CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile"]
