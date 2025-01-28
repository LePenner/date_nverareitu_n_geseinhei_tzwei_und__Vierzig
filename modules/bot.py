import json
import string


class Bot():

    def input(user_question, api):

        tags = Bot.check_tags(user_question)
        Bot.answer(tags, api)
        Bot.log_tags(tags)

    def check_tags(question):

        translator = str.maketrans(
            '', '', string.punctuation)  # translation key

        # remove punctuation from string
        q_striped = question.translate(translator)
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

    def answer(tags):
        pass

    def log_tags():
        pass
