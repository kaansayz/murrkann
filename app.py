import os
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

DATA_DIR = 'data'
MASALAR_FILE = os.path.join(DATA_DIR, 'masalar.json')

# Masaların dosyadan yüklenmesi
def load_masalar():
    if not os.path.exists(MASALAR_FILE):
        with open(MASALAR_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False)
    with open(MASALAR_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# Masaların dosyaya kaydedilmesi
def save_masalar(masalar):
    with open(MASALAR_FILE, 'w', encoding='utf-8') as f:
        json.dump(masalar, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    masalar = load_masalar()
    return render_template('index.html', masalar=masalar)

@app.route('/masalar', methods=['GET'])
def get_masalar():
    masalar = load_masalar()
    return jsonify(masalar)

@app.route('/add_masa', methods=['POST'])
def add_masa():
    masalar = load_masalar()
    new_name = request.form['masa_adi']
    if new_name and new_name not in masalar:
        masalar.append(new_name)
        save_masalar(masalar)
    return redirect(url_for('index'))

@app.route('/delete_masa', methods=['POST'])
def delete_masa():
    masalar = load_masalar()
    masa_adi = request.form['masa_adi']
    if masa_adi in masalar:
        masalar.remove(masa_adi)
        save_masalar(masalar)
    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs(DATA_DIR, exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)