class BreachAlert:
    def __init__(self, sender, recipient, subject, message):
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        self.message = message


normal = BreachAlert("no-reply@org.com",
                     "a.b@c.com",
                     "Breach Alert Notification",
                     'Hi there, The temperature is currently in Normal State :-)'
                     )

too_low = BreachAlert("no-reply@org.com",
                      "a.b@c.com",
                      "Breach Alert Notification",
                      'Hi there, The temperature is too low :-|, Immediate action is needed!'
                      )

too_high = BreachAlert("no-reply@org.com",
                       "a.b@c.com",
                       "Breach Alert Notification",
                       'Hi there, The temperature is too high :-|, Immediate action is needed!'
                       )
