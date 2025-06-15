from flask import Flask, request, jsonify, render_template_string
from llama_cpp import Llama
import logging
import os

# حساب المسار المطلق للنموذج مرة واحدة
MODEL_FILE = "DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf"
model_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../model", MODEL_FILE)
)

# طباعة DEBUG
print(f"[DEBUG] Looking for model at: {model_path}")
print(f"[DEBUG] Exists? {os.path.exists(model_path)}")

# ضبط اللوج
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# تهيئة نموذج GGUF عبر llama-cpp-python
logger.info(f"Loading GGUF model from {model_path}")
try:
    llm = Llama(model_path=model_path)
except Exception as e:
    logger.error(f"Failed to load GGUF model: {e}")
    exit(1)

# صفحة الواجهة الرئيسية
INDEX_HTML = """
<!DOCTYPE html>
<html lang="ar">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>DeepSeek Chat</title>
  <style>
    body { font-family: sans-serif; margin: 2rem; }
    textarea { width: 100%; height: 100px; }
    #output { white-space: pre-wrap; margin-top: 1rem; background: #f4f4f4; padding: 1rem; }
    button { padding: 0.5rem 1rem; margin-top: 0.5rem; }
  </style>
</head>
<body>
  <h1>DeepSeek Chat</h1>
  <textarea id="prompt" placeholder="أدخل النص هنا..."></textarea><br />
  <button onclick="sendPrompt()">أرسل</button>
  <div id="output"></div>

  <script>
    async function sendPrompt() {
      const prompt = document.getElementById('prompt').value;
      if (!prompt) return alert('الرجاء إدخال نص.');
      document.getElementById('output').innerText = 'جاري المعالجة...';
      try {
        const res = await fetch('/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ prompt: prompt })
        });
        if (!res.ok) throw new Error('فشل الطلب');
        const data = await res.json();
        document.getElementById('output').innerText = data.generated_text;
      } catch (err) {
        document.getElementById('output').innerText = 'حدث خطأ: ' + err.message;
      }
    }
  </script>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(INDEX_HTML)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json(force=True)
    prompt = data.get('prompt', '')
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    try:
        response = llm(prompt, max_tokens=512, temperature=0.7)
        generated = response.get('choices', [{}])[0].get('text', '')
    except Exception as e:
        logger.error(f"Generation error: {e}")
        return jsonify({'error': 'Generation failed'}), 500

    logger.info(f"Generated text length: {len(generated)}")
    return jsonify({'generated_text': generated})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
