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
        body { font-family: 'Plus Jakarta Sans', sans-serif; background: #030014; overflow: hidden; position: relative; }
        #spaceCanvas { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 1; pointer-events: none; }
        .main-card { position: relative; z-index: 10; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); background: rgba(13, 11, 36, 0.75); border: 1px solid rgba(139, 92, 246, 0.3); box-shadow: 0 0 50px rgba(124, 58, 237, 0.25), 0 20px 50px rgba(0, 0, 0, 0.9); }
        .cosmic-title { background: linear-gradient(90deg, #c084fc, #60a5fa, #f472b6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 0 0 20px rgba(192, 132, 252, 0.4); }
        input[type=range] { -webkit-appearance: none; width: 100%; background: transparent; }
        input[type=range]:focus { outline: none; }
        input[type=range]::-webkit-slider-runnable-track { width: 100%; height: 4px; cursor: pointer; background: #1e1b4b; border-radius: 2px; }
        input[type=range]::-webkit-slider-thumb { height: 12px; width: 12px; border-radius: 50%; background: #a855f7; box-shadow: 0 0 10px #a855f7; cursor: pointer; -webkit-appearance: none; margin-top: -4px; }
    </style>
</head>
<body class="min-h-screen flex items-center justify-center p-4">
    <canvas id="spaceCanvas"></canvas>
    <button id="toggleVolume" class="fixed top-5 left-5 z-20 text-purple-400 hover:text-pink-300 transition">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072M18.364 5.636a9 9 0 010 12.728M11 5L6 9H2v6h4l5 4V5z"/></svg>
    </button>
    <div id="enterOverlay" class="fixed inset-0 bg-[#030014]/90 z-50 flex items-center justify-center cursor-pointer transition-opacity duration-500">
        <p class="text-purple-300 font-mono text-sm tracking-widest animate-pulse drop-shadow-[0_0_10px_rgba(168,85,247,0.8)]">[ CLICK TO ENTER THE GALAXY ]</p>
    </div>
    <div class="main-card rounded-2xl p-6 md:p-8 max-w-lg w-full text-center flex flex-col items-center">
        <div class="w-full bg-[#07051a]/90 border border-purple-900/50 rounded-xl p-4 mb-6 overflow-hidden flex items-center justify-center shadow-inner relative">
            <div class="absolute inset-0 flex items-center justify-center bg-purple-950/30 backdrop-blur-[2px]">
                <span class="cosmic-title text-xl md:text-2xl font-black tracking-widest uppercase px-5 py-2 bg-[#030014]/80 border border-purple-500/60 rounded-xl shadow-[0_0_25px_rgba(168,85,247,0.6)]">Hoang Phat Solver</span>
            </div>
        </div>
        <div class="inline-block bg-purple-950/80 border border-purple-600/50 text-purple-300 text-xs font-bold px-4 py-1.5 rounded-full mb-3 tracking-wide shadow-[0_0_12px_rgba(168,85,247,0.3)]">CamPC Real</div>
        <h1 class="cosmic-title text-2xl font-extrabold tracking-wider mb-6">Hoang Phat Solver</h1>
        <div class="w-full bg-[#07051a]/80 border border-purple-900/40 rounded-xl p-4 flex flex-col gap-2 shadow-lg">
            <div class="flex items-center justify-between text-xs text-purple-300/80">
                <div class="flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-pink-500 animate-ping"></span><span class="font-medium text-purple-200">Cosmic Night Stories</span></div>
                <div class="font-mono text-purple-400"><span id="currentTime">0:00</span> / <span id="duration">0:00</span></div>
            </div>
            <input type="range" id="seekBar" value="0" min="0" max="100" class="w-full">
            <div class="flex items-center justify-center gap-4 pt-1">
                <button id="playBtn" class="text-white hover:text-purple-200 transition bg-purple-600/40 p-2.5 rounded-full border border-purple-500/50 shadow-[0_0_15px_rgba(168,85,247,0.5)]">
                    <svg id="playIcon" class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                </button>
            </div>
        </div>
    </div>
    <audio id="bgMusic" loop src="https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=lofi-study-112191.mp3"></audio>
    <script>
        const canvas = document.getElementById('spaceCanvas'), ctx = canvas.getContext('2d');
        let w, h;
        function resize() { w = canvas.width = window.innerWidth; h = canvas.height = window.innerHeight; }
        window.addEventListener('resize', resize); resize();
        const stars = Array.from({length: 220}, () => ({ x: Math.random()*w, y: Math.random()*h, radius: Math.random()*1.5+0.3, color: ['#ffffff','#a855f7','#60a5fa','#f472b6'][Math.floor(Math.random()*4)], alpha: Math.random(), speed: Math.random()*0.02+0.005 }));
        const planets = [{x:w*.12,y:h*.2,r:28,color:'#8b5cf6',ring:true,vx:.15,vy:.08,glow:'rgba(139,92,246,.4)'},{x:w*.85,y:h*.75,r:42,color:'#ec4899',ring:true,vx:-.1,vy:-.12,glow:'rgba(236,72,153,.35)'},{x:w*.82,y:h*.18,r:18,color:'#3b82f6',ring:false,vx:-.08,vy:.1,glow:'rgba(59,130,246,.4)'},{x:w*.15,y:h*.82,r:22,color:'#c084fc',ring:false,vx:.12,vy:-.06,glow:'rgba(192,132,252,.3)'}];
        const meteors = [];
        function drawSpace() {
            ctx.clearRect(0,0,w,h);
            [['rgba(124,58,237,.18)',w*.2,h*.25,450],['rgba(236,72,153,.15)',w*.8,h*.75,500]].forEach(([c,x,y,r])=>{ const g=ctx.createRadialGradient(x,y,50,x,y,r); g.addColorStop(0,c); g.addColorStop(1,'transparent'); ctx.fillStyle=g; ctx.fillRect(0,0,w,h); });
            stars.forEach(s=>{ s.alpha+=s.speed; if(s.alpha>1||s.alpha<0)s.speed=-s.speed; ctx.beginPath(); ctx.arc(s.x,s.y,s.radius,0,Math.PI*2); ctx.fillStyle=s.color; ctx.globalAlpha=Math.abs(s.alpha); ctx.fill(); }); ctx.globalAlpha=1;
            planets.forEach(p=>{ p.x+=p.vx; p.y+=p.vy; if(p.x<-100)p.x=w+100; if(p.x>w+100)p.x=-100; if(p.y<-100)p.y=h+100; if(p.y>h+100)p.y=-100; const gw=ctx.createRadialGradient(p.x,p.y,p.r*.5,p.x,p.y,p.r*2); gw.addColorStop(0,p.glow); gw.addColorStop(1,'transparent'); ctx.fillStyle=gw; ctx.beginPath(); ctx.arc(p.x,p.y,p.r*2,0,Math.PI*2); ctx.fill(); const pg=ctx.createLinearGradient(p.x-p.r,p.y-p.r,p.x+p.r,p.y+p.r); pg.addColorStop(0,p.color); pg.addColorStop(1,'#0f0c29'); ctx.fillStyle=pg; ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2); ctx.fill(); if(p.ring){ctx.save();ctx.translate(p.x,p.y);ctx.rotate(-Math.PI/6);ctx.beginPath();ctx.ellipse(0,0,p.r*2.2,p.r*.5,0,0,Math.PI*2);ctx.strokeStyle=p.glow;ctx.lineWidth=3;ctx.stroke();ctx.restore();} });
            if(Math.random()<.04)meteors.push({x:Math.random()*(w*1.2),y:-50,len:Math.random()*90+60,speed:Math.random()*12+8,size:Math.random()*2+1,color:Math.random()>.5?'#a855f7':'#60a5fa'});
            for(let i=meteors.length-1;i>=0;i--){const m=meteors[i];const g=ctx.createLinearGradient(m.x,m.y,m.x-m.len,m.y+m.len);g.addColorStop(0,m.color);g.addColorStop(1,'transparent');ctx.strokeStyle=g;ctx.lineWidth=m.size;ctx.beginPath();ctx.moveTo(m.x,m.y);ctx.lineTo(m.x-m.len,m.y+m.len);ctx.stroke();ctx.beginPath();ctx.arc(m.x,m.y,m.size*1.5,0,Math.PI*2);ctx.fillStyle='#fff';ctx.fill();m.x+=m.speed;m.y+=m.speed;if(m.y>h+100||m.x>w+100)meteors.splice(i,1);}
            requestAnimationFrame(drawSpace);
        }
        drawSpace();
        const audio=document.getElementById('bgMusic'),overlay=document.getElementById('enterOverlay'),playBtn=document.getElementById('playBtn'),playIcon=document.getElementById('playIcon'),seekBar=document.getElementById('seekBar'),currentTimeEl=document.getElementById('currentTime'),durationEl=document.getElementById('duration');
        let isPlaying=false;
        const fmt=s=>isNaN(s)?'0:00':`${Math.floor(s/60)}:${String(Math.floor(s%60)).padStart(2,'0')}`;
        const togglePlay=()=>{ if(isPlaying){audio.pause();playIcon.innerHTML='<path d="M8 5v14l11-7z"/>';}else{audio.play();playIcon.innerHTML='<path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>';} isPlaying=!isPlaying; };
        overlay.addEventListener('click',()=>{ overlay.classList.add('opacity-0'); setTimeout(()=>overlay.remove(),500); audio.play(); isPlaying=true; playIcon.innerHTML='<path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>'; });
        playBtn.addEventListener('click',togglePlay);
        audio.addEventListener('loadedmetadata',()=>durationEl.innerText=fmt(audio.duration));
        audio.addEventListener('timeupdate',()=>{ currentTimeEl.innerText=fmt(audio.currentTime); if(audio.duration)seekBar.value=(audio.currentTime/audio.duration)*100; });
        seekBar.addEventListener('input',()=>{ if(audio.duration)audio.currentTime=(seekBar.value/100)*audio.duration; });
    </script>
</body>
</html>"""

# =============================================================================
# LOCAL SOLVERS -- Giai truc tiep, khong can goi API
# =============================================================================

# ---------------------------------------------------------------------------
# [DANG 1] CAU DO DICH CHUYEN CHU CAI (Letter Shift Puzzle)
# ---------------------------------------------------------------------------
#
# QUY TAC 3 BUOC:
#
# BUOC 1 — XAC DINH TU GOC (Word)
#   Tim tu nam o cuoi cau do, thuong dung sau cum "in the word ...".
#   Vi du: "...in the word route" -> tu goc la: r-o-u-t-e
#
# BUOC 2 — XAC DINH VI TRI CAN THAY (Position)
#   Doc tu chi thu tu de biet phai sua chu cai thu may:
#     first  / 1st  -> chu thu 1  (index 0)
#     second / 2nd  -> chu thu 2  (index 1)
#     third  / 3rd  -> chu thu 3  (index 2)
#     fourth / 4th  -> chu thu 4  (index 3)
#     ...v.v. den tenth / 10th
#
# BUOC 3 — DOI CHU CAI SANG VI TRI TIEP THEO (+1 Alphabet)
#   Lay chu cai tai vi tri do va thay bang chu ngay sau no:
#     a->b, b->c, c->d, ..., y->z, z->a  (vong lai)
#   Giu nguyen cac chu cai con lai trong tu.
#
# VI DU MINH HOA:
#   De bai : "Change the third letter to the following alphabet letter
#              in the word route"
#   Tu goc : r - o - u - t - e
#   Vi tri 3: chu 'u'
#   Chu lien sau 'u': chu 'v'
#   Dap an : r - o - V - t - e  =>  "rovte"
#
# BANG CHU CAI THAM CHIEU (+1):
#   a->b  b->c  c->d  d->e  e->f  f->g  g->h  h->i  i->j
#   j->k  k->l  l->m  m->n  n->o  o->p  p->q  q->r  r->s
#   s->t  t->u  u->v  v->w  w->x  x->y  y->z  z->a (vong)
# ---------------------------------------------------------------------------

# Ban do so thu tu -> chi so 0-based
_ORDINAL_MAP = {
    'first': 0,   '1st': 0,
    'second': 1,  '2nd': 1,
    'third': 2,   '3rd': 2,
    'fourth': 3,  '4th': 3,
    'fifth': 4,   '5th': 4,
    'sixth': 5,   '6th': 5,
    'seventh': 6, '7th': 6,
    'eighth': 7,  '8th': 7,
    'ninth': 8,   '9th': 8,
    'tenth': 9,   '10th': 9,
}

# Cac cum tu nhan dang dang cau do dich chuyen chu cai +1
_LETTER_SHIFT_TRIGGERS = [
    'following alphabet letter',
    'next alphabet letter',
    'next letter in the alphabet',
    'following letter in the alphabet',
    'next letter of the alphabet',
    'following letter of the alphabet',
]


def solve_letter_shift(question: str):
    """
    [DANG 1] Giai cau do dich chuyen chu cai (+1 Alphabet).

    QUY TAC 3 BUOC:
    ---------------
    BUOC 1 — Xac dinh tu goc:
        Tim tu dung sau "in the word ..." hoac "of the word ...".
        Vi du: "...in the word route" -> word = "route"

    BUOC 2 — Xac dinh vi tri can thay:
        Doc tu chi thu tu (first/1st, second/2nd, third/3rd, ...).
        Vi du: "third" -> vi tri 3 -> index 2 (0-based)

    BUOC 3 — Doi chu cai sang vi tri ke tiep trong alphabet (+1):
        Lay chu tai vi tri do, thay bang chu ngay sau no.
        Quy tac: a->b, b->c, ..., y->z, z->a (vong lai).
        Giu nguyen tat ca chu cai con lai.

    Vi du day du:
        Input : "Change the third letter to the following alphabet letter in the word route"
        Word  : r-o-u-t-e
        Vi tri: thu 3 -> index 2 -> chu 'u'
        Shift : u -> v
        Output: "rovte"

    Returns:
        str  -- dap an neu nhan dang va giai duoc
        None -- neu khong phai dang cau do nay
    """
    q = question.lower().strip()

    # BUOC 1: Kiem tra tu khoa nhan dang dang cau do nay
    if not any(phrase in q for phrase in _LETTER_SHIFT_TRIGGERS):
        return None

    # BUOC 2a: Trich xuat tu goc sau "in the word" / "of the word"
    word_match = re.search(r'(?:in|of) the word\s+([a-z]+)', q)
    if not word_match:
        return None
    word = word_match.group(1)
    # Vi du: word = "route" -> ['r','o','u','t','e']

    # BUOC 2b: Xac dinh vi tri (so thu tu) can thay
    idx = None
    for token, zero_idx in _ORDINAL_MAP.items():
        # Dung word boundary de tranh nham (vi du: 'second' trong 'secondary')
        if re.search(r'\b' + re.escape(token) + r'\b', q):
            idx = zero_idx  # chuyen sang 0-based index
            break

    if idx is None or idx >= len(word):
        return None

    # BUOC 3: Doi chu cai tai vi tri do sang chu ke tiep (+1)
    # Bang tham chieu: a->b, b->c, ..., y->z, z->a
    original_char = word[idx]
    new_char = 'a' if original_char == 'z' else chr(ord(original_char) + 1)

    # Ghep lai thanh tu hoan chinh, giu nguyen phan con lai
    result = word[:idx] + new_char + word[idx + 1:]
    return result


def try_local_solvers(question: str):
    """
    Thu tat ca cac bo giai cuc bo theo thu tu uu tien.
    Tra ve dap an (str) neu giai duoc, hoac None neu khong.
    Them cac solver moi o day khi can.
    """
    answer = solve_letter_shift(question)
    if answer:
        return answer
    return None


# =============================================================================
# GROQ / LLM helpers
# =============================================================================

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
    answer = re.sub(r'^(dap an:|answer:|a:|ans:)\s*', '', answer, flags=re.IGNORECASE)
    return answer.strip().lower()


def build_prompt(question):
    is_viet = any(c in question for c in
        '\u00e0\u00e1\u1ea3\u00e3\u1ea1\u0103\u1eaf\u1eb1\u1eb3\u1eb5\u1eb7\u00e2\u1ea5\u1ea7\u1ea9\u1eab\u1ead'
        '\u00e8\u00e9\u1ebb\u1ebd\u1eb9\u00ea\u1ebf\u1ec1\u1ec3\u1ec5\u1ec7\u00ec\u00ed\u1ec9\u0129\u1ecb'
        '\u00f2\u00f3\u1ecf\u00f5\u1ecd\u00f4\u1ed1\u1ed3\u1ed5\u1ed7\u1ed9\u01a1\u1edb\u1edd\u1edf\u1ee1\u1ee3'
        '\u00f9\u00fa\u1ee7\u0169\u1ee5\u01b0\u1ee9\u1eeb\u1eed\u1eef\u1ef1\u1ef3\u00fd\u1ef7\u1ef9\u1ef5\u0111'
        '\u00c0\u00c1\u1ea2\u00c3\u1ea0\u0102\u1eae\u1eb0\u1eb2\u1eb4\u1eb6\u00c2\u1ea4\u1ea6\u1ea8\u1eaa\u1eac'
        '\u00c8\u00c9\u1eba\u1ebc\u1eb8\u00ca\u1ebe\u1ec0\u1ec2\u1ec4\u1ec6\u00cc\u00cd\u1ec8\u0128\u1eca'
        '\u00d2\u00d3\u1ece\u00d5\u1ecc\u00d4\u1ed0\u1ed2\u1ed4\u1ed6\u1ed8\u01a0\u1eda\u1edc\u1ede\u1ee0\u1ee2'
        '\u00d9\u00da\u1ee6\u0168\u1ee4\u01af\u1ee8\u1eea\u1eec\u1eee\u1ef0\u1ef2\u00dd\u1ef6\u1ef8\u1ef4\u0110')
    if is_viet:
        return (
            "Ban la bot tra loi captcha. Tra loi BANG TIENG VIET, ngan nhat co the (1-3 tu toi da).\n"
            "Quy tac TUYET DOI:\n"
            "- Chi tra loi tu/cum tu, KHONG giai thich, KHONG cau day du\n"
            "- Toan hoc: chi ghi ket qua la so\n"
            "- Mau sac, dong vat, do vat: ten tieng Viet\n"
            "- Khong dung dau cham, phay hay ky tu thua\n"
            "- KHONG duoc tra loi bang tieng Anh\n\n"
            f"Cau hoi: {question}\nDap an:"
        )
    return (
        "Captcha bot. English answer only, 1-3 words max, no punctuation.\n"
        "Math: number only. Colors/animals: exact English name.\n\n"
        f"Question: {question}\nAnswer:"
    )


# =============================================================================
# ROUTES
# =============================================================================

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

    # -- Uu tien 1: Giai cuc bo (khong ton API quota) --
    local_answer = try_local_solvers(question)
    if local_answer:
        return jsonify({'answer': local_answer})

    # -- Uu tien 2: Goi Groq LLM --
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
