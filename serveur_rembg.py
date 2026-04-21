from flask import Flask, request, send_file
from rembg import remove, new_session
from PIL import Image
import io

app = Flask(__name__)

# On précharge le modèle "Poids Plume" (u2netp)
my_session = new_session("u2netp")

@app.route('/remove-bg', methods=['GET'])
def test_serveur():
    return "👋 Coucou ! Le serveur de détourage Poids Plume est bien allumé !"

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return 'Erreur : Aucune image reçue', 400
        
    file = request.files['image']
    input_image = Image.open(file.stream)
    
    # Détourage avec le modèle léger
    output_image = remove(input_image, session=my_session)
    
    img_byte_arr = io.BytesIO()
    output_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    return send_file(img_byte_arr, mimetype='image/png')

if __name__ == '__main__':
    # Render aime le port 10000
    app.run(host='0.0.0.0', port=10000)
