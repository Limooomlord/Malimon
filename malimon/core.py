import operator
import re


class MalimonError(Exception):
    """Базовое исключение для библиотеки Malimon"""
    pass


class ParseError(MalimonError):
    """Ошибка разбора выражения"""
    pass


class CalculationError(MalimonError):
    """Ошибка вычисления"""
    pass


def calculate(expression):
    """
    Вычисляет математическое выражение.

    Args:
        expression (str): Математическое выражение, например "6+6-6*6:6-(6.6-6)"

    Returns:
        float/int: Результат вычисления

    Raises:
        ParseError: Если выражение содержит синтаксические ошибки
        CalculationError: Если происходит ошибка вычисления (например, деление на ноль)
    """
    parser = MathParser()
    return parser.evaluate(expression)


def calc(expr):
    """Алиас для calculate"""
    return calculate(expr)


class MathParser:
    def __init__(self):
        self.operators = {
            '+': (1, operator.add),
            '-': (1, operator.sub),
            '*': (2, operator.mul),
            '/': (2, operator.truediv),
            ':': (2, operator.truediv),
        }
        self.token_pattern = re.compile(r'\d+\.\d+|\d+|[()+*:-]|\S')

    def tokenize(self, expression):
        expression = expression.replace(' ', '')
        tokens = self.token_pattern.findall(expression)
        if not tokens:
            raise ParseError("Пустое выражение")
        return tokens

    @staticmethod
    def is_number(token):
        try:
            float(token)
            return True
        except ValueError:
            return False

    def shunting_yard(self, tokens):
        output = []
        stack = []

        for token in tokens:
            if self.is_number(token):
                output.append(float(token) if '.' in token else int(token))
            elif token in self.operators:
                while (stack and stack[-1] != '(' and
                       self.operators.get(stack[-1], (0,))[0] >= self.operators[token][0]):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack:
                    raise ParseError("Непарная закрывающая скобка")
                stack.pop()

        while stack:
            if stack[-1] == '(':
                raise ParseError("Непарная открывающая скобка")
            output.append(stack.pop())

        return output

    def evaluate_rpn(self, rpn_tokens):
        stack = []

        for token in rpn_tokens:
            if isinstance(token, (int, float)):
                stack.append(token)
            elif token in self.operators:
                if len(stack) < 2:
                    raise CalculationError("Недостаточно операндов")
                b = stack.pop()
                a = stack.pop()
                try:
                    result = self.operators[token][1](a, b)
                    stack.append(result)
                except ZeroDivisionError:
                    raise CalculationError("Деление на ноль")
            else:
                raise ParseError(f"Неизвестный оператор: {token}")

        if len(stack) != 1:
            raise CalculationError("Некорректное выражение")

        return stack[0]

    def evaluate(self, expression):
        try:
            tokens = self.tokenize(expression)
            rpn_tokens = self.shunting_yard(tokens)
            result = self.evaluate_rpn(rpn_tokens)
            return result
        except (ParseError, CalculationError):
            raise
        except Exception as e:
            raise CalculationError(f"Ошибка вычисления: {e}")