from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
import random
import requests
import re
import threading

app = Flask(__name__)
CORS(app)

# api solver CamPC Real v1 
fake_404 = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hoang Phat</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@500;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background: #030014;
            overflow: hidden;
            position: relative;
        }
        #spaceCanvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 1;
            pointer-events: none;
        }
        .main-card {
            position: relative;
            z-index: 10;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            background: rgba(13, 11, 36, 0.75);
            border: 1px solid rgba(139, 92, 246, 0.3);
            box-shadow: 0 0 50px rgba(124, 58, 237, 0.25), 0 20px 50px rgba(0, 0, 0, 0.9);
        }
        .ascii-banner {
            font-family: 'Fira Code', monospace;
            line-height: 1.15;
            font-size: 11px;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, #a855f7, #3b82f6, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .cosmic-title {
            background: linear-gradient(90deg, #c084fc, #60a5fa, #f472b6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 20px rgba(192, 132, 252, 0.4);
        }
        /* Custom Seekbar Cosmic Style */
        input[type=range] {
            -webkit-appearance: none;
            width: 100%;
            background: transparent;
        }
        input[type=range]:focus { outline: none; }
        input[type=range]::-webkit-slider-runnable-track {
            width: 100%;
            height: 4px;
            cursor: pointer;
            background: #1e1b4b;
            border-radius: 2px;
        }
        input[type=range]::-webkit-slider-thumb {
            height: 12px;
            width: 12px;
            border-radius: 50%;
            background: #a855f7;
            box-shadow: 0 0 10px #a855f7;
            cursor: pointer;
            -webkit-appearance: none;
            margin-top: -4px;
        }
    </style>
</head>
<body class="min-h-screen flex items-center justify-center p-4">

    <!-- Canvas Vũ Trụ: Ngôi sao, Bụi tinh vân, Hành tinh di chuyển & Mưa Thiên Thạch -->
    <canvas id="spaceCanvas"></canvas>

    <!-- Nút Loa Mute/Unmute -->
    <button id="toggleVolume" class="fixed top-5 left-5 z-20 text-purple-400 hover:text-pink-300 transition">
        <svg id="volumeIcon" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072M18.364 5.636a9 9 0 010 12.728M11 5L6 9H2v6h4l5 4V5z"/>
        </svg>
    </button>

    <!-- Overlay Click to Enter (Bypass Autoplay) -->
    <div id="enterOverlay" class="fixed inset-0 bg-[#030014]/90 z-50 flex items-center justify-center cursor-pointer transition-opacity duration-500">
        <p class="text-purple-300 font-mono text-sm tracking-widest animate-pulse drop-shadow-[0_0_10px_rgba(168,85,247,0.8)]">[ CLICK TO ENTER THE GALAXY ]</p>
    </div>

    <!-- Container Card Căn Giữa -->
    <div class="main-card rounded-2xl p-6 md:p-8 max-w-lg w-full text-center flex flex-col items-center transition-all duration-500 hover:border-purple-500/60 hover:shadow-[0_0_60px_rgba(168,85,247,0.4)]">
        
        <!-- Khung chứa Banner ASCII Art / Ảnh Bìa (Có lớp Overlay đè lên) -->
        <div class="w-full bg-[#07051a]/90 border border-purple-900/50 rounded-xl p-4 mb-6 overflow-hidden flex items-center justify-center shadow-inner relative group">
            
            <!-- Nền ASCII Art làm Banner -->
            <pre class="ascii-banner font-bold select-none whitespace-pre text-left opacity-40 transition-opacity duration-300 group-hover:opacity-60">
⠤⣤⣤⣤⣄⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣠⣤⠤⠤⠴⠶⠶⠶⠶
⢠⣤⣤⡄⣤⣤⣤⠄⣀⠉⣉⣙⠒⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠴⠘⣉⢡⣤⡤⠐⣶⡆⢶⠀⣶⣶⡦
⣄⢻⣿⣧⠻⠇⠋⠀⠋⠀⢘⣿⢳⣦⣌⠳⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠞⣡⣴⣧⠻⣄⢸⣿⣿⡟⢁⡻⣸⣿⡿⠁
⠈⠃⠙⢿⣧⣙⠶⣿⣿⡷⢘⣡⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣷⣝⡳⠶⠶⠾⣛⣵⡿⠋⠀⠀
⠀⠀⠀⠀⠉⠻⣿⣶⠂☶⠛⠛⠛⢛⡛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠛⠀⠉⠒⠛⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⢸⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⣾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢻⡁⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠘⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠿⠀⠀⠀</pre>

            <!-- LớpOverlay đè chính giữa Ảnh Bìa -->
            <div class="absolute inset-0 flex items-center justify-center bg-purple-950/30 backdrop-blur-[2px]">
                <span class="cosmic-title text-xl md:text-2xl font-black tracking-widest uppercase px-5 py-2 bg-[#030014]/80 border border-purple-500/60 rounded-xl shadow-[0_0_25px_rgba(168,85,247,0.6)]">
                    Hoang Phat Solver 
                </span>
            </div>
        </div>

        <!-- Cosmic Tag Badge -->
        <div class="inline-block bg-purple-950/80 border border-purple-600/50 text-purple-300 text-xs font-bold px-4 py-1.5 rounded-full mb-3 tracking-wide shadow-[0_0_12px_rgba(168,85,247,0.3)]">
            CamPC Real
        </div>

        <!-- Title Cosmic -->
        <h1 class="cosmic-title text-2xl font-extrabold tracking-wider mb-6">
            Hoang Phat Solver 
        </h1>

        <!-- Audio Player Widget Cosmic Style -->
        <div class="w-full bg-[#07051a]/80 border border-purple-900/40 rounded-xl p-4 flex flex-col gap-2 shadow-lg">
            <div class="flex items-center justify-between text-xs text-purple-300/80">
                <div class="flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-pink-500 animate-ping"></span>
                    <span id="trackTitle" class="font-medium text-purple-200">Cosmic Night Stories</span>
                </div>
                <div class="font-mono text-purple-400">
                    <span id="currentTime">0:00</span> / <span id="duration">0:00</span>
                </div>
            </div>

            <!-- Seekbar Slider -->
            <input type="range" id="seekBar" value="0" min="0" max="100" class="w-full">

            <!-- Controls -->
            <div class="flex items-center justify-center gap-4 pt-1">
                <button id="prevBtn" class="text-purple-400 hover:text-pink-300 transition">
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M6 6h2v12H6zm3.5 6l8.5 6V6z"/></svg>
                </button>
                <button id="playBtn" class="text-white hover:text-purple-200 transition bg-purple-600/40 p-2.5 rounded-full border border-purple-500/50 shadow-[0_0_15px_rgba(168,85,247,0.5)]">
                    <svg id="playIcon" class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                </button>
                <button id="nextBtn" class="text-purple-400 hover:text-pink-300 transition">
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M6 18l8.5-6L6 6v12zM16 6v12h2V6h-2z"/></svg>
                </button>
            </div>
        </div>
    </div>

    <!-- Audio Element -->
    <audio id="bgMusic" loop src="https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=lofi-study-112191.mp3"></audio>

    <!-- Canvas Engine hiệu ứng Vũ Trụ, Hành Tinh & Thiên Thạch Rơi -->
    <script>
        const canvas = document.getElementById('spaceCanvas');
        const ctx = canvas.getContext('2d');
        let w, h;

        function resize() {
            w = canvas.width = window.innerWidth;
            h = canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resize);
        resize();

        // 1. Khởi tạo các ngôi sao
        const starCount = 220;
        const stars = [];
        const starColors = ['#ffffff', '#a855f7', '#60a5fa', '#f472b6'];

        for (let i = 0; i < starCount; i++) {
            stars.push({
                x: Math.random() * w,
                y: Math.random() * h,
                radius: Math.random() * 1.5 + 0.3,
                color: starColors[Math.floor(Math.random() * starColors.length)],
                alpha: Math.random(),
                speed: Math.random() * 0.02 + 0.005
            });
        }

        // 2. Khởi tạo các Hành tinh (Planets) bay ở viền ngoài
        const planets = [
            {
                x: w * 0.12, y: h * 0.2, radius: 28, color: '#8b5cf6', ring: true,
                vx: 0.15, vy: 0.08, glowColor: 'rgba(139, 92, 246, 0.4)'
            },
            {
                x: w * 0.85, y: h * 0.75, radius: 42, color: '#ec4899', ring: true,
                vx: -0.1, vy: -0.12, glowColor: 'rgba(236, 72, 153, 0.35)'
            },
            {
                x: w * 0.82, y: h * 0.18, radius: 18, color: '#3b82f6', ring: false,
                vx: -0.08, vy: 0.1, glowColor: 'rgba(59, 130, 246, 0.4)'
            },
            {
                x: w * 0.15, y: h * 0.82, radius: 22, color: '#c084fc', ring: false,
                vx: 0.12, vy: -0.06, glowColor: 'rgba(192, 132, 252, 0.3)'
            }
        ];

        // 3. Khởi tạo danh sách Thiên Thạch / Sao Băng rơi
        const meteors = [];

        function spawnMeteor() {
            meteors.push({
                x: Math.random() * (w * 1.2),
                y: -50,
                length: Math.random() * 90 + 60,
                speed: Math.random() * 12 + 8,
                size: Math.random() * 2 + 1,
                opacity: 1,
                color: Math.random() > 0.5 ? '#a855f7' : '#60a5fa'
            });
        }

        function drawSpace() {
            ctx.clearRect(0, 0, w, h);

            // Tinh vân nền (Cosmic Nebulas)
            const nebula1 = ctx.createRadialGradient(w * 0.2, h * 0.25, 50, w * 0.2, h * 0.25, 450);
            nebula1.addColorStop(0, 'rgba(124, 58, 237, 0.18)');
            nebula1.addColorStop(1, 'transparent');
            ctx.fillStyle = nebula1;
            ctx.fillRect(0, 0, w, h);

            const nebula2 = ctx.createRadialGradient(w * 0.8, h * 0.75, 50, w * 0.8, h * 0.75, 500);
            nebula2.addColorStop(0, 'rgba(236, 72, 153, 0.15)');
            nebula2.addColorStop(1, 'transparent');
            ctx.fillStyle = nebula2;
            ctx.fillRect(0, 0, w, h);

            // Vẽ Ngôi Sao
            for (let i = 0; i < stars.length; i++) {
                const s = stars[i];
                s.alpha += s.speed;
                if (s.alpha > 1 || s.alpha < 0) s.speed = -s.speed;

                ctx.beginPath();
                ctx.arc(s.x, s.y, s.radius, 0, Math.PI * 2);
                ctx.fillStyle = s.color;
                ctx.globalAlpha = Math.abs(s.alpha);
                ctx.fill();
            }
            ctx.globalAlpha = 1;

            // Vẽ & Di chuyển các Hành Tinh
            planets.forEach(p => {
                p.x += p.vx;
                p.y += p.vy;

                // Bật lại vị trí nếu rời quá xa màn hình
                if (p.x < -100) p.x = w + 100;
                if (p.x > w + 100) p.x = -100;
                if (p.y < -100) p.y = h + 100;
                if (p.y > h + 100) p.y = -100;

                // Hào quang quanh hành tinh
                const glow = ctx.createRadialGradient(p.x, p.y, p.radius * 0.5, p.x, p.y, p.radius * 2);
                glow.addColorStop(0, p.glowColor);
                glow.addColorStop(1, 'transparent');
                ctx.fillStyle = glow;
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.radius * 2, 0, Math.PI * 2);
                ctx.fill();

                // Thân hành tinh
                const pGrad = ctx.createLinearGradient(p.x - p.radius, p.y - p.radius, p.x + p.radius, p.y + p.radius);
                pGrad.addColorStop(0, p.color);
                pGrad.addColorStop(1, '#0f0c29');
                ctx.fillStyle = pGrad;
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                ctx.fill();

                // Vành đai đĩa (Saturn Ring) nếu p.ring = true
                if (p.ring) {
                    ctx.save();
                    ctx.translate(p.x, p.y);
                    ctx.rotate(-Math.PI / 6);
                    ctx.beginPath();
                    ctx.ellipse(0, 0, p.radius * 2.2, p.radius * 0.5, 0, 0, Math.PI * 2);
                    ctx.strokeStyle = p.glowColor;
                    ctx.lineWidth = 3;
                    ctx.stroke();
                    ctx.restore();
                }
            });

            // Sinh thiên thạch mới ngẫu nhiên
            if (Math.random() < 0.04) { 
                spawnMeteor();
            }

            // Vẽ & Di chuyển Thiên Thạch Rơi
            for (let i = meteors.length - 1; i >= 0; i--) {
                const m = meteors[i];
                
                ctx.beginPath();
                const grad = ctx.createLinearGradient(
                    m.x, m.y,
                    m.x - m.length, m.y + m.length
                );
                grad.addColorStop(0, m.color);
                grad.addColorStop(1, 'transparent');

                ctx.strokeStyle = grad;
                ctx.lineWidth = m.size;
                ctx.moveTo(m.x, m.y);
                ctx.lineTo(m.x - m.length, m.y + m.length);
                ctx.stroke();

                // Đầu thiên thạch sáng rực
                ctx.beginPath();
                ctx.arc(m.x, m.y, m.size * 1.5, 0, Math.PI * 2);
                ctx.fillStyle = '#ffffff';
                ctx.fill();

                m.x += m.speed;
                m.y += m.speed;
                m.opacity -= 0.01;

                if (m.y > h + 100 || m.x > w + 100 || m.opacity <= 0) {
                    meteors.splice(i, 1);
                }
            }

            requestAnimationFrame(drawSpace);
        }
        drawSpace();

        // --- Trình Phát Âm Thanh (Audio Player) ---
        const audio = document.getElementById('bgMusic');
        const overlay = document.getElementById('enterOverlay');
        const playBtn = document.getElementById('playBtn');
        const playIcon = document.getElementById('playIcon');
        const seekBar = document.getElementById('seekBar');
        const currentTimeEl = document.getElementById('currentTime');
        const durationEl = document.getElementById('duration');
        const toggleVolume = document.getElementById('toggleVolume');

        let isPlaying = false;

        function formatTime(sec) {
            if (isNaN(sec)) return "0:00";
            const m = Math.floor(sec / 60);
            const s = Math.floor(sec % 60);
            return `${m}:${s < 10 ? '0' : ''}${s}`;
        }

        function togglePlay() {
            if (isPlaying) {
                audio.pause();
                playIcon.innerHTML = '<path d="M8 5v14l11-7z"/>';
            } else {
                audio.play();
                playIcon.innerHTML = '<path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>';
            }
            isPlaying = !isPlaying;
        }

        overlay.addEventListener('click', () => {
            overlay.classList.add('opacity-0');
            setTimeout(() => overlay.remove(), 500);
            audio.play();
            isPlaying = true;
            playIcon.innerHTML = '<path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>';
        });

        playBtn.addEventListener('click', togglePlay);

        audio.addEventListener('loadedmetadata', () => {
            durationEl.innerText = formatTime(audio.duration);
        });

        audio.addEventListener('timeupdate', () => {
            currentTimeEl.innerText = formatTime(audio.currentTime);
            if (audio.duration) {
                seekBar.value = (audio.currentTime / audio.duration) * 100;
            }
        });

        seekBar.addEventListener('input', () => {
            if (audio.duration) {
                audio.currentTime = (seekBar.value / 100) * audio.duration;
            }
        });

        toggleVolume.addEventListener('click', () => {
            audio.muted = !audio.muted;
            toggleVolume.classList.toggle('text-red-400', audio.muted);
        });
    </script>
