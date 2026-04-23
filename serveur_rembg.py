from flask import Flask, request, send_file
from flask_cors import CORS
from rembg import remove, new_session
from PIL import Image
import io
import os

# --- OPTIMISATION RAM ---
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

app = Flask(__name__)
CORS(app) 

# Variable globale vide au démarrage pour ne pas bloquer Render
my_session = None

# Fonction qui charge l'IA uniquement quand on en a besoin
def get_model_session():
    global my_session
    if my_session is None:
        print("⏳ Premier lancement : Chargement du modèle u2netp...")
        my_session = new_session("u2netp")
        print("✅ Modèle chargé !")
    return my_session

@app.route('/', methods=['GET'])
def home():
    return "🧠 Le serveur IA de Thezia est en ligne et prêt !"

@app.route('/remove-bg', methods=['GET'])
def test_serveur():
    return "✅ La route de détourage est active. Envoyez une image en POST."

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    try:
        if 'image' not in request.files:
            return 'Erreur : Aucune image reçue', 400
            
        file = request.files['image']
        input_image = Image.open(file.stream)
        
        # On demande le cerveau (il se chargera tout seul si c'est la 1ère fois)
        session_legere = get_model_session()
        
        output_image = remove(input_image, session=session_legere)
        
        img_byte_arr = io.BytesIO()
        output_image.save(img_byte_arr, format='PNG', optimize=True)
        img_byte_arr.seek(0)
        
        print("✅ Détourage réussi et envoyé !")
        return send_file(img_byte_arr, mimetype='image/png')

    except Exception as e:
        print(f"❌ Erreur lors du détourage : {e}")
        return f"Erreur interne : {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    # Flask s'allume instantanément !
    app.run(host='0.0.0.0', port=port)
