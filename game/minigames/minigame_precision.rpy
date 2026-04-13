# game/minigames/minigame_precision.rpy

init python:
    import random

    # Класс должен быть в init python, чтобы Ren'Py видел его при загрузке
    class PrecisionGame:
        def __init__(self, rounds=5):
            self.rounds = rounds
            self.reset()

        def reset(self):
            self.position = 0.5
            self.direction = 1
            self.speed = 0.7
            self.current_round = 0
            self.perfect_cuts = 0
            self.good_cuts = 0
            self.miss_cuts = 0
            self.active = True
            self.game_over = False
            self.misses_allowed = 1
            self.yellow_center = 0.5
            self.yellow_width = 0.4
            self.green_width = 0.15
            self.min_yellow_px = 50
            self.min_green_px = 25

        def update(self):
            if not self.active or self.game_over:
                return

            # 0.016 соответствует примерно 60 FPS
            self.position += self.speed * self.direction * 0.016

            if self.position >= 1.0:
                self.position = 1.0
                self.direction = -1
            elif self.position <= 0.0:
                self.position = 0.0
                self.direction = 1

        def cut(self):
            if not self.active or self.game_over:
                return

            pos = self.position
            yellow_left = self.yellow_center - self.yellow_width / 2
            yellow_right = self.yellow_center + self.yellow_width / 2
            green_left = self.yellow_center - self.green_width / 2
            green_right = self.yellow_center + self.green_width / 2

            # Логика попадания
            if green_left <= pos <= green_right:
                self.perfect_cuts += 1
            elif yellow_left <= pos <= yellow_right:
                self.good_cuts += 1
            else:
                self.miss_cuts += 1
                if self.miss_cuts > self.misses_allowed:
                    self.game_over = True
                    self.active = False
                    return

            # Проверка завершения игры
            self.current_round += 1
            if self.current_round >= self.rounds:
                self.active = False
            else:
                # Усложнение и сброс позиции для следующего раунда
                self.speed = min(self.speed * 1.15, 1.8)
                self.adjust_zones()
                self.position = random.uniform(0.1, 0.9)
                self.direction = random.choice([-1, 1])

        def adjust_zones(self):
            # Сдвигаем центр зоны
            shift = random.uniform(-0.15, 0.15)
            self.yellow_center = max(self.yellow_width/2, min(1.0 - self.yellow_width/2, self.yellow_center + shift))

            # Сужаем зоны
            min_yellow_rel = self.min_yellow_px / 600.0
            min_green_rel = self.min_green_px / 600.0

            self.yellow_width = max(min_yellow_rel, self.yellow_width * 0.9)
            self.green_width = max(min_green_rel, self.green_width * 0.85)

        def get_score(self):
            if self.game_over:
                return "fail"
            if self.perfect_cuts >= 3:
                return "perfect"
            elif self.perfect_cuts + self.good_cuts >= 4:
                return "good"
            else:
                return "ok"

# Объявляем переменную через default для системы сохранений
default current_precision_game = None

label minigame_precision:
    window hide
    $ renpy.block_rollback()

    python:
        current_precision_game = PrecisionGame(rounds=5)
        # Вызываем экран и ждем результат через Return()
        result = renpy.call_screen("precision_game_screen", game=current_precision_game)

    window show
    return result

screen precision_game_screen(game):
    # Управление: Пробел, Enter или Клик (через кнопку ниже)
    key "K_SPACE" action Function(game.cut)
    key "K_RETURN" action Function(game.cut)
    key "K_KP_ENTER" action Function(game.cut)

    # Обновление состояния игры
    timer 0.016 repeat True action [Function(game.update), renpy.restart_interaction]

    frame:
        background Solid("#000000CC")
        xfill True
        yfill True

        vbox:
            spacing 25
            xalign 0.5
            yalign 0.4

            text "Точная нарезка" size 50 xalign 0.5 color "#fff" outlines [(2, "#000")]

            # Игровое поле
            fixed:
                xalign 0.5
                xsize 600
                ysize 100

                # Фон полоски
                add Solid("#444"):
                    pos (0, 30)
                    size (600, 40)

                # Вычисляем координаты зон
                $ y_w = int(game.yellow_width * 600)
                $ y_x = int((game.yellow_center - game.yellow_width/2) * 600)
                $ g_w = int(game.green_width * 600)
                $ g_x = int((game.yellow_center - game.green_width/2) * 600)

                # Желтая зона
                add Solid("#b3b300"):
                    pos (y_x, 30)
                    size (y_w, 40)

                # Зеленая зона
                add Solid("#008000"):
                    pos (g_x, 30)
                    size (g_w, 40)

                # Указатель (нож)
                $ knife_x = int(game.position * 600)
                add Solid("#ffffff"):
                    pos (knife_x - 2, 20)
                    size (4, 60)
                    subpixel True

            # Статистика
            hbox:
                xalign 0.5
                spacing 50
                text "Идеально: [game.perfect_cuts]" color "#0f0" size 24
                text "Хорошо: [game.good_cuts]" color "#ff0" size 24
                text "Промахи: [game.miss_cuts]/[game.misses_allowed + 1]" color "#f00" size 24

            text "Осталось нарезать: [game.rounds - game.current_round]" size 30 xalign 0.5 color "#fff"

            # Кнопка действия
            button:
                xalign 0.5
                background Frame(Solid("#4a4"), 4, 4)
                xpadding 80
                ypadding 20
                action Function(game.cut)
                hover_background Solid("#6c6")
                text "РЕЗАТЬ!" size 40 color "#000" bold True xalign 0.5

    # Проверка условий выхода
    if game.game_over:
        timer 0.5 action Return("fail")
    elif not game.active:
        timer 0.5 action Return(game.get_score())