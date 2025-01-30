from modules.ticket import Ticket_db

"""response = response:
    GenerateContentResponse(
        done=True,
        iterator=None,
        result=protos.GenerateContentResponse({
          "candidates": [
            {
              "content": {
                "parts": [
                  {
                    "text": "Subject: Regarding your recent BUGLAND Ltd. Support Request (Ticket #c71fc5d6-abd1-48e0-bb93-4549fe1d1082)\n\nDear erikblunk42,\n\nThank you for contacting BUGLAND Ltd. regarding the issues you experienced with your Cleanbug and Gardenbeetle. We appreciate you bringing these matters to our attention and value your business.\n\nWe understand your frustration with the Cleanbug's reduced suction power and the Gardenbeetle's unexpected pursuit of your dog. We're also looking into the reported weakening battery in your Gardenbeetle.  These issues are being investigated by our specialist team.\n\nA member of our support team will be in touch with you within 24-48 hours to discuss these problems in more detail and to find a suitable solution. This may involve troubleshooting steps, a repair, or a replacement depending on the nature of the faults.  We will strive to resolve this for you as quickly and efficiently as possible.\n\nWe greatly appreciate your patience and understanding as we work to resolve these issues.  Thank you again for choosing BUGLAND Ltd.\n\nSincerely,\n\nThe BUGLAND Ltd. Customer Support Team\n"
                  }
                ],
                "role": "model"
              },
              "finish_reason": "STOP",
              "avg_logprobs": -0.2866160972445619
            }
          ],
          "usage_metadata": {
            "prompt_token_count": 738,
            "candidates_token_count": 255,
            "total_token_count": 993
          },
          "model_version": "gemini-1.5-flash"
        }),
    )"""


ticket_instance = Ticket_db()
ticket_instance.create_ticket(UUID, email, complaint, response.result["candidates"][0]["content"]["parts"][0]["text"], processedcomplaint, data)