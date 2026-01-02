from django import template

register = template.Library()

BAD_WORDS = ['редиска', 'плохоеслово', 'мат', 'матерноеслово']


@register.filter()
def censor(value):
    if not isinstance(value, str):
        return value

    text = value
    for word in BAD_WORDS:
        if word.lower() in text.lower():
            replacement = word[0] + '*' * (len(word) - 1)
            text = text.replace(word, replacement)

    return text
