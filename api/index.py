from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
import random
import requests
import re
import threading

app = Flask(__name__)
CORS(app)

# Giao diện đơn giản: 1 Card nằm giữa màn hình
fake_404 = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CampC Services</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background: #0d1117;
        }
    </style>
</head>
<body class="min-h-screen flex items-center justify-center p-4">

    <!-- Card căn giữa -->
    <div class="bg-[#161b22] border border-gray-800 rounded-2xl p-6 md:p-8 max-w-sm w-full text-center shadow-2xl flex flex-col items-center">
        
        <!-- Logo Container -->
        <div class="w-48 h-48 bg-white rounded-xl p-3 flex items-center justify-center shadow-lg mb-6 overflow-hidden">
            <img src="https://i.ibb.co/3sL9V44/hsp.jpg" alt="HSP Logo" class="w-full h-full object-contain">
        </div>

        <!-- Title / Link Tag -->
        <div class="inline-block bg-blue-950/60 border border-blue-800/50 text-blue-400 text-xs font-bold px-3 py-1 rounded-full mb-3 tracking-wide">
            CampC Official
        </div>

        <!-- Caption -->
        <h1 class="text-2xl font-extrabold text-white tracking-wider">
            AE HSP
        </h1>
    </div>

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
