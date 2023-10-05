from flask import Flask, render_template, request, jsonify
from nltk.chat.util import Chat, reflections
import re
from spellchecker import SpellChecker
spell = SpellChecker()



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
    ("Analakely", "Ambodivona"): "157",
    ("Mahamasina", "Ambodivona"): "130",
    ("Ambodivona", "Analakely"): "127",
    # Ajoutez d'autres combinaisons de lieux et leurs réponses ici
}

chat = Chat(pairs, reflections)

default_response = "Je m'excuse, je ne peux pas répondre à cette question. Pouvez-vous la poser de manière différente ?"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get')
def get_bot_response():
    user_msg = request.args.get('msg')
    # user_msg = spell.correction(user_msg)
    # Recherche des noms de lieux dans la question de l'utilisateur
    lieux_extraits = [lieu.capitalize() for lieu in re.findall(r'\b(?:' + '|'.join(lieux_connus) + r')\b', user_msg, flags=re.IGNORECASE)]
    
    if "bus" in user_msg and len(lieux_extraits) >= 2:
        lieu_depart = lieux_extraits[0]
        lieu_arrivee = lieux_extraits[1]
        
        combinaison = (lieu_depart, lieu_arrivee)
        if combinaison in combinaisons_lieux:
            return combinaisons_lieux[combinaison]

    response = chat.respond(user_msg)
    if not response:
        response = default_response
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
