# Malimon

Математическая библиотека для вычисления выражений

# Инструкция

Команды библиотеки:
import malimon

# Основная функция calculate()
result = malimon.calculate("6+6-6*6:6-(6.6-6)")
print(result)  # 5.4

# Короткая команда calc()
result = malimon.calc("2 + 3 * 4")
print(result)  # 14.0

# С дробными числами
result = malimon.calculate("3.5 * 2 + 1.5")
print(result)  # 8.5

# Со скобками
result = malimon.calc("(10 + 5) * 2 - 8 / 4")
print(result)  # 28.0

# Использование класса MathParser
from malimon import MathParser
parser = MathParser()
result = parser.evaluate("5 * (3 + 2)")
print(result)  # 25.0

## Установка

```bash
pip install git+https://github.com/Limooomlord/Malimon.git
