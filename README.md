# README for fantasy football playoff project
🏈 NFL Fantasy Football Playoff Project
A real-time fantasy football leaderboard that syncs active NFL player data from the Sleeper API and provides a searchable, high-performance web interface.

🚀 Features
Automated Sync: A Python-based engine that fetches and filters over 2,000+ NFL players (QB, RB, WR, TE).

Fast Search: Instant client-side filtering by player name, team, or position.

Reliable Backend: Node.js API serving data from a persistent PostgreSQL database.

Dockerized: Entire stack (DB, API, Engine) launches with a single command.

🛠️ Tech Stack
Frontend: HTML5, CSS3 (Modern Slate UI), Vanilla JavaScript.

Backend: Node.js, Express.js.

Data Engine: Python 3.x, psycopg2, requests.

Database: PostgreSQL 15.

Orchestration: Docker & Docker Compose.

📦 Installation & Setup
Prerequisites
Docker Desktop installed and running.

A .env file in the root directory (optional, defaults are provided).

Quick Start
Clone the repository:

Bash

git clone https://github.com/bassoccer56/fantasy_football_playoff_project.git
cd fantasy_football_playoff_project
Launch the containers:

Bash

docker compose up --build
Access the app:

Frontend: http://localhost:3000

Raw API: http://localhost:3000/players

🏗️ Project Structure
Plaintext

.
├── backend-node/
│   ├── public/
│   │   └── index.html      # Main UI & Search logic
│   ├── index.js            # Express API server
│   └── Dockerfile
├── engine-python/
│   ├── main.py             # Sleeper API Sync Logic
│   └── Dockerfile
├── database/
│   └── init.sql            # Database schema
└── docker-compose.yml      # Orchestration file
🚦 Roadmap
[x] Initial Sleeper API Sync

[x] Search & Filter Functionality

[ ] Live Scoring Simulation

[ ] User Authentication & "My Team" Selection

[ ] Mobile-Responsive Design Improvements

📄 License
Distributed under the MIT License.
