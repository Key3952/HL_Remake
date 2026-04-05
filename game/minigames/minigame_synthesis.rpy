# minigame_synthesis.rpy
# Финальная мини-игра: синтез блюда-ключа (только логика)

init python:
    import random

    class SynthesisGame:
        def __init__(self, точность, риск, основы, отношение_ивлев, отношение_агзамов, отношение_рамзи):
            self.точность = точность
            self.риск = риск
            self.основы = основы
            self.отношение_ивлев = отношение_ивлев
            self.отношение_агзамов = отношение_агзамов
            self.отношение_рамзи = отношение_рамзи

            self.ingredients = []
            self.build_ingredients()
            random.shuffle(self.ingredients)

            self.selected = []
            self.max_selected = 5
            self.time_left = 20.0
            self.active = True
            self.game_over = False

        def build_ingredients(self):
            # Точность
            if self.точность >= 5:
                self.ingredients.append(("Идеально нарезанные овощи", "precision", 15))
            if self.точность >= 3:
                self.ingredients.append(("Калиброванные специи", "precision", 10))
            if self.точность >= 1:
                self.ingredients.append(("Равномерные кубики", "precision", 5))
            if self.отношение_ивлев >= 20:
                self.ingredients.append(("Секретный соус Ивлева", "precision", 20))
            if not any(cat=="precision" for _,cat,_ in self.ingredients):
                self.ingredients.append(("Обычная нарезка", "precision", 2))

            # Хаос
            if self.риск >= 5:
                self.ingredients.append(("Жгучий перец-чили", "chaos", 15))
            if self.риск >= 3:
                self.ingredients.append(("Карамелизированный бекон", "chaos", 10))
            if self.риск >= 1:
                self.ingredients.append(("Спонтанная приправа", "chaos", 5))
            if self.отношение_агзамов >= 20:
                self.ingredients.append(("Энергетик Агзамова", "chaos", 20))
            if not any(cat=="chaos" for _,cat,_ in self.ingredients):
                self.ingredients.append(("Случайная щепотка", "chaos", 2))

            # Основа
            if self.основы >= 5:
                self.ingredients.append(("Идеальный бульон", "basis", 15))
            if self.основы >= 3:
                self.ingredients.append(("Томлёное мясо", "basis", 10))
            if self.основы >= 1:
                self.ingredients.append(("Свежая зелень", "basis", 5))
            if self.отношение_рамзи >= 20:
                self.ingredients.append(("Секрет Рамзи", "basis", 20))
            if not any(cat=="basis" for _,cat,_ in self.ingredients):
                self.ingredients.append(("Простой бульон", "basis", 2))

        def select_ingredient(self, idx):
            if not self.active or self.game_over:
                return False
            if len(self.selected) >= self.max_selected:
                return False
            ing = self.ingredients[idx]
            if ing in self.selected:
                return False
            self.selected.append(ing)
            renpy.restart_interaction()
            return True

        def finish(self):
            if not self.active or self.game_over:
                return
            self.game_over = True
            self.active = False
            renpy.restart_interaction()

        def calc_score(self):
            s = sum(ing[2] for ing in self.selected)
            cats = set(ing[1] for ing in self.selected)
            if len(cats) == 3:
                s += 15
            elif len(cats) == 2:
                s += 5
            return s

        def get_quality(self):
            s = self.calc_score()
            if s >= 80:
                return "perfect"
            elif s >= 50:
                return "good"
            else:
                return "poor"

label minigame_synthesis:
    window hide
    $ renpy.block_rollback()
    $ game = SynthesisGame(точность, риск, основы, отношение_ивлев, отношение_агзамов, отношение_рамзи)

    screen synthesis_screen():
        default hover_index = 0

        timer 0.1 repeat True action If(game.active and not game.game_over, SetVariable("game.time_left", game.time_left - 0.1), None)
        if game.time_left <= 0 and not game.game_over:
            timer 0.01 action Function(game.finish)

        key "K_UP" action SetScreenVariable("hover_index", max(0, hover_index - 1))
        key "K_DOWN" action SetScreenVariable("hover_index", min(len(game.ingredients)-1, hover_index + 1))
        key "K_RETURN" action Function(game.select_ingredient, hover_index)
        key "K_KP_ENTER" action Function(game.select_ingredient, hover_index)

        frame:
            background Solid("#000000CC")
            xfill True yfill True
            vbox:
                spacing 15
                xalign 0.5 yalign 0.5
                text "Синтез блюда-ключа" size 60 xalign 0.5 color "#ffcc00"
                text "Кликайте мышкой или используйте ↑↓ и Enter" size 28 xalign 0.5 color "#ccc"

                hbox:
                    spacing 50
                    text "Очки: [game.calc_score()]" size 40 color "#0f0"
                    text "Время: [int(game.time_left)] сек" size 40 color "#ffaa44"
                text "Выбрано: [len(game.selected)] / [game.max_selected]" size 30 xalign 0.5

                frame:
                    xsize 800
                    background Solid("#1a1a2e")
                    vbox:
                        text "Выбранные ингредиенты:" size 24 color "#fff"
                        if game.selected:
                            for ing in game.selected:
                                $ name, cat, pts = ing
                                $ col = "#ff8888" if cat == "precision" else "#ffcc88" if cat == "chaos" else "#88ff88"
                                text "- [name] ([pts] очков)" color col size 22
                        else:
                            text "(пока ничего)" color "#888" size 22
                        if len(game.selected) == game.max_selected:
                            text "ГОТОВО! Нажмите «Представить»." color "#0f0" size 22

                viewport:
                    xsize 800 ysize 300
                    scrollbars "vertical"
                    vbox:
                        spacing 8
                        for idx, ing in enumerate(game.ingredients):
                            $ name, cat, pts = ing
                            $ col = "#ff6666" if cat == "precision" else "#ffaa66" if cat == "chaos" else "#66ff66"
                            $ is_hover = (idx == hover_index)
                            textbutton "[name] ([pts] очков)":
                                action Function(game.select_ingredient, idx)
                                text_color col
                                background (Solid("#ffffff30") if is_hover else None)
                                xsize 760
                                hover_background Solid("#ffffff30")

                hbox:
                    spacing 40
                    xalign 0.5
                    textbutton "Представить блюдо":
                        action Function(game.finish)
                        sensitive (not game.game_over and (len(game.selected) == game.max_selected or game.time_left <= 0))
                    if game.game_over:
                        textbutton "Завершить синтез" action Return(game.get_quality()) xalign 0.5
                    elif game.time_left <= 0:
                        text "Время вышло!" color "#f00" size 30
                        textbutton "Завершить" action Return("poor")

    call screen synthesis_screen
    $ synthesis_quality = _return
    window show
    return synthesis_quality