# minigame_final_battle.rpy - финальная битва с Габеном (вопросы + последовательность)
# Добавлены подложки под текст для читаемости

init python:
    import random

    class FinalBattle:
        def __init__(self, точность, риск, основы, скорость, эффективность, хитрость, секретки,
                     отношение_ивлев, отношение_агзамов, отношение_рамзи,
                     рецепты, союзники):
            self.точность = точность
            self.риск = риск
            self.основы = основы
            self.скорость = скорость
            self.эффективность = эффективность
            self.хитрость = хитрость
            self.секретки = секретки
            self.отношение_ивлев = отношение_ивлев
            self.отношение_агзамов = отношение_агзамов
            self.отношение_рамзи = отношение_рамзи
            self.рецепты = рецепты
            self.союзники = союзники

            # Вычисляем бонусные очки за навыки и рецепты
            self.bonus = 0
            if точность >= 5: self.bonus += 1
            if риск >= 5: self.bonus += 1
            if основы >= 5: self.bonus += 1
            if скорость >= 3: self.bonus += 1
            if эффективность >= 3: self.bonus += 1
            if хитрость >= 3: self.bonus += 1
            if секретки >= 2: self.bonus += 1
            if "дневник_ивлева" in рецепты: self.bonus += 2
            if "змеиный_аппетит" in рецепты: self.bonus += 1
            if "кольца_соника" in рецепты: self.bonus += 1
            if "соник_друг" in союзники: self.bonus += 1
            if отношение_ивлев >= 20: self.bonus += 1
            if отношение_агзамов >= 20: self.bonus += 1
            if отношение_рамзи >= 20: self.bonus += 1
            self.bonus = min(self.bonus, 10)  # не больше 10

            self.total_score = 0
            self.current_stage = 0
            self.questions_score = 0
            self.sequence_score = 0
            self.sequence = []
            self.user_sequence = []
            self.sequence_attempts = 0
            self.active = True
            self.waiting_input = True

        def get_question(self, index):
            if index == 0:
                return ("Что важнее всего в идеальном блюде?",
                        ("Точность и выверенность каждого действия", "Точность"),
                        ("Энергия и рискованные эксперименты", "Хаос"),
                        ("Душа и традиции", "Душа"))
            elif index == 1:
                return ("Что даёт блюду неповторимый вкус?",
                        ("Идеальная температура и пропорции", "Точность"),
                        ("Неожиданные сочетания и огонь", "Хаос"),
                        ("Любовь и память о доме", "Душа"))
            else:
                return ("Как исправить ошибку в рецепте?",
                        ("Пересчитать всё заново", "Точность"),
                        ("Импровизировать на ходу", "Хаос"),
                        ("Вернуться к истокам и начать сначала", "Душа"))

        def check_question_answer(self, index, selected):
            if index == 0:
                if self.точность >= self.риск and self.точность >= self.основы:
                    correct = "Точность"
                elif self.риск > self.точность and self.риск > self.основы:
                    correct = "Хаос"
                elif self.основы > self.точность and self.основы > self.риск:
                    correct = "Душа"
                else:
                    if self.отношение_ивлев >= self.отношение_агзамов and self.отношение_ивлев >= self.отношение_рамзи:
                        correct = "Точность"
                    elif self.отношение_агзамов >= self.отношение_ивлев and self.отношение_агзамов >= self.отношение_рамзи:
                        correct = "Хаос"
                    else:
                        correct = "Душа"
            elif index == 1:
                if self.риск >= self.точность and self.риск >= self.основы:
                    correct = "Хаос"
                elif self.точность > self.риск and self.точность > self.основы:
                    correct = "Точность"
                elif self.основы > self.риск and self.основы > self.точность:
                    correct = "Душа"
                else:
                    if self.отношение_агзамов >= self.отношение_ивлев and self.отношение_агзамов >= self.отношение_рамзи:
                        correct = "Хаос"
                    elif self.отношение_ивлев >= self.отношение_агзамов and self.отношение_ивлев >= self.отношение_рамзи:
                        correct = "Точность"
                    else:
                        correct = "Душа"
            else:
                if self.основы >= self.риск and self.основы >= self.точность:
                    correct = "Душа"
                elif self.риск > self.основы and self.риск > self.точность:
                    correct = "Хаос"
                elif self.точность > self.основы and self.точность > self.риск:
                    correct = "Точность"
                else:
                    if self.отношение_рамзи >= self.отношение_ивлев and self.отношение_рамзи >= self.отношение_агзамов:
                        correct = "Душа"
                    elif self.отношение_ивлев >= self.отношение_рамзи and self.отношение_ивлев >= self.отношение_агзамов:
                        correct = "Точность"
                    else:
                        correct = "Хаос"

            if selected == correct:
                return 2
            else:
                if selected == "Точность" and self.точность >= 5:
                    return 1
                elif selected == "Хаос" and self.риск >= 5:
                    return 1
                elif selected == "Душа" and self.основы >= 5:
                    return 1
                else:
                    return 0

        def generate_sequence(self):
            length = 3 + (self.скорость // 3) + (self.эффективность // 3)
            length = min(length, 5)
            actions = ["резать", "мешать", "жарить", "солить", "полить соусом"]
            self.sequence = [random.choice(actions) for _ in range(length)]
            return self.sequence

        def check_sequence(self, user_seq):
            if user_seq == self.sequence:
                score = len(self.sequence)
            else:
                score = sum(1 for i in range(min(len(user_seq), len(self.sequence))) if user_seq[i] == self.sequence[i])
            self.sequence_score = score
            return score


label minigame_final_battle:
    window hide
    $ renpy.block_rollback()
    python:
        battle = FinalBattle(точность, риск, основы, скорость, эффективность, хитрость, секретки,
                             отношение_ивлев, отношение_агзамов, отношение_рамзи,
                             рецепты, союзники)
        total = battle.bonus
        question_answers = [0, 0, 0]

    $ renpy.say(None, f"Габен анализирует ваши навыки... Вы получаете {battle.bonus} бонусных очков за подготовку.", interact=True)

    screen final_question_screen(q_index, question, opt1, opt2, opt3):
        frame:
            background Solid("#000000aa")
            xalign 0.5 yalign 0.3
            xpadding 30 ypadding 30
            vbox:
                spacing 20
                text question size 30 xalign 0.5 color "#ffffff"
                textbutton opt1[0] action Return(opt1[1]) xsize 400 xalign 0.5
                textbutton opt2[0] action Return(opt2[1]) xsize 400 xalign 0.5
                textbutton opt3[0] action Return(opt3[1]) xsize 400 xalign 0.5

    python:
        for i in range(3):
            q_text, opt1, opt2, opt3 = battle.get_question(i)
            answer = renpy.call_screen("final_question_screen", i, q_text, opt1, opt2, opt3)
            points = battle.check_question_answer(i, answer)
            question_answers[i] = points
            total += points
            if points == 2:
                renpy.say(None, "Верно! Габен вынужден признать вашу правоту.")
            elif points == 1:
                renpy.say(None, "Не совсем точно, но вы всё равно убедительны.")
            else:
                renpy.say(None, "Габен не впечатлён, но вы не сдаётесь.")
        total_questions = sum(question_answers)

    $ renpy.say(None, "Теперь Габен проверит вашу реакцию. Повторите последовательность действий!")
    python:
        sequence = battle.generate_sequence()
        seq_str = " → ".join(sequence)
        renpy.say(None, f"Запомните: {seq_str}")
        renpy.pause(2.0)
        user_seq = []
        actions_list = ["резать", "мешать", "жарить", "солить", "полить соусом"]

    screen sequence_input(step, total_steps):
        frame:
            background Solid("#000000aa")
            xalign 0.5 yalign 0.4
            xpadding 30 ypadding 30
            vbox:
                spacing 10
                text "Шаг [step] из [total_steps]" size 30 color "#ffffff"
                for act in actions_list:
                    textbutton act action Return(act) xsize 200

    python:
        for step in range(len(sequence)):
            chosen = renpy.call_screen("sequence_input", step+1, len(sequence))
            user_seq.append(chosen)
        seq_score = battle.check_sequence(user_seq)
        total += seq_score
        if seq_score == len(sequence):
            renpy.say(None, f"Идеально! Вы повторили всю последовательность! +{seq_score} очков.")
        else:
            renpy.say(None, f"Вы повторили {seq_score} из {len(sequence)} действий. Неплохо для начала.")

    $ final_score = total
    $ renpy.say(None, f"Общий счёт: {final_score} очков. Габен впечатлён вашей подготовкой!")

    window show
    return final_score