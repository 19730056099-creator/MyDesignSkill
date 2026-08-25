const http = require('http');
const { ItemStore } = require('./store');

function send(response, status, body) {
  response.writeHead(status, { 'content-type': 'application/json' });
  response.end(JSON.stringify(body));
}

function readJson(request) {
  return new Promise((resolve, reject) => {
    let body = '';
    request.on('data', chunk => {
      body += chunk;
      if (body.length > 10000) reject(new Error('body too large'));
    });
    request.on('end', () => {
      try { resolve(JSON.parse(body)); } catch (error) { reject(error); }
    });
    request.on('error', reject);
  });
}

function createServer(store = new ItemStore()) {
  return http.createServer(async (request, response) => {
    if (request.method === 'GET' && request.url === '/items') {
      return send(response, 200, store.list());
    }
    if (request.method === 'POST' && request.url === '/items') {
      try {
        const input = await readJson(request);
        return send(response, 201, store.create(input.name));
      } catch (error) {
        return send(response, 400, { error: error.message });
      }
    }
    return send(response, 404, { error: 'not found' });
  });
}

if (require.main === module) {
  createServer().listen(3000, () => console.log('listening on 3000'));
}

module.exports = { createServer };
