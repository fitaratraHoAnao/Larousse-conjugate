from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Route pour scraper les conjugaisons d'un verbe
@app.route('/conjugate/<verb>', methods=['GET'])
def conjugate_verb(verb):
    url = f'https://www.larousse.fr/conjugaison/francais/{verb}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Trouver la section contenant les conjugaisons
        conjugations_section = soup.find('div', class_='conjugation')

        # Extraire les conjugaisons
        conjugations = {}
        if conjugations_section:
            # Scraper les temps de conjugaison
            for tense in conjugations_section.find_all('table'):
                tense_name = tense.find_previous('h2').get_text(strip=True)
                conjugation_rows = tense.find_all('tr')

                # Dictionnaire pour les conjugaisons par temps
                conjugation_dict = {}
                for row in conjugation_rows:
                    cols = row.find_all('td')
                    if cols:
                        pronoun = cols[0].get_text(strip=True)
                        conjugated_form = cols[1].get_text(strip=True)
                        conjugation_dict[pronoun] = conjugated_form
                
                conjugations[tense_name] = conjugation_dict

        return jsonify(conjugations)
    else:
        return jsonify({"error": "Échec de la requête"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
