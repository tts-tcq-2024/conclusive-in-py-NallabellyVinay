def infer_breach(value, lowerLimit, upperLimit):
    if value < lowerLimit:
        return 'TOO_LOW'
    if value > upperLimit:
        return 'TOO_HIGH'
    return 'NORMAL'


def classify_temperature_breach(coolingType, temperatureInC):
    temperature_ranges = {
        'PASSIVE_COOLING': (0, 35),
        'HI_ACTIVE_COOLING': (0, 45),
        'MED_ACTIVE_COOLING': (0, 40),
    }
    
    if coolingType not in temperature_ranges:
        raise ValueError("Invalid cooling type")

    lowerLimit, upperLimit = temperature_ranges[coolingType]
    return infer_breach(temperatureInC, lowerLimit, upperLimit)


def check_and_alert(alertTarget, batteryChar, temperatureInC):
    breachType = classify_temperature_breach(batteryChar['coolingType'], temperatureInC)
    alert_method = get_alert_method(alertTarget)
    alert_method(breachType)


def get_alert_method(alertTarget):
    alert_methods = {
        'TO_CONTROLLER': send_to_controller,
        'TO_EMAIL': send_to_email,
    }
    
    if alertTarget not in alert_methods:
        raise ValueError("Invalid alert target")
    
    return alert_methods[alertTarget]


def send_to_controller(breachType):
    header = 0xfeed
    print(f'{header}, {breachType}')


def send_to_email(breachType):
    recipient = "a.b@c.com"
    messages = {
        'TOO_LOW': "Hi, the temperature is too low",
        'TOO_HIGH': "Hi, the temperature is too high",
    }
    
    if breachType in messages:
        print(f'To: {recipient}')
        print(messages[breachType])
