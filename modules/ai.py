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
    try:
        genai.configure(api_key=creds["GenAiApiKey"])
        return genai.GenerativeModel("gemini-1.5-flash").generate_content(promt)
    except Exception as e:
        Console.status(f'no response generated, error: {e}')

# determinse handling of question


def ai_answer(data, question):

    # returns tags and how to proceed with request
    # cut jason```[ actual data ]```
    # interpret as dictionary with json.loads
    try:
        evaluation = json.loads(evaluate_question(
            data, question).text[7:-4])

        # check if forwarded to staff or faq
        if evaluation['continue'] == 'employee':

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

        elif evaluation['continue'] == 'faq':
            answer = faq(data, question)
        else:
            answer = misc(data, question)

        Console.log("complaint processed")
        return answer
    except:
        return 1


def evaluate_question(data, question):
    evaluation = get_model_response(data['paths'],
                                    f"""
                                    You are managing the support request for a firm called BUGLAND Ltd.
                                    Our Products are the Windowfly, a window cleaning robot,
                                    the Cleanbug, a vacuum mop robot
                                    and the Gardenbeetle, a lawnmower and weed killer robot.

                                    For the complaint: {question}, distil the individual products our customer is experiencing issues with and the issues themselves.

                                    Also determine if the complaint is forwarded to an employee, to the FAQ or misc (eg. spam or no problems provided).
                                    As of now this FAQ does not exist, so just ask yourself if the stated problem should be covered in an faq and commense from there :)
                                    Keep in mind forward to an employee is costly as a ticket gets opened, so only forward them to an employee if you are absolutely sure they need advanced assistance.

                                    ONLY RETURN A JSON FILE IN THE CORRECT FORMAT OF:

                                    {{
                                    “tags”:
                                        {{
                                        “product”: -product name goes here-,
                                        “problem”: [-problem1-, -problem2, …]
                                        }},
                                        “continue”: -either “faq”, “employee" or "misc”-
                                    }}
                                    """
                                    )
    Console.status("evaluated problem")
    return evaluation


def faq(data, question):
    ai_text = get_model_response(data['paths'],
                                 f"""
                                You are managing the support request for a firm called BUGLAND Ltd.
                                Our Products are the Windowfly, a window cleaning robot,
                                the Cleanbug, a vacuum mop robot
                                and the Gardenbeetle, a lawnmower and weed killer robot.

                                For this customer question/complaint: {question},
                                please Generate a polite Email text, starting with the greeting (no subject) following roughly this structure (this shall only serve as a guide, you are not bound to exactly replicate the structure, but it should have the same effective use):
                                Dear {data['name']},

                                Regarding [summary of complaint here]

                                You can find a solution to the Problem here: [redirect them to relevant FAQ page]
                                If the issue persists, get back to me.

                                In best regards,
                                The BUGLAND Support Team
                                """
                                 )
    Console.status("refer to faq")
    return ai_text.text


def forward_to_employee(data, question, ticket_id):
    ai_text = get_model_response(data['paths'],
                                 f"""
        You are managing the support request for a firm called BUGLAND Ltd.
        Our Products are the Windowfly, a window cleaning robot,
        the Cleanbug, a vacuum mop robot
        and the Gardenbeetle, a lawnmower and weed killer robot.

        For this customer question/complaint: {question},
        please Generate a polite Email text, starting with the greeting (no subject) following roughly this structure (this shall only serve as a guide, you are not bound to exactly replicate the structure, but it should have the same effective use):

        Dear {data['name']},

        Regarding [summary of complaint here]

        You will be forwarded to an employee to further diagnose the issue, this process might take up to 24 hours.
        Your Ticket is as follows: {ticket_id}

        In best regards,
        The BUGLAND Support Team
        """)
    Console.status('forward to employee')
    return ai_text.text


def misc(data, question):
    ai_text = get_model_response(data['paths'],
                                 f"""
        You are managing the support request for a firm called BUGLAND Ltd.
        Our Products are the Windowfly, a window cleaning robot,
        the Cleanbug, a vacuum mop robot
        and the Gardenbeetle, a lawnmower and weed killer robot.

        For this customer question/complaint: {question},
        please Generate a polite Email text, starting with the greeting (no subject) following roughly this structure (this shall only serve as a guide, you are not bound to exactly replicate the structure, but it should have the same effective use):

        Dear {data['name']},

        Sadly we were unable to adress your complaint, because information about [product and/or problems] was missing,
        we ask you to restate your problem.

        In best regards,
        The BUGLAND Support Team
        """)
    Console.status('misc')
    return ai_text.text
