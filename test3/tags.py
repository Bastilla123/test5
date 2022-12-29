from __future__ import unicode_literals
from django.template.loader import render_to_string

from django import template



import base64
import requests
from django.conf import settings


from django.template import Library, Node

register = Library()


class EscapeScriptNode(Node):
    TAG_NAME = 'escapescript'

    def __init__(self, nodelist):
        super(EscapeScriptNode, self).__init__()
        self.nodelist = nodelist

    def render(self, context):
        out = self.nodelist.render(context)
        escaped_out = out.replace('</script>', '<\\/script>')
        return escaped_out


@register.tag(EscapeScriptNode.TAG_NAME)
def media(parser, token):
    nodelist = parser.parse(('end' + EscapeScriptNode.TAG_NAME,))
    parser.delete_first_token()
    return EscapeScriptNode(nodelist)


register = template.Library()

@register.simple_tag(name='default_domain')
def default_domain():

    return settings.DEFAULT_DOMAIN

@register.simple_tag
def to_base64(url):
    return "data:image/png;base64, " + str(base64.b64encode(requests.get(url).content))


@register.simple_tag
def is_product_on_sale(product):
    return utils.is_product_on_sale(product)


@register.simple_tag
def calculate_product_price_incl_discounts(product, price_data):
    return utils.calculate_product_price_incl_discounts(product, price_data)


@register.simple_tag
def get_flash_sale_offer(product):
    return utils.get_flash_sale_offer(product)


@register.simple_tag
def calculate_percentage(firstvalue, secondvalue):
    return 100 - (firstvalue * 100 / secondvalue)


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter
def render_footermenu(menu):
    return render_to_string("footermenu.html", {'menu': menu})


@register.filter
def get_type(value):
    return str(type(value))


@register.filter
def substract(originalvalue, substractvalue):
    print("substract original {} original2 {}".format(originalvalue,substractvalue))
    return originalvalue - substractvalue


@register.filter
def getform(forms, key):
    if (key in forms):
        return forms[key]
    return ""


@register.filter(name='getmanytomanyvalues')
def getmanytomanyvalues(instance, fieldname):
    attr = getattr(instance, str(fieldname)).all()

    if ('None' in attr):
        return ""
    string = ""
    i = 0
    for items in attr:
        if (i != 0):
            string += ','
        string += str(items)
        i += 1

    return string


@register.filter
def get_attr(value, arg):
    try:
        if (value._meta.get_field(arg).choices is not None):
            for choice_entry in value._meta.get_field(arg).choices:

                if (choice_entry[0] == getattr(value, arg)):
                    return choice_entry[1]
    except Exception as e:

        return getattr(value, arg)

    try:
        value = getattr(value, arg)

        if (value is None):
            return ""
        return value
    except:
        return ""
    return ""


@register.filter
def modulo(num, val):
    return num % val == 0


@register.filter(name='desctimes')
def desctimes(number, descnumber):
    if (number is None):
        return None
    number += 1
    return range(1, int(number) - int(descnumber))


@register.filter(name='times')
def times(number):
    if (number is None):
        return None
    number += 1
    return range(1, int(number))

@register.filter(name='istrue')
def istrue(obj,key):


    return getattr(obj,key)

@register.filter(name='hasattr')
def hasattr(obj,key):

    return hasattr(obj,key)

@register.filter(name='split')
def split(value, key):
    """
        Returns the value turned into a list.
    """
    return value.split(key)

@register.filter(name='stringlisttolist')
def stringlisttolist(stringlist):

    return stringlist.strip("]['").split(',')

