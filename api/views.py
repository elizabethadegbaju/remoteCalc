"""api views"""

import base64
import re

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(('GET',))
def calculus(request):
    """
    API view to decode base64 utf-8 string, compute it and send back a
    suitable response.

    :param request:
    :return:
    """

    try:
        query = request.GET.get("query", default="")
        query = check_padding(query)

        e = re.compile(r"\s+")
        expression = e.sub("", decode(query))

        print(expression)

        unwanted_characters = filter_unwanted_characters(expression)
        if not unwanted_characters:
            result = interpret(expression)
            return Response(data={"error": False, "result": result})
        else:
            return Response(
                data={"error": True,
                      "message": "Contains prohibited operators"}, status=400)
    except Exception as error:
        return Response(data={"error": True, "message": str(error)}, status=400)


def filter_unwanted_characters(expression):
    """
    Check it there are unwanted characters in the decoded expression.

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
    Decode query to utf-8 string.

    :param query:
    :return: expression
    """

    expression = base64.b64decode(query).decode('utf-8')
    return expression.strip()


def check_padding(query):
    """
    Check for missing padding in base64 encoding and fill it up with "=".

    :param query:
    :return: query
    """

    missing_padding = len(query) % 4
    if missing_padding:
        query += "=" * (4 - missing_padding)
    return query


def solve_matched_parenthesis(expression):
    """
    Recursively solve expressions in matched parenthesis.

    :param expression:
    :return: expression
    """
    if ")" in expression:
        end = expression.find(")")
        start = max([index for index, char in enumerate(expression[:end]) if
                     char == "("])
        first_half = expression[:start]
        print(first_half)
        if not (first_half == "" or first_half.endswith(
                "+") or first_half.endswith("-") or first_half.endswith(
            "*") or first_half.endswith("/")):
            expression = solve_matched_parenthesis(
                expression[:start] + "*" + str(
                    interpret(expression[start + 1:end])) + expression[
                                                            end + 1:])
            print(expression)
        else:
            expression = solve_matched_parenthesis(expression[:start] + str(
                interpret(expression[start + 1:end])) + expression[end + 1:])
            print(expression)
    return expression


def get_numerical_value(expression):
    """
    Recursively check if the expression can be treated as a numerical value.

    :param expression:
    :return: boolean
    """
    if expression.startswith("(") and expression.endswith(")") and (len(expression) > 2):
        new_expression = expression[1:-1]
        return get_numerical_value(new_expression)
    else:
        try:
            return float(expression)
        except ValueError:
            return None


def interpret(expression):
    """
    Interpret the expression according to operator precedence and return
    the solved value.

    :param expression:
    :return:
    """
    number = get_numerical_value(expression)
    if number is not None:
        return number

    expression = solve_matched_parenthesis(expression)
    statements = split_expression(expression)

    if statements[0].count("(") != statements[0].count(")"):
        nested_level = statements[0].count("(") - statements[0].count(")")
        position = len(statements[0])
        for statement in statements[1:]:
            if "(" in statement:
                nested_level += statement.count("(")
            if ")" in statement:
                nested_level -= statement.count(")")
            position += len(statement) + 1
            if nested_level == 0:
                break
    else:
        position = len(statements[0])

    left_operand = expression[:position]
    right_operand = expression[position + 1:]
    operator = expression[position]

    try:
        if right_operand == "":
            return left_operand
        if operator == "+":
            return interpret(left_operand) + interpret(right_operand)
        elif operator == "-":
            return interpret(left_operand) - interpret(right_operand)
        elif operator == "*":
            return interpret(left_operand) * interpret(right_operand)
        elif operator == "/":
            denominator = interpret(right_operand)
            if denominator == 0 or None:
                return None
            else:
                return interpret(left_operand) / denominator
    except TypeError:
        # one of the operands is a string because there remains an operator
        # after splitting e.g "23/(2+2)" becomes "23/" "4" after resolving
        return interpret(str(left_operand) + str(right_operand))
    return None


def split_expression(expression):
    """
    Split the given expression into atomic statements.

    :param expression:
    :return: statements
    """
    if "-" in expression:
        statements = re.compile(r'[-]').split(expression)
    elif "+" in expression:
        statements = re.compile(r'[+]').split(expression)
    elif "/" in expression:
        statements = re.compile(r'[/]').split(expression)
    else:
        statements = re.compile(r'[*]').split(expression)
    return statements
