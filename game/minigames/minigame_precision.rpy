# game/minigames/minigame_precision.rpy

label minigame_precision:
    window hide
    $ renpy.block_rollback()

    python:
        import random

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
                self.misses_allowed = 1  # можно допустить 1 промах

                self.yellow_center = 0.5
                self.yellow_width = 0.4
                self.green_width = 0.15
                self.min_yellow_px = 50
                self.min_green_px = 25

            def update(self):
                if not self.active or self.game_over:
                    return
                self.position += self.speed * self.direction * 0.016
                if self.position >= 1.0:
                    self.position = 1.0 - (self.position - 1.0)
                    self.direction = -1
                elif self.position <= 0.0:
                    self.position = -self.position
                    self.direction = 1
                self.position = max(0.0, min(1.0, self.position))

            def cut(self):
                if not self.active or self.game_over:
                    return
                pos = self.position
                yellow_left = self.yellow_center - self.yellow_width / 2
                yellow_right = self.yellow_center + self.yellow_width / 2
                green_left = self.yellow_center - self.green_width / 2
                green_right = self.yellow_center + self.green_width / 2

                if green_left <= pos <= green_right:
                    self.perfect_cuts += 1
                    success = True
                elif yellow_left <= pos <= yellow_right:
                    self.good_cuts += 1
                    success = True
                else:
                    self.miss_cuts += 1
                    if self.miss_cuts > self.misses_allowed:
                        self.game_over = True
                        self.active = False
                    else:
                        # промах, но не фатальный – просто пропускаем раунд без изменений
                        self.current_round += 1
                        if self.current_round >= self.rounds:
                            self.active = False
                        else:
                            self.position = random.uniform(0.2, 0.8)
                            self.direction = random.choice([-1, 1])
                        return

                # Успешный рез
                self.speed = min(self.speed * 1.1, 1.5)
                self.adjust_zones(self.direction)

                self.current_round += 1
                if self.current_round >= self.rounds:
                    self.active = False
                else:
                    self.position = random.uniform(0.2, 0.8)
                    self.direction = random.choice([-1, 1])

            def adjust_zones(self, direction):
                shift = random.uniform(0.03, 0.1)
                if direction == 1:
                    self.yellow_center -= shift
                else:
                    self.yellow_center += shift

                shrink_yellow = random.uniform(0.01, 0.05)
                shrink_green = random.uniform(0.01, 0.04)
                min_yellow_rel = self.min_yellow_px / 600.0
                min_green_rel = self.min_green_px / 600.0
                self.yellow_width = max(min_yellow_rel, self.yellow_width - shrink_yellow)
                self.green_width = max(min_green_rel, self.green_width - shrink_green)
                self.green_width = min(self.green_width, self.yellow_width)

                half_yellow = self.yellow_width / 2
                if self.yellow_center - half_yellow < 0:
                    self.yellow_center = half_yellow
                if self.yellow_center + half_yellow > 1:
                    self.yellow_center = 1 - half_yellow

            def get_score(self):
                if self.game_over:
                    return "fail"
                if self.perfect_cuts >= 3:
                    return "perfect"
                elif self.perfect_cuts + self.good_cuts >= 4:
                    return "good"
                else:
                    return "ok"

    # Основной цикл игры – будет повторяться при выборе "Повторить испытание"
    label .game_loop:
        python:
            game = PrecisionGame(rounds=5)
            result = renpy.call_screen("precision_game_screen", game=game)
    if result == "fail":
        # Провал: два промаха
        menu:
            "Испытание провалено. Что делаем?"
            "Повторить испытание":
                jump .game_loop
            "Вернуться к выбору испытаний":
                window show
                jump scene_1
    else:
        # Успех (perfect/good/ok – но ok не бывает, т.к. 5 раундов, всегда будет good или perfect)
        # Сохраняем результат в переменную для последующей обработки
        $ final_result = result
        if final_result == "perfect":
            $ точность += 3
            $ порядок_фактор += 10
            $ отношение_ивлев += 25
            $ рецепты.append("идеальная_нарезка")
            ai "Превосходно! Ваша точность достойна уважения. Идеальные кубы."
            i "Фримен! Ты справился блестяще! Я горжусь."
        else:
            $ точность += 1
            $ порядок_фактор += 5
            $ отношение_ивлев += 10
            $ рецепты.append("аккуратная_нарезка")
            ai "Неплохо. Не идеал, но кубики вполне пригодны."
            i "Хорошая работа, но стремись к совершенству!"
        window show
        return


screen precision_game_screen(game):
    key "dismiss" action Function(game.cut)

    frame:
        background Solid("#000000CC")
        xfill True
        yfill True

        vbox:
            spacing 25
            xalign 0.5
            yalign 0.5

            text "Точная нарезка кубов" size 60 xalign 0.5 color "#fff"
            text "Кликайте ЛКМ или нажмите «РЕЗАТЬ!», когда нож в ЖЁЛТОЙ или ЗЕЛЁНОЙ зоне" size 24 xalign 0.5 color "#ccc"

            fixed:
                xalign 0.5
                xsize 600
                ysize 80

                $ yellow_left = int((game.yellow_center - game.yellow_width/2) * 600)
                $ yellow_right = int((game.yellow_center + game.yellow_width/2) * 600)
                $ yellow_left = max(0, min(600, yellow_left))
                $ yellow_right = max(0, min(600, yellow_right))
                $ yellow_w = max(0, yellow_right - yellow_left)

                $ green_left = int((game.yellow_center - game.green_width/2) * 600)
                $ green_right = int((game.yellow_center + game.green_width/2) * 600)
                $ green_left = max(yellow_left, min(yellow_right, green_left))
                $ green_right = max(yellow_left, min(yellow_right, green_right))
                $ green_w = max(0, green_right - green_left)

                add Solid("#800000"):
                    pos (0, 20)
                    size (600, 40)

                if yellow_w > 0:
                    add Solid("#b3b300"):
                        pos (yellow_left, 20)
                        size (yellow_w, 40)

                if green_w > 0:
                    add Solid("#008000"):
                        pos (green_left, 20)
                        size (green_w, 40)

                if yellow_left > 0:
                    add Solid("#fff"):
                        pos (yellow_left, 20)
                        size (2, 40)
                if yellow_right < 600:
                    add Solid("#fff"):
                        pos (yellow_right - 2, 20)
                        size (2, 40)

                $ knife_x = int(game.position * 600)
                add Solid("#000000"):
                    pos (knife_x - 3, 15)
                    size (6, 50)

            text "Скорость ножа: [game.speed:.2f]" size 20 xalign 0.5 color "#ffa"
            text "Жёлтая зона: {:.0f}px, Зелёная: {:.0f}px".format(game.yellow_width*600, game.green_width*600) size 16 xalign 0.5 color "#aaa"
            text "Допустимо промахов: [game.misses_allowed - game.miss_cuts]" size 16 xalign 0.5 color "#ffa"

            hbox:
                xalign 0.5
                spacing 40
                text "Идеально: [game.perfect_cuts]" color "#0f0" size 28
                text "Хорошо: [game.good_cuts]" color "#ff0" size 28
                text "Промах: [game.miss_cuts]" color "#f00" size 28

            text "Осталось кубов: [game.rounds - game.current_round]" size 32 xalign 0.5 color "#fff"

            button:
                xalign 0.5
                background Solid("#4a4")
                xpadding 60
                ypadding 20
                action Function(game.cut)
                text "РЕЗАТЬ!" size 45 color "#000"

            if game.game_over:
                timer 0.1 action Return("fail")
            elif not game.active:
                timer 0.1 action Return(game.get_score())

    timer 0.016 repeat True action [Function(game.update), renpy.restart_interaction]