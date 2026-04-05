# Мини-игра "Змейка: Агзамов против зомби"

label minigame_snake:
    window hide
    python:
        import random

        class SnakeGame:
            def __init__(self, width=20, height=15, cell_size=40):
                self.width = width
                self.height = height
                self.cell_size = cell_size
                self.reset()

            def reset(self):
                # Начальная позиция змейки (середина поля)
                start_x = self.width // 2
                start_y = self.height // 2
                self.snake = [(start_x, start_y), (start_x-1, start_y), (start_x-2, start_y)]
                self.direction = (1, 0)  # вправо
                self.next_direction = (1, 0)
                self.food = self.spawn_food()
                self.score = 0
                self.game_over = False
                self.paused = False

            def spawn_food(self):
                while True:
                    x = random.randint(0, self.width-1)
                    y = random.randint(0, self.height-1)
                    if (x, y) not in self.snake:
                        return (x, y)

            def update(self):
                if self.game_over or self.paused:
                    return

                # Обновляем направление
                self.direction = self.next_direction

                # Новая голова
                head_x, head_y = self.snake[0]
                new_head = (head_x + self.direction[0], head_y + self.direction[1])

                # Проверка столкновения со стенами
                if (new_head[0] < 0 or new_head[0] >= self.width or
                    new_head[1] < 0 or new_head[1] >= self.height):
                    self.game_over = True
                    return

                # Проверка столкновения с собой
                if new_head in self.snake:
                    self.game_over = True
                    return

                # Добавляем новую голову
                self.snake.insert(0, new_head)

                # Проверка еды
                if new_head == self.food:
                    self.score += 1
                    self.food = self.spawn_food()
                else:
                    self.snake.pop()

            def change_direction(self, new_dir):
                # Запрещаем движение в противоположную сторону
                if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
                    self.next_direction = new_dir

        game = SnakeGame()
        renpy.call_screen("snake_game_screen", game=game)
        result = game.score  # или можно вернуть больше данных
    window show
    return result

screen snake_game_screen(game):
    key "K_UP" action Function(game.change_direction, (0, -1))
    key "K_DOWN" action Function(game.change_direction, (0, 1))
    key "K_LEFT" action Function(game.change_direction, (-1, 0))
    key "K_RIGHT" action Function(game.change_direction, (1, 0))
    key "p" action ToggleScreenVariable("paused")
    key "P" action ToggleScreenVariable("paused")
    key "game_menu" action Return()  # ESC выходит из игры

    default paused = False
    timer 0.1 repeat True action If(not paused and not game.game_over, Function(game.update), None)

    frame:
        background Solid("#000000")
        xfill True
        yfill True

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20

            text "ЗМЕЙКА: АГЗАМОВ ПРОТИВ ЗОМБИ" size 40 xalign 0.5 color "#ffaa00"

            fixed:
                xsize game.width * game.cell_size
                ysize game.height * game.cell_size

                # Рисуем фон
                add Solid("#2c5a2c")  # тёмно-зелёный фон

                # Рисуем еду (зомби)
                for x, y in [game.food]:
                    $ xpos = x * game.cell_size
                    $ ypos = y * game.cell_size
                    add "images/minigames/zombie_food.png":
                        pos (xpos, ypos)
                        size (game.cell_size, game.cell_size)

                # Рисуем змейку
                for i, (x, y) in enumerate(game.snake):
                    $ xpos = x * game.cell_size
                    $ ypos = y * game.cell_size
                    if i == 0:  # голова
                        add "images/minigames/agzamov_head.png":
                            pos (xpos, ypos)
                            size (game.cell_size, game.cell_size)
                    else:
                        add "images/minigames/snake_body.png":
                            pos (xpos, ypos)
                            size (game.cell_size, game.cell_size)

            hbox:
                spacing 40
                text "Счёт: [game.score]" size 30 color "#fff"
                if game.game_over:
                    text "ИГРА ОКОНЧЕНА!" size 30 color "#f00"
                if paused:
                    text "ПАУЗА (нажмите P)" size 30 color "#ff0"

            hbox:
                spacing 20
                if game.game_over:
                    textbutton "Играть снова" action [Function(game.reset), SetScreenVariable("paused", False)]
                textbutton "Выйти" action Return()

    timer 0.1 repeat True action If(game.game_over, None, None)