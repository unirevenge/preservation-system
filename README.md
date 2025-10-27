# CADE System (v6.0)

**C**ognitive **A**rtificial **D**igital **E**ntity System

A sophisticated AI framework designed for cognitive processing, knowledge management, and autonomous operation.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for version control)

### Installation

#### Windows

1. Open Command Prompt or PowerShell
2. Navigate to the project directory
3. Run the initialization script:

   ```batch
   init.bat
   ```

#### Linux/macOS

1. Open Terminal
2. Navigate to the project directory
3. Make the script executable and run it:

   ```bash
   chmod +x init.sh
   ./init.sh
   ```

### First-Time Setup

The initialization script will:

1. Create a Python virtual environment
2. Install all required dependencies
3. Set up the configuration files
4. Create necessary directories
5. Initialize the database

## 🏗️ Project Structure

```text
preservation-system/
├── cade/                  # Python package: core, models, plugins, utils
├── scripts/               # Orchestrator, production server, init, watchdog
│   ├── auto_init_all.py   # Auto init: cspell merge, syntax check, hints
│   ├── auto_init_cade.py  # Environment/config checks and setup
│   ├── cade_production.py # FastAPI production app (uvicorn entry)
│   └── watchdog_runner.py # Filesystem monitoring to logs/
├── json/                  # JSON configuration and data files
├── logs/                  # Application logs
├── tests/                 # Test suite
├── init/                  # Platform init scripts (init.bat, init.sh)
├── requirements.txt       # Development dependencies
├── requirements-prod.txt  # Production dependencies
├── pyproject.toml         # Project config, console scripts, tooling
└── .github/workflows/     # CI pipeline (ruff, black, mypy, orchestrator)
```

## 🛠️ Development

### Activate Virtual Environment

#### Windows

```batch
.\venv\Scripts\activate
```

#### Linux/macOS

```bash
source venv/bin/activate
```

### Running the Development/Production Server

Options:

- Console script (after install):

  ```bash
  cade-auto-init            # orchestrator (safe)
  uvicorn scripts.cade_production:app --reload
  ```

- Direct module:

  ```bash
  python -m scripts.auto_init_all
  uvicorn scripts.cade_production:app --reload
  ```

Server default: `http://localhost:8000`

### API Documentation

Once the server is running, you can access:

- Interactive API docs: `http://localhost:8000/docs`
- Alternative API docs: `http://localhost:8000/redoc`

## 🚀 Production Deployment

### Using Docker (Recommended)

1. Build the Docker image:

   ```bash
   docker build -t cade-system .
   ```

2. Run the container:

   ```bash
   docker run -d -p 8000:8000 --name cade-api cade-system
   ```

### Manual Deployment

1. Install production dependencies:

   ```bash
   pip install -r requirements-prod.txt
   ```

2. Set environment variables in `.env` for production

3. Run with a production ASGI server:

   ```bash
   uvicorn scripts.cade_production:app --host 0.0.0.0 --port 8000 --workers 4
   ```

## 🤖 Using the CADE System

### Basic Commands

- Start the interactive shell:

  ```bash
  python -m cade_core
  ```

- Run a specific module:

  ```bash
  python -m cade_custom
  ```

### Configuration

Edit `config.ini` to customize the system behavior. Key sections:

```ini
[database]
engine = sqlite  # or postgresql, mysql
name = cade
host = localhost
port =
username =
password =

[logging]
level = INFO
file = logs/cade.log
max_size = 10  # MB
backup_count = 5

[server]
host = 0.0.0.0
port = 8000
debug = True
```

## 📚 Documentation

For detailed documentation, please refer to the `docs/` directory.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

For support or questions, please open an issue in the repository.