</body>
</html>"""

_model_cache = {}
_model_cache_lock = threading.Lock()
FREE_MODELS_FALLBACK = [
    'llama-3.3-70b-versatile',
    'llama-3.1-8b-instant',
    'llama3-70b-8192',
    'llama3-8b-8192',
    'gemma2-9b-it',
    'mistral-saba-24b',
]

def fetch_models_for_key(api_key):
    with _model_cache_lock:
        if api_key in _model_cache:
            return _model_cache[api_key]
    try:
        resp = requests.get(
            'https://api.groq.com/openai/v1/models',
            headers={'Authorization': f'Bearer {api_key}'},
            timeout=5
        )
        if resp.status_code == 200:
            data = resp.json()
            models = [m['id'] for m in data.get('data', []) if 'id' in m]
            priority = ['70b', '90b', '32b', '27b', '13b', '9b', '8b', '7b']
            def model_priority(mid):
                ml = mid.lower()
                for i, p in enumerate(priority):
                    if p in ml:
                        return i
                return len(priority)
            models.sort(key=model_priority)
            if models:
                with _model_cache_lock:
                    _model_cache[api_key] = models
                return models
    except Exception:
        pass
    with _model_cache_lock:
        _model_cache[api_key] = FREE_MODELS_FALLBACK[:]
    return FREE_MODELS_FALLBACK[:]

def is_safe_request(req):
    user_agent = req.headers.get('User-Agent', '').lower()
    for bot in ['curl', 'wget', 'python-requests', 'postman', 'insomnia']:
        if bot in user_agent:
            return False
    return True

def load_user_keys():
    keys = []
    env_keys = os.getenv('USER_KEYS', '')
    if env_keys:
        for k in env_keys.split(','):
            k = k.strip()
            if k and k not in keys:
                keys.append(k)
                
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for p in [os.path.join(base_dir, 'user_keys.txt'), 'user_keys.txt', '../user_keys.txt']:
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                for line in f:
                    k = line.strip()
                    if k and k not in keys:
                        keys.append(k)
            if keys:
                break
    return keys

def load_keys():
    keys = []
    env_keys = os.getenv('GROQ_KEYS', '')
    if env_keys:
        for k in env_keys.split(','):
            k = k.strip()
            if k and k not in keys:
                keys.append(k)
                
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for p in [os.path.join(base_dir, 'groq.txt'), 'groq.txt', '../groq.txt']:
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                for line in f:
                    k = line.strip()
                    if k and k not in keys:
                        keys.append(k)
            if keys:
                break
    return keys

def clean_answer(answer):
    answer = answer.strip().strip('"\'')
    answer = re.sub(r'[.,!?;:()\[\]{}]', '', answer)
    answer = re.sub(r'^(đáp án:|answer:|a:|ans:)\s*', '', answer, flags=re.IGNORECASE)
    return answer.strip().lower()

def build_prompt(question):
    is_viet = any(c in question for c in
        'àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợ'
        'ùúủũụưứừửữựỳýỷỹỵđÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊ'
        'ÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴĐ')
    if is_viet:
        return (
            "Bạn là bot trả lời captcha. Trả lời BẰNG TIẾNG VIỆT, ngắn nhất có thể (1-3 từ tối đa).\n"
            "Quy tắc TUYỆT ĐỐI:\n"
            "- Chỉ trả lời từ/cụm từ, KHÔNG giải thích, KHÔNG câu đầy đủ\n"
            "- Toán học: chỉ ghi kết quả là số\n"
            "- Màu sắc, động vật, đồ vật: tên tiếng Việt\n"
            "- Không dùng dấu chấm, phẩy hay ký tự thừa\n"
            "- KHÔNG được trả lời bằng tiếng Anh\n\n"
            f"Câu hỏi: {question}\nĐáp án:"
        )
    return (
        "Captcha bot. English answer only, 1-3 words max, no punctuation.\n"
        "Math: number only. Colors/animals: exact English name.\n\n"
        f"Question: {question}\nAnswer:"
    )

@app.route('/campc', methods=['GET'])
def flask_serve_loader_js():
    if not is_safe_request(request):
        return Response(fake_404, status=200, mimetype='text/html')
        
    user_key = request.args.get('user_key', '').strip()
    valid_user_keys = load_user_keys()
    if not user_key or (valid_user_keys and user_key not in valid_user_keys):
        return Response(fake_404, status=200, mimetype='text/html')

    payload_url = request.host_url.rstrip('/') + f'/api/payload?user_key={user_key}'
    loader_script = f"""
    (async function() {{
        try {{
            const req = await fetch('{payload_url}&_t=' + Date.now());
            if (req.ok) {{
                const code = await req.text();
                new Function(code)();
            }}
        }} catch(e) {{}}
    }})();
    """
    import base64
    encoded_loader = base64.b64encode(loader_script.encode('utf-8')).decode('utf-8')
    final_loader = f"Function(decodeURIComponent(escape(atob('{encoded_loader}'))))();"
    return Response(final_loader, mimetype='application/javascript')

@app.route('/api/payload', methods=['GET'])
def flask_serve_payload_js():
    if not is_safe_request(request):
        return Response(fake_404, status=200, mimetype='text/html')
        
    user_key = request.args.get('user_key', '').strip()
    valid_user_keys = load_user_keys()
    if not user_key or (valid_user_keys and user_key not in valid_user_keys):
        return Response(fake_404, status=200, mimetype='text/html')

    api_url = request.host_url.rstrip('/') + '/api/solve'
    import string
    def r_name(length=10):
        return ''.join(random.choices(string.ascii_letters, k=length))
    def js_str(s):
        chars = [str(ord(c)) for c in s]
        return f"String.fromCharCode({','.join(chars)})"
    v = {k: r_name() for k in [
        'qS', 'qSA', 'Time', 'sleep', 'now', 'simulateMouseClick',
        'solveWithServer', 'switchToTextChallenge', 'getTask',
        'isTaskRunning', 'checkAndSolve', 'rect', 'targetX', 'targetY',
        'currX', 'currY', 'steps', 'eventNames', 'eventName', 'detail',
        'evt', 'fulltask', 'query', 'res', 'data', 'menu',
        'textChBtn', 'lastQuestion', 'lastAnswer', 'startTime', 'headerEl',
        'questionEl', 'fixedString', 'inp', 'nativeSetter', 'submitBtn',
        'anchor', 'isChecked', 'apiUrl', 'uKey', 'i', 'el'
    ]}
    script = f"""
(() => {{
    'use strict';
    const {v['apiUrl']} = '{api_url}';
    const {v['uKey']} = '{user_key}';
    const {v['Time']} = (() => {{
        const {v['sleep']} = ({v['i']} = 1000) => new Promise((resolve) => setTimeout(resolve, {v['i']}));
        const {v['now']} = () => Date.now ? Date.now() : new Date().getTime();
        return {{ '{v['sleep']}': {v['sleep']}, '{v['now']}': {v['now']} }};
    }})();
    const {v['qS']} = document.querySelector.bind(document);
    const {v['qSA']} = document.querySelectorAll.bind(document);
    const {v['simulateMouseClick']} = ({v['el']}) => {{
        if (!{v['el']}) return false;
        try {{
            const {v['rect']} = {v['el']}.getBoundingClientRect();
            const {v['targetX']} = {v['rect']}.x + {v['rect']}.width / 2;
            const {v['targetY']} = {v['rect']}.y + {v['rect']}.height / 2;
            let {v['currX']} = {v['targetX']} - 50 - Math.random() * 100;
            let {v['currY']} = {v['targetY']} - 50 - Math.random() * 100;
            const {v['steps']} = 10;
            for (let {v['i']} = 1; {v['i']} <= {v['steps']}; {v['i']}++) {{
                {v['currX']} += ({v['targetX']} - {v['currX']}) * ({v['i']} / {v['steps']}) + (Math.random() - 0.5) * 5;
                {v['currY']} += ({v['targetY']} - {v['currY']}) * ({v['i']} / {v['steps']}) + (Math.random() - 0.5) * 5;
                window.dispatchEvent(new MouseEvent({js_str('mousemove')}, {{ bubbles: true, cancelable: true, clientX: {v['currX']}, clientY: {v['currY']} }}));
            }}
            const {v['eventNames']} = [{js_str('mouseover')}, {js_str('mouseenter')}, {js_str('mousedown')}, {js_str('mouseup')}, {js_str('click')}, {js_str('mouseout')}];
            {v['eventNames']}.forEach(({v['eventName']}) => {{
                const {v['detail']} = {v['eventName']} === {js_str('mouseover')} ? 0 : 1;
                const {v['evt']} = new MouseEvent({v['eventName']}, {{ detail: {v['detail']}, view: window, bubbles: true, cancelable: true, clientX: {v['targetX']}, clientY: {v['targetY']} }});
                {v['el']}.dispatchEvent({v['evt']});
            }});
            return true;
        }} catch (e) {{ return false; }}
    }};
    const {v['solveWithServer']} = async ({v['fulltask']}) => {{
        const {v['query']} = ({v['fulltask']} || '').trim();
        if (!{v['query']}) return '';
        try {{
            const {v['res']} = await fetch({v['apiUrl']}, {{
                method: {js_str('POST')},
                headers: {{ [{js_str('Content-Type')}]: {js_str('application/json')} }},
                body: JSON.stringify({{ question: {v['query']}, user_key: {v['uKey']} }})
            }});
            if ({v['res']}.status === 403) {{ {v['isTaskRunning']} = false; return ''; }}
            if ({v['res']}.ok) {{
                const {v['data']} = await {v['res']}.json();
                if ({v['data']}.answer) return {v['data']}.answer;
            }}
        }} catch (e) {{}}
        return '';
    }};
    const {v['switchToTextChallenge']} = async () => {{
        if ({v['qS']}({js_str('.challenge-input')}) || {v['qS']}({js_str('input[type="text"]')})) return;
        for (let {v['i']} = 0; {v['i']} < 5; {v['i']}++) {{
            if ({v['qS']}({js_str('.challenge-input')}) || {v['qS']}({js_str('input[type="text"]')})) return;
            const {v['menu']} = {v['qS']}({js_str('.accessibility-button')}) || {v['qS']}({js_str('#menu-info')}) || {v['qS']}({js_str('.challenge-container .menu')}) || {v['qS']}({js_str('[title="Menu"]')}) || {v['qS']}({js_str('[aria-label="Menu"]')}) || {v['qS']}({js_str('.menu-icon')});
            if ({v['menu']}) {{ {v['simulateMouseClick']}({v['menu']}); await {v['Time']}['{v['sleep']}'](30); }}
            const {v['textChBtn']} = {v['qS']}({js_str('#text_challenge')}) || {v['qS']}({js_str('.text-challenge-button')}) || {v['qS']}({js_str('[title="Text Challenge"]')}) || Array.from({v['qSA']}({js_str('div, button')})).find(e => e[{js_str('innerText')}] && e[{js_str('innerText')}].toLowerCase().includes({js_str('text challenge')}));
            if ({v['textChBtn']}) {{ {v['simulateMouseClick']}({v['textChBtn']}); await {v['Time']}['{v['sleep']}'](50); }} else {{ await {v['Time']}['{v['sleep']}'](30); }}
        }}
    }};
    const {v['getTask']} = async () => {{
        let {v['lastQuestion']} = null;
        let {v['lastAnswer']} = null;
        const {v['startTime']} = {v['Time']}['{v['now']}']();
        while (true) {{
            if ({v['Time']}['{v['now']}']() - {v['startTime']} > 120000) break;
            if (!{v['qS']}({js_str('.challenge-container')}) && !{v['qS']}({js_str('#menu-info')}) && !{v['qS']}({js_str('.button-submit')})) break;
            await {v['switchToTextChallenge']}();
            try {{
                const {v['headerEl']} = {v['qS']}({js_str('#prompt-question')});
                const {v['questionEl']} = {v['qS']}({js_str('[id^="prompt-text"]')});
                if (!{v['headerEl']} && !{v['questionEl']}) {{ await {v['Time']}['{v['sleep']}'](30); continue; }}
                let {v['query']} = "";
                if ({v['headerEl']} && {v['headerEl']}.innerText) {v['query']} += {v['headerEl']}.innerText.trim() + " ";
                if ({v['questionEl']} && {v['questionEl']}.innerText && {v['questionEl']}.id !== {js_str('prompt-question')}) {v['query']} += {v['questionEl']}.innerText.trim();
                {v['query']} = {v['query']}.trim();
                if (!{v['query']} || {v['query']} === {v['lastQuestion']}) {{ await {v['Time']}['{v['sleep']}'](30); continue; }}
                const {v['fixedString']} = await {v['solveWithServer']}({v['query']});
                {v['lastQuestion']} = {v['query']};
                {v['lastAnswer']} = {v['fixedString']};
                if (!{v['fixedString']}) {{ await {v['Time']}['{v['sleep']}'](100); continue; }}
                let {v['inp']} = {v['qS']}({js_str('div.challenge-input input')}) || {v['qS']}({js_str('input[type="text"]')});
                if ({v['inp']}) {{
                    {v['simulateMouseClick']}({v['inp']});
                    await {v['Time']}['{v['sleep']}'](10);
                    try {{
                        const {v['nativeSetter']} = Object.getOwnPropertyDescriptor(Object.getPrototypeOf({v['inp']}), {js_str('value')})?.set;
                        if ({v['nativeSetter']}) {{ {v['nativeSetter']}.call({v['inp']}, {v['fixedString']}); }} else {{ {v['inp']}.value = {v['fixedString']}; }}
                        {v['inp']}.dispatchEvent(new Event({js_str('input')}, {{ bubbles: true }}));
                    }} catch(e) {{
                        {v['inp']}.value = {v['fixedString']};
                        {v['inp']}.dispatchEvent(new Event({js_str('input')}, {{ bubbles: true }}));
                    }}
                    {v['inp']}.dispatchEvent(new Event({js_str('change')}, {{ bubbles: true }}));
                    await {v['Time']}['{v['sleep']}'](5);
                }}
                const {v['submitBtn']} = {v['qS']}({js_str('.button-submit')});
                if ({v['submitBtn']}) {{ {v['simulateMouseClick']}({v['submitBtn']}); await {v['Time']}['{v['sleep']}'](5); }}
            }} catch (e) {{ await {v['Time']}['{v['sleep']}'](20); }}
        }}
    }};
    let {v['isTaskRunning']} = false;
    const {v['checkAndSolve']} = async () => {{
        if ({v['isTaskRunning']}) return;
        const {v['anchor']} = {v['qS']}({js_str('#anchor')});
        if ({v['anchor']} && !{v['qS']}({js_str('.challenge-container')})) {{
            const {v['isChecked']} = {v['anchor']}.getAttribute({js_str('aria-checked')}) === {js_str('true')};
            if (!{v['isChecked']}) {{
                {v['isTaskRunning']} = true;
                {v['simulateMouseClick']}({v['anchor']});
                await {v['Time']}['{v['sleep']}'](5);
                {v['isTaskRunning']} = false;
            }}
            return;
        }}
        if ({v['qS']}({js_str('.challenge-container')}) || {v['qS']}({js_str('#menu-info')}) || {v['qS']}({js_str('.button-submit')})) {{
            {v['isTaskRunning']} = true;
            await {v['getTask']}();
            {v['isTaskRunning']} = false;
        }}
    }};
    setInterval({v['checkAndSolve']}, 10);
    {v['checkAndSolve']}();
}})();
"""
    import base64
    import urllib.parse
    encoded_url = urllib.parse.quote(script)
    xor_key = random.randint(10, 200)
    xor_encrypted = [ord(c) ^ xor_key for c in encoded_url]
    hex_array = [f"0x{x:02x}" for x in xor_encrypted]
    hex_str = ",".join(hex_array)
    decoder_func = r_name(8)
    arr_name = r_name(8)
    i_var = r_name(4)
    char_var = r_name(4)
    str_var = r_name(4)
    obfuscator_template = f"""(function(){{
        var {arr_name} = [{hex_str}];
        var {decoder_func} = function() {{
            var {str_var} = '';
            for (var {i_var} = 0; {i_var} < {arr_name}.length; {i_var}++) {{
                var {char_var} = {arr_name}[{i_var}] ^ {xor_key};
                {str_var} += String.fromCharCode({char_var});
            }}
            return decodeURIComponent({str_var});
        }};
        var run = new Function({decoder_func}());
        run();
    }})();"""
    final_encoded = base64.b64encode(obfuscator_template.encode('utf-8')).decode('utf-8')
    obfuscated_script = f"Function(decodeURIComponent(escape(atob('{final_encoded}'))))();"
    return Response(obfuscated_script, mimetype='application/javascript')

@app.route('/api/solve', methods=['POST', 'OPTIONS'])
def solve_captcha():
    if request.method == 'OPTIONS':
        return '', 200
    if not is_safe_request(request):
        return Response(fake_404, status=200, mimetype='text/html')

    data = request.json
    if not data or 'question' not in data:
        return Response(fake_404, status=200, mimetype='text/html')
        
    provided_user_key = data.get('user_key', '').strip()
    valid_user_keys = load_user_keys()
    if not provided_user_key or (valid_user_keys and provided_user_key not in valid_user_keys):
        return Response(fake_404, status=200, mimetype='text/html')

    question = data['question']
    keys = load_keys()
    if not keys:
        return jsonify({'error': 'No API keys available'}), 500

    system_prompt = build_prompt(question)

    for api_key in keys:
        models = fetch_models_for_key(api_key)
        key_exhausted = False

        for model in models:
            try:
                resp = requests.post(
                    'https://api.groq.com/openai/v1/chat/completions',
                    headers={
                        'Authorization': f'Bearer {api_key}',
                        'Content-Type': 'application/json'
                    },
                    json={
                        'model': model,
                        'messages': [{'role': 'user', 'content': system_prompt}],
                        'temperature': 0,
                        'max_tokens': 12,
                        'stop': ['\n', '.', ',']
                    },
                    timeout=8
                )

                if resp.status_code == 200:
                    resp_data = resp.json()
                    raw = resp_data.get('choices', [{}])[0].get('message', {}).get('content', '')
                    if raw:
                        answer = clean_answer(raw)
                        if 0 < len(answer) < 50:
                            return jsonify({'answer': answer})

                elif resp.status_code == 429:
                    key_exhausted = True
                    with _model_cache_lock:
                        _model_cache.pop(api_key, None)
                    break

                elif resp.status_code in (401, 403):
                    key_exhausted = True
                    break

            except Exception:
                continue

        if key_exhausted:
            continue

    return jsonify({'error': 'All keys and models failed'}), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return Response(fake_404, status=200, mimetype='text/html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