@register.filter(name='getvaluefromfield')
def getvaluefromfield(dictionary, fieldname):

    fieldname = fieldname.replace('"', '')

    fieldname = fieldname.strip()


    if (fieldname.strip() == ""):
        return
    try:
        if ("." in fieldname):
            fieldtype = "ForeignKey"
        else:
            fieldtype = eval(dictionary._meta.object_name)._meta.get_field(fieldname).get_internal_type()

    except Exception as e:
        print("tags.py Eval funktioniert nicht. Error {}".format(e))
        return ""

    if (fieldtype == "DateTimeField"):

        feldeintrag = get_attr(dictionary, fieldname)

        if (str(type(feldeintrag)) == "<class 'datetime.datetime'>"):
            return "{}".format(get_attr(dictionary, fieldname).strftime("%d.%m.%Y %H:%m"))
        return "{}".format(get_attr(dictionary, fieldname))

    if (fieldtype == "DateField"):

        date = get_attr(dictionary, fieldname)
        if (date == ""):
           return "{}".format(date)
        else:
            return "{}".format(date.strftime("%d.%m.%Y"))
            #

    elif (fieldtype == "ManyToManyField"):

        return "{}".format(getmanytomanyvalues(dictionary, fieldname))
    elif (fieldtype == "BooleanField"):

        if (get_attr(dictionary, fieldname) == True):
            return '<i class="fas fa-check"></i>'
        else:
            return '<i class="fa fa-times" aria-hidden="true"></i>'
    elif (fieldtype == "OneToOneField"):

        return "{}".format(get_attr(dictionary, fieldname))
    elif ("DecimalField" in fieldtype or "FloatField" in fieldtype):

        if (get_attr(dictionary, fieldname) is None or get_attr(dictionary, fieldname) == ""):
            return ""
        return round(get_attr(dictionary, fieldname),2)
    elif (fieldtype == "ForeignKey"):
        if ("." in fieldname):
            fieldarray = fieldname.split(".")
            fieldname = fieldarray[0]

            relatedfield = fieldarray[1]



            try:
                return "{}".format(get_attr(get_attr(dictionary, fieldname).first(),relatedfield))
            except Exception:
                return "{}".format(get_attr(get_attr(dictionary, fieldname), relatedfield))
        else:
            return "{}".format(get_attr(dictionary, fieldname))

    return "{}".format(get_attr(dictionary, fieldname))


@register.filter
def replace(value, arg):

    """
    Replacing filter
    Use `{{ "aaa"|replace:"a|b" }}`
    """
    if len(arg.split('|')) != 2:
        return value

    what, to = arg.split('|')
    return value.replace(what, to)


# from random import randint
# @register.simple_tag
# def random_number(forms):
#    return randint(0,999)


@register.filter(name='getcheckboxes')
def getcheckboxes(allfieldlist, activefieldlist):
    deletelist = ['is_deleteable', 'is_editable', 'trash', 'create_date', 'is_active', 'modified_date', 'create_user',
                  'modified_user', 'delete_user', 'change_date']
    html = '<div class="custom-control ">'

    for field in allfieldlist:
        if (field in deletelist):
            continue
        html += '<div class="form-group"><label for="id_homepage">' + str(
            translateheader(field)) + ':</label><div class="form-group">'
        found = False

        for activefield in activefieldlist:

            if (field.strip() == activefield.strip().replace('"', '')):
                found = True

                html += '<input type="checkbox" name="id_' + str(field) + '" id="id_' + str(
                    field) + '" style="border-radius: 4px;" checked="">'
                break
        if (found == False):
            html += '<input type="checkbox" name="id_' + str(field) + '" id="id_' + str(
                field) + '" style="border-radius: 4px;" >'

        html += '</div></div>'

    return html


@register.filter(name='getlinkfromfield')
def getlinkfromfield(instance, fieldname):
    attr = get_attr(instance, fieldname)
    model = attr._meta.model_name
    return '<a href="/edit/' + str(model) + "/" + str(attr.id) + '">' + str(attr) + "</a>"


@register.filter(name='times')
def times(number):
    if (number is None):
        return None
    number += 1
    return range(1, int(number))


@register.filter(name='getallfieldsfrommodel')
def getallfieldsfrommodel(modelname):
    model = eval('Clientaddress')
    allfields = [f.name for f in model._meta.get_fields()]

    return allfields


@register.filter(name='translateheader')
def translateheader(fieldname):
    fieldname = fieldname.replace('"', '').replace(' ', '')

    translatedict = {'kurzname': 'Kurzname', 'firstname': 'Vorname', 'lastname': 'Nachname', 'city': 'Ort', 'id': 'Id',
                     'zip': 'PLZ', 'letter_salutation': 'Briefanrede', 'birthdate': 'Geburtstag',
                     'is_active': 'Aktiv', 'country': 'Land', "status": "Status", "title": 'Überschrift',
                     'description': "Beschreibung", 'date': "Datum", 'assigned_to': "Zugordneter Benutzer",
                     'queue_link': "Zugeordnete Queue", 'address_link': "Zugeordnete Adresse", "priority": "Priorität"
                     }
    for key, value in translatedict.items():

        if (key == fieldname):
            return value

    return fieldname
