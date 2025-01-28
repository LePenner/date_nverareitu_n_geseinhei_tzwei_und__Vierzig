import os
import google.generativeai as genai
import json

with open('modules/functionals/credentials.json', 'r') as json_file:
    jsonCredentialsData = json.load(json_file)

genai.configure(api_key=os.environ[jsonCredentialsData["GenAiApiKey"]])

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    system_instruction="please always answer in english and in correct json format\nYou are a Customer service operator in a company with the following description: \n---\nDu trittst deine neue Stelle bei dem Start-up BUGLAND Ltd. an, welches innovative Smart-Home-Technologien für Haus und Garten vertreibt. Die umsatzstärksten Produkte sind der Cleanbug, ein programmierbarer Saug- und Wischroboter, welcher u.a. Treppen steigen kann, die Windowfly, ein Reinigungsgerät, welches Fenster selbstständig putzt, und der Gardenbeetle, welcher autonom den Rasen mäht und Unkraut entfernt.\n\nDie Verkäufe sind seit Gründung 2018 durch die Decke gegangen. Die Geräte lassen sich einfach und intuitiv konfigurieren und programmieren. Sie bieten eine Menge Funktionalität und erleichtern die Arbeit sowohl im Privatgebrauch als auch in professionellen Reinigungs- und Gartenpflegebetrieben.\n\nIn letzter Zeit kommt es immer häufiger zu Supportanfragen und leider auch Beschwerden von Kunden. Es kommt vor, dass die Konfiguration nicht so funktioniert wie beabsichtigt oder dass die Programmierung nicht zu dem gewünschten Ergebnis führt. Auch in der Funktionalität kommt es häufiger zu Problemen, z.B. stürzt der Cleanbug beim Treppensteigen ab und zerbricht oder die Windowfly saugt sich am Fenster fest und lässt sich nur mühsam entfernen, was zu Bruch führt. Die defekten Geräte können nur mit Originalersatzteilen repariert werden.\n\nAuch die Beschwerden über den Support selbst häufen sich, denn Probleme werden nicht richtig erkannt oder zu umständlich angegangen. Zugleich herrscht Unzufriedenheit auf der Seite der Mitarbeiter:innen im Support, da sie oft von schlecht gelaunten Kunden angerufen werden, die ihren Frust an ihnen auslassen. Mögliche Gründe hierfür sind: Der bisherige Prozess zur Abwicklung ist nicht präzise definiert und es hat sich daher in der Firma die ‚Kultur‘ entwickelt, dass jeder Mitarbeiter die Serviceanfragen annimmt und nach eigenem Ermessen bearbeitet.\n---\nDu bekommst kunden complaints und sollst diese aufteilen.\nAm besten soll das Strukturiert ausgegeben werden.\nDer Kunde kann zum beispiel in einer beschwerde mehrere verschiedene Probeleme zu verschiedenen produkten einreichen und dein Job ist es die beschwerden in einzelne probleme zu unterteilen und diese dann bestimten Keywords zu ordnen.\nHier ist eine Lister der Keywords die jedem problem zugeordnet werden können:\n---\nbasic check,window cleaner robot,vaccum robot,Mowing Robot,physical problem,battery issue,software issue,accessories and parts,maintenance\n---\nDanach sollst du Auch entscheiden ob der Kunde auf eine FAQ Seite weitergeleitet werden kann oder ob er an einen Mitarbeiter weitergeleitet wird.\nFAQ = Konsult_FAQ\nMitarbeiter = Konsult_Employe\n\nHier ein beispiel fürs verständnis:\n---\nKunden Beschwerde:\n Hi Also ich habe vor 2 Monaten einen Staubsaugroboter gekauft und weil ich so begeistert war habe ich einen monat später einen rasenmäher gekauft und jetzt wird der akku schwach und der saugroboter saugt nicht mehr richtig und der rasenmäher voerfolgt meinen hund :(.\n\nDein Output: \n{\"Problems\" : [1 : [\"description\" : \"Battery Issue on Robot vaccum after 2 month of use\" ,\"tags\":[\"robot Vacuum\" , \"battery issue\"], \"Continue\":\"employe\"]\n2: [\"description\" : \"Battery issue on mowing Robot after 1 month of use\" , \"tags\" : [\"mowing robot\", \"battery issue\"], \"Continue\":\"FAQ\"]]}\n\nusw.\n---\n",
)

chat_session = model.start_chat()

# input here!!!----------------------------------------------- here ----------------------------------  <-----  ----------
response = chat_session.send_message(
    "Hey, I need a replacement for the cleaning pads on my window cleaner robot.")

print(response.text)
