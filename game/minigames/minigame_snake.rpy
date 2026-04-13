# minigame_snake.rpy

init python:
    import random
    import renpy.exports as renpy

    # 1. Функция поиска ассетов (змейка ищется везде, зомби - в своей папке)
    def find_snake_asset(name, extension=".jpg"):
        all_files = renpy.list_files()
        target = name.lower() + extension.lower()
        for f in all_files:
            if f.lower().endswith(target):
                return f
        return None

    # 2. Явное определение функций в store, чтобы экран их всегда видел
    def get_head_sprite(dx, dy):
        if (dx, dy) == (0, -1): return store.head_img_u
        if (dx, dy) == (0, 1):  return store.head_img_d
        if (dx, dy) == (-1, 0): return store.head_img_l
        if (dx, dy) == (1, 0):  return store.head_img_r
        return store.head_img_u

    def get_body_sprite(dx, dy):
        if (dx, dy) == (0, -1): return store.body_img_u
        if (dx, dy) == (0, 1):  return store.body_img_d
        if (dx, dy) == (-1, 0): return store.body_img_l
        if (dx, dy) == (1, 0):  return store.body_img_r
        return store.body_img_u

    # Регистрируем функции в глобальном хранилище Ren'Py
    store.get_head_sprite = get_head_sprite
    store.get_body_sprite = get_body_sprite

    def load_snake_sprites():
        store.head_img_u = find_snake_asset("agzamov_head_u")
        store.head_img_d = find_snake_asset("agzamov_head_d")
        store.head_img_l = find_snake_asset("agzamov_head_l")
        store.head_img_r = find_snake_asset("agzamov_head_r")
        store.body_img_u = find_snake_asset("agzamov_body_u")
        store.body_img_d = find_snake_asset("agzamov_body_d")
        store.body_img_l = find_snake_asset("agzamov_body_l")
        store.body_img_r = find_snake_asset("agzamov_body_r")

        store.use_sprites = all([
            store.head_img_u, store.head_img_d, store.head_img_l, store.head_img_r,
            store.body_img_u, store.body_img_d, store.body_img_l, store.body_img_r
        ])

    class SnakeGame:
        def __init__(self, grid_size=15, cell_size=50, target_score=15):
            self.grid_size = grid_size
            self.cell_size = cell_size
            self.target_score = target_score
            self.field_w = grid_size * cell_size
            self.field_h = grid_size * cell_size

            # Поиск зомби: ТОЛЬКО в папке images/zoombies/
            all_files = renpy.list_files()
            self.zombie_images = [
                f for f in all_files
                if f.startswith("images/zoombies/") and f.lower().endswith((".png", ".jpg", ".jpeg"))
            ]

            self.reset()

        def reset(self):
            self.snake = [(7, 7), (6, 7), (5, 7)]
            self.direction = (1, 0)
            self.next_direction = (1, 0)
            self.score = 0
            self.game_over = False
            self.win = False
            self.active = True
            self.paused = True
            self.food = None
            self.food_image = None
            self._random_food()

        def _random_food(self):
            free_cells = [(x, y) for x in range(self.grid_size) for y in range(self.grid_size) if (x, y) not in self.snake]
            if free_cells:
                self.food = random.choice(free_cells)
                self.food_image = random.choice(self.zombie_images) if self.zombie_images else None
            else:
                self.game_over = True
                self.win = True

        def set_direction(self, new_dir):
            if self.game_over or not self.active: return
            if self.paused: self.paused = False
            if (self.direction[0] == -new_dir[0] and self.direction[1] == -new_dir[1]): return
            self.next_direction = new_dir

        def move(self):
            if self.game_over or not self.active or self.paused: return
            self.direction = self.next_direction
            head = self.snake[0]
            new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

            if not (0 <= new_head[0] < self.grid_size and 0 <= new_head[1] < self.grid_size) or new_head in self.snake:
                self.game_over = True
                self.active = False
                return

            self.snake.insert(0, new_head)
            if new_head == self.food:
                self.score += 1
                if self.score >= self.target_score:
                    self.win = True
                    self.game_over = True
                else:
                    self._random_food()
            else:
                self.snake.pop()

        def get_segment_direction(self, idx):
            if idx == 0: return self.direction
            prev = self.snake[idx-1]
            curr = self.snake[idx]
            # Направление для сегмента тела (откуда приползли)
            return (prev[0] - curr[0], prev[1] - curr[1])

# --- ЭКРАН ---
screen snake_game(game):
    timer 0.19 repeat True action Function(game.move)

    key "K_UP" action Function(game.set_direction, (0, -1))
    key "K_DOWN" action Function(game.set_direction, (0, 1))
    key "K_LEFT" action Function(game.set_direction, (-1, 0))
    key "K_RIGHT" action Function(game.set_direction, (1, 0))
    key "K_w" action Function(game.set_direction, (0, -1))
    key "K_s" action Function(game.set_direction, (0, 1))
    key "K_a" action Function(game.set_direction, (-1, 0))
    key "K_d" action Function(game.set_direction, (1, 0))

    frame:
        background Solid("#1a3a1a")
        xalign 0.5 yalign 0.5
        padding (20, 20)

        vbox:
            spacing 10
            hbox:
                spacing 40
                text "Счёт: [game.score]" size 40 color "#fff"
                $ left = max(0, game.target_score - game.score)
                text "Осталось зомби: [left]" size 40 color ("#44ff44" if left == 0 else "#ffaa44")

            text "Цель: [game.target_score] очков" size 24 color "#aaa" xalign 0.5

            fixed:
                xsize game.field_w
                ysize game.field_h

                # ПОЧИНЕННАЯ СЕТКА
                add Solid("#2a5a2a", xysize=(game.field_w, game.field_h))
                for i in range(game.grid_size + 1):
                    add Solid("#ffffff15", xysize=(1, game.field_h)) xpos (i * game.cell_size)
                    add Solid("#ffffff15", xysize=(game.field_w, 1)) ypos (i * game.cell_size)

                # Еда (Зомби)
                if game.food and not game.game_over:
                    $ fx, fy = game.food
                    if game.food_image:
                        add Transform(game.food_image, xysize=(game.cell_size, game.cell_size)):
                            pos (fx * game.cell_size, fy * game.cell_size)
                    else:
                        add Solid("#ff4444", xysize=(game.cell_size, game.cell_size)):
                            pos (fx * game.cell_size, fy * game.cell_size)

                # Змейка (Агзамов)
                for idx, (sx, sy) in enumerate(game.snake):
                    $ dx, dy = game.get_segment_direction(idx)
                    if use_sprites:
                        # Используем функции через store
                        $ img = store.get_head_sprite(dx, dy) if idx == 0 else store.get_body_sprite(dx, dy)
                        add Transform(img, xysize=(game.cell_size, game.cell_size)):
                            pos (sx * game.cell_size, sy * game.cell_size)
                    else:
                        $ clr = "#ffaa00" if idx == 0 else "#88aa00"
                        add Solid(clr, xysize=(game.cell_size-2, game.cell_size-2)):
                            pos (sx * game.cell_size + 1, sy * game.cell_size + 1)

            if game.game_over:
                vbox:
                    xalign 0.5 spacing 10
                    if game.win:
                        text "ПОБЕДА! Вы накормили Агзамова!" size 40 color "#0f0" xalign 0.5
                    else:
                        text "Уупс, стеночка вышла" size 40 color "#f00" xalign 0.5
                    textbutton "Вернуться" action Return(game.score) xalign 0.5
            elif game.paused:
                text "Нажмите стрелки или WASD, чтобы начать!" size 30 color "#ffff00" xalign 0.5

label minigame_snake:
    window hide
    $ renpy.block_rollback()
    python:
        load_snake_sprites()
        game_inst = SnakeGame()
    call screen snake_game(game_inst)
    window show
    return _return