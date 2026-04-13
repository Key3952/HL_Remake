# minigame_sonic_runner.rpy - гонка с Соником (раннер) с автоматическим масштабированием

init python:
    import random

    class SonicRunner:
        def __init__(self, lanes=3, target_score=10, start_lives=3):
            self.lanes = lanes
            self.target_score = target_score
            self.start_lives = start_lives
            self.reset()

        def reset(self):
            self.score = 0
            self.lives = self.start_lives
            self.game_over = False
            self.win = False
            self.active = True
            self.paused = True
            self.player_lane = 1
            self.objects = []
            self.spawn_delay = 12          # уменьшили с 25 до 12 (чаще появление)
            self.spawn_timer = 0

        def update(self):
            if self.game_over or not self.active or self.paused:
                return
            # Движение объектов влево
            new_objects = []
            for x, lane, obj_type in self.objects:
                x -= 1
                if x >= 0:
                    new_objects.append((x, lane, obj_type))
            self.objects = new_objects

            # Столкновения
            for obj in self.objects[:]:
                x, lane, obj_type = obj
                if lane == self.player_lane and x == 0:
                    if obj_type == "ring":
                        self.score += 1
                        if self.score >= self.target_score:
                            self.win = True
                            self.game_over = True
                            self.active = False
                            return
                        self.objects.remove(obj)
                    else:  # obstacle
                        self.lives -= 1
                        self.objects.remove(obj)
                        if self.lives <= 0:
                            self.game_over = True
                            self.active = False
                            return

            # Создание новых объектов
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_delay and not self.game_over:
                self.spawn_timer = 0
                lane = random.randint(0, self.lanes-1)
                # Новое соотношение: 50% кольцо, 50% препятствие (раньше было 2 кольца : 1 препятствие)
                obj_type = random.choice(["ring", "obstacle"])
                self.objects.append((10, lane, obj_type))

        def get_score(self):
            return self.score

        def get_lives(self):
            return self.lives

        def is_game_over(self):
            return self.game_over

        def is_win(self):
            return self.win

        def is_paused(self):
            return self.paused

        def start(self):
            self.paused = False


label minigame_sonic_runner:
    window hide
    $ renpy.block_rollback()
    python:
        # Автоматическое определение и масштабирование изображений из папки items
        sonic_img = "images/characters/sonic.png" if renpy.loadable("images/characters/sonic.png") else None
        ring_img = "images/items/ring.png" if renpy.loadable("images/items/ring.png") else None
        obstacle_img = "images/items/barrier.png" if renpy.loadable("images/items/barrier.png") else None
        use_images = all([sonic_img, ring_img, obstacle_img])
        game = SonicRunner()

    screen sonic_runner():
        timer 0.1 repeat True action Function(game.update)

        key "K_UP" action Function(game.set_lane, -1)
        key "K_DOWN" action Function(game.set_lane, 1)
        key "K_w" action Function(game.set_lane, -1)
        key "K_s" action Function(game.set_lane, 1)
        key "K_SPACE" action Function(game.start)

        frame:
            background Solid("#000033")
            xalign 0.5 yalign 0.5
            padding (20, 20)
            vbox:
                spacing 10
                hbox:
                    spacing 40
                    text "Кольца: [game.score] / [game.target_score]" size 40 color "#ffff00"
                    text "Жизни: [game.lives]" size 40 color "#ff4444"
                text "Собирай жёлтые кольца, избегай красных препятствий!" size 24 color "#aaa" xalign 0.5

                fixed:
                    xsize 600
                    ysize 300
                    add Solid("#1a3a5a", xysize=(600, 300))

                    # Дорожки
                    for i in range(game.lanes):
                        $ y = 50 + i * 80
                        add Solid("#ffffff20", xysize=(600, 2)) pos (0, y)

                    # Соник
                    $ player_y = 50 + game.player_lane * 80
                    if use_images and sonic_img:
                        add Transform(sonic_img, xysize=(50, 50), xanchor=0.5, yanchor=0.5):
                            pos (60, player_y)
                    else:
                        add Solid("#0000ff", xysize=(40, 40), xanchor=0.5, yanchor=0.5):
                            pos (60, player_y)

                    # Объекты
                    for x, lane, obj_type in game.objects:
                        $ y = 50 + lane * 80
                        if obj_type == "ring":
                            if use_images and ring_img:
                                add Transform(ring_img, xysize=(30, 30), xanchor=0.5, yanchor=0.5):
                                    pos (60 + x * 50, y)
                            else:
                                add Solid("#ffff00", xysize=(25, 25), xanchor=0.5, yanchor=0.5):
                                    pos (60 + x * 50, y)
                        else:
                            if use_images and obstacle_img:
                                add Transform(obstacle_img, xysize=(40, 40), xanchor=0.5, yanchor=0.5):
                                    pos (60 + x * 50, y)
                            else:
                                add Solid("#ff0000", xysize=(30, 30), xanchor=0.5, yanchor=0.5):
                                    pos (60 + x * 50, y)

                if game.game_over:
                    vbox:
                        xalign 0.5 spacing 10
                        if game.win:
                            text "ПОБЕДА! Вы собрали все кольца!" size 40 color "#0f0" xalign 0.5
                        else:
                            text "ПОРАЖЕНИЕ! Соник разбился..." size 40 color "#f00" xalign 0.5
                        textbutton "Вернуться" action Return(game.score) xalign 0.5
                elif game.paused:
                    text "Нажмите ПРОБЕЛ, чтобы начать гонку!" size 30 color "#ffff88" xalign 0.5
                else:
                    text "Управление: ↑↓ / W S" size 20 color "#aaa" xalign 0.5

    call screen sonic_runner
    window show
    return game.score