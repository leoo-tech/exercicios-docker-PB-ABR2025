# Projeto Docker Compose - React + Express + MongoDB

## Objetivo
Criar um projeto full-stack completo usando Docker Compose para orquestrar uma aplicação React (frontend), Express.js (backend) e MongoDB (banco de dados), incluindo Mongo Express para administração.

## Arquitetura do Projeto

```
react-express-mongo/
├── frontend/                 # Aplicação React
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── backend/                  # API Express.js
│   ├── src/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml        # Orquestração dos serviços
├── .env                     # Variáveis de ambiente
├── .dockerignore           # Arquivos a ignorar
└── README.md
```

## Estrutura dos Serviços

| Serviço | Porta | Tecnologia | Função |
|---------|-------|------------|--------|
| frontend | 3000 | React | Interface do usuário |
| backend | 5000 | Express.js | API REST |
| mongodb | 27017 | MongoDB | Banco de dados |
| mongo-express | 8081 | Mongo Express | Admin do MongoDB |

## 1. Backend - Express.js

### backend/package.json
```json
{
  "name": "backend",
  "version": "1.0.0",
  "description": "Express API for React App",
  "main": "src/server.js",
  "scripts": {
    "start": "node src/server.js",
    "dev": "nodemon src/server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "mongoose": "^7.5.0",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1",
    "body-parser": "^1.20.2"
  },
  "devDependencies": {
    "nodemon": "^3.0.1"
  }
}
```

### backend/src/server.js
```javascript
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const bodyParser = require('body-parser');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// MongoDB Connection
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://mongodb:27017/reactexpressdb';

mongoose.connect(MONGODB_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => {
  console.log('✅ Connected to MongoDB');
})
.catch((error) => {
  console.error('❌ MongoDB connection error:', error);
});

// User Schema
const userSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  age: { type: Number, required: true },
  createdAt: { type: Date, default: Date.now }
});

const User = mongoose.model('User', userSchema);

// Routes
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    service: 'Express API',
    timestamp: new Date().toISOString(),
    database: mongoose.connection.readyState === 1 ? 'connected' : 'disconnected'
  });
});

// Get all users
app.get('/api/users', async (req, res) => {
  try {
    const users = await User.find().sort({ createdAt: -1 });
    res.json({ success: true, users });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Create user
app.post('/api/users', async (req, res) => {
  try {
    const { name, email, age } = req.body;
    const user = new User({ name, email, age });
    await user.save();
    res.status(201).json({ success: true, user });
  } catch (error) {
    res.status(400).json({ success: false, error: error.message });
  }
});

// Delete user
app.delete('/api/users/:id', async (req, res) => {
  try {
    const user = await User.findByIdAndDelete(req.params.id);
    if (!user) {
      return res.status(404).json({ success: false, error: 'User not found' });
    }
    res.json({ success: true, message: 'User deleted successfully' });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 Server running on port ${PORT}`);
});
```

### backend/Dockerfile
```dockerfile
FROM node:18-alpine

WORKDIR /app

# Copiar package.json e package-lock.json
COPY package*.json ./

# Instalar dependências
RUN npm install

# Copiar código fonte
COPY . .

# Expor porta
EXPOSE 5000

# Comando para executar aplicação
CMD ["npm", "start"]
```

## 2. Frontend - React

### frontend/package.json
```json
{
  "name": "frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "^5.0.1",
    "axios": "^1.5.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "proxy": "http://backend:5000",
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
```

### frontend/src/App.js
```javascript
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [users, setUsers] = useState([]);
  const [formData, setFormData] = useState({ name: '', email: '', age: '' });
  const [loading, setLoading] = useState(false);
  const [health, setHealth] = useState(null);

  // Fetch users
  const fetchUsers = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/users');
      setUsers(response.data.users);
    } catch (error) {
      console.error('Error fetching users:', error);
    } finally {
      setLoading(false);
    }
  };

  // Check API health
  const checkHealth = async () => {
    try {
      const response = await axios.get('/api/health');
      setHealth(response.data);
    } catch (error) {
      console.error('Error checking health:', error);
    }
  };

  // Create user
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/api/users', {
        ...formData,
        age: parseInt(formData.age)
      });
      setFormData({ name: '', email: '', age: '' });
      fetchUsers();
    } catch (error) {
      console.error('Error creating user:', error);
      alert('Error creating user: ' + error.response?.data?.error);
    }
  };

  // Delete user
  const deleteUser = async (id) => {
    try {
      await axios.delete(`/api/users/${id}`);
      fetchUsers();
    } catch (error) {
      console.error('Error deleting user:', error);
    }
  };

  useEffect(() => {
    fetchUsers();
    checkHealth();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>🐳 React + Express + MongoDB</h1>
        
        {health && (
          <div className="health-status">
            <p>API Status: <span className="status-healthy">{health.status}</span></p>
            <p>Database: <span className="status-healthy">{health.database}</span></p>
          </div>
        )}

        <div className="container">
          <div className="form-section">
            <h2>Add New User</h2>
            <form onSubmit={handleSubmit}>
              <input
                type="text"
                placeholder="Name"
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                required
              />
              <input
                type="email"
                placeholder="Email"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                required
              />
              <input
                type="number"
                placeholder="Age"
                value={formData.age}
                onChange={(e) => setFormData({...formData, age: e.target.value})}
                required
              />
              <button type="submit">Add User</button>
            </form>
          </div>

          <div className="users-section">
            <h2>Users ({users.length})</h2>
            {loading ? (
              <p>Loading...</p>
            ) : (
              <div className="users-list">
                {users.map(user => (
                  <div key={user._id} className="user-card">
                    <h3>{user.name}</h3>
                    <p>Email: {user.email}</p>
                    <p>Age: {user.age}</p>
                    <p>Created: {new Date(user.createdAt).toLocaleDateString()}</p>
                    <button 
                      onClick={() => deleteUser(user._id)}
                      className="delete-btn"
                    >
                      Delete
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </header>
    </div>
  );
}

export default App;
```

### frontend/src/App.css
```css
.App {
  text-align: center;
}

.App-header {
  background-color: #282c34;
  padding: 20px;
  color: white;
  min-height: 100vh;
}

.health-status {
  background: #1a1a1a;
  padding: 10px;
  border-radius: 8px;
  margin: 20px auto;
  max-width: 300px;
}

.status-healthy {
  color: #4caf50;
  font-weight: bold;
}

.container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
  margin-top: 20px;
}

.form-section, .users-section {
  background: #1a1a1a;
  padding: 20px;
  border-radius: 12px;
  min-width: 300px;
  max-width: 500px;
}

.form-section form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-section input {
  padding: 12px;
  border: none;
  border-radius: 6px;
  font-size: 16px;
}

.form-section button {
  padding: 12px 24px;
  background: #61dafb;
  color: #282c34;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s;
}

.form-section button:hover {
  background: #21a9c7;
}

.users-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.user-card {
  background: #2a2a2a;
  padding: 15px;
  border-radius: 8px;
  text-align: left;
}

.user-card h3 {
  margin: 0 0 10px 0;
  color: #61dafb;
}

.user-card p {
  margin: 5px 0;
  color: #ccc;
}

.delete-btn {
  background: #f44336;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}

.delete-btn:hover {
  background: #d32f2f;
}

@media (max-width: 768px) {
  .container {
    flex-direction: column;
    align-items: center;
  }
}
```

### frontend/Dockerfile
```dockerfile
FROM node:18-alpine

WORKDIR /app

# Copiar package.json e package-lock.json
COPY package*.json ./

# Instalar dependências
RUN npm install

# Copiar código fonte
COPY . .

# Expor porta
EXPOSE 3000

# Comando para executar aplicação
CMD ["npm", "start"]
```

## 3. Docker Compose Configuration

### docker-compose.yml
```yaml
version: '3.8'

services:
  # MongoDB Database
  mongodb:
    image: mongo:7.0
    container_name: mongodb
    restart: unless-stopped
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGO_ROOT_USERNAME}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_ROOT_PASSWORD}
      MONGO_INITDB_DATABASE: ${MONGO_DB_NAME}
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
      - ./init-mongo.js:/docker-entrypoint-initdb.d/init-mongo.js:ro
    networks:
      - app-network

  # Mongo Express - MongoDB Admin Interface
  mongo-express:
    image: mongo-express:1.0.0
    container_name: mongo-express
    restart: unless-stopped
    depends_on:
      - mongodb
    environment:
      ME_CONFIG_MONGODB_ADMINUSERNAME: ${MONGO_ROOT_USERNAME}
      ME_CONFIG_MONGODB_ADMINPASSWORD: ${MONGO_ROOT_PASSWORD}
      ME_CONFIG_MONGODB_SERVER: mongodb
      ME_CONFIG_MONGODB_PORT: 27017
      ME_CONFIG_BASICAUTH_USERNAME: ${MONGOEXPRESS_LOGIN}
      ME_CONFIG_BASICAUTH_PASSWORD: ${MONGOEXPRESS_PASSWORD}
    ports:
      - "8081:8081"
    networks:
      - app-network

  # Backend API
  backend:
    build: 
      context: ./backend
      dockerfile: Dockerfile
    container_name: backend
    restart: unless-stopped
    depends_on:
      - mongodb
    environment:
      NODE_ENV: development
      PORT: 5000
      MONGODB_URI: mongodb://${MONGO_ROOT_USERNAME}:${MONGO_ROOT_PASSWORD}@mongodb:27017/${MONGO_DB_NAME}?authSource=admin
    ports:
      - "5000:5000"
    volumes:
      - ./backend:/app
      - /app/node_modules
    networks:
      - app-network

  # Frontend React App
  frontend:
    build: 
      context: ./frontend
      dockerfile: Dockerfile
    container_name: frontend
    restart: unless-stopped
    depends_on:
      - backend
    environment:
      REACT_APP_API_URL: http://localhost:5000
      CHOKIDAR_USEPOLLING: true
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    networks:
      - app-network
    stdin_open: true
    tty: true

volumes:
  mongodb_data:

networks:
  app-network:
    driver: bridge
```

### .env
```env
# MongoDB Configuration
MONGO_ROOT_USERNAME=admin
MONGO_ROOT_PASSWORD=password123
MONGO_DB_NAME=reactexpressdb

# Mongo Express Configuration
MONGOEXPRESS_LOGIN=admin
MONGOEXPRESS_PASSWORD=admin123

# Application Configuration
NODE_ENV=development
PORT=5000
```

### init-mongo.js
```javascript
// Initialize MongoDB with sample data
db = db.getSiblingDB('reactexpressdb');

db.users.insertMany([
  {
    name: "João Silva",
    email: "joao@example.com",
    age: 30,
    createdAt: new Date()
  },
  {
    name: "Maria Santos",
    email: "maria@example.com",
    age: 25,
    createdAt: new Date()
  },
  {
    name: "Carlos Oliveira",
    email: "carlos@example.com",
    age: 35,
    createdAt: new Date()
  }
]);

print('Database initialized with sample data');
```

### .dockerignore
```
node_modules
npm-debug.log
.git
.gitignore
README.md
.env
.nyc_output
coverage
.dockerignore
Dockerfile
.DS_Store
*.log
```

## 4. Scripts de Automação

### start.sh
```bash
#!/bin/bash

echo "🚀 Starting React + Express + MongoDB Stack..."

# Parar containers existentes
docker-compose down

# Build e start dos serviços
docker-compose up --build -d

# Aguardar serviços ficarem prontos
echo "⏳ Waiting for services to be ready..."
sleep 10

# Verificar status dos serviços
echo "📊 Services Status:"
docker-compose ps

echo "✅ Stack is running!"
echo ""
echo "🌐 Access your applications:"
echo "  - Frontend (React):     http://localhost:3000"
echo "  - Backend API:          http://localhost:5000/api/health"
echo "  - Mongo Express:        http://localhost:8081"
echo "  - MongoDB:              mongodb://localhost:27017"
echo ""
echo "🔐 Mongo Express Login:"
echo "  Username: admin"
echo "  Password: admin123"
```

### stop.sh
```bash
#!/bin/bash

echo "🛑 Stopping React + Express + MongoDB Stack..."

# Parar e remover containers
docker-compose down

# Remover volumes (opcional - descomente se quiser limpar dados)
# docker-compose down -v

echo "✅ Stack stopped!"
```

### logs.sh
```bash
#!/bin/bash

echo "📋 Docker Compose Logs"
echo "Press Ctrl+C to exit"
echo ""

# Mostrar logs de todos os serviços
docker-compose logs -f
```

## 5. Comandos para Executar

### Pré-requisitos
```bash
# Verificar se Docker e Docker Compose estão instalados
docker --version
docker-compose --version

# Criar estrutura do projeto
mkdir react-express-mongo && cd react-express-mongo
mkdir frontend backend
```

### Executar o projeto
```bash
# Tornar scripts executáveis
chmod +x start.sh stop.sh logs.sh

# Iniciar stack completa
./start.sh

# Ou manualmente:
docker-compose up --build -d
```

### Monitoramento
```bash
# Ver logs em tempo real
./logs.sh

# Status dos containers
docker-compose ps

# Estatísticas de recursos
docker stats
```

### Parar o projeto
```bash
# Parar containers
./stop.sh

# Ou manualmente:
docker-compose down

# Parar e remover volumes (limpar dados)
docker-compose down -v
```

## 6. Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/health` | Status da API e conexão DB |
| GET | `/api/users` | Listar todos os usuários |
| POST | `/api/users` | Criar novo usuário |
| DELETE | `/api/users/:id` | Deletar usuário |

### Exemplos de uso
```bash
# Verificar saúde da API
curl http://localhost:5000/api/health

# Listar usuários
curl http://localhost:5000/api/users

# Criar usuário
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","age":28}'
```

## 7. Acesso aos Serviços

### URLs de Acesso
- **Frontend React**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Mongo Express**: http://localhost:8081 (admin/admin123)
- **MongoDB**: mongodb://localhost:27017

### Estrutura de Dados
```javascript
// User Schema
{
  "_id": "ObjectId",
  "name": "String",
  "email": "String (unique)",
  "age": "Number",
  "createdAt": "Date"
}
```

## Resultado Esperado

Após executar o projeto, você terá:

1. **Frontend React** rodando na porta 3000 com interface para gerenciar usuários
2. **API Express** na porta 5000 com endpoints REST
3. **MongoDB** na porta 27017 com dados persistentes
4. **Mongo Express** na porta 8081 para administração do banco

A aplicação demonstra uma stack completa MERN dockerizada com comunicação entre todos os serviços, persistência de dados e interface de administração.