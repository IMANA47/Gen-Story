from groq import Groq

from groqaikey import GROQ_API_KEY
# pyrefly: ignore [untyped-import]
import requests
import openai

client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

"""
client = Groq(
    api_key=GROQ_API_KEY
)
"""


def getCompletion(prompt, system_prompt="", messages=None):

    if messages is None:
        messages = []

    if system_prompt != "" and len(messages) == 0:
        messages.append({
            "role": "system",
            "content": system_prompt
        })

    if prompt != "":
        messages.append({
            "role": "user",
            "content": prompt
        })

    try:

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )

        text = completion.choices[0].message.content

        messages.append({
            "role": "assistant",
            "content": text
        })

        return text

    except Exception as e:
        print("OpenAi Exception : " + str(e))

    return None


def generateImage(
    prompt,
    resolution="1024x1024",
    filename="",
    cheap_mode=False
):

    print("Génération de l'image...")

    # Pollinations AI (gratuit)
    image_url = f"https://image.pollinations.ai/prompt/{prompt}"

    try:

        if filename != "":

            print("Téléchargement de l'image...")

            image_data = requests.get(image_url).content

            with open(filename, 'wb') as file:
                file.write(image_data)

        print("Image générée")

        return image_url

    except Exception as e:
        print("Erreur génération image : " + str(e))

    return None


def textToSpeech(text, filename):

    try:

        from gtts import gTTS

        tts = gTTS(text=text, lang="fr")

        tts.save(filename)

        print("Audio généré")

    except Exception as e:
        print("Erreur TextToSpeech : " + str(e))


if __name__ == "__main__":

    # print(getCompletion("Bonjour"))

    # print(generateImage(
    #     "a very big cat in the snow",
    #     filename="cat.png",
    #     cheap_mode=True
    # ))

    textToSpeech(
        "Bonjour, comment allez-vous  et vous je vais super bien?",
        "speech.mp3"
    )
