# Свободная игра: Испытание точностью

label freeplay_precision:
    $ renpy.block_rollback()
    window hide
    call minigame_precision
    $ result = _return
    window show

    if result == "perfect":
        $ message = "Идеально! Вы набрали максимальный результат."
    elif result == "good":
        $ message = "Хорошо! Неплохая точность."
    else:
        $ message = "Провал. Попробуйте ещё раз."

    call screen minigame_result_screen(message)
    jump minigames_menu

# Свободная игра: Испытание хаосом
label freeplay_chaos:
    window hide
    call minigame_chaos_run
    $ score = _return
    window show

    if score >= 12:
        $ message = "Великолепно! Счёт: [score]"
    elif score >= 5:
        $ message = "Неплохо. Счёт: [score]"
    else:
        $ message = "Ужасно. Счёт: [score]. Попробуйте снова."

    call screen minigame_result_screen(message)
    jump minigames_menu

# Экран с результатом
screen minigame_result_screen(message):
    modal True
    frame:
        xalign 0.5
        yalign 0.5
        background Solid("#000000CC")
        padding (50, 50)
        vbox:
            spacing 30
            text message size 40 xalign 0.5
            hbox:
                spacing 50
                xalign 0.5
                textbutton "Повторить" action Return()
                textbutton "В меню" action ShowMenu("minigames_menu")