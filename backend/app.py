from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import logging
from config import settings

# ضبط اللوج
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# تحميل النموذج
logger.info(f"Loading model from {settings.MODEL_PATH}")
tokenizer = AutoTokenizer.from_pretrained(settings.MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(settings.MODEL_PATH)
model.eval()

try:
    logger.info(f"Loading model from {settings.MODEL_PATH}")
    tokenizer = AutoTokenizer.from_pretrained(settings.MODEL_PATH)
    model = AutoModelForCausalLM.from_pretrained(settings.MODEL_PATH)
    model.eval()
except Exception as e:
    logger.error(f"Failed to load model: {e}")
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

    inputs = tokenizer(prompt, return_tensors='pt')
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=settings.MAX_LENGTH,
            do_sample=True,
            temperature=settings.TEMPERATURE,
        )
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    logger.info(f"Generated text length: {len(result)}")
    return jsonify({'generated_text': result})

if __name__ == '__main__':
    app.run(host=settings.HOST, port=settings.PORT)
