import json
import uuid
import google.generativeai as genai

# own imports
from modules.ticket import Ticket_db
from modules.console import Console

# returns object, call .text to get response as str


def get_model_response(PATHS, promt):

    # fetch creds from json file
    with open(PATHS['credentials'], 'r') as json_file:
        creds = json.load(json_file)

    # initiate AI and return response
    genai.configure(api_key=creds["GenAiApiKey"])
    return genai.GenerativeModel("gemini-1.5-flash").generate_content(promt)

# determinse handling of question


def ai_answer(data, question):

    # returns tags and how to proceed with request, cut jason```[ actual data ]```
    evaluation = evaluate_question(
        data, question).text[7:-4]

    # eval_structure = json.loads(evaluation.text.split("```")[1].split("json")[1])
    Console.log(evaluation)

    evaluation = json.loads(evaluation)

    # check if forwarded to staff or faq
    if evaluation['continue'] != 'faq':

        ticket_id = str(uuid.uuid4())
        email = data['email']
        answer = forward_to_employee(data, question, ticket_id)

        # create ticket
        try:
            ticket_instance = Ticket_db()
            ticket_instance.create_ticket(
                ticket_id, email, question, answer, evaluation, data)

        except Exception as e:
            Console.status(f'Ticket Creation failed: {e}')
    else:
        answer = faq(data, question)

    return answer


def evaluate_question(data, question):
    evaluation = get_model_response(data['paths'],
                                    f"""
                                    You are managing the support request for a firm called BUGLAND Ltd.
                                    Our Products are the Windowfly, a window cleaning robot,
                                    the Cleanbug, a vacuum mop robot
                                    and the Gardenbeetle, a lawnmower and weed killer robot.

                                    For the complaint: {question}, distil the individual products our customer is experiencing issues with and the issues themselves.

                                    Also determine if the complaint is forwarded to an employee or to the FAQ, if a person explicitly states they want human assistance forward them to an employee.

                                    ONLY RETURN A JSON FILE IN THE CORRECT FORMAT OF:

                                    {{
                                    “tags”:
                                        {{
                                        “product”: -product name goes here-,
                                        “problem”: [-problem1-, -problem2, …]
                                        }},
                                        “continue”: -either “faq” or “employee-”
                                    }}
                                    """
                                    )
    Console.log("generated response")
    return evaluation


def faq(data, question):

    name = data['name']

    ai_text = get_model_response(data['paths'],
                                 f"""
                                You are managing the support request for a firm called BUGLAND Ltd.
                                Our Products are the Windowfly, a window cleaning robot,
                                the Cleanbug, a vacuum mop robot
                                and the Gardenbeetle, a lawnmower and weed killer robot.

                                For this customer question/complaint: {question},
                                please Generate a polite Email following roughly this structure (this shall only serve as a guide, you are not bound to exactly replicate the structure, but it should have the same effective use):
                                Dear {name},

                                Regarding [summary of complaint here]

                                You can find a solution to the Problem here: [redirect them to relevant FAQ page]
                                If the issue persists, get back to me.

                                In best regards,
                                The BUGLAND Support Team
                                """
                                 )

    Console.log(ai_text.text)

    return ai_text.text


def forward_to_employee(data, question, ticket_id):

    name = data['name']

    ai_text = get_model_response(data['paths'],
                                 f"""
        You are managing the support request for a firm called BUGLAND Ltd.
        Our Products are the Windowfly, a window cleaning robot,
        the Cleanbug, a vacuum mop robot
        and the Gardenbeetle, a lawnmower and weed killer robot.

        For this customer question/complaint: {question},
        please Generate a polite Email text, starting with the greeting (no subject) following roughly this structure (this shall only serve as a guide, you are not bound to exactly replicate the structure, but it should have the same effective use):

        Dear {name},

        Regarding [summary of complaint here]

        You will be forwarded to an employee to further diagnose the issue, this process might take up to 24 hours.
        Your Ticket is as follows: {ticket_id}

        In best regards,
        The BUGLAND Support Team
        """)

    Console.log(ai_text.text)

    return ai_text.text
