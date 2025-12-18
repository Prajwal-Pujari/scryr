# Scryr

A minimal CLI tool that maps project structure and intent across **all programming languages**. Think of it as `tree`, but smarter and calmer.

## Features

- 🌍 **Multi-language support**: Python, JavaScript/TypeScript, Go, Rust, Java, C/C++, Ruby, PHP, and more
- 🌳 Clean ASCII tree visualization with Unicode box characters
- 🧠 Intelligent file analysis based on imports, comments, and folder context
- 🎨 Beautiful terminal output using Rich
- 🚫 Automatic filtering of noise folders (venv, node_modules, .git, etc.)
- ⚡ Fast and lightweight - no ML, no AST parsing
- 📦 Easy to install and use

## Installation

```bash
pip install scryr
```

Or install from source:

```bash
git clone https://github.com/Prajwal-Pujari/scryr.git
cd scryr
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

## Usage

Map the current directory:
```bash
scryr
```

Map a specific directory:
```bash
scryr /path/to/project
```

Limit depth:
```bash
scryr . --depth 3
```

Hide descriptions:
```bash
scryr . --no-description
```

Add custom ignore patterns:
```bash
scryr . --ignore logs --ignore temp
```
Help
```bash
scryr --help
```

## Example Output

### Python Project
```
myproject/
├── agents/
│   ├── planner.py        # Agent module: task planning logic
│   └── executor.py       # Agent module: action execution
├── vector_store/
│   └── chroma.py         # Memory module: ChromaDB vector storage
├── api/
│   ├── routes.py         # API route definitions
│   └── dependencies.py   # Dependency injection
├── main.py               # Application entry point
└── requirements.txt      # Python dependencies
```

### JavaScript/React Project
```
webapp/
├── src/
│   ├── components/
│   │   ├── Header.tsx    # React component
│   │   └── Footer.tsx    # React component
│   ├── pages/
│   │   └── Home.tsx      # Page component
│   ├── hooks/
│   │   └── useAuth.ts    # React hooks
│   └── index.tsx         # React entry point
├── package.json          # NPM package manifest
└── tsconfig.json         # TypeScript configuration
```

### Go Project
```
goapp/
├── cmd/
│   └── server/
│       └── main.go       # Main entry point
├── internal/
│   ├── handlers/
│   │   └── user.go       # HTTP handler
│   ├── services/
│   │   └── auth.go       # Service layer
│   └── models/
│       └── user.go       # Data model
├── go.mod                # Go module definition
└── Dockerfile            # Docker container definition
```

### Rust Project
```
rustapp/
├── src/
│   ├── main.rs           # Main entry point
│   ├── lib.rs            # Library root
│   └── handlers/
│       └── api.rs        # HTTP handler
├── Cargo.toml            # Rust package manifest
└── Cargo.lock            # Lock file
```

## Supported Languages

| Language | File Types | Detection |
|----------|-----------|-----------|
| **Python** | `.py` | Docstrings, imports (FastAPI, Django, Flask, etc.) |
| **JavaScript** | `.js`, `.mjs`, `.cjs` | JSDoc, imports (Express, React, etc.) |
| **TypeScript** | `.ts`, `.tsx` | JSDoc, imports |
| **Go** | `.go` | Package comments, imports (Gin, Fiber, etc.) |
| **Rust** | `.rs` | Doc comments, use statements (Actix, Tokio, etc.) |
| **Java** | `.java` | Imports (Spring, Hibernate, etc.) |
| **C/C++** | `.c`, `.cpp`, `.h`, `.hpp` | Includes |
| **Ruby** | `.rb` | Requires (Rails, Sinatra, etc.) |
| **PHP** | `.php` | Use statements (Laravel, Symfony, etc.) |

## Intelligence Rules

Scryr uses multiple signals to infer file purpose:

- **Special filenames**: `main.py`, `index.js`, `Dockerfile`, etc.
- **Import/require statements**: Detects frameworks and libraries
- **Folder context**: Files in `api/`, `models/`, `components/`, etc.
- **Documentation**: Docstrings, JSDoc, package comments
- **Naming conventions**: `*Controller.java`, `*_test.go`, etc.

## Folder Intelligence

Scryr recognizes common project structures:

- **API/Backend**: `api/`, `routes/`, `controllers/`, `handlers/`, `middleware/`
- **Services**: `services/`, `business/`, `logic/`, `domain/`
- **Data Layer**: `models/`, `entities/`, `schemas/`, `repositories/`, `db/`
- **Frontend**: `components/`, `views/`, `pages/`, `hooks/`, `store/`
- **AI/ML**: `agents/`, `vector_store/`, `embeddings/`, `llm/`
- **Utilities**: `utils/`, `helpers/`, `lib/`, `common/`
- **Configuration**: `config/`, `settings/`, `env/`
- **Testing**: `tests/`, `__tests__/`, `spec/`

## Philosophy

- No machine learning
- No AST parsing
- No over-engineering
- If something is printed, it must help
- Works across all major programming languages

## Requirements

- Python 3.9+
- rich >= 13.0.0

## Testing

Try Scryr on different types of projects:

```bash
# Python project
scryr ~/my-python-app

# JavaScript/React project
scryr ~/my-react-app

# Go project
scryr ~/my-go-api

# Rust project  
scryr ~/my-rust-service

# Mixed polyglot project
scryr ~/my-microservices
```

The tool will intelligently detect the language, parse imports/requires/uses, extract documentation, and provide meaningful descriptions for every file type!

## License

MIT License - see LICENSE file for details

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## Author

Prajwal (imprajwal793@gmail.com)