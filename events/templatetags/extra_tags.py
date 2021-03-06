from django import template

register = template.Library()




# @register.filter(name='add')    
# def add(value, arg):
#     return value + arg




@register.filter(name='get_range')
def get_range( value ):
  """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
  """
  return range( value )

  
@register.simple_tag()
def multiply(a, b):
    return a * b
    
@register.simple_tag()
def sum(a, b):
    return a + b
