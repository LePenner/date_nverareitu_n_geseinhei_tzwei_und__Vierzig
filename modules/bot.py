import json
import string


class Bot():

    def input(user_text):

        tags = Bot.check_tags(user_text)
        Bot.answer(tags)
        Bot.log_tags(tags)

    def check_tags(question):

        translator = str.maketrans('', '', string.punctuation) # translation key

        q_striped = question.translate(translator) # 
        q_list = q_striped.lower().split()

        with open('modules/functionals/tags.json') as json_file:
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

            for tag in json_tag_data["tags"]:
                for values in tag.values():
                    for word in q_list:
                        if word in values:
                            # tag.keys returns dict_keys object --> conversion to string with list
                            q_tags.append(list(tag.keys())[0])

    def answer(tags):
        pass

    def log_tags():
        pass
