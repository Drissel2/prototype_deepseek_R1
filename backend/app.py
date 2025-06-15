from flask import Flask, request, jsonify
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

# نستخدم فقط المتغير model_path الذي تحققنا منه أعلاه
logger.info(f"Loading GGUF model from {model_path}")
try:
    llm = Llama(model_path=model_path)
except Exception as e:
    logger.error(f"Failed to load GGUF model: {e}")
    exit(1)

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
        response = llm(prompt, max_tokens=settings.MAX_LENGTH, temperature=settings.TEMPERATURE)
        generated = response.get('choices', [{}])[0].get('text', '')
    except Exception as e:
        logger.error(f"Generation error: {e}")
        return jsonify({'error': 'Generation failed'}), 500

    logger.info(f"Generated text length: {len(generated)}")
    return jsonify({'generated_text': generated})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
