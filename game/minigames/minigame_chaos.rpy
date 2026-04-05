init python:
    import random

    class ChaosItem:
        def __init__(self, text, is_good, color, cell):
            self.text = text
            self.is_good = is_good
            self.color = color
            self.cell = cell
            self.life_time = random.uniform(4.0, 7.0)
            self.base_size = random.randint(55, 85)
            self.pulse_max = random.uniform(1.1, 1.3)
            self.pulse_speed = random.uniform(1.5, 3.0)

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

    def age_chaos_items(items_list):
        to_remove = []
        for i in items_list:
            i.life_time -= 0.1
            if i.life_time <= 0:
                to_remove.append(i)
        for i in to_remove:
            items_list.remove(i)

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

screen chaos_minigame_screen():
    default items = []
    default score = 0
    default time_left = 20.0

    default grid_positions = [
        (0.15, 0.2), (0.38, 0.2), (0.62, 0.2), (0.85, 0.2),
        (0.15, 0.4), (0.38, 0.4), (0.62, 0.4), (0.85, 0.4),
        (0.15, 0.6), (0.38, 0.6), (0.62, 0.6), (0.85, 0.6),
        (0.15, 0.8), (0.38, 0.8), (0.62, 0.8), (0.85, 0.8)
    ]

    timer 0.1 repeat True action If(time_left > 0, SetScreenVariable("time_left", time_left - 0.1), Return(score))
    timer 0.8 repeat True action Function(spawn_chaos_item, items, grid_positions)
    timer 0.1 repeat True action Function(age_chaos_items, items)

    add Solid("#000e")

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

label minigame_chaos_run:
    window hide
    call screen chaos_minigame_screen
    $ chaos_res = _return
    window show
    return chaos_res