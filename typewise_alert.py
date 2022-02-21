from CoolingType import passive, med_active, hi_active
from BreachAlert import normal, too_low, too_high


class TypewiseAlert:
    def __init__(self):

        self.cooling_types = {'PASSIVE_COOLING': passive, 'HI_ACTIVE_COOLING': hi_active,
                              'MED_ACTIVE_COOLING': med_active}

        self.breach_alerts = {'NORMAL': normal, 'TOO_LOW': too_low, 'TOO_HIGH': too_high}

        self.alert_target_funcs = {'TO_CONTROLLER': self.send_to_controller,
                                   'TO_EMAIL': self.send_to_email}

        self.controller_interface = controller_status_stub
        self.mail_server_interface = mail_server_status_stub

    def infer_breach(self, value, lower_limit, upper_limit):

        if value < lower_limit:
            return 'TOO_LOW'
        if value > upper_limit:
            return 'TOO_HIGH'
        return 'NORMAL'

    def get_cooling_type_object(self, cooling_type_input):
        return self.cooling_types.get(cooling_type_input)

    def classify_temperature_breach(self, cooling_type, temperature_in_c):

        classified_cooling_type = self.get_cooling_type_object(cooling_type)

        if self.is_valid_cooling_type(classified_cooling_type):
            return self.infer_breach(temperature_in_c, classified_cooling_type.lower_limit,
                                     classified_cooling_type.upper_limit)
        else:
            print_exit_message()
            exit(0)

    def get_alert_object(self, breach_type):

        return self.breach_alerts.get(breach_type)

    def check_and_alert(self, alert_target, battery_char, temperature_in_c):

        breach_type = \
            self.classify_temperature_breach(battery_char['cooling_type'], temperature_in_c)
        breach_alert_object = self.get_alert_object(breach_type)

        alert_target_func = self.alert_target_funcs.get(alert_target)

        alert_sent = alert_target_func(breach_alert_object, temperature_in_c)

        return alert_sent

    def send_to_controller(self, breach_alert, temperature_in_c):

        is_alert_sent = self.send_alert_to_controller(self.controller_interface, temperature_in_c, breach_alert)
        return is_alert_sent

    def send_to_email(self, breach_alert, temperature_in_c):

        is_email_sent = self.send_alert_to_email(self.mail_server_interface, temperature_in_c, breach_alert)

        return is_email_sent

    def is_valid_cooling_type(self, classified_cooling_type):

        if classified_cooling_type is not None:
            return True
        else:
            return False

    def print_alert_to_email(self, breach_alert):

        print(f'From: {breach_alert.sender}')
        print(f'To: {breach_alert.recipient}')
        print(f'Subject: {breach_alert.subject}')
        print(f'Body: {breach_alert.message}')

        return True

    def print_alert_to_controller(self, breach_alert):
        header = 0xfeed
        print(f'{header}, {list(self.breach_alerts.keys())[list(self.breach_alerts.values()).index(breach_alert)]}')
        return True

    def send_alert_to_email(self, network_alert_func, temperature_in_c, breach_alert):
        if network_alert_func(temperature_in_c) != 500:
            return self.print_alert_to_email(breach_alert)

        return False

    def send_alert_to_controller(self, controller_alert_func, temperature_in_c, breach_alert):
        if controller_alert_func(temperature_in_c) == 'OK':
            return self.print_alert_to_controller(breach_alert)

        return False


def mail_server_status_stub(temperature_in_c, higher_threshold=50, lower_threshold=-5):
    if higher_threshold >= temperature_in_c >= lower_threshold:
        return 200
    else:
        return 500


def controller_status_stub(temperature_in_c, higher_threshold=50, lower_threshold=-5):
    if higher_threshold >= temperature_in_c >= lower_threshold:
        return 'OK'
    else:
        return 'Not OK'


def print_exit_message():
    print("Please provide valid inputs")
