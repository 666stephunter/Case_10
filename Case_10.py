from random import randint

def convert_fuel_to_minutes(fuel):
    fuel = int(fuel)
    time_minutes = fuel // 10
    if (fuel % 10 > 0):
        time_minutes += 1
    time_minutes += randint(-1, 1)
    if (time_minutes < 1):
        time_minutes = 1
    return time_minutes

def convert_minutes_to_time(minutes):
    hours = (minutes//60)%24
    minutes = minutes%60
    hours = str(hours)
    minutes = str(minutes)
    if (len (hours) < 2):
        hours = '0' + hours
    if (len (minutes) < 2):
        minutes = '0' + minutes
    return hours + ':' + minutes

# Наименования файлов:
setup = "azs.txt"
data = "input.txt"

AI = {}
AI["AI-80"] = "AI-80"
AI["AI-92"] = "AI-92"
AI["AI-95"] = "AI-95"
AI["AI-98"] = "AI-98"

# Стоимость одного литра бензина.
COST = {}
COST["AI-80"] = 38
COST["AI-92"] = 41
COST["AI-95"] = 44
COST["AI-98"] = 49

# Итоговый отчёт.
report = {}
report['liters'] = {}
report['liters']["AI-80"] = 0
report['liters']["AI-92"] = 0
report['liters']["AI-95"] = 0
report['liters']["AI-98"] = 0
report['revenue'] = 0
report['customer_losses'] = 0

time_current = -1 # Время инициализации обработчика событий в минутах.
time_limit = 24*60 # Время предположительного завершения работы обработчика событий в минутах.

"""
timeline - 
Хранилище для событий в виде словаря списков.
ключ - время в минутах, 
значение - list событий на это время.
событие:
    [type, liters, time, mark, station]
    type:
        Строка. Возможные значения: 'IN' или 'OUT'.
        'IN' - машина пытается войти в очередь.
        'OUT' - машина заправилась и покидает очередь.
    liters:
        Целое число - количество литров, необходимое водителю.
    time:
        Время, необходимое на заправку.
        Если type = 'IN', то time изначально равен -1.
        Значение time присваивается в цикле обработчика событий.
    mark:
        Марка бензина. Строка в исправленной кодировке.
    station:
        Номер разливочного автомата. 
        Если type = 'IN', то time изначально равен -1.
        Значение station присваивается в цикле обработчика событий.
"""
timeline = {}


"""
gas_station - 
Хранилище информации об разливочных автоматах в виде словаря словарей.
ключ - целочисленный номер автомата, 
значение - словарь:
    ['busy'] - время в минутах, когда автомат освободится.
        -1, если автомат не занят.
    ['capacity'] - максимальный размер очереди перед разливочным автоматом.
    ['filling'] - текущий размер очереди перед разливочным автоматом.
    ['support'] - список поддерживаемых марок бензина.
"""
gas_station = {}
