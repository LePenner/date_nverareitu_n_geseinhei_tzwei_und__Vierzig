import json
import string

# own imports
from modules.functionals.sending_messages import send_mail

class Bot():

    def input(user_question, chat_session):

        tags = Bot.check_tags(user_question)
        Bot.answer(tags, chat_session)
        Bot.log_tags(tags)

    def check_tags(question):

        translator = str.maketrans('', '', string.punctuation) # translation key

        q_striped = question.translate(translator) # remove punctuation from string
        q_list = q_striped.lower().split()

        with open('modules/functionals/tags.json', 'r') as json_file:
            json_tag_data = json.load(json_file)

            # {
            # "tags": [
            #    {
            #       "tag": [
            #           "key", "words"
            #       ]
            #    }
            # }

            q_tags = []

            # excess keywords from json file and get tags of matching words from user question
            for tag in json_tag_data["tags"]:
                for values in tag.values():
                    for word in q_list:
                        if word in values:
                            # tag.keys returns dict_keys object --> conversion to string with list
                            q_tags.append(list(tag.keys())[0])

        # remove duplicates
        t_list = []
        	
        for element in q_tags:
            if element not in t_list:
                t_list.append(element)

        q_tags = t_list.copy()
    

        return q_tags

    def answer(tags, chat_session):
        send_mail(chat_session.send_message)

    def log_tags(tags):
        pass