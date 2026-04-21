from flask import Flask, request, send_file
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

# Petite page d'accueil pour tester
@app.route('/remove-bg', methods=['GET'])
def test_serveur():
    return "👋 Coucou ! Le serveur de détourage est bien allumé !"

# La fonction qui reçoit la photo et enlève le fond
@app.route('/remove-bg', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return 'Erreur : Aucune image reçue', 400
        
    file = request.files['image']
    input_image = Image.open(file.stream)
    
    # 🪄 MAGIE DU DÉTOURAGE
    output_image = remove(input_image)
    
    # Préparation du fichier PNG transparent
    img_byte_arr = io.BytesIO()
    output_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    return send_file(img_byte_arr, mimetype='image/png')

if __name__ == '__main__':
    # On lance le serveur sur le port 5000
    app.run(host='0.0.0.0', port=5000)