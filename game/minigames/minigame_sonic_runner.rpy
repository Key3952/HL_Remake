# minigame_sonic_runner.rpy - простая версия, без плавности, но со случайной задержкой

init python:
    import random

    class SonicRunner:
        def __init__(self, lanes=7, target_score=10, start_lives=3, max_objects=4):
            self.lanes = lanes
            self.target_score = target_score
            self.start_lives = start_lives
            self.max_objects = max_objects
            self.reset()

        def reset(self):
            self.score = 0
            self.lives = self.start_lives
            self.game_over = False
            self.win = False
            self.active = True
            self.paused = True
            self.player_lane = 3
            self.objects = []          # (x, lane, type)
            self.spawn_timer = 0
            self.spawn_delay = random.uniform(0.1, 0.7)
            self.move_counter = 0

        def set_lane(self, delta):
            if self.game_over or not self.active or self.paused:
                return
            new_lane = self.player_lane + delta
            if 0 <= new_lane < self.lanes:
                self.player_lane = new_lane

        def _is_lane_free(self, lane):
            for x, l, _ in self.objects:
                if l == lane and x >= 0:
                    return False
            return True

        def _get_free_lanes(self, exclude_player=False):
            free = []
            for lane in range(self.lanes):
                if exclude_player and lane == self.player_lane:
                    continue
                if self._is_lane_free(lane):
                    free.append(lane)
            return free

        def _spawn_obstacle(self):
            # сначала на линию игрока
            if self._is_lane_free(self.player_lane):
                self.objects.append((20, self.player_lane, "obstacle"))
                return True
            # ближайшая свободная
            best_lane = None
            best_dist = self.lanes + 1
            for lane in range(self.lanes):
                if lane == self.player_lane:
                    continue
                if self._is_lane_free(lane):
                    dist = abs(lane - self.player_lane)
                    if dist < best_dist:
                        best_dist = dist
                        best_lane = lane
            if best_lane is not None:
                self.objects.append((20, best_lane, "obstacle"))
                return True
            return False

        def _spawn_ring(self):
            free_lanes = self._get_free_lanes(exclude_player=True)
            if free_lanes:
                lane = random.choice(free_lanes)
                self.objects.append((20, lane, "ring"))
                return True
            return False

        def update(self):
            if self.game_over or not self.active or self.paused:
                return

            # 1. Движение: раз в 2 тика (0.2 сек) сдвигаем на 1
            self.move_counter += 1
            if self.move_counter >= 2:
                self.move_counter = 0
                new_objects = []
                for x, lane, typ in self.objects:
                    x -= 1
                    if x >= 0:
                        new_objects.append((x, lane, typ))
                self.objects = new_objects

            # 2. Столкновения
            for obj in self.objects[:]:
                x, lane, typ = obj
                if lane == self.player_lane and x == 0:
                    if typ == "ring":
                        self.score += 1
                        if self.score >= self.target_score:
                            self.win = True
                            self.game_over = True
                            self.active = False
                            return
                        self.objects.remove(obj)
                    else:
                        self.lives -= 1
                        self.objects.remove(obj)
                        if self.lives <= 0:
                            self.game_over = True
                            self.active = False
                            return

            # 3. Спаун с случайной задержкой (таймер увеличивается каждые 0.1 сек)
            self.spawn_timer += 0.1
            if len(self.objects) < self.max_objects and self.spawn_timer >= self.spawn_delay:
                self.spawn_timer = 0
                self.spawn_delay = random.uniform(0.1, 0.7)
                if random.random() < 0.5:
                    self._spawn_obstacle()
                else:
                    self._spawn_ring()

        def start(self):
            self.paused = False

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


label minigame_sonic_runner:
    window hide
    $ renpy.block_rollback()
    python:
        game = SonicRunner()
        sonic_img = "images/characters/sonic.png" if renpy.loadable("images/characters/sonic.png") else None
        ring_img = "images/items/ring.png" if renpy.loadable("images/items/ring.png") else None
        obstacle_img = "images/items/barrier.png" if renpy.loadable("images/items/barrier.png") else None
        use_images = all([sonic_img, ring_img, obstacle_img])

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
            xpadding 30 ypadding 30
            vbox:
                spacing 15
                hbox:
                    spacing 60
                    text "Кольца: [game.score] / [game.target_score]" size 40 color "#ffff00"
                    text "Жизни: [game.lives]" size 40 color "#ff4444"
                text "Собирай жёлтые кольца, избегай красных препятствий!" size 24 color "#aaa" xalign 0.5

                fixed:
                    xsize 800
                    ysize 600
                    add Solid("#1a3a5a", xysize=(800, 600))

                    # Дорожки
                    for i in range(game.lanes):
                        $ y = 40 + i * 70
                        add Solid("#ffffff20", xysize=(800, 2)) pos (0, y)

                    # Соник
                    $ player_y = 40 + game.player_lane * 70
                    if use_images and sonic_img:
                        add Transform(sonic_img, xysize=(100, 100), xanchor=0.5, yanchor=0.5):
                            pos (60, player_y)
                    else:
                        add Solid("#0000ff", xysize=(50, 50), xanchor=0.5, yanchor=0.5):
                            pos (60, player_y)

                    # Объекты
                    for x, lane, typ in game.objects:
                        $ y = 40 + lane * 70
                        if typ == "ring":
                            if use_images and ring_img:
                                add Transform(ring_img, xysize=(80, 80), xanchor=0.5, yanchor=0.5):
                                    pos (80 + x * 60, y)
                            else:
                                add Solid("#ffff00", xysize=(35, 35), xanchor=0.5, yanchor=0.5):
                                    pos (80 + x * 60, y)
                        else:
                            if use_images and obstacle_img:
                                add Transform(obstacle_img, xysize=(87, 87), xanchor=0.5, yanchor=0.5):
                                    pos (80 + x * 60, y)
                            else:
                                add Solid("#ff0000", xysize=(40, 40), xanchor=0.5, yanchor=0.5):
                                    pos (80 + x * 60, y)

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