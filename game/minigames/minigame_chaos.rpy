init python:
    import random

    # Класс для хранения данных о каждом слове
    class ChaosItem:
        def __init__(self, text, is_good, color, cell):
            self.text = text
            self.is_good = is_good
            self.color = color
            self.cell = cell
            # Время жизни от 4 до 7 секунд
            self.life_time = random.uniform(4.0, 7.0)

            # Параметры анимации (фиксируются один раз при создании)
            self.base_size = random.randint(55, 85) # Крупный размер
            self.pulse_max = random.uniform(1.1, 1.3)
            self.pulse_speed = random.uniform(1.5, 3.0)

    # Функция создания нового предмета
    def spawn_chaos_item(items_list, positions):
        occupied_cells = [i.cell for i in items_list]
        available_cells = [c for c in range(len(positions)) if c not in occupied_cells]

        if not available_cells:
            return

        goods = ["МЯСО", "ТОМАТ", "СЫР", "ЛУК", "ПЕРЕЦ", "МАСЛО"]
        bads = ["БОМБА", "САПОГ", "КУРИЦА(живая)", "ЛОМ", "ГВОЗДЬ", "МУСОР"]
        colors = ["#ff0000", "#00ff00", "#00aaff", "#ffff00", "#ff00ff", "#00ffff", "#ffffff"]

        is_good = random.choice([True, True, False])
        txt = random.choice(goods if is_good else bads)
        clr = random.choice(colors)
        cell = random.choice(available_cells)

        items_list.append(ChaosItem(txt, is_good, clr, cell))

    # Функция старения и удаления предметов
    def age_chaos_items(items_list):
        to_remove = []
        for i in items_list:
            i.life_time -= 0.1
            if i.life_time <= 0:
                to_remove.append(i)
        for i in to_remove:
            items_list.remove(i)

# --- Плавная анимация дыхания ---
transform chaos_pulse(m_zoom, m_speed):
    subpixel True
    zoom 1.0
    parallel:
        easein m_speed zoom m_zoom
        easeout m_speed zoom 1.0
        repeat
    parallel:
        easein (m_speed*1.2) rotate 2
        easeout (m_speed*1.2) rotate -2
        repeat

# --- Экран игры ---
screen chaos_minigame_screen():
    default items = []
    default score = 0
    default time_left = 20.0

    # Сетка (не дает надписям накладываться)
    default grid_positions = [
        (0.15, 0.2), (0.38, 0.2), (0.62, 0.2), (0.85, 0.2),
        (0.15, 0.4), (0.38, 0.4), (0.62, 0.4), (0.85, 0.4),
        (0.15, 0.6), (0.38, 0.6), (0.62, 0.6), (0.85, 0.6),
        (0.15, 0.8), (0.38, 0.8), (0.62, 0.8), (0.85, 0.8)
    ]

    # Таймеры
    timer 0.1 repeat True action If(time_left > 0, SetScreenVariable("time_left", time_left - 0.1), Return(score))
    timer 0.8 repeat True action Function(spawn_chaos_item, items, grid_positions)
    timer 0.1 repeat True action Function(age_chaos_items, items)

    add Solid("#000e") # Темный фон

    vbox:
        xalign 0.5 ypos 30
        text "{b}ИСПЫТАНИЕ ХАОСОМ{/b}" color "#ff4400" size 50 xalign 0.5
        text "Осталось: [int(time_left)] | Счёт: [score]" color "#fff" size 30 xalign 0.5

    for item in items:
        textbutton item.text:
            pos grid_positions[item.cell]
            anchor (0.5, 0.5)
            at chaos_pulse(item.pulse_max, item.pulse_speed)

            text_color item.color
            text_size item.base_size
            text_outlines [ (2, "#000", 0, 0) ]

            background Frame(Solid("#ffffff15"), 4, 4)
            padding (25, 12)

            action [
                If(item.is_good, SetScreenVariable("score", score + 1), SetScreenVariable("score", score - 4)),
                RemoveFromSet(items, item)
            ]

# --- ВОТ ЭТОТ БЛОК БЫЛ ПРОПУЩЕН ---
label minigame_chaos_run:
    window hide
    call screen chaos_minigame_screen
    $ chaos_res = _return
    window show

    if chaos_res >= 12:
        i "Великолепно! Ты обуздал этот беспорядок! Настоящая кулинарная сингулярность."
        $ отношение_ивлев += 15
        return # Успех, возвращаемся в основной сюжет

    elif chaos_res >= 5:
        i "Приемлемо. По крайней мере, кухня всё еще стоит. Идем дальше."
        $ основы += 1
        return # Средний результат, идем дальше

    else:
        # СЕКЦИЯ ПРОВАЛА
        $ хаос_фактор += 10
        $ отношение_ивлев -= 10
        i "ПОЛНЫЙ ПРОВАЛ! Ты набрал мусора вместо еды! GladOS смеется над тобой!"

        menu:
            i "Что будем делать, Фримен?"

            "Перепройти испытание":
                i "Ладно, выкинь этот ботинок из кастрюли и начни заново!"
                jump minigame_chaos_run # Рекурсивный прыжок в начало этого же лейбла

            "Вернуться к выбору испытаний":
                i "Позорное бегство... Но лучше так, чем кормить людей этим хламом."
                jump scene_1 # Прыжок в начало, как ты и просил

            "Смириться и идти дальше":
                i "Ты хочешь оставить всё как есть? Ну, твоя совесть... И твой желудок."
                $ рецепты.append("полный_провал")
                return # Возвращаемся в script.rpy и продолжаем сюжет с плохим счетом