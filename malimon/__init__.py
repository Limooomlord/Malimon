"""
Malimon - простая математическая библиотека для вычисления выражений.
"""

from .core import calculate, calc, MathParser, MalimonError, ParseError, CalculationError

__version__ = "1.0.0"
__all__ = ['calculate', 'calc', 'MathParser', 'MalimonError', 'ParseError', 'CalculationError']