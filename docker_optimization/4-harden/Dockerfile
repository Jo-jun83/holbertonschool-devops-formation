FROM node:20-alpine

WORKDIR /usr/src/app


COPY package*.json ./
RUN npm install
COPY . .
RUN addgroup app && adduser -S -G app app
USER app


HEALTHCHECK CMD wget -q --spider http://localhost:3000/health || exit 1

CMD ["node", "server.js"]
