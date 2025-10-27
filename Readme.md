<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Pokémon ETL Pipeline</title>
  
  <!-- Tailwind CSS via CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  
  <!-- Google Fonts: Inter & Roboto Mono -->
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Roboto+Mono:wght@400;700&display=swap" rel="stylesheet">
  
  <!-- Font Awesome for Icons -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>

  <!-- Custom Tailwind Config -->
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['Inter', 'sans-serif'],
            mono: ['"Roboto Mono"', 'monospace'],
          },
          colors: {
            primary: '#3B82F6',
            accent: '#10B981',
            glass: 'rgba(255, 255, 255, 0.1)',
            glassborder: 'rgba(255, 255, 255, 0.2)',
          },
          backdropBlur: {
            xs: '2px',
          },
        },
      },
    }
  </script>

  <style>
    body {
      background: linear-gradient(-45deg, #1e3a8a, #0f172a, #1e293b, #0f172a);
      background-size: 400% 400%;
      animation: gradientShift 15s ease infinite;
      min-height: 100vh;
      color: #e2e8f0;
    }

    @keyframes gradientShift {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }

    .glass {
      background: rgba(255, 255, 255, 0.05);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 1rem;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    .glass-card {
      transition: all 0.3s ease;
    }
    .glass-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
    }

    .particle {
      position: absolute;
      background: rgba(59, 130, 246, 0.3);
      border-radius: 50%;
      pointer-events: none;
      animation: float 6s infinite ease-in-out;
    }

    @keyframes float {
      0%, 100% { transform: translateY(0) rotate(0deg); opacity: 0.6; }
      50% { transform: translateY(-20px) rotate(10deg); opacity: 1; }
    }

    pre {
      background: rgba(15, 23, 42, 0.8) !important;
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 0.75rem;
      padding: 1rem;
      overflow-x: auto;
      font-family: 'Roboto Mono', monospace;
    }

    code {
      font-family: 'Roboto Mono', monospace;
      background: rgba(15, 23, 42, 0.8);
      padding: 0.2rem 0.4rem;
      border-radius: 0.375rem;
      font-size: 0.875rem;
    }

    .toc a {
      color: #94a3b8;
      transition: color 0.2s;
    }
    .toc a:hover {
      color: #60a5fa;
    }

    .fade-in {
      animation: fadeIn 1s ease-out;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }
  </style>
</head>
<body class="text-slate-300 leading-relaxed">

  <!-- Particle Background -->
  <div id="particles"></div>

  <div class="container mx-auto px-6 py-12 max-w-5xl">
    
    <!-- Hero Section -->
    <section class="text-center mb-16 fade-in">
      <h1 class="text-5xl md:text-6xl font-bold text-white mb-4">
        Pokémon ETL Pipeline
      </h1>
      <p class="text-xl text-slate-400 max-w-3xl mx-auto">
        A comprehensive ETL pipeline that fetches Pokémon data from the PokéAPI, processes it, stores it in SQLite, and serves it via a stunning web interface.
      </p>
      <div class="mt-8 flex justify-center gap-4">
        <a href="#usage" class="px-6 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white font-medium rounded-lg shadow-lg hover:shadow-blue-500/50 transition">
          Get Started
        </a>
        <a href="https://github.com/yourusername/pokemon-etl-pipeline" target="_blank" class="px-6 py-3 bg-slate-800 text-white font-medium rounded-lg border border-slate-700 hover:bg-slate-700 transition">
          <i class="fab fa-github mr-2"></i> GitHub
        </a>
      </div>
    </section>

    <!-- Features Grid -->
    <section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-16">
      <div class="glass glass-card p-6">
        <div class="text-3xl text-blue-400 mb-3">Complete ETL</div>
        <p>Extract → Transform → Load with full logging and error handling</p>
      </div>
      <div class="glass glass-card p-6">
        <div class="text-3xl text-emerald-400 mb-3">Modern UI</div>
        <p>Glassmorphic design with animations and particle effects</p>
      </div>
      <div class="glass glass-card p-6">
        <div class="text-3xl text-purple-400 mb-3">Advanced Filters</div>
        <p>Filter by type, HP, attack, and evolution status</p>
      </div>
      <div class="glass glass-card p-6">
        <div class="text-3xl text-yellow-400 mb-3">FastAPI Backend</div>
        <p>RESTful API with auto-docs and rate limiting</p>
      </div>
      <div class="glass glass-card p-6">
        <div class="text-3xl text-pink-400 mb-3">Normalized DB</div>
        <p>Proper relationships and referential integrity</p>
      </div>
      <div class="glass glass-card p-6">
        <div class="text-3xl text-cyan-400 mb-3">Idempotent</div>
        <p>Run the pipeline multiple times safely</p>
      </div>
    </section>

    <!-- Table of Contents -->
    <section class="glass p-8 mb-12">
      <h2 class="text-3xl font-bold text-white mb-6 flex items-center">
        Table of Contents
      </h2>
      <ul class="space-y-2 toc text-lg">
        <li><a href="#project-structure" class="hover:text-blue-400">Project Structure</a></li>
        <li><a href="#prerequisites" class="hover:text-blue-400">Prerequisites</a></li>
        <li><a href="#installation" class="hover:text-blue-400">Installation</a></li>
        <li><a href="#usage" class="hover:text-blue-400">Usage</a></li>
        <li><a href="#database-schema" class="hover:text-blue-400">Database Schema</a></li>
        <li><a href="#api-endpoints" class="hover:text-blue-400">API Endpoints</a></li>
        <li><a href="#configuration" class="hover:text-blue-400">Configuration</a></li>
        <li><a href="#architecture" class="hover:text-blue-400">Architecture</a></li>
        <li><a href="#contributing" class="hover:text-blue-400">Contributing</a></li>
        <li><a href="#license" class="hover:text-blue-400">License</a></li>
      </ul>
    </section>

    <!-- Project Structure -->
    <section id="project-structure" class="glass p-8 mb-12">
      <h2 class="text-3xl font-bold text-white mb-6">Project Structure</h2>
      <pre class="text-sm text-green-300">
pokemon-etl-pipeline/
├── app.py                      # FastAPI application & endpoints
├── main.py                     # ETL pipeline orchestration
├── constants.py                # Configuration constants
├── index.html                  # Frontend UI
├── data_processing/
│   ├── extract.py             # API data extraction
│   ├── transform.py           # Data transformation logic
│   └── load.py                # Database operations
├── db/
│   └── pokemon_database.db    # SQLite database (generated)
├── requirements.txt           # Python dependencies
└── README.md                  # This file
      </pre>
    </section>

    <!-- Prerequisites -->
    <section id="prerequisites" class="glass p-8 mb-12">
      <h2 class="text-3xl font-bold text-white mb-6">Prerequisites</h2>
      <ul class="space-y-3 text-lg">
        <li><span class="text-blue-400">•</span> Python 3.10+ (recommended 3.11 or 3.12)</li>
        <li><span class="text-blue-400">•</span> <code>pip</code> (Python package manager)</li>
        <li><span class="text-blue-400">•</span> Internet connection (for PokéAPI)</li>
      </ul>
    </section>

    <!-- Installation -->
    <section id="installation" class="glass p-8 mb-12">
      <h2 class="text-3xl font-bold text-white mb-6">Installation</h2>
      <div class="space-y-6">
        <div>
          <h3 class="text-xl font-semibold text-blue-300 mb-2">1. Clone the Repository</h3>
          <pre><code>git clone https://github.com/yourusername/pokemon-etl-pipeline.git
cd pokemon-etl-pipeline</code></pre>
        </div>
        <div>
          <h3 class="text-xl font-semibold text-blue-300 mb-2">2. Create Virtual Environment</h3>
          <pre><code># macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate</code></pre>
        </div>
        <div>
          <h3 class="text-xl font-semibold text-blue-300 mb-2">3. Install Dependencies</h3>
          <pre><code>pip install -r requirements.txt</code></pre>
        </div>
        <div>
          <h3 class="text-xl font-semibold text-blue-300 mb-2">4. Create DB Directory</h3>
          <pre><code>mkdir -p db</code></pre>
        </div>
      </div>
    </section>

    <!-- Usage -->
    <section id="usage" class="glass p-8 mb-12">
      <h2 class="text-3xl font-bold text-white mb-6">Usage</h2>
      <div class="space-y-8">
        <div>
          <h3 class="text-2xl font-semibold text-emerald-300 mb-3">Running the ETL Pipeline</h3>
          <pre><code>python3 main.py</code></pre>
          <p class="mt-3">Fetches first 12 Pokémon, transforms, and loads into SQLite with progress bar.</p>
        </div>
        <div>
          <h3 class="text-2xl font-semibold text-emerald-300 mb-3">Running the Web App</h3>
          <pre><code>uvicorn app:app --reload</code></pre>
          <div class="mt-3 space-y-2">
            <p><span class="text-blue-400">Web:</span> <a href="http://localhost:8000" class="text-blue-300 underline">http://localhost:8000</a></p>
            <p><span class="text-blue-400">Docs:</span> <a href="http://localhost:8000/docs" class="text-blue-300 underline">http://localhost:8000/docs</a></p>
          </div>
        </div>
      </div>
    </section>

    <!-- Database Schema -->
    <section id="database-schema" class="glass p-8 mb-12">
      <h2 class="text-3xl font-bold text-white mb-6">Database Schema</h2>
      <div class="grid md:grid-cols-2 gap-6">
        <div>
          <h3 class="text-xl font-semibold text-yellow-300 mb-3">Core Tables</h3>
          <ul class="space-y-2 text-sm">
            <li><code>pokemon</code> - id, name, is_evolved</li>
            <li><code>types</code>, <code>abilities</code>, <code>stats</code> - lookup tables</li>
          </ul>
        </div>
        <div>
          <h3 class="text-xl font-semibold text-yellow-300 mb-3">Junction & Evolution</h3>
          <ul class="space-y-2 text-sm">
            <li><code>pokemon_types</code>, <code>pokemon_abilities</code>, <code>pokemon_stats</code></li>
            <li><code>evolution_chains</code> + <code>evolution_links</code></li>
          </ul>
        </div>
      </div>
    </section>

    <!-- API Endpoints -->
    <section id="api-endpoints" class="glass p-8 mb-12">
      <h2 class="text-3xl font-bold text-white mb-6">API Endpoints</h2>
      <div class="space-y-4">
        <div class="bg-slate-800 p-4 rounded-lg">
          <code class="text-green-400">POST /etl/run-pipeline</code> → Run ETL
        </div>
        <div class="bg-slate-800 p-4 rounded-lg">
          <code class="text-blue-400">GET /pokemon</code> → All names
        </div>
        <div class="bg-slate-800 p-4 rounded-lg">
          <code class="text-purple-400">GET /pokemon/filter?type_name=water&hp_min=50</code>
        </div>
      </div>
    </section>

    <!-- Configuration -->
    <section id="configuration" class="glass p-8 mb-12">
      <h2 class="text-3xl font-bold text-white mb-6">Configuration</h2>
      <p>Edit <code>constants.py</code>:</p>
      <pre class="text-sm mt-3">
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"
API_DELAY = 0.5
DATABASE_FILE = "db/pokemon_database.db"
POKEMON_TO_FETCH = 12
      </pre>
    </section>

    <!-- Architecture -->
    <section id="architecture" class="glass p-8 mb-12">
      <h2 class="text-3xl font-bold text-white mb-6">Architecture</h2>
      <div class="text-center">
        <div class="inline-block bg-slate-800 p-6 rounded-xl">
          <p class="text-lg font-mono text-emerald-400">
            EXTRACT → TRANSFORM → LOAD
          </p>
          <p class="text-sm text-slate-400 mt-2">PokéAPI → Normalize → SQLite</p>
        </div>
      </div>
    </section>

    <!-- Contributing & License -->
    <section class="grid md:grid-cols-2 gap-8 mb-12">
      <div id="contributing" class="glass p-8">
        <h2 class="text-2xl font-bold text-white mb-4">Contributing</h2>
        <ol class="space-y-2 text-sm">
          <li>Fork → Create branch</li>
          <li>Commit → Push</li>
          <li>Open Pull Request</li>
        </ol>
      </div>
      <div id="license" class="glass p-8">
        <h2 class="text-2xl font-bold text-white mb-4">License</h2>
        <p class="text-sm">MIT License — Free to use, modify, and distribute.</p>
      </div>
    </section>

    <!-- Footer -->
    <footer class="text-center py-8 text-slate-500 text-sm">
      <p>Made with <span class="text-red-500">❤</span> for Pokémon fans and data engineers</p>
      <p class="mt-2">Powered by PokéAPI • FastAPI • Tailwind CSS</p>
    </footer>
  </div>

  <!-- Particle JS -->
  <script>
    const particlesContainer = document.getElementById('particles');
    const particleCount = 30;

    for (let i = 0; i < particleCount; i++) {
      const particle = document.createElement('div');
      particle.className = 'particle';
      particle.style.width = `${Math.random() * 6 + 2}px`;
      particle.style.height = particle.style.width;
      particle.style.left = `${Math.random() * 100}%`;
      particle.style.top = `${Math.random() * 100}%`;
      particle.style.animationDelay = `${Math.random() * 5}s`;
      particle.style.animationDuration = `${Math.random() * 8 + 4}s`;
      particlesContainer.appendChild(particle);
    }

    // Smooth scroll for TOC
    document.querySelectorAll('.toc a').forEach(link => {
      link.addEventListener('click', e => {
        e.preventDefault();
        const target = document.querySelector(link.getAttribute('href'));
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });
  </script>
</body>
</html>