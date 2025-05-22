from django import template

register = template.Library()

@register.filter
def score_class(score):
    try:
        score = float(score)
        if score >= 0.7:
            return "bg-danger text-white"
        elif score >= 0.4:
            return "bg-warning text-dark"
        else:
            return "bg-success text-white"
    except:
        return ""
