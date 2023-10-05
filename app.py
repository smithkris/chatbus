from flask import Flask, render_template, request, jsonify
from nltk.chat.util import Chat, reflections
import re

app = Flask(__name__)

# Vos paires de questions/réponses ici
pairs = [
    ["Mon nom c'est (.*)", ["Hello %1☺"]],
    ["(.*)bonjour(.*)|(.*)salut(.*)|(.*)coucou(.*)|(.*)hey(.*)", ["Salut toi☺", "Hello", "en quoi vous aider"]],
    ["(.*)merci(.*)", ["De rien...et à bientot", "De rien ! Si vous avez d'autres questions ou avez besoin d'aide supplémentaire n'hésitez pas à demander"]],
    ["(.*)où est (.*)", ["Voici le lien Google Maps : <a id='google-maps-link' href='https://www.google.com/maps?q=%2' target='_blank'>Lieu recherché</a> vers %1"]],
    ["(.*)contact(.*)|(.*)tél(.*)", ["034 48 354 82"]],
    ["(.*)email(.*)|(.*)mail(.*)|(.*)émail(.*)", ["smith@gmail.com"]],
    ["Quel est votre nom|(.*)ton nom(.*)", ["Mon nom c'est Kristian-boot"]],
    ["Au revoir|(.*)Bye(.*)|Adieu", ["Au revoir ! N'hésitez pas à revenir si vous avez d'autres questions."]],
    ["cava|(.*)cava(.*)|comment allez vous?", ["je vais bien et toi?"]],
    ["je vais bien|(.*)ja vais(.*)", ["C'est encourageant de savoir que vous allez très bien."]],
    ["Qui est votre épouse ?", ["Qui est cette personne?"]],
    ["ok|Ok|OK", ["Okey", "Sur","D'accord"]],
    ["(.*)une blague(.*)|Peux-tu me raconter une blague ?|As-tu une blague amusante à partager ?|Donne-moi un peu d'humour, s'il te plaît !|Racontes-moi une blague drôle.|J'ai besoin de rire, tu as une blague pour ça ?|T'entends une bonne blague récemment ?", 
     ["Pourquoi les plongeurs plongent-ils toujours en arrière et jamais en avant ? Parce que sinon ils tombent dans le bateau", "Qu'est-ce qui est jaune et qui attend ? Jonathan.","Qu'est-ce qui est petit, vert, et qui pique ? Un petit pois avec un cactus.", "Pourquoi les poissons n'utilisent-ils jamais d'ordinateurs ? Parce qu'ils ont peur du net.","Qu'est-ce qui a quatre roues et qui vole ? Une poubelle. J'ai menti à propos des quatre roues.","Quel est le comble pour un électricien ? De ne pas être au courant.","Pourquoi les plongeurs plongent-ils toujours en arrière et jamais en avant ? Parce que sinon ils tombent dans le bateau."]],
    ["c'est drole|(.*)haha(.*)|(.*)drole(.*)", ["hahahaha"]],

]

# Liste des noms de lieux connus
lieux_connus = ["Ambodivona", "Analakely", "Antananarivo", "Mahamasina"]
combinaisons_lieux = {
    ("Analakely", "Ambodivona"): {
        "numero_bus": "Bus N°:157",
        "couleur": "couleur jaune",
        "image": "./static/image/bus1.jpg"
    },
    ("Mahamasina", "Ambodivona"): {
        "numero_bus": "Bus N°:130",
        "couleur": "couleur rouge",
        "image": "./static/image/bus3.jpg"
    },
    ("Ambodivona", "Analakely"): {
        "numero_bus": "Bus N°: 127",
        "couleur": "couleur noir et blanc",
        "image": "./static/image/bus2.jpg"
    },
    # Ajoutez d'autres combinaisons de lieux et leurs informations ici
}

chat = Chat(pairs, reflections)

default_response = "Désolé, je n'ai pas d'informations sur cette demande"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get')
def get_bot_response():
    user_msg = request.args.get('msg')

    # Vérifiez si le mot-clé "bus" est présent dans le message de l'utilisateur
    if "bus" in user_msg.lower():
        lieux_extraits = [lieu.capitalize() for lieu in re.findall(r'\b(?:' + '|'.join(lieux_connus) + r')\b', user_msg, flags=re.IGNORECASE)]

        if len(lieux_extraits) >= 2:
            lieu_depart = lieux_extraits[0]
            lieu_arrivee = lieux_extraits[1]

            combinaison = (lieu_depart, lieu_arrivee)
            if combinaison in combinaisons_lieux:
                info_bus = combinaisons_lieux[combinaison]
                numero_bus = info_bus["numero_bus"]
                couleur = info_bus["couleur"]
                image_url = info_bus["image"]

                response_text = f"{numero_bus} avec de {couleur}."
                response_data = {
                    "response_text": response_text,
                    "image_url": image_url
                }
                return jsonify(response_data)

    response = chat.respond(user_msg)
    if not response:
        response = default_response
    return jsonify({"response_text": response})

if __name__ == '__main__':
    app.run(debug=True)
