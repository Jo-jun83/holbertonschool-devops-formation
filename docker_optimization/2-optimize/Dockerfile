FROM node:20-alpine

WORKDIR /app

COPY package.json .

RUN npm install

COPY . .

RUN adduser --disabled-password appuser

USER appuser

CMD ["node", "index.js"]
