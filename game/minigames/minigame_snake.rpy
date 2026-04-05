# minigame_snake.rpy
# Змейка с лицом Агзамова (кушает зомби)

label minigame_snake:
    window hide
    $ renpy.block_rollback()
    python:
        import random
        import os

        # ------------------- ПРОВЕРКА НАЛИЧИЯ ИЗОБРАЖЕНИЙ -------------------
        def has_image(filename):
            return renpy.loadable(filename)

        # Изображения змейки
        head_img = "images/agzamov_head.png" if has_image("images/agzamov_head.png") else None
        body_img = "images/agzamov_body.png" if has_image("images/agzamov_body.png") else None

        # ------------------- ЗАГРУЗКА ВСЕХ ИЗОБРАЖЕНИЙ ЕДЫ ИЗ ПАПКИ -------------------
        food_images = []
        # Пытаемся найти файлы в game/images/zoombies/
        # В Ren'Py нет прямого доступа к файловой системе, но можно перечислить возможные имена
        # или использовать renpy.list_files().
        # Более надёжный способ: собрать все .png/.jpg из папки zoombies при инициализации
        # Сделаем это динамически:
        all_files = renpy.list_files()
        for f in all_files:
            if f.startswith("images/zoombies/") and (f.endswith(".png") or f.endswith(".jpg") or f.endswith(".jpeg")):
                food_images.append(f)
        # Если ни одного не нашли, используем заглушку-цвет
        use_random_food_image = len(food_images) > 0

        # Параметры поля
        grid_size = 15
        cell_size = 50
        field_w = grid_size * cell_size
        field_h = grid_size * cell_size
        target_score = 15

        snake = [(7, 7), (6, 7), (5, 7)]
        direction = (1, 0)
        next_direction = (1, 0)
        food = None
        food_image = None   # текущее изображение еды
        score = 0
        game_over = False
        win = False
        active = True

        def random_food():
            global food, food_image
            while True:
                x = random.randint(0, grid_size-1)
                y = random.randint(0, grid_size-1)
                if (x, y) not in snake:
                    food = (x, y)
                    # Выбираем случайное изображение еды, если они есть
                    if use_random_food_image:
                        food_image = random.choice(food_images)
                    else:
                        food_image = None
                    break

        def move_snake():
            global snake, direction, game_over, active, score, win
            if game_over or not active:
                return
            direction = next_direction
            head = snake[0]
            new_head = (head[0] + direction[0], head[1] + direction[1])

            # Столкновение со стеной
            if not (0 <= new_head[0] < grid_size and 0 <= new_head[1] < grid_size):
                game_over = True
                active = False
                return

            # Столкновение с собой
            if new_head in snake:
                game_over = True
                active = False
                return

            snake.insert(0, new_head)

            # Съели еду
            if new_head == food:
                score += 1
                if score >= target_score:
                    win = True
                    game_over = True
                    active = False
                else:
                    random_food()
            else:
                snake.pop()

        # Функция проверки допустимости направления (защита от 180°)
        def set_direction(new_dir):
            global next_direction
            if not game_over and active:
                # Проверяем, не противоположное ли направление
                if (direction[0] == -new_dir[0] and direction[1] == -new_dir[1]):
                    return  # запрещаем
                next_direction = new_dir

        random_food()

    # ---------- ЭКРАН ИГРЫ ----------
    screen snake_game():
        default timer = 0
        on "show" action SetVariable("active", True), SetVariable("game_over", False), SetVariable("win", False)
        on "hide" action SetVariable("active", False)

        # Управление с защитой
        key "K_UP" action Function(set_direction, (0, -1))
        key "K_DOWN" action Function(set_direction, (0, 1))
        key "K_LEFT" action Function(set_direction, (-1, 0))
        key "K_RIGHT" action Function(set_direction, (1, 0))
        key "K_w" action Function(set_direction, (0, -1))
        key "K_s" action Function(set_direction, (0, 1))
        key "K_a" action Function(set_direction, (-1, 0))
        key "K_d" action Function(set_direction, (1, 0))
        key "ц" action Function(set_direction, (0, -1))
        key "ы" action Function(set_direction, (0, 1))
        key "ф" action Function(set_direction, (-1, 0))
        key "в" action Function(set_direction, (1, 0))

        frame:
            background Solid("#1a3a1a")
            xalign 0.5 yalign 0.5
            xpadding 20 ypadding 20
            vbox:
                spacing 10
                hbox:
                    spacing 40
                    text "Счёт: [score]" size 40 color "#fff"
                    $ left = target_score - score
                    if left > 0:
                        text "Осталось зомби: [left]" size 40 color "#ffaa44"
                    else:
                        text "Осталось зомби: 0" size 40 color "#44ff44"
                text "1 зомби = 1 очко   |   Цель: [target_score] очков" size 24 color "#aaa" xalign 0.5

                fixed:
                    xsize field_w
                    ysize field_h
                    # Сетка
                    for i in range(grid_size):
                        for j in range(grid_size):
                            add Solid("#2a5a2a", xysize=(cell_size, cell_size)):
                                pos (i*cell_size, j*cell_size)
                            add Solid("#ffffff10", xysize=(cell_size, 1)):
                                pos (i*cell_size, j*cell_size)
                            add Solid("#ffffff10", xysize=(1, cell_size)):
                                pos (i*cell_size, j*cell_size)
                    # Еда (случайное изображение из папки zoombies)
                    if food and not game_over:
                        if food_image and has_image(food_image):
                            add Image(food_image, xysize=(cell_size, cell_size)):
                                pos (food[0]*cell_size, food[1]*cell_size)
                        else:
                            add Solid("#ff4444", xysize=(cell_size, cell_size)):
                                pos (food[0]*cell_size, food[1]*cell_size)
                    # Змейка
                    for idx, (sx, sy) in enumerate(snake):
                        if idx == 0:
                            if head_img:
                                add Image(head_img, xysize=(cell_size, cell_size)):
                                    pos (sx*cell_size, sy*cell_size)
                            else:
                                add Solid("#ffaa00", xysize=(cell_size, cell_size)):
                                    pos (sx*cell_size, sy*cell_size)
                        else:
                            if body_img:
                                add Image(body_img, xysize=(cell_size, cell_size)):
                                    pos (sx*cell_size, sy*cell_size)
                            else:
                                add Solid("#88aa00", xysize=(cell_size, cell_size)):
                                    pos (sx*cell_size, sy*cell_size)

                if game_over:
                    if win:
                        text "ПОБЕДА! Вы накормили Агзамова!" size 40 color "#0f0" xalign 0.5
                    else:
                        text "ПОРАЖЕНИЕ! Зомби тебя съели..." size 40 color "#f00" xalign 0.5
                    textbutton "Вернуться" action Return(score) xalign 0.5
                else:
                    text "Управление: стрелки / WASD / ФЫВЦ" size 20 color "#aaa" xalign 0.5

    screen snake_timer():
        timer 0.2 repeat True action If(not game_over, Function(move_snake), None)

    show screen snake_timer
    call screen snake_game
    hide screen snake_timer
    window show
    return score