from flask import Flask, request, send_file
from flask_cors import CORS  # Importation pour le lien avec Flutter
from rembg import remove, new_session
from PIL import Image
import io
import os

# --- OPTIMISATION RAM POUR RENDER ---
# On force l'IA à être moins gourmande en ressources
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

app = Flask(__name__)
CORS(app) # Autorise les requêtes provenant de ton app Flutter

# On précharge le modèle "Poids Plume" (u2netp) au démarrage
print("Chargement du modèle IA léger (u2netp)...")
my_session = new_session("u2netp")

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
        
        # On ouvre l'image
        input_image = Image.open(file.stream)
        
        # Détourage avec le modèle léger
        # On utilise la session préchargée pour aller plus vite
        output_image = remove(input_image, session=my_session)
        
        # Préparation de la réponse
        img_byte_arr = io.BytesIO()
        # On enregistre en PNG (obligatoire pour la transparence)
        # 'optimize=True' aide à réduire le poids du fichier final
        output_image.save(img_byte_arr, format='PNG', optimize=True)
        img_byte_arr.seek(0)
        
        print("Détourage réussi et envoyé !")
        return send_file(img_byte_arr, mimetype='image/png')

    except Exception as e:
        print(f"Erreur lors du détourage : {e}")
        return f"Erreur interne : {str(e)}", 500

if __name__ == '__main__':
    # Configuration du port Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
