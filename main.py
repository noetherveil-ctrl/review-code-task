import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # Рекомендация: разбить выбор даты на обычный if/else для читаемости.
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        # Рекомендация: вычислить сегодняшнюю дату один раз, а в sum передать
        # генератор. Это уберёт повторные вызовы now и промежуточный список.
        return sum([rec.amount for rec in self.records if rec.date == dt.datetime.now().date()])

    def get_week_stats(self):
        today = dt.datetime.now().date()
        # Рекомендация: записать условие как 0 <= (today - rec.date).days < 7.
        # Так границы интервала читаются привычнее и их проще проверить.
        return sum([rec.amount for rec in self.records if 7 > (today - rec.date).days >= 0])


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # Рекомендация: назвать x calories_remained, чтобы было понятно его назначение.
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            return ('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # Ошибка: если после создания класса присвоить CashCalculator.USD_RATE = 80,
        # метод всё равно использует 60. Значения аргументов запоминаются при
        # определении метода. Брать курсы из self.USD_RATE и self.EURO_RATE.
        # Ошибка: при лимите 0.3 и расходах 0.1 и 0.2 в рублях получается
        # «долг - 0.00» из-за погрешности float. Для денег использовать Decimal
        # из строк либо целое число копеек и согласованно округлять результат.
        cash_remained = self.limit - self.get_today_stats()

        d = {'usd': (USD_RATE, 'USD'), 'eur': (EURO_RATE, 'Euro'), 'rub': (1.0, 'руб')}

        rate = d.get(currency)
        if rate is None:
            return f'Неизвестная валюта {currency}'

        # Ошибка: вызов get_today_cash_remained('usd', USD_RATE=0)
        # завершится ZeroDivisionError. До деления проверить, что курс больше нуля.
        cash_remained /= rate[0]
        # Рекомендация: распаковать rate в rate_value, currency_type, чтобы
        # не искать ту же валюту в словаре второй раз и улучшить читаемость.
        currency_type = d.get(currency)[1]

        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    def get_week_stats(self):
        # Ошибка: CashCalculator(100).get_week_stats() возвращает None даже
        # без записей. Нужен return super().get_week_stats(), либо удалить
        # переопределение: метод уже унаследован от Calculator.
        super().get_week_stats()
