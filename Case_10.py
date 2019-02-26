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

"""
Блок считывания информации о разливочных автоматах.
"""
setup_file = open(setup, 'r+')
for line in setup_file:
    if (line[len(line)-1:len(line)] == '\n'):
        line = line[0:len(line)-1] # Убираю символ сноса строки.
    raw_line = line.split(' ') # Разделение по пробелу.
    number = int(raw_line[0])
    capacity = int(raw_line[1])
    gas_station[number] = {} # Формирование информации о разливочном автомате.
    gas_station[number]['busy'] = -1
    gas_station[number]['capacity'] = capacity
    gas_station[number]['filling'] = 0
    gas_station[number]['support'] = []
    for i in range(2, len(raw_line)):
        support_str = AI[raw_line[i]]
        gas_station[number]['support'].append(support_str) # Формирование списка поддерживаемых марок топлива.
setup_file.close()


"""
Блок считывания информации о событиях.
"""
data_file = open(data, 'r+')
for line in data_file:
    if (line[len(line)-1:len(line)] == '\n'):
        line = line[0:len(line)-1]
    raw_line = line.split(' ')
    time_str = raw_line[0].split(':') # Разделение по двоеточию для формирования времени в минутах.
    time_minutes = int(time_str[0])*60 + int(time_str[1]) # Формирование времени в минутах.
    liters = int (raw_line[1])
    mark = AI[raw_line[2]] # Исправление кодировки.
    if (timeline.get(time_minutes) == None):
        timeline[time_minutes] = [] # Создаю список событий в словаре от времени time_minutes, если его ещё нет.
    timeline[time_minutes].append(['IN', liters, -1, mark, -1]) # Добавляю в словарь событий от времени новое событие.
data_file.close()


"""
Блок обработчика событий.
"""
while (time_current <= time_limit):
    time_current += 1
    if (timeline.get(time_current) == None):
        continue
    for i in range(1, len(gas_station)+1):
        if gas_station[i]['busy'] <= time_current:
            gas_station[i]['busy'] = -1
    events = timeline[time_current]
    for event in events:
        if (event[0] == 'OUT'):
            gas_station[event[4]]['filling'] -= 1
            gas_station[event[4]]['busy'] = -1
            report['liters'][event[3]] += event[1]
            report['revenue'] += event[1]*COST[event[3]]
            print("В {} часов клиент {} {} {} {} заправил свой автомобиль и покинул АЗС.".format(
                convert_minutes_to_time(time_current),
                convert_minutes_to_time(time_current - event[2]),
                event[3], event[1], event[2]))
            for station in gas_station:
                print("Автомат №{} максимальная очередь: {} Марки бензина: ".format(station,
                                                                                    gas_station[station]['capacity'], ),
                      end='')
                for gas in gas_station[station]['support']:
                    print(gas, end=' ')
                print('->' + '*' * gas_station[station]['filling'])
        elif (event[0] == 'IN'):
            station_count = len(gas_station)
            event[4] = -1
            for i in range(1, station_count+1):
                if (event[4] == -1 and
                        gas_station[i]['filling'] < gas_station[i]['capacity'] and
                        gas_station[i]['support'].count(event[3]) > 0):
                    event[4] = i
                elif (event[4] != -1 and
                        gas_station[i]['filling'] < gas_station[i]['capacity'] and
                        gas_station[i]['filling'] < gas_station[event[4]]['filling'] and
                        gas_station[i]['support'].count(event[3]) > 0):
                    event[4] = i
            if (event[4] == -1):
                event[2] = convert_fuel_to_minutes(event[1])
                print("В {} часов новый клиент: {} {} {} {} не смог заправить автомобиль и покинул АЗС.".format(convert_minutes_to_time(time_current),
                                                                                            convert_minutes_to_time(time_current),
                                                                                            event[3], event[1], event[2]))
                report['customer_losses'] += 1
                for station in gas_station:
                    print("Автомат №{} максимальная очередь: {} Марки бензина: ".format(station, gas_station[station]['capacity'], ), end='')
                    for gas in gas_station[station]['support']:
                        print(gas, end=' ')
                    print('->' + '*'*gas_station[station]['filling'])
            else:
                gas_station[event[4]]['filling'] += 1
                event[2] = convert_fuel_to_minutes(event[1])
                if (gas_station[event[4]]['busy'] == -1):
                    gas_station[event[4]]['busy'] = time_current + event[2]
                else:
                    gas_station[event[4]]['busy'] += event[2]
                if (gas_station[event[4]]['busy'] > time_limit):
                    time_limit = gas_station[event[4]]['busy']
                if (timeline.get(gas_station[event[4]]['busy']) == None):
                    timeline[gas_station[event[4]]['busy']] = []
                timeline[gas_station[event[4]]['busy']].append(['OUT', event[1], event[2], event[3], event[4]])
                print("В {} часов новый клиент: {} {} {} {} встал в очередь к автомату №{}".format(convert_minutes_to_time(time_current),
                                                                                            convert_minutes_to_time(time_current),
                                                                                            event[3], event[1], event[2], event[4]))
                for station in gas_station:
                    print("Автомат №{} максимальная очередь: {} Марки бензина: ".format(station, gas_station[station]['capacity'], ), end='')
                    for gas in gas_station[station]['support']:
                        print(gas, end=' ')
                    print('->' + '*'*gas_station[station]['filling'])
print('\nОтчёт:')
print('Количество литров, проданное за сутки по каждой марке бензина:')
for sold in report['liters']:
    print(sold, ' продали ', report['liters'][sold], ' литров')
print('Общая сумма продаж за сутки: ', report['revenue'])
print('Количество клиентов, которые покинули АЗС не заправив автомобиль из-за \"скопившейся\" очереди: ', report['customer_losses'])
