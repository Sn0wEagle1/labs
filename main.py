import random
import itertools
from collections import Counter
import time
import tkinter as tk
from tkinter import messagebox

# Константы и переменные
N = 5 # Количество маршруток
DRIVERS_COUNT = 6 # Количество водителей
POINTS = 6  # Количество пунктов (не считая автопарка)
BUS_CAPACITY = 20  # Вместимость маршрутки
WORKING_HOURS = (24 + 3 - 6) * 60  # Рабочее время с 6:00 до 3:00
SHIFT_1_DURATION = 8 * 60  # Продолжительность смены 1 типа
SHIFT_2_DURATION = 12 * 60  # Продолжительность смены 2 типа
BREAK_DURATION_SHORT = 15  # Короткий перерыв
BREAK_DURATION_LONG = 30  # Длинный перерыв (2 коротких)
PEAK_HOURS_WEEKDAYS = [(7 * 60, 9 * 60), (17 * 60, 19 * 60)]  # Часы пик в будни
PEAK_HOURS_WEEKENDS = [(9 * 60, 19 * 60)]  # Возможный час пик в выходные
PEAK_PROBABILITY_WEEKENDS = 0.3  # Вероятность часа пик в выходные
SHIFT_CHANGE_DURATION = 15 # Длительность пересмены

# Генерация маршрутов
def generate_routes(points):
    routes = []

    # Цикличные маршруты (по часовой и против часовой)
    if points >= 1:  # Только если пунктов >= 4
        cyclic_route_clockwise = list(range(1, points + 1)) + [1]
        cyclic_route_counter_clockwise = [1] + list(range(points, 0, -1))
        routes.append(cyclic_route_clockwise)
        routes.append(cyclic_route_counter_clockwise)

    # Конечные маршруты
    for end_point in range(2, points + 1):
        if end_point >= 4 or points <= 4:  # Проверяем, что маршрут содержит хотя бы 4 пункта
            # Стандартный конечный маршрут (без 0)
            route_to_end = list(range(1, end_point + 1)) + list(range(end_point - 1, 0, -1))
            routes.append(route_to_end)

    return routes


# Распределение маршрутов: 1/4 кольцевые, остальные конечные, не более 2 маршруток на маршрут
def select_routes(routes, num_buses):
    cyclic_routes = [route for route in routes[:2]]  # Только длинные кольцевые маршруты
    cyclic_count = max(1, num_buses // 4)  # 1/4 маршрутов должны быть кольцевыми (минимум 1)

    # Создаем список кольцевых маршрутов, чередуя их
    selected_cyclic = []
    for i in range(cyclic_count):
        selected_cyclic.append(cyclic_routes[i % len(cyclic_routes)])  # Чередуем по часовой и против

    # Остальные маршруты — конечные
    terminal_routes = [route for route in routes[1:]] # Исключаем короткие маршруты
    remaining_count = num_buses - len(selected_cyclic)  # Сколько маршрутов осталось заполнить

    # Для конечных маршрутов также ограничиваем по 2 автобуса
    selected_terminal = []
    route_counter = Counter()

    while remaining_count > 0:
        # Выбираем случайный маршрут из конечных
        route = random.choice(terminal_routes)
        if route_counter[tuple(route)] < 2 or len(routes) < 4:  # Ограничение: не более 2 автобусов на маршрут
            selected_terminal.append(route)
            route_counter[tuple(route)] += 1
            remaining_count -= 1
    # Возвращаем итоговое распределение маршрутов
    return selected_cyclic + selected_terminal


def is_driver_available(driver_type, driver_state):
    # Дневной водитель: работает с 6:00 до 22:00
    if driver_type == 1:
        return driver_state['worked_hours'] < SHIFT_1_DURATION
    # Ночной водитель: работает с 22:00 до 6:00
    elif driver_type == 2:
        return driver_state['worked_hours'] < SHIFT_2_DURATION
    return False

# Генерация пассажиропотока
def generate_passenger_flow(current_time, is_peak):
    if is_peak:
        probabilities = [(3, 0.5), (4, 0.3), (2, 0.2)]
    else:
        probabilities = [(1, 0.5), (2, 0.4), (3, 0.1)]

    rand_val = random.random()
    cumulative = 0
    for passengers, probability in probabilities:
        cumulative += probability
        if rand_val <= cumulative:
            return passengers
    return 0

# Форматирование времени
def format_time(minutes):
    hours = (minutes // 60) % 24
    minutes = minutes % 60
    return f"{hours:02}:{minutes:02}"

# Проверка, является ли текущий момент часом пик
def is_peak_hour(current_time, weekday):
    if weekday < 5:  # Будний день
        return any(start <= current_time < end for start, end in PEAK_HOURS_WEEKDAYS)
    else:  # Выходной
        return random.random() < PEAK_PROBABILITY_WEEKENDS

# Логика обедов для первого типа водителей
def handle_type1_breaks(driver_state, current_time, is_peak, driver_id):
    if is_peak or driver_state['has_rest']:  # Не отдыхает в час пик или уже отдыхал
        return 0

    if driver_state['worked_hours'] >= 6:  # После 6 часов обязательно обед, чтобы не пропустить его
        driver_state['has_rest'] = True
        driver_state['rest_end_time'] = current_time + 60  # Обед на час
        print(f"Водитель {driver_id + 1} (тип 1) завершил маршрут в {format_time(current_time)} и уходит на обед длительностью 1 час.")
        return 60

    if random.random() < 0.2:  # С вероятностью 20%
        driver_state['has_rest'] = True
        driver_state['rest_end_time'] = current_time + 60  # Обед на час
        print(f"Водитель {driver_id + 1} (тип 1) завершил маршрут в {format_time(current_time)} и уходит на обед длительностью 1 час.")
        return 60

    return 0

# Логика обедов для второго типа водителей
def handle_type2_breaks(driver_state, current_time, driver_id):
    if driver_state['worked_hours'] >= 120:  # Отдых после 2 часов работы
        if not driver_state['had_long_break']:
            driver_state['had_long_break'] = True
            driver_state['rest_end_time'] = current_time + random.randint(30, 40)  # Длинный перерыв
            print(f"Водитель {driver_id + 1} (тип 2) завершил маршрут в {format_time(current_time)} и уходит на длинный перерыв.")
            return random.randint(30, 40)

        driver_state['rest_end_time'] = current_time + random.randint(15, 20)  # Короткий перерыв
        print(f"Водитель {driver_id + 1} (тип 2) завершил маршрут в {format_time(current_time)} и уходит на короткий перерыв.")
        return random.randint(15, 20)

    if not driver_state['had_long_break'] and current_time > 13 * 60 and driver_state['worked_hours'] >= 240:
        driver_state['had_long_break'] = True
        driver_state['rest_end_time'] = current_time + random.randint(30, 40)  # Длинный перерыв
        print(f"Водитель {driver_id + 1} (тип 2) завершил маршрут в {format_time(current_time)} и уходит на длинный перерыв.")
        return random.randint(30, 40)

    return 0


def handle_shift_change(driver_states, active_drivers, reserve_drivers, current_time, end_of_workday):
    """
    Выполняет пересмену водителей с учетом их состояния, включая отдых.
    """
    for driver_id in active_drivers[:]:  # Копируем список активных водителей
        driver_state = driver_states[driver_id]

        # Проверяем, нужно ли менять водителя
        if (
                driver_state['worked_hours'] >= (SHIFT_2_DURATION if driver_id % 2 == 0 else SHIFT_1_DURATION)
                and (end_of_workday - current_time) > 60  # До конца дня > 1 часа
        ):
            # Ищем доступного резервного водителя
            for reserve_driver_id in reserve_drivers[:]:
                reserve_driver_state = driver_states[reserve_driver_id]
                active_driver_state = driver_states[driver_id]

                # Проверяем, доступен ли резервный водитель
                if (
                        current_time >= reserve_driver_state['rest_end_time'] and
                        reserve_driver_state['rest_until_day'] <= (current_time // (24 * 60))  # Доступен по дням
                ):
                    # Выполняем пересмену
                    active_driver_state['rest_until_day'] += 3
                    active_drivers.remove(driver_id)
                    reserve_drivers.remove(reserve_driver_id)

                    active_drivers.append(reserve_driver_id)
                    reserve_drivers.append(driver_id)  # Перемещаем текущего водителя в резерв

                    # Обновляем состояние текущего водителя (теперь он в резерве)
                    driver_state['breaks'].append(
                        (format_time(current_time), format_time(current_time + SHIFT_CHANGE_DURATION))
                    )
                    driver_state['rest_end_time'] = current_time + SHIFT_CHANGE_DURATION
                    driver_state['worked_hours'] = 0
                    driver_state['is_on_shift'] = False  # Уход со смены

                    # Обновляем состояние нового водителя (теперь он активный)
                    reserve_driver_state['is_on_shift'] = True
                    reserve_driver_state['shift_start_time'] = current_time
                    reserve_driver_state['worked_hours'] = 0

                    print(f"Пересмена: водитель {driver_id + 1} заменен на {reserve_driver_id + 1}")
                    break
            else:
                # Нет доступных водителей для пересмены
                print(f"Пересмена невозможна для водителя {driver_id + 1}: нет доступных резервных водителей")


def simulate_bus_route(bus_id, route, start_time, stops, drivers, driver_state, driver_type, is_peak):
    current_time = start_time
    total_passengers = 0
    remaining_capacity = BUS_CAPACITY
    total_boarded_passengers = 0

    for i in range(len(route) - 1):
        # Проверка доступности водителя
        if not is_driver_available(driver_type, driver_state):
            return total_boarded_passengers, current_time, 0  # Завершаем маршрут без вывода

        start_point = route[i]
        passengers_at_stop = stops[start_point]
        passengers_to_board = min(passengers_at_stop, remaining_capacity)
        stops[start_point] -= passengers_to_board
        total_passengers += passengers_to_board
        total_boarded_passengers += passengers_to_board
        remaining_capacity -= passengers_to_board

        # Обновляем время на поездку между пунктами
        current_time += random.randint(12, 18)

        if i < len(route) - 2:  # Не на конечной остановке
            passengers_to_exit = int(total_passengers * 0.4)
            total_passengers -= passengers_to_exit
            remaining_capacity += passengers_to_exit

    remaining_capacity += total_passengers
    total_passengers = 0

    # Завершаем маршрут
    if is_driver_available(driver_type, driver_state):  # Только если водитель доступен
        print(f"Водитель {bus_id + 1} завершил маршрут в {format_time(current_time)}.")

    # Добавляем время для отдыха
    if driver_type == 1:
        rest_time = handle_type1_breaks(driver_state, current_time, is_peak, bus_id)
    else:
        rest_time = handle_type2_breaks(driver_state, current_time, bus_id)

    driver_state['worked_hours'] += current_time - start_time
    current_time += rest_time

    return total_boarded_passengers, current_time - rest_time, rest_time


def genetic_algorithm(drivers, buses, points, all_routes, generations=30, population_size=20, mutation_rate=0.1):
    num_buses = len(buses)

    # Инициализация популяции
    population = [
        (
            random.sample(all_routes, num_buses),  # Случайный выбор маршрутов
            random.sample(range(len(drivers)), num_buses)  # Случайное распределение водителей
        )
        for _ in range(population_size)
    ]

    for generation in range(generations):
        # Оценка пригодности
        fitness_scores = [
            (calculate_fitness(individual, drivers, buses, points), individual)
            for individual in population
        ]
        fitness_scores.sort(reverse=True, key=lambda x: x[0])  # Сортируем по убыванию пригодности

        # Отбор лучших
        elites = fitness_scores[:5]  # Топ-5 переходит в следующее поколение
        best_individuals = fitness_scores[:population_size // 2]

        # Создание нового поколения
        new_population = [individual for _, individual in elites]

        while len(new_population) < population_size:
            parent1 = random.choice(best_individuals)[1]
            parent2 = random.choice(best_individuals)[1]
            child = (
                parent1[0][:num_buses // 2] + parent2[0][num_buses // 2:],
                parent1[1][:num_buses // 2] + parent2[1][num_buses // 2:]
            )

            # Мутация
            if random.random() < mutation_rate:
                child = (
                    random.sample(all_routes, num_buses),
                    random.sample(range(len(drivers)), num_buses)
                )

            new_population.append(child)

        population = new_population

    # Находим лучшее решение
    best_fitness, best_solution = max(
        (calculate_fitness(individual, drivers, buses, points), individual)
        for individual in population
    )

    return best_solution, best_fitness


# Функция пригодности
def calculate_fitness(solution, drivers, buses, points):
    """Оценка пригодности решения на основе короткой недели."""
    route_combination, driver_assignment = solution
    total_passengers = simulate_short_week(drivers, buses, points, route_combination, driver_assignment)
    return total_passengers

# Главная функция симуляции
# Функция симуляции недели с учетом распределения маршрутов
def simulate_week(drivers, buses, points, route_combination=None, driver_assignment=None):
    """Симуляция недели с заданными маршрутами и распределением водителей."""
    all_routes = generate_routes(points)
    routes = select_routes(all_routes, len(buses)) if route_combination is None else route_combination

    max_total_passengers = 0
    best_schedule = []
    total_revenue = 0
    best_combinations = []

    for route_combination in itertools.combinations(routes, len(buses)):
        if not validate_route_combination(route_combination):
            continue

        for driver_assignment in itertools.permutations(range(len(drivers)), len(buses)):
            schedule = []
            total_passengers = 0
            driver_states = [
                {
                    'has_rest': False, 'worked_hours': 0, 'had_long_break': False,
                    'rest_end_time': 0, 'rest_until_day': 0,
                    'is_on_shift': False, 'shift_start_time': 0,
                    'breaks': []
                }
                for _ in drivers
            ]

            for day in range(7):
                # Инициализация пула водителей
                active_drivers = list(driver_assignment)
                reserve_drivers = list(set(range(len(drivers))) - set(active_drivers))

                # Сброс состояния водителей в начале нового дня
                for i, state in enumerate(driver_states):
                    rest_until_day = state['rest_until_day']
                    driver_states[i] = {
                        'has_rest': False,
                        'worked_hours': 0,
                        'had_long_break': False,
                        'rest_end_time': 0,
                        'rest_until_day': rest_until_day,
                        'is_on_shift': False,
                        'shift_start_time': 0,
                        'breaks': []
                    }

                stops = [0] * (points + 1)
                bus_states = [6 * 60] * len(buses)  # Все автобусы начинают работу в 6:00

                for minute in range(6 * 60, 27 * 60):  # Симуляция рабочего дня
                    weekday = day % 7

                    if minute % 20 == 0:
                        for stop in range(len(stops)):
                            stops[stop] += generate_passenger_flow(minute, is_peak_hour(minute, weekday))

                    # Выполняем пересмену водителей
                    handle_shift_change(
                        driver_states,
                        active_drivers=active_drivers,
                        reserve_drivers=reserve_drivers,
                        current_time=minute,
                        end_of_workday=27 * 60
                    )

                    for bus_id, route in enumerate(route_combination):
                        if bus_states[bus_id] <= minute:  # Если автобус свободен
                            driver_id = active_drivers[bus_id]
                            driver_state = driver_states[driver_id]

                            # Проверка доступности водителя
                            if day < driver_state['rest_until_day']:
                                continue  # Пропускаем водителя, если он находится на отдыхе

                            if minute < driver_state['rest_end_time']:
                                continue

                            driver_type = 1 if driver_id % 2 == 0 else 2
                            if not is_driver_available(driver_type, driver_state):
                                continue

                            # Если водитель начинает новую смену, фиксируем время
                            if not driver_state['is_on_shift']:
                                driver_state['is_on_shift'] = True
                                driver_state['shift_start_time'] = minute

                            # Добавляем автопарк (пункт `0`) в начало маршрута для первого рейса
                            if driver_state['worked_hours'] == 0:
                                route = [0] + route

                            # Выполняем маршрут
                            passengers, end_time, rest_time = simulate_bus_route(
                                bus_id, route, minute, stops, drivers, driver_state, driver_type,
                                is_peak_hour(minute, weekday)
                            )

                            if passengers == 0:  # Если пассажиров нет
                                # Обновляем время следующего возможного старта автобуса
                                bus_states[bus_id] = minute + 20  # Добавляем простой 20 минут
                                continue

                            total_passengers += passengers

                            # Обновляем состояние автобуса
                            bus_states[bus_id] = end_time  # Обновляем время завершения маршрута

                            # Записываем данные о рейсе
                            schedule.append(
                                (day, bus_id + 1, driver_id + 1, driver_type, route, passengers,
                                 format_time(minute), format_time(end_time))
                            )

                            if rest_time > 0:
                                schedule.append(
                                    (day, bus_id + 1, driver_id + 1, driver_type, "Обед", 0,
                                     format_time(end_time), format_time(end_time + rest_time))
                                )

                            # Обновляем состояние для водителя 2 типа после завершения смены
                            if driver_type == 2 and (
                                    driver_state['worked_hours'] >= SHIFT_2_DURATION or minute >= 26 * 60):
                                driver_state['rest_until_day'] = day + 3  # Добавляем 2 дня отдыха

            # Сравнение с максимальным значением пассажиропотока
            if total_passengers > max_total_passengers:
                max_total_passengers = total_passengers
                best_schedule = schedule
                total_revenue = max_total_passengers
                best_combinations = []

                for entry in schedule:
                    day, bus_id, driver_id, driver_type, route, passengers, start_time, end_time = entry
                    best_combinations.append({
                        'day': day,
                        'bus_id': bus_id,
                        'driver_id': driver_id,
                        'driver_type': driver_type,
                        'route': route,
                        'passengers': passengers,
                        'start_time': start_time,
                        'end_time': end_time
                    })

    return best_schedule, total_revenue, best_combinations

def simulate_short_week(drivers, buses, points, route_combination=None, driver_assignment=None):
    """Симуляция двух дней подряд: одного буднего и одного выходного."""
    all_routes = generate_routes(points)
    routes = select_routes(all_routes, len(buses)) if route_combination is None else route_combination

    total_passengers = 0
    driver_states = [
        {
            'has_rest': False, 'worked_hours': 0, 'had_long_break': False,
            'rest_end_time': 0, 'rest_until_day': 0,
            'is_on_shift': False, 'shift_start_time': 0,
            'breaks': []
        }
        for _ in drivers
    ]

    days_to_simulate = [0, 5]  # Один будний (пн) и один выходной (сб)
    stops = [0] * (points + 1)  # Состояние остановок
    bus_states = [6 * 60] * len(buses)  # Все автобусы начинают работу в 6:00

    for day in days_to_simulate:
        # Сброс состояния водителей в начале нового дня
        for i, state in enumerate(driver_states):
            rest_until_day = state['rest_until_day']
            driver_states[i] = {
                'has_rest': False,
                'worked_hours': 0,
                'had_long_break': False,
                'rest_end_time': 0,
                'rest_until_day': rest_until_day,
                'is_on_shift': False,
                'shift_start_time': 0,
                'breaks': []
            }

        for minute in range(6 * 60, 27 * 60):  # Симуляция рабочего дня
            if minute % 20 == 0:
                for stop in range(len(stops)):
                    stops[stop] += generate_passenger_flow(minute, is_peak_hour(minute, day))

            # Выполняем пересмену водителей
            active_drivers = list(driver_assignment)
            reserve_drivers = list(set(range(len(drivers))) - set(active_drivers))
            handle_shift_change(
                driver_states,
                active_drivers=active_drivers,
                reserve_drivers=reserve_drivers,
                current_time=minute,
                end_of_workday=27 * 60
            )

            # Симуляция работы каждого автобуса
            for bus_id, route in enumerate(routes):
                if bus_states[bus_id] <= minute:  # Если автобус свободен
                    driver_id = active_drivers[bus_id]
                    driver_state = driver_states[driver_id]

                    # Проверка доступности водителя
                    if day < driver_state['rest_until_day']:
                        continue
                    if minute < driver_state['rest_end_time']:
                        continue

                    driver_type = 1 if driver_id % 2 == 0 else 2
                    if not is_driver_available(driver_type, driver_state):
                        continue

                    # Если водитель начинает новую смену
                    if not driver_state['is_on_shift']:
                        driver_state['is_on_shift'] = True
                        driver_state['shift_start_time'] = minute

                    # Добавляем автопарк (пункт `0`) в начало маршрута для первого рейса
                    if driver_state['worked_hours'] == 0:
                        route = [0] + route

                    # Выполняем маршрут
                    passengers, end_time, rest_time = simulate_bus_route(
                        bus_id, route, minute, stops, drivers, driver_state, driver_type,
                        is_peak_hour(minute, day)
                    )

                    total_passengers += passengers
                    bus_states[bus_id] = end_time  # Обновляем время завершения маршрута

                    # Обновляем состояние для водителей 2 типа
                    if driver_type == 2 and (
                            driver_state['worked_hours'] >= SHIFT_2_DURATION or minute >= 26 * 60):
                        driver_state['rest_until_day'] = day + 3

    return total_passengers



# Проверка ограничения на маршруты
def validate_route_combination(route_combination):
    # Преобразуем маршруты в кортежи для подсчета
    route_counter = Counter(tuple(route) for route in route_combination)
    return all(count <= 2 for count in route_counter.values())


def log_to_output(text):
    output_text.insert(tk.END, text + '\n')
    output_text.yview(tk.END)

# Функция для запуска обычного перебора
def run_brute_force():
    try:
        drivers_count = int(drivers_entry.get())
        buses_count = int(buses_entry.get())
        points_count = int(points_entry.get())

        if drivers_count <= 0 or buses_count <= 0 or points_count <= 0:
            raise ValueError("Все значения должны быть больше нуля.")

        log_to_output(f"Запуск обычного перебора с параметрами:\n"
                      f"Водители: {drivers_count} | Маршрутки: {buses_count} | Пункты: {points_count}")

        # Инициализация данных
        drivers = [1] * drivers_count
        buses = [1] * buses_count
        points = points_count

        # Запуск обычного перебора
        log_to_output("Запуск обычного перебора...")
        start_time = time.time()
        best_schedule_brute, total_revenue_brute, best_combinations_brute = simulate_week(drivers, buses, points)
        brute_time = time.time() - start_time

        log_to_output(f"\nОбщий пассажиропоток за неделю (перебор): {total_revenue_brute}")
        if best_combinations_brute:
            log_to_output(f"\nОптимальные комбинации маршрутов, водителей и автобусов за неделю (перебор):")
            for comb in best_combinations_brute:
                # Преобразуем все пункты маршрута в строки
                route_str = ' - '.join(map(str, comb['route']))  # Преобразуем каждый пункт в строку
                if "б" in comb['route']:
                    log_to_output(f"День: {comb['day'] + 1} | Водитель: {comb['driver_id']} "
                              f"(Тип {comb['driver_type']}) | Автобус: {comb['bus_id']} | Ушёл на обед | "
                              f"Время: {comb['start_time']} - {comb['end_time']}")
                else:
                    log_to_output(f"День: {comb['day'] + 1} | Маршрут: {route_str} | Водитель: {comb['driver_id']} "
                                  f"(Тип {comb['driver_type']}) | Автобус: {comb['bus_id']} | Пассажиры: {comb['passengers']} | "
                                  f"Время: {comb['start_time']} - {comb['end_time']}")

        log_to_output(f"\nВремя выполнения обычного перебора: {brute_time:.2f} секунд")

    except ValueError as ve:
        messagebox.showerror("Ошибка", f"Неверный ввод: {ve}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

def run_genetic_algorithm():
    try:
        drivers_count = int(drivers_entry.get())
        buses_count = int(buses_entry.get())
        points_count = int(points_entry.get())

        if drivers_count <= 0 or buses_count <= 0 or points_count <= 0:
            raise ValueError("Все значения должны быть больше нуля.")

        log_to_output(f"Запуск генетического алгоритма с параметрами:\n"
                      f"Водители: {drivers_count} | Маршрутки: {buses_count} | Пункты: {points_count}")

        # Корректировка данных
        if points_count < drivers_count:
            log_to_output("Предупреждение: количество пунктов меньше числа водителей. Расширяем список пунктов.")
            points_count = drivers_count

        # Инициализация данных
        drivers = [1] * drivers_count
        buses = [1] * buses_count
        points = points_count
        all_routes = generate_routes(points)  # Генерация маршрутов с проверкой

        log_to_output(f"Сгенерировано маршрутов: {len(all_routes)}")

        # Запуск генетического алгоритма
        log_to_output("Запуск генетического алгоритма...")
        start_time = time.time()
        best_solution, best_fitness = genetic_algorithm(drivers, buses, points, all_routes)
        ga_time = time.time() - start_time

        log_to_output(f"\nГенетический алгоритм: {best_fitness} пассажиров, время {ga_time:.2f} секунд")

        schedule, total_revenue, best_combinations = simulate_week(drivers, buses, points, *best_solution)

        if best_combinations:
            log_to_output(f"\nОптимальные комбинации маршрутов, водителей и автобусов за неделю (генетический алгоритм):")
            for comb in best_combinations:
                route_str = ' - '.join(map(str, comb.get('route', [])))
                if "б" in comb['route']:
                    log_to_output(f"День: {comb['day'] + 1} | Водитель: {comb['driver_id']} "
                                  f"(Тип {comb['driver_type']}) | Автобус: {comb['bus_id']} | Ушёл на обед | "
                                  f"Время: {comb['start_time']} - {comb['end_time']}")
                else:
                    log_to_output(f"День: {comb['day'] + 1} | Маршрут: {route_str} | Водитель: {comb['driver_id']} "
                                  f"(Тип {comb['driver_type']}) | Автобус: {comb['bus_id']} | Пассажиры: {comb['passengers']} | "
                                  f"Время: {comb['start_time']} - {comb['end_time']}")

        log_to_output(f"\nВремя выполнения генетического алгоритма: {ga_time:.2f} секунд")

    except ValueError as ve:
        messagebox.showerror("Ошибка", f"Неверный ввод: {ve}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")


# Основное окно приложения
root = tk.Tk()
root.title("Параметры симуляции")

# Устанавливаем размеры окна
root.geometry("900x720")

# Текст и поле ввода для количества водителей
drivers_label = tk.Label(root, text="Количество водителей:")
drivers_label.pack(pady=5)
drivers_entry = tk.Entry(root)
drivers_entry.pack(pady=5)

# Текст и поле ввода для количества маршруток
buses_label = tk.Label(root, text="Количество маршруток:")
buses_label.pack(pady=5)
buses_entry = tk.Entry(root)
buses_entry.pack(pady=5)

# Текст и поле ввода для количества пунктов
points_label = tk.Label(root, text="Количество пунктов (без автопарка):")
points_label.pack(pady=5)
points_entry = tk.Entry(root)
points_entry.pack(pady=5)

# Кнопка для запуска обычного перебора
brute_button = tk.Button(root, text="Запуск обычного перебора", command=run_brute_force)
brute_button.pack(pady=10)

# Кнопка для запуска генетического алгоритма
ga_button = tk.Button(root, text="Запуск генетического алгоритма", command=run_genetic_algorithm)
ga_button.pack(pady=10)

# Текстовое поле для вывода логов
output_text = tk.Text(root, width=120, height=20)
output_text.pack(pady=10)

# Запуск GUI
root.mainloop()
