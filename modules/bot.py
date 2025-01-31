import json
import string

# own imports
from modules.console import Console
from modules.functionals.sending_messages import send_mail
from modules.ai import ai_answer


class Bot():

    def input(data):

        user_question = data['mail']['body']

        # not in use currently
        tags = Bot.check_tags(data['paths'], user_question)
        Console.status(f'tags generated: {tags}')
        Bot.answer(data, user_question)
        Console.status('Request Handled')

    def check_tags(PATHS, question):

        translator = str.maketrans(
            '', '', string.punctuation)  # translation key

        # remove punctuation from string
        q_striped = question.translate(translator)
        q_list = q_striped.lower().split()

        with open(PATHS['tags'], 'r') as json_file:
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

            # acess keywords from json file and get tags of matching words from user question
            for tag in json_tag_data["tags"]:
                for values in tag.values():
                    for word in q_list:
                        if word in values:
                            # tag.keys() returns dict_keys object --> conversion to string with list
                            q_tags.append(list(tag.keys())[0])

        # remove duplicates
        t_list = []

        for element in q_tags:
            if element not in t_list:
                t_list.append(element)

        q_tags = t_list.copy()

        return q_tags

    def answer(data, question):
        send_mail(data, ai_answer(data, question))

    def log_tags(tags):
        pass
