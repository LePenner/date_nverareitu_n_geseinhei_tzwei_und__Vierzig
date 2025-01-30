import json
import uuid
import google.generativeai as genai

# own imports
from modules.ticket import Ticket_db
from modules.console import Console


def get_model_response(PATHS, promt):
    with open(PATHS['credentials'], 'r') as json_file:
        creds = json.load(json_file)

    genai.configure(api_key=creds["GenAiApiKey"])
    return genai.GenerativeModel("gemini-1.5-flash").generate_content(promt)


def ai_stucture_answer(PATHS, complaint: str):

    response = get_model_response(PATHS, "please always answer in english and in correct json format\nYou are a Customer service operator in a company with the following description: \n---\nDu trittst deine neue Stelle bei dem Start-up BUGLAND Ltd. an, welches innovative Smart-Home-Technologien für Haus und Garten vertreibt. Die umsatzstärksten Produkte sind der Cleanbug, ein programmierbarer Saug- und Wischroboter, welcher u.a. Treppen steigen kann, die Windowfly, ein Reinigungsgerät, welches Fenster selbstständig putzt, und der Gardenbeetle, welcher autonom den Rasen mäht und Unkraut entfernt.\n\nDie Verkäufe sind seit Gründung 2018 durch die Decke gegangen. Die Geräte lassen sich einfach und intuitiv konfigurieren und programmieren. Sie bieten eine Menge Funktionalität und erleichtern die Arbeit sowohl im Privatgebrauch als auch in professionellen Reinigungs- und Gartenpflegebetrieben.\n\nIn letzter Zeit kommt es immer häufiger zu Supportanfragen und leider auch Beschwerden von Kunden. Es kommt vor, dass die Konfiguration nicht so funktioniert wie beabsichtigt oder dass die Programmierung nicht zu dem gewünschten Ergebnis führt. Auch in der Funktionalität kommt es häufiger zu Problemen, z.B. stürzt der Cleanbug beim Treppensteigen ab und zerbricht oder die Windowfly saugt sich am Fenster fest und lässt sich nur mühsam entfernen, was zu Bruch führt. Die defekten Geräte können nur mit Originalersatzteilen repariert werden.\n\nAuch die Beschwerden über den Support selbst häufen sich, denn Probleme werden nicht richtig erkannt oder zu umständlich angegangen. Zugleich herrscht Unzufriedenheit auf der Seite der Mitarbeiter:innen im Support, da sie oft von schlecht gelaunten Kunden angerufen werden, die ihren Frust an ihnen auslassen. Mögliche Gründe hierfür sind: Der bisherige Prozess zur Abwicklung ist nicht präzise definiert und es hat sich daher in der Firma die ‚Kultur‘ entwickelt, dass jeder Mitarbeiter die Serviceanfragen annimmt und nach eigenem Ermessen bearbeitet.\n---\nDu bekommst kunden complaints und sollst diese aufteilen.\nAm besten soll das Strukturiert ausgegeben werden.\nDer Kunde kann zum beispiel in einer beschwerde mehrere verschiedene Probeleme zu verschiedenen produkten einreichen und dein Job ist es die beschwerden in einzelne probleme zu unterteilen und diese dann bestimten Keywords zu ordnen.\nHier ist eine Liste der Keywords die jedem problem zugeordnet werden können:\n---\nbasic check,window cleaner robot,vaccum robot,Mowing Robot,physical problem,battery issue,software issue,accessories and parts,maintenance\n---\nDanach sollst du Auch entscheiden ob der Kunde auf eine FAQ Seite weitergeleitet werden kann oder ob er an einen Mitarbeiter weitergeleitet wird.\nFAQ = Konsult_FAQ\nMitarbeiter = Konsult_Employe\n\nHier ein beispiel fürs verständnis:\n---\nKunden Beschwerde:\n Hi Also ich habe vor 2 Monaten einen Staubsaugroboter gekauft und weil ich so begeistert war habe ich einen monat später einen rasenmäher gekauft und jetzt wird der akku schwach und der saugroboter saugt nicht mehr richtig und der rasenmäher voerfolgt meinen hund :(.\n\nDein Output: \n{\"Problems\" : [1 : [\"description\" : \"Battery Issue on Robot vaccum after 2 month of use\" ,\"tags\":[\"robot Vacuum\" , \"battery issue\"], \"Continue\":\"employe\"]\n2: [\"description\" : \"Battery issue on mowing Robot after 1 month of use\" , \"tags\" : [\"mowing robot\", \"battery issue\"], \"Continue\":\"FAQ\"]]}\n\nusw.\n---\n"
                                  f"the complaint is as follows: ---{complaint}---")
    Console.log("generated response")

    # check if forwarded to staff, generate ticket here
    # gemeni adds ```json ... ``` to the output and im removing it in hope that there is not another json in the output
    return json.loads(response.text.split("```")[1].split("json")[1])


def ai_text_answer(data, question):

    PATHS = data['paths']
    UUID = str(uuid.uuid4())
    name = data['name']
    email = data['email']

    ai_structure = ai_stucture_answer(PATHS, question)
    ai_text = get_model_response(PATHS, "please always answer in english and in a valid Email Format\nYou are a Customer service operator in a company with the following description: \n---\nDu trittst deine neue Stelle bei dem Start-up BUGLAND Ltd. an, welches innovative Smart-Home-Technologien für Haus und Garten vertreibt. Die umsatzstärksten Produkte sind der Cleanbug, ein programmierbarer Saug- und Wischroboter, welcher u.a. Treppen steigen kann, die Windowfly, ein Reinigungsgerät, welches Fenster selbstständig putzt, und der Gardenbeetle, welcher autonom den Rasen mäht und Unkraut entfernt.\n\nDie Verkäufe sind seit Gründung 2018 durch die Decke gegangen. Die Geräte lassen sich einfach und intuitiv konfigurieren und programmieren. Sie bieten eine Menge Funktionalität und erleichtern die Arbeit sowohl im Privatgebrauch als auch in professionellen Reinigungs- und Gartenpflegebetrieben.\n\nIn letzter Zeit kommt es immer häufiger zu Supportanfragen und leider auch Beschwerden von Kunden. Es kommt vor, dass die Konfiguration nicht so funktioniert wie beabsichtigt oder dass die Programmierung nicht zu dem gewünschten Ergebnis führt. Auch in der Funktionalität kommt es häufiger zu Problemen, z.B. stürzt der Cleanbug beim Treppensteigen ab und zerbricht oder die Windowfly saugt sich am Fenster fest und lässt sich nur mühsam entfernen, was zu Bruch führt. Die defekten Geräte können nur mit Originalersatzteilen repariert werden.\n\nAuch die Beschwerden über den Support selbst häufen sich, denn Probleme werden nicht richtig erkannt oder zu umständlich angegangen. Zugleich herrscht Unzufriedenheit auf der Seite der Mitarbeiter:innen im Support, da sie oft von schlecht gelaunten Kunden angerufen werden, die ihren Frust an ihnen auslassen. Mögliche Gründe hierfür sind: Der bisherige Prozess zur Abwicklung ist nicht präzise definiert und es hat sich daher in der Firma die ‚Kultur‘ entwickelt, dass jeder Mitarbeiter die Serviceanfragen annimmt und nach eigenem Ermessen bearbeitet.\n---\nDu bekommst kunden complaints und sollst eine nette und Kundenfereundliche Email zurückgeben\nAm besten soll diese immer gleich strukturiert sein\nDer Kunde kann zum beispiel in einer beschwerde mehrere verschiedene Probeleme zu verschiedenen produkten einreichen und dein Job ist es dem Kunden zu versichern das wir an dem Problem oder an den mehreren problemnen dran sind und das wir ihn sehr als kunden schätzen. Achte auch darauf das Porblem in der Email irgendwie zu erwähnen um zu zeigen, dass jede Email einzigartig ist. Hier ein beispiel fürs verständnis:\n---\nKunden Beschwerde:\n Hi Also ich habe vor 2 Monaten einen Staubsaugroboter gekauft und weil ich so begeistert war habe ich einen monat später einen rasenmäher gekauft und jetzt wird der akku schwach und der saugroboter saugt nicht mehr richtig und der rasenmäher voerfolgt meinen hund :(.\n\nDein Output: \nDear valued Customer, we have recieved your complaint and will connect you to a human operator shortly. we value you alot and will see that this is done as fast as possible. Thank you for staying with us all this time. Bugland Ldt."
                                 f"the complaint is as follows: ---{
                                     question}---"
                                 f"the customer name is as follows: ---{
                                     name}---"
                                 f"the customer ticket id is as follows: ---{
                                     UUID}---"
                                 )
    # \
    # move to complaint_processing
    try:
        ticket_instance = Ticket_db()

        ticket_instance.create_ticket(
            UUID, email, question, ai_structure["candidates"][0]["content"]["parts"][0]["text"], ai_structure, data)
    except Exception as e:
        Console.status(f'Ticket Creation failed: {e}')
    # move to complaint_processing
    # /

    return ai_text.text
