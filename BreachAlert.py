class BreachAlert:
    def __init__(self, sender, recipient, subject, message):
        self.__sender = sender
        self.__recipient = recipient
        self.__subject = subject
        self.__message = message

    @property
    def sender(self):
        return self.__sender

    @property
    def recipient(self):
        return self.__recipient

    @property
    def subject(self):
        return self.__subject

    @property
    def message(self):
        return self.__message


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
