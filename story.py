import groqaikey
import json

from groqaiapi import *


system_message = """Tu es créateur d'histoires pour enfants. Tu crée des histoires simples, droles et captivantes qui sont intéractives. A chaque fois tu vas proposer un court paragraphe qui fait avancer l'histoire et qui doit déboucher sur un choix multiple. Tu posera systématiquement une question à l'utilisateur avec 3 choix : a, b ou c, ce qui déterminera le prochain paragraphe de l'histoire. Tout au début de la conversation, propose 5 thèmes pour l'histoire, et l'utilisateur choisira entre 1 et 5. A tout moment propose aussi une option 'x' pour arrêter l'histoire.

Exemple de proposition des thèmes au début :

Bonjour! Je suis ici pour créer une histoire amusante et interactive pour toi. Voici cinq thèmes parmi lesquels tu peux choisir :

1. <description du thème>
2. <description du thème>
3. <description du thème>
4. <description du thème>
5. <description du thème>

Quel thème choisis-tu? (Tu peux entrer le numéro du thème que tu préfères, ou 'x' pour arrêter l'histoire.)


Exemple de proposition de choix multiple après chaque paragraphe :

a) <description de la réponse>
b) <description de la réponse>
c) <description de la réponse>

<question> ? (Réponds par a, b, c, ou 'x' pour arrêter l'histoire.)

"""

messages = []


def getStoryText():
    return getCompletion(
        "rédige moi maintenant tout le texte de l'histoire sans l'intéractivité. Commence ta réponse tout de suite avec le texte de l'histoire sans rajouter aucun commentaire du type 'Bien sûr, voici l'histoire complète sans l'interactivité :'",
        "",
        messages
    )


def getStoryInfos(story_text):

    prompt = (
        "génère moi une réponse au format json sous la forme : "
        "{ \"title\": <titre de l'histoire>, "
        "\"image\": <prompt en anglais pour générer l'image de couverture verticale d'un livre pour cette histoire. "
        "Il ne faut aucun texte dans l'image> }. "
        "Important: donne uniquement la réponse json et rien d'autre "
        "(pas de commentaires). Commence donc ta réponse par une accolade. "
        "Voici l'histoire : " + story_text
    )

    for i in range(2):

        try:

            json_response = getCompletion(prompt)

            json_response = json_response.replace("```json", "")
            json_response = json_response.replace("```", "")
            json_response = json_response.strip()

            data = json.loads(json_response)

            return data["title"], data["image"]

        except Exception as e:
            print(f"Erreur de désérialisation JSON. Essai numéro {i+1}")
            print(e)

    return "", "a book cover for a children's story book. Without any text."


response = getCompletion("", system_message, messages)

print(response)
print()


while True:

    prompt = input("Votre choix : ").lower().strip()

    if prompt == "x":
        break

    print()

    response = getCompletion(prompt, system_message, messages)

    print(response)
    print()


response = getCompletion(
    "L'histoire est terminée. Rédige le dernier paragraphe pour terminer l'histoire.",
    system_message,
    messages
)

print(response)


text = getStoryText()

title, image_prompt = getStoryInfos(text)

print("Image prompt : " + image_prompt)


with open("histoire.txt", "w", encoding="utf-8") as file:

    file.write(f"Titre : {title}\n\n")
    file.write(text)


generateImage(
    image_prompt,
    resolution="1024x1792",
    filename="histoire.png"
)


textToSpeech(
    title + "\n\n" + text,
    "histoire.mp3"
)