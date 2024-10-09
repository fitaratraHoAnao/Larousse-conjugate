from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/conjugate/<verb>', methods=['GET'])
def conjugate(verb):
    url = f'https://www.conjugaison.com/conjugaison/{verb}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Exemple de la manière dont vous pourriez extraire les conjugaisons
        conjugations = {}
        for tense_section in soup.find_all('div', class_='tense-section'):
            tense_name = tense_section.find('h3').get_text(strip=True)
            forms = {}
            for form in tense_section.find_all('li'):
                person = form.find('span', class_='person').get_text(strip=True)
                conjugated_form = form.find('span', class_='form').get_text(strip=True)
                forms[person] = conjugated_form
            conjugations[tense_name] = forms
        
        return jsonify(conjugations)
    else:
        return jsonify({"error": "Échec de la requête"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
