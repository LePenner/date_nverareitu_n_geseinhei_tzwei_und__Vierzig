import os
import json
from modules.bot import Bot


def input_tests():

    # open test data
    with open('test_cases/json/inputs.json', 'r') as json_test_file:
        json_test_data = json.load(json_test_file)

    # check all test cases
    for test in json_test_data["inputs"]:

        fail = False
        tags = Bot.check_tags(test.get('text'))

        # check if calulated and should tags match
        if set(tags) == set(test.get('tags')):
            print('Full Clear', end='')
        else:
            for tag in tags:

                # can never fail basic check detection
                # special case
                if 'basic check' not in tags and 'basic check' in test.get('tags'):
                    fail = True
                    break

                # no halucinated tags
                if tag not in test.get('tags'):
                    fail = True
                    break

            # must at least get 60% of tags
            if fail == False and len(tags) >= len(test.get('tags'))*0.6:
                print('Clear     ', end='')
            else:
                print('Fail      ', end='')

        print(f'  Calc tags: {tags}, test tags: {
              test.get('tags')}\n            {test.get('text')}\n')
