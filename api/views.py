"""api views"""

import base64

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(('GET',))
def calculus(request):
    """

    :param request:
    :return:
    """

    try:
        query = request.GET.get("query", default="")
        query = check_padding(query)
        expression = decode(query)
        unwanted_characters = filter_unwanted_characters(expression)
        if not unwanted_characters:
            return Response(data={"error": False, "result": expression})
        else:
            return Response(
                data={"error": True,
                      "message": "Contains prohibited operators"})
    except Exception as error:
        return Response(
            data={"error": True, "message": str(error)})


def filter_unwanted_characters(expression):
    """
    check it there are unwanted characters and proceed to solve

    :param expression:
    :return: string
    """
    allowed_symbols = ["+", "-", "/", "*", "(", ")"]
    string = "".join(filter(
        lambda x: (not str(x).isdigit() and x not in allowed_symbols),
        expression))
    print(string)
    return string


def decode(query):
    """
    decode to utf-8 string

    :param query:
    :return: expression
    """

    expression = base64.b64decode(query).decode('utf-8')
    return expression


def check_padding(query):
    """
    check for missing padding in base64 encoding and fill it up with "="

    :param query:
    :return: query
    """

    missing_padding = len(query) % 4
    if missing_padding:
        query += "=" * (4 - missing_padding)
    return query
