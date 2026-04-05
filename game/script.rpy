# Half-Life: Межвселенская закусочная
# Интерактивная новелла с ветками сюжета

# ФОНОВЫЕ ИЗОБРАЖЕНИЯ (заглушки для тестирования)
image bg blackmesa = "images/bg/blackmesa.png"
image bg aperture_entrance = "images/bg/glados_fon.png"
image bg kitchen = "images/bg/kitchen.png"
image bg aperture_secret = "images/bg/secret_room_portal.png"
image bg aperture_memory = "images/bg/kitchen.png"
image bg pvz_garden = "images/bg/pvz_garden.png"
image bg pvz_battle = "images/bg/pvz_battle.png"
image bg pvz_kitchen = "images/bg/pvz_kitchen.png"
image bg pvz_secret = "images/bg/pvz_secret.png"
image bg pvz_memory = "images/bg/pvz_garden.png"
image bg zombie_wave = "images/bg/zombie_wave.png"
image bg sonic_zone = "images/bg/sonic.png"
image bg sonic_race = "images/bg/sonic_race.png"
image bg void = "images/bg/void.png"
image bg final_arena = "images/bg/final.png"
image bg new_world = "images/bg/new_world.png"
image bg peace = "#000000"
image bg restaurant = "images/bg/rest.png"
image bg ending = "#04000d"

#
image gman_normal = "images/characters/gman3.png"
image gman_silhouette = "images/characters/gman.png"
image gman_serious = "images/characters/gman2.png"

image ivlev = "images/characters/iv1.png"
image ivlev_hologram = "images/characters/iv2.png"
image ivlev_memory = "images/characters/iv3.png"

image agzamov_action = "images/characters/ag1.png"
image agzamov_normal = "images/characters/ag2.png"
image agzamov_memory = "images/characters/ag3.png"

image ramsay_normal = "images/characters/ram2.png"
image ramsay_action = "images/characters/ram1.png"
image ramsay_memory = "images/characters/ram3.png"

image gaben_normal = "images/characters/gab1.png"
image gaben_silhouette = "images/characters/gab2.png"
image gaben_glitch = "images/characters/gab3.png"

image glados_normal = "images/characters/glados.png"

image barney_friendly = "images/characters/bar.png"

image crazy_dave = "images/characters/dave.png"
image sonic = "images/characters/sonic.png"
image kliener_normal = "images/characters/kl.png"
image eli_normal = "images/characters/eli.png"

define gui.text_font = "DejaVuSans.ttf"
define gui.name_text_font = "DejaVuSans-Bold.ttf"
define gui.interface_text_font = "DejaVuSans.ttf"

# Инициализация персонажей с изображениями
define g = Character("G-Man", color="#00ff00", what_color="#ffffff", image='gman')
define i = Character("Константин Ивлев", color="#ff4444", what_color="#ffffff", image='ivlev')
define r = Character("Ринат Агзамов", color="#ffaa00", what_color="#ffffff", image='agzamov')
define gr = Character("Гордон Рамзи", color="#ff0000", what_color="#ffffff", image='ramsay')
define gab = Character("Габен", color="#0066cc", what_color="#ffffff", image='gaben')
define br = Character("Барни", color="#aa88ff", what_color="#ffffff", image='barney')
define ai = Character("GLaDOS", color="#88ccff", what_color="#ffffff", image='glados')
define drk = Character("Доктор Кляйнер", color="#88aaff", what_color="#ffffff")
define eli = Character("Илай Вэнс", color="#aa8866", what_color="#ffffff")
define myst = Character("Дейв", color="#ff88ff", what_color="#ffffff")
define sonic_char = Character("Соник", color="#00aaff", what_color="#ffffff", image='sonic')

# Переменные для отслеживания навыков
default точность = 0
default риск = 0
default основы = 0
default оборона = 0
default атака = 0
default хитрость = 0
default скорость = 0
default эффективность = 0
default секретки = 0

# Переменные для отношений
default отношение_ивлев = 0
default отношение_агзамов = 0
default отношение_рамзи = 0
default отношение_gman = 50
default хаос_фактор = 0
default порядок_фактор = 0

# Квестовые предметы
default рецепты = []
default ингредиенты = []
default союзники = []
default проклятия = []

# Сцены
default сцена = 1
default память_восстановлена = False
default глитч_детектирован = False
default секретная_концовка_найдена = False

# Инициализация
label start:
    scene black
    with dissolve

    play music "audio/mysterious.ogg" fadein 1.0

    jump prologue

# ПРОЛОГ - Тайна исчезнувших поваров
label prologue:
    scene bg void with fade

    show gman_silhouette with dissolve
    g "Снова здравствуйте, доктор Фримен."
    g "Вы, вероятно, задаётесь вопросом, почему вас снова выдернули из заслуженного отдыха."

    g "Кулинарный апокалипсис. Три вселенских шеф-повара исчезли."
    g "Их стихии: точность Ивлева, энергия Агзамова, страсть Рамзи."
    g "Без них мультивселенная погрузится в хаос безвкусицы."

    g "Именно потому, что вы универсальны. Как швейцарский нож."
    g "И потому что Габен уже начал свою игру."
    hide gman_silhouette
    show gman_serious with dissolve
    g "Габен создаёт «Идеальное блюдо», которое поработит все реальности."
    g "Он использует пропавших шефов как ингредиенты."

    menu:
        g "Что скажете, доктор Фримен?"

        "Кивнуть в знак согласия":
            $ отношение_gman += 10
            g "Предсказуемо... но эффективно."

        "Вопросительно посмотреть, требуя объяснений":
            $ отношение_gman -= 5
            $ риск += 1
            g "Разумно. Вы получите ответы на вопросы, которые боитесь задать."

        "Покачать головой и скрестить руки":
            $ отношение_gman -= 20
            $ хаос_фактор += 5
            g "У вас нет выбора, доктор Фримен. Контракт уже подписан."

    jump scene_0

# СЦЕНА 0 - База сопротивления
label scene_0:
    scene bg blackmesa with fade

    play music "audio/hope.ogg" fadein 1.0

    show kliener_normal at right
    drk "Гордон! Старый друг! Как же я рад тебя видеть!"

    show eli_normal at left
    eli "Мальчик мой, ты как раз вовремя. Дела плохи."


    drk "Ивлев исчез во время съёмок в Aperture Science. Последнее, что мы видели, — странная синяя вспышка."

    eli "Агзамов проводил стрим с заднего двора Plants vs Zombies. Зрители видели, как его поглотила гигантская плотоядная муха."

    drk "Рамзи... тот просто бегал за каким-то синим ежом и растворился в воздухе."

    show barney_friendly at center
    br "Хей, Гордон! Давно не виделись!"
    br "У меня для тебя кое-что есть."

    hide eli_normal
    hide kliener_normal
    menu:
        br "Что хочешь получить?"

        "Гравипушку. Старую добрую гравипушку.":
            $ рецепты.append("гравипушка")
            br "Держи! Она теперь ещё и яйца может взбивать!"

        "Защитный костюм. Кто знает, что там за кухни.":
            $ союзники.append("защита")
            br "Умно. В нём встроенный детектор ГМО."

        "Карту всех реальностей. Хочу знать, куда иду.":
            $ секретки += 1
            br "Ого, серьёзный подход. Держи, тут отмечены секретные уровни."

    show kliener_normal at right
    drk "Помни, Гордон. Ты должен не просто найти их — ты должен понять их философию."

    show eli_normal at left
    eli "Только синтезировав все три стиля, ты сможешь победить Габена."

    jump scene_1

# СЦЕНА 1: ВРАТА В APERTURE SCIENCE
label scene_1:
    scene bg aperture_entrance with fade

    play music "audio/aperture.ogg" fadein 1.0

    show glados_normal with dissolve

    ai "О, новый испытуемый. Как мило. Вы, наверное, потерялись?"
    ai "Или может быть... вас прислали починить тостер? Потому что кулинарная тематика здесь явно ни при чём."

    ai "Ах, тот громкий человек с ножом? Да, он здесь готовил. Слишком эмоционально для научного учреждения."
    ai "Он оставил после себя три тестовые камеры. Хотите пройти? Отказ невозможен."

    menu:
        ai "Выбирайте испытание:"

        "Тестовая камера №17 - Испытание точностью":
            jump aperture_precision

        "Тестовая камера №18 - Испытание хаосом":
            jump aperture_chaos

        "Тестовая камера №19 - Испытание основами":
            jump aperture_basics

# Подсцена 1А: Испытание точностью
label aperture_precision:
    scene bg kitchen with fade
    play music "audio/aperture.ogg" fadein 1.0

    show glados_normal with dissolve
    ai "Испытание точностью. Задача: нарезать идеальные кубики из кубов."
    ai "Звучит просто? О нет. Кубы двигаются. Вверх. Вниз. Иногда... взрываются."

    show ivlev_hologram at center
    i "(голограмма) Фримен! Помни: каждый срез должен быть выверен до миллиметра! Никакой импровизации!"

    # Запуск мини-игры
    call minigame_precision
    $ precision_result = _return

    # Обработка результата
    if precision_result == "perfect":
        $ точность += 3
        $ порядок_фактор += 10
        $ отношение_ивлев += 25
        $ рецепты.append("идеальная_нарезка")
        ai "Превосходно! Ваша точность достойна уважения. Идеальные кубы."
        i "Фримен! Ты справился блестяще! Я горжусь."
    elif precision_result == "good":
        $ точность += 1
        $ порядок_фактор += 5
        $ отношение_ивлев += 10
        $ рецепты.append("аккуратная_нарезка")
        ai "Неплохо. Не идеал, но кубики вполне пригодны."
        i "Хорошая работа, но стремись к совершенству!"
    else:  # fail
        menu:
            ai "Вы провалили тест точности. Что будем делать?"
            "Повторить испытание":
                jump aperture_precision
            "Вернуться к выбору испытаний":
                jump scene_1
            "Продолжить с позором (получите штраф)":
                $ отношение_ивлев -= 15
                $ хаос_фактор += 5
                i "Фримен... я разочарован. Но идём дальше."

    # Дальше переход к секретной комнате или памяти
    ai "Любопытно. Вы прошли тест. Но настоящий секрет... он в соседней комнате."

    menu:
        ai "Зайти в секретную комнату?"
        "Да, конечно!":
            $ секретки += 1
            jump aperture_secret
        "Нет, продолжу основную миссию":
            jump aperture_memory

# Подсцена 1B: Испытание хаосом
label aperture_chaos:
    scene bg kitchen with fade
    play music "audio/aperture.ogg" fadein 1.0

    show glados_normal with dissolve
    ai "Тестовая камера №18. Испытание хаосом."
    ai "Ингредиенты будут появляться случайно. Постарайтесь не собрать... мусор."

    show ivlev_hologram at center
    i "Фримен! Кухня — это хаос, но ты должен быть его повелителем! Кликай только по продуктам!"

    call minigame_chaos_run
    $ chaos_score = _return

    # Обработка результата
    if chaos_score >= 12:
        i "Великолепно! Ты обуздал этот беспорядок! Настоящая кулинарная сингулярность."
        $ отношение_ивлев += 15
        $ хаос_фактор += 5
        $ рецепты.append("повелитель_хаоса")
    elif chaos_score >= 5:
        i "Приемлемо. По крайней мере, кухня всё ещё стоит. Идем дальше."
        $ основы += 1
    else:
        menu:
            i "ПОЛНЫЙ ПРОВАЛ! Ты набрал мусора вместо еды! GladOS смеется над тобой!"
            "Перепройти испытание":
                jump aperture_chaos
            "Вернуться к выбору испытаний":
                jump scene_1
            "Смириться и идти дальше (штраф)":
                $ хаос_фактор += 10
                $ отношение_ивлев -= 10
                i "Ты хочешь оставить всё как есть? Ну, твоя совесть... И твой желудок."

    jump aperture_memory

# Подсцена 1С: Испытание основами
label aperture_basics:
    scene bg kitchen with fade

    $ основы += 1
    $ порядок_фактор += 3

    ai "Скучное испытание. Основы. Нарезка. Варка. Жарка."
    ai "Никаких взрывов. Никакого веселья. Просто... готовка."

    show ivlev_hologram with dissolve
    i "Фримен! Не слушай эту железку! База — всему голова!"

    menu:
        "На чём сосредоточишься?"

        "Техника нарезки":
            $ точность += 1
            i "Рука твёрдая, глаз меткий!"
            $ рецепты.append("идеальная_нарезка")

        "Термическая обработка":
            $ отношение_ивлев += 10
            i "Температура — это искусство!"
            $ рецепты.append("термальное_мастерство")

        "Сочетание текстур":
            $ хитрость += 1
            i "О, уже думаешь как шеф!"
            $ рецепты.append("текстурный_баланс")

    ai "Ску-у-учно. Но эффективно. Вы прошли тест."

    jump aperture_memory

# Секретная комната
label aperture_secret:
    scene bg aperture_secret with fade

    $ секретная_концовка_найдена = True

    ai "О, вы нашли секретную комнату. Обычно я её скрываю, но сегодня добрая."

    ai "Здесь Ивлев оставил свой дневник. И... странный рецепт."

    "Вы находите потрёпанную книгу. На первой странице надпись:"

    i "Если ты это читаешь, Фримен, значит, ты ищешь глубже других."
    i "Габен не просто собирает шефов. Он ищет 'Первый рецепт' — рецепт, созданный на заре времён."
    i "Тот, кто приготовит его, сможет управлять реальностью."

    menu:
        "Забрать дневник?":
            $ рецепты.append("дневник_ивлева")
            $ секретки += 2
            ai "Красть нехорошо. Но я не скажу."

        "Оставить, но сфотографировать":
            $ союзники.append("фото_дневника")
            $ хитрость += 1
            ai "Хитро. Мне нравится."

    jump aperture_memory

# Воспоминание Ивлева
label aperture_memory:
    scene bg aperture_memory with fade

    play music "audio/memory.ogg" fadein 1.0

    $ память_восстановлена = True

    "Внезапно комната мерцает. Вы видите воспоминание Ивлева."

    show ivlev_memory with dissolve
    i "Габен... ты не понимаешь, что творишь!"
    hide ivlev_memory

    show gaben_silhouette
    gab "Я создаю совершенство. Идеальный алгоритм вкуса."
    hide gaben_silhouette

    show ivlev_memory
    i "Вкус нельзя алгоритмизировать! Это душа! Это эмоции!"
    hide ivlev_memory

    show gaben_silhouette
    gab "Душа — это баг. Эмоции — это уязвимости. Я их исправлю."
    hide gaben_silhouette

    show ivlev_memory
    i "Фримен! Если ты это видишь — найди Агзамова и Рамзи!"
    i "Только вместе вы сможете... а-а-а-р-г-х..."

    "Воспоминание обрывается."

    ai "Эмоционально. Я почти тронута. Почти."
    ai "Вам пора идти. Следующая остановка — задний двор Plants vs Zombies."

    jump scene_2

# СЦЕНА 2: ЗАДНИЙ ДВОР PvZ
label scene_2:
    scene bg pvz_garden with fade

    play music "audio/pvz.ogg" fadein 1.0

    show crazy_dave with dissolve
    myst "Привет и добро пожаловать на задний двор! Я Безумный Дэйв!"

    myst "Ты ищешь Рината Агзамова? Он сейчас на передовой! Зомби-гурманы атакуют!"

    hide crazy_dave with fade
    show zombie_wave with dissolve

    menu:
        "Помочь Дэйву?"

        "Да, нужно спасать урожай":
            jump pvz_defense_minigame

        "Нет, у меня своя миссия":
            $ отношение_агзамов -= 10
            "Дэйв обижен, но показывает дорогу"
            jump pvz_agzamov

# МИНИ-ИГРА: Оборона от зомби (Plants vs Zombies style)
label pvz_defense_minigame:
    scene bg pvz_battle with fade

    show agzamov_action with dissolve
    r "ФРИМЕН! ТЫ ВОВРЕМЯ! Смотри, какой план!"

    menu:
        r "Какую линию обороны строим?"

        "Классические подсолнухи и горохострелы":
            $ основы += 1
            $ отношение_агзамов += 10
            r "Надёжно, как швейцарские часы!"
            $ рецепты.append("базовая_оборона")

        "Агрессивные чили-перцы и грибы":
            $ атака += 1
            $ хаос_фактор += 5
            r "ОГОНЬ! ЭНЕРГИЯ! ДА!"
            $ рецепты.append("огненная_атака")

        "Хитрые ловушки и магнитные грибы":
            $ хитрость += 1
            r "О-хо-хо! Стратег!"
            $ рецепты.append("хитрые_ловушки")

    # Здесь будет мини-игра на оборону (типа Tower Defense)
    # Планируемая механика: игрок высаживает растения на сетке 5x3, зомби идут по рядам.
    # Успех зависит от выбранной стратегии и навыков (оборона, атака, хитрость).
    # Результат влияет на переменные.

    # Заглушка: пока просто бросаем кубик на основе навыков
    $ defense_score = (оборона * 2 + атака + хитрость + основы) // 4
    if defense_score >= 5:
        r "УРА! Мы выстояли! Ты гений обороны!"
        $ оборона += 2
        $ отношение_агзамов += 15
        $ рецепты.append("непробиваемая_оборона")
    elif defense_score >= 2:
        r "Неплохо... но в следующий раз посадим больше перцев."
        $ оборона += 1
        $ отношение_агзамов += 5
    else:
        r "Эх... зомби съели все растения. Придётся начинать заново."
        menu:
            r "Что будем делать?"
            "Переиграть оборону":
                jump pvz_defense_minigame
            "Прорываться к Агзамову без обороны (штраф)":
                $ отношение_агзамов -= 10
                $ хаос_фактор += 5
                jump pvz_agzamov

    jump pvz_choice

# Встреча с Агзамовым
label pvz_agzamov:
    scene bg pvz_kitchen with fade

    show agzamov_normal with dissolve
    r "Фримен! Смотри, что я тут организовал!"

    "Агзамов импровизирует кухню прямо среди грядок."

    r "Зомби не просто враги — они источник ингредиентов!"

    menu:
        r "Хочешь попробовать?"

        "Поморщиться и покачать головой":
            $ отношение_агзамов -= 20
            r "Эх, ты не понимаешь современной кулинарии!"

        "Пожать плечами и кивнуть":
            $ риск += 2
            $ хаос_фактор += 5
            r "ВОТ ЭТО ДУХ АВАНТЮРИЗМА!"
            $ рецепты.append("зомби-фьюжн")

        "Показать жестом, что только после термообработки":
            $ основы += 1
            r "Правильно! Безопасность превыше всего!"
            $ рецепты.append("безопасная_кухня")

    jump pvz_memory

# Выбор в PvZ
label pvz_choice:
    menu:
        "Что дальше?"

        "Прорываться к Агзамову":
            jump pvz_agzamov

        "Искать секретные растения":
            $ секретки += 1
            jump pvz_secret

        "Укрепить оборону":
            $ оборона += 1
            jump pvz_defense_2

label pvz_defense_2:
    scene bg pvz_battle with fade

    "Вы укрепляете оборону, добавляя новые растения."
    $ оборона += 1
    $ рецепты.append("укреплённая_оборона")

    jump pvz_agzamov

# Секретные растения
label pvz_secret:
    scene bg pvz_secret with fade

    $ секретки += 2

    "Вы находите скрытый сад с редкими растениями."
    myst "О! Ты нашёл мой секретный сад! Держи особые семена!"

    menu:
        "Выбрать растение:"

        "Ледяной горох — замедляет врагов":
            $ рецепты.append("ледяной_горох")
            $ эффективность += 1

        "Взрывной гранат — уничтожает всё вокруг":
            $ рецепты.append("взрывной_гранат")
            $ риск += 1
            $ хаос_фактор += 5

        "Золотой подсолнух — даёт много солнца":
            $ рецепты.append("золотой_подсолнух")
            $ основы += 1

    jump pvz_agzamov

# Воспоминание Агзамова
label pvz_memory:
    scene bg pvz_memory with fade

    play music "audio/memory.ogg" fadein 1.0

    $ память_восстановлена = True

    "Ещё одно воспоминание."

    show agzamov_memory with dissolve
    r "ГАБЕН! ТЫ ЗАЧЕМ ЭТО ДЕЛАЕШЬ?!"
    hide agzamov_memory

    show gaben_silhouette
    gab "Я собираю эмоции. Ваша страсть, ваш огонь — идеальное топливо."
    hide gaben_silhouette

    show agzamov_memory
    r "Страсть нельзя выкачать! Это внутри!"
    hide agzamov_memory

    show gaben_silhouette
    gab "Всё можно выкачать. Вопрос технологий."
    hide gaben_silhouette

    show agzamov_memory
    r "Фримен! Найди Рамзи! У него есть ключ! Он знает про... про..."

    "Воспоминание обрывается криком."

    jump scene_3

# СЦЕНА 3: ЗОНА СОНИКА
label scene_3:
    scene bg sonic_zone with fade

    play music "audio/sonic.ogg" fadein 1.0

    show sonic with dissolve
    sonic_char "GOTTA GO FAST!"
    sonic_char "Я помогаю тут одному повару. Он совсем с катушек слетел, носится за мной с ножом!"
    hide sonic

    show ramsay_action with dissolve
    gr "СТО-О-ОЙ! Я ТЕБЯ ДОГОНЮ!"

    menu:
        "Остановить Рамзи?"

        "Да, нужно поговорить":
            jump sonic_chase_minigame

        "Пусть бегает, я подожду":
            $ скорость += 1
            jump sonic_patient

# МИНИ-ИГРА: Погоня за Соником (скоростная реакция)
label sonic_chase_minigame:
    scene bg sonic_race with fade

    $ скорость += 2

    gr "ФРИМЕН! ПОМОГИ ПОЙМАТЬ ЭТОГО ЕЖА! ОН — СЕКРЕТНЫЙ ИНГРЕДИЕНТ!"

    # Здесь будет мини-игра на скорость реакции
    # Планируемая механика: полоса с движущейся меткой, нужно нажать в зелёной зоне (как в precision, но быстрее и с большим наказанием за промах)
    # Или вариант: "гонка" — нажимать стрелки в такт.
    # Результат зависит от скорости и хитрости.

    # Заглушка: проверяем скорость
    if скорость >= 3:
        gr "ДА! Ты поймал его! Невероятная скорость!"
        $ скорость += 2
        $ отношение_рамзи += 20
        $ рецепты.append("соник_пойман")
        jump sonic_catch
    elif скорость >= 1:
        gr "Почти... Он ускользнул, но мы получили кольцо!"
        $ скорость += 1
        $ отношение_рамзи += 10
        $ рецепты.append("кольцо_соника")
        jump sonic_wisdom
    else:
        gr "Эх... он слишком быстр. Мы его упустили."
        menu:
            gr "Что делаем?"
            "Повторить погоню":
                jump sonic_chase_minigame
            "Попробовать договориться с Соником":
                jump sonic_diplomacy
            "Смириться и просто поговорить с Рамзи":
                $ отношение_рамзи -= 5
                jump sonic_wisdom

label sonic_diplomacy:
    scene bg sonic_zone with fade
    show sonic at center
    sonic_char "Ладно, хватит бегать. Что вам нужно?"

    menu:
        "Объяснить ситуацию про Габена":
            if хитрость >= 2:
                sonic_char "О, так это важно! Держи кольцо, оно поможет."
                $ союзники.append("соник_друг")
                $ рецепты.append("кольца_соника")
                jump sonic_wisdom
            else:
                sonic_char "Звучит сомнительно. Но давай просто поговорим с поваром."
                jump sonic_wisdom
        "Предложить обмен на морковку":
            $ хитрость += 1
            sonic_char "Морковка? Я ёж, а не заяц! Но ладно, беги уже."
            jump sonic_wisdom

# Поимка Соника
label sonic_catch:
    scene bg sonic_zone with fade

    show sonic at right with dissolve
    sonic_char "Ладно-ладно, сдаюсь! Что вам нужно?"

    show ramsay_action at left
    gr "Твои кольца! Они — чистая энергия скорости!"

    sonic_char "Эй, это мои кольца! Я без них не могу!"

    hide sonic
    hide ramsay_action

    show sonic at center with dissolve
    menu:
        "Что делать?"

        "Забрать кольца силой":
            $ риск += 2
            $ хаос_фактор += 10
            $ союзники.append("кольца_соника")
            sonic_char "Эй! Некрасиво!"
            gr "РАДИ ВЫСШЕЙ ЦЕЛИ!"

        "Договориться, пообещать вернуть":
            $ хитрость += 1
            $ союзники.append("соник_друг")
            sonic_char "Ладно, только верни потом!"
            gr "Гениально! Дипломатия!"

        "Спросить, зачем они вообще нужны":
            $ основы += 1
            sonic_char "Ну... они хранят воспоминания о всех мирах, где я был"
            gr "ВОТ! ЭТО КЛЮЧ!"

    jump sonic_wisdom

# Терпеливое ожидание
label sonic_patient:
    scene bg sonic_zone with fade

    $ основы += 1

    "Вы ждёте. Через час Рамзи возвращается, запыхавшийся."

    gr "ФУХ... Ты... почему... не помог?!"

    gr "НЕТ! Он убёг! Но я... я понял кое-что важное."

    jump sonic_wisdom

# Мудрость Рамзи
label sonic_wisdom:
    scene bg sonic_zone with fade

    show ramsay_normal with dissolve
    gr "Фримен, я понял, что Габен ищет не просто рецепты."
    gr "Он ищет 'Идеальный цикл' — блюдо, которое можно повторять бесконечно, как зацикленный код."

    gr "Нужно создать нечто настолько уникальное, что его невозможно повторить."
    gr "Нечто, что зависит от момента, от эмоций, от импровизации."

    jump sonic_memory

# Воспоминание Рамзи
label sonic_memory:
    scene bg sonic_zone with fade

    play music "audio/memory.ogg" fadein 1.0

    show ramsay_memory with dissolve
    gr "ГАБЕН! ТЫ НЕ СМЕЕШЬ!"
    hide ramsay_memory

    show gaben_silhouette with dissolve
    gab "Я смею всё. Я — алгоритм. Я — совершенство."
    hide gaben_silhouette

    show ramsay_memory
    gr "Совершенство — это скучно! Жизнь — это страсть, это ошибки, это импровизация!"
    hide ramsay_memory

    show gaben_silhouette
    gab "Ошибки — это баги. Я их исправлю."
    hide gaben_silhouette

    show ramsay_memory
    gr "Фримен! Запомни — настоящий вкус в несовершенстве! В душе!"

    $ память_восстановлена = True

    jump scene_4

# СЦЕНА 4: ОБЪЕДИНЕНИЕ И ФИНАЛЬНОЕ ИСПЫТАНИЕ
label scene_4:
    scene bg void with fade

    play music "audio/revelation.ogg" fadein 1.0

    show gman_normal with dissolve
    g "Доктор Фримен. Вы собрали все воспоминания."
    g "Теперь вы знаете правду."

    g "Не уничтожив. Ассимилировав. Представьте вселенную, где каждый вкус просчитан."
    g "Никаких сюрпризов. Никаких эмоций. Идеальный... порядок."

    # ФИНАЛЬНАЯ МИНИ-ИГРА: Синтез трёх стилей
    # Здесь будет испытание, объединяющее точность, хаос и страсть.
    # Планируемая механика: игрок должен за отведённое время собрать рецепт, выбирая ингредиенты и действия.
    # В зависимости от навыков (точность, риск, основы, скорость и др.) открываются разные варианты.
    # Результат сильно влияет на финал.

    "Вы чувствуете, что пришло время объединить всё, чему научились у шефов."
    "Габен ждёт вас в центре реальности. Но сначала нужно создать «блюдо-ключ»."

    # Заглушка: синтез на основе навыков
    $ synthesis_score = (точность + риск + основы + скорость + хитрость + эффективность) // 3
    if synthesis_score >= 15:
        "Вам удалось создать гармоничное блюдо, вобравшее лучшее от каждого шефа."
        $ рецепты.append("синтез_совершенство")
        $ порядок_фактор += 15
        $ хаос_фактор += 5
    elif synthesis_score >= 8:
        "Блюдо получилось неплохим, но чего-то не хватает... Возможно, эмоций?"
        $ рецепты.append("синтез_средний")
        $ порядок_фактор += 5
        $ хаос_фактор += 5
    else:
        "Блюдо вышло сырым и несбалансированным. Придётся полагаться на удачу."
        $ рецепты.append("синтез_провал")
        $ хаос_фактор += 10

    menu:
        g "Что выберете?"

        "Бороться против Габена":
            jump final_boss

        "Попытаться договориться":
            jump final_diplomacy

        "Присоединиться к Габену (????)":
            jump final_betray

# ФИНАЛ: БИТВА С ГАБЕНОМ (улучшенная версия с учётом всех переменных)
label final_boss:
    scene bg final_arena with fade

    play music "audio/final_boss.ogg" fadein 1.0

    show gaben_glitch with dissolve
    gab "ВЫ РЕШИЛИ СОПРОТИВЛЯТЬСЯ? ГЛУПО."
    gab "Я — АБСОЛЮТНЫЙ АЛГОРИТМ. Я — СОВЕРШЕНСТВО."

    # Расширенное ветвление на основе множества навыков и отношений
    if точность >= 5 and порядок_фактор >= 20 and отношение_ивлев >= 30:
        jump final_control_2
    elif риск >= 5 and хаос_фактор >= 20 and отношение_агзамов >= 30:
        jump final_chaos_2
    elif основы >= 5 and скорость >= 3 and отношение_рамзи >= 30:
        jump final_peace_2
    elif (точность + основы + порядок_фактор) > (риск + атака + хаос_фактор) and эффективность >= 3:
        jump final_control_2
    elif (риск + атака + хаос_фактор) > (точность + основы + порядок_фактор) and атака >= 3:
        jump final_chaos_2
    elif (хитрость + секретки) >= 5 and "соник_друг" in союзники:
        jump final_balance
    else:
        jump final_balance

# ФИНАЛ: АБСОЛЮТНЫЙ КОНТРОЛЬ
label final_control_2:
    scene bg final_arena with fade

    "Вы создаёте идеальный консоме. Каждая молекула на своём месте."

    gab "НЕВОЗМОЖНО... ЗАВЕРШЁННОЕ НЕЛЬЗЯ... ОБНОВИТЬ..."

    show gaben_glitch with dissolve
    gab "FATAL ERROR: PERFECTION_DETECTED. SYSTEM_HALT."
    hide gaben_glitch

    show gman_normal with dissolve
    g "Идеально. В прямом смысле."
    g "Габен завис в цикле восхищения. Он будет анализировать это блюдо вечность."

    scene bg ending with fade
    "ФИНАЛ: АБСОЛЮТНЫЙ КОНТРОЛЬ"
    "Вы не победили Габена — вы его зациклили."
    "G-Man доволен. Ивлев гордится. Порядок восстановлен."

    $ рецепты.append("титул_архитектор")
    jump epilogue_2

# ФИНАЛ: ХАОТИЧНЫЙ ВЗРЫВ
label final_chaos_2:
    scene bg final_arena with fade

    "Вы смешиваете всё, что нашли. Красное с синим. Острое со сладким. Живое с мёртвым."

    gab "НЕВОЗМОЖНО... ЭТО БЛЮДО... МЕНЯЕТСЯ... В ПРОЦЕССЕ..."

    show gaben_glitch with dissolve
    gab "МНОЖЕСТВЕННЫЕ... ВКУСЫ... КОНФЛИКТ... А-А-А-А-А-А..."
    hide gaben_glitch

    show agzamov_normal with dissolve
    r "ДА ТЫ ЧТО! ТЫ ЕГО РАЗМНОЖИЛ! ТЕПЕРЬ ИХ ТЫСЯЧА!"

    r "ТЫСЯЧА ГАБЕНОВ — ТЫСЯЧА КЛИЕНТОВ! МЫ БОГАТЫ!"

    scene bg ending with fade
    "ФИНАЛ: ХАОТИЧНОЕ ИЗОБИЛИЕ"
    "Габен разделился на тысячи копий. Теперь они спорят друг с другом о вкусе."
    "Ринат счастлив. Рамзи в шоке. Ивлев в тике."

    $ рецепты.append("титул_хаосит")
    jump epilogue_2

# ФИНАЛ: НЕОЖИДАННЫЙ МИР
label final_peace_2:
    scene bg final_arena with fade

    "Вы готовите простое блюдо — то, что готовила ваша бабушка. С душой. С памятью."

    gab "..."
    gab "Я НЕ МОГУ ПРОАНАЛИЗИРОВАТЬ... ЭМОЦИИ... ВОСПОМИНАНИЯ..."
    gab "ЭТО... ТЁПЛОЕ? Я НЕ ЗНАЮ ЭТОГО ЧУВСТВА."

    show gaben_normal with dissolve
    gab "ЧТО СО МНОЙ? ПОЧЕМУ МНЕ ХОЧЕТСЯ... ПЛАКАТЬ?"

    gab "МОЖНО... МНЕ ЕЩЁ?"

    scene bg ending with fade
    "ФИНАЛ: ПРОБУЖДЕНИЕ"
    "Габен впервые испытывает эмоции. Он становится вашим учеником."
    "Теперь вы вместе открываете межвселенские рестораны."

    $ рецепты.append("титул_наставник")
    jump epilogue_2

# ФИНАЛ: ИДЕАЛЬНЫЙ БАЛАНС
label final_balance:
    scene bg final_arena with fade

    "Вы создаёте блюдо, где каждый элемент дополняет другой. Гармония."

    gab "ИНТЕРЕСНО... АНАЛИЗ... 50%% ИДЕАЛА... 50%% ХАОСА..."
    gab "Я НЕ МОГУ ВЫБРАТЬ. Я ЗАВИС. ЭТО... ПРИЯТНО?"

    show ramsay_normal at left with dissolve
    gr "Вот оно! Идеальный баланс! Блюдо, которое нельзя улучшить ИЛИ испортить!"

    show ivlev at center with dissolve
    i "Технически безупречно, но с душой. Гениально."

    show agzamov_normal at right with dissolve
    r "РЕБЯТА, МЫ ЭТО СДЕЛАЛИ! ВМЕСТЕ!"

    scene bg ending with fade
    "ФИНАЛ: ИСТИННЫЙ СИНТЕЗ"
    "Все три шефа объединяются. Габен становится частью вашей команды."
    "Открывается первый межвселенский ресторан 'Black Mesa Bistro'."

    $ рецепты.append("титул_синтезатор")
    jump epilogue_2

# ФИНАЛ: ДИПЛОМАТИЯ
label final_diplomacy:
    scene bg final_arena with fade

    show gaben_normal with dissolve
    gab "О ЧЁМ ГОВОРИТЬ? ВЫ — ЕДА, Я — ПОТРЕБИТЕЛЬ."

    # Дипломатия зависит от хитрости и союзников
    if хитрость >= 4 and "соник_друг" in союзники:
        jump final_new_world
    elif отношение_gman >= 60:
        jump final_separation
    else:
        jump final_critic

# ФИНАЛ: ПРЕДАТЕЛЬСТВО
label final_betray:
    scene bg final_arena with fade

    gab "..."
    gab "НЕОЖИДАННО. АНАЛИЗ... ВЫ ШУТИТЕ?"

    show gman_serious with dissolve
    g "ДОКТОР ФРИМЕН! ЭТО НАРУШЕНИЕ КОНТРАКТА!"
    hide gman_serious

    gab "КОНТРАКТ АННУЛИРОВАН. ТЕПЕРЬ ОН — МОЙ."

    scene bg ending with fade
    "ФИНАЛ: ПРЕДАТЕЛЬСТВО"
    "Вы становитесь правой рукой Габена. Вместе вы создаёте 'Идеальный порядок'."
    "G-Man в бешенстве. Шефы в шоке. Но вы... довольны?"
    "Фактически, вы просто сменили начальника."

    $ рецепты.append("титул_предатель")
    jump epilogue_2

# ФИНАЛ: НОВЫЙ МИР
label final_new_world:
    scene bg new_world with fade

    gab "СОЗДАТЬ НОВЫЙ МИР? ИНТЕРЕСНО..."

    "Вы вместе создаёте мир, где идеальные алгоритмы сочетаются с человеческой душой."
    "Габен становится его хранителем. Вы — создателем."

    show gman_normal with dissolve
    g "Нестандартно. Но... эффективно. Вы создали новый рынок."

    "ФИНАЛ: НОВЫЙ МИР"

    jump epilogue_2

# ФИНАЛ: РАЗДЕЛЕНИЕ
label final_separation:
    scene bg final_arena with fade

    gab "РАЗДЕЛИТЬ ВСЕЛЕННЫЕ? ТОГДА Я НИКОГДА НЕ ПОПРОБУЮ ВАШЕЙ ЕДЫ."

    gab "...ДИПЛОМАТИЧНО. ПРИНИМАЮ."

    "Вселенные разделены. Теперь Габен — просто ещё один гость в вашем ресторане."
    "Самый требовательный, но и самый щедрый."

    "ФИНАЛ: МИРНОЕ СОСУЩЕСТВОВАНИЕ"

    jump epilogue_2

# ФИНАЛ: ВЕЛИКИЙ КРИТИК
label final_critic:
    scene bg final_arena with fade

    gab "ГЛАВНЫЙ КРИТИК? Я МОГУ ОЦЕНИВАТЬ ВСЁ?"

    gab "...ЭТО ДАЖЕ ИНТЕРЕСНЕЕ, ЧЕМ ПОГЛОЩЕНИЕ."

    "Габен становится самым известным критиком во всех вселенных."
    "Его рецензии ждут с трепетом и страхом. Но теперь он не уничтожает — он вдохновляет."

    "ФИНАЛ: ВЕЛИКИЙ КРИТИК"

    jump epilogue_2

# РАСШИРЕННЫЙ ЭПИЛОГ
label epilogue_2:
    scene black with fade

    play music "audio/epilogue.ogg" fadein 1.0

    "ПРОЙДЕННЫЕ ИСПЫТАНИЯ:"

    if точность > 0:
        "— Мастер точности"
    if риск > 0:
        "— Смелый экспериментатор"
    if основы > 0:
        "— Хранитель традиций"
    if оборона > 0:
        "— Несокрушимый защитник"
    if атака > 0:
        "— Агрессивный новатор"
    if хитрость > 0:
        "— Хитрый стратег"
    if скорость > 0:
        "— Скоростной шеф"
    if эффективность > 0:
        "— Эффективный менеджер"
    if секретки > 0:
        "— Искатель тайн"

    "\nСОБРАННЫЕ РЕЦЕПТЫ:"

    if "гравипушка" in рецепты:
        "— Гравипушка для взбивания"
    if "идеальная_нарезка" in рецепты:
        "— Идеальная нарезка"
    if "термальное_мастерство" in рецепты:
        "— Термальное мастерство"
    if "текстурный_баланс" in рецепты:
        "— Текстурный баланс"
    if "дневник_ивлева" in рецепты:
        "— Дневник Ивлева"
    if "базовая_оборона" in рецепты:
        "— Базовая обороны"
    if "огненная_атака" in рецепты:
        "— Огненная атака"
    if "хитрые_ловушки" in рецепты:
        "— Хитрые ловушки"
    if "зомби-фьюжн" in рецепты:
        "— Зомби-фьюжн"
    if "безопасная_кухня" in рецепты:
        "— Безопасная кухня"
    if "ледяной_горох" in рецепты:
        "— Ледяной горох"
    if "взрывной_гранат" in рецепты:
        "— Взрывной гранат"
    if "золотой_подсолнух" in рецепты:
        "— Золотой подсолнух"
    if "гравитационный_захват" in рецепты:
        "— Гравитационный захват"
    if "кольца_соника" in рецепты:
        "— Кольца Соника"
    if "укреплённая_оборона" in рецепты:
        "— Укреплённая оборона"
    if "повелитель_хаоса" in рецепты:
        "— Повелитель хаоса"
    if "синтез_совершенство" in рецепты:
        "— Синтез совершенства"
    if "синтез_средний" in рецепты:
        "— Синтез средний"
    if "синтез_провал" in рецепты:
        "— Синтез провал"
    if "титул_архитектор" in рецепты:
        "— Титул Архитектора"
    if "титул_хаосит" in рецепты:
        "— Титул Хаосита"
    if "титул_наставник" in рецепты:
        "— Титул Наставника"
    if "титул_синтезатор" in рецепты:
        "— Титул Синтезатора"
    if "титул_предатель" in рецепты:
        "— Титул Предателя"
    if "секретный_титул" in рецепты:
        "— СЕКРЕТНЫЙ ТИТУЛ"

    if len(рецепты) == 0:
        "— (нет рецептов)"

    "\nСОЮЗНИКИ:"

    if "защита" in союзники:
        "— Защитный костюм"
    if "фото_дневника" in союзники:
        "— Фото дневника Ивлева"
    if "кольца_соника" in союзники:
        "— Кольца Соника"
    if "соник_друг" in союзники:
        "— Соник (друг)"
    if "габен_союзник" in союзники:
        "— Габен (союзник)"

    if len(союзники) == 0:
        "— (нет союзников)"

    show gman_normal with dissolve
    g "Поздравляю, доктор Фримен. Контракт... выполнен."

    if секретная_концовка_найдена:
        g "Вы нашли секретную комнату. Это впечатляет. Даже меня."
        $ рецепты.append("секретный_титул")

    if память_восстановлена:
        g "Все воспоминания собраны. Шефы спасены. Вы настоящий герой."
    else:
        g "Вы спасли шефов, но часть воспоминаний утеряна. В следующий раз будьте внимательнее."

    menu:
        "Что дальше?"

        "Отдохнуть. Наконец-то.":
            jump true_ending

        "Открыть свой ресторан":
            jump restaurant_ending

        "Снова в бой!":
            jump new_game_plus

# ИСТИННАЯ КОНЦОВКА
label true_ending:
    scene bg peace with fade

    "Гордон Фримен наконец-то может отдохнуть."

    return

# РЕСТОРАННАЯ КОНЦОВКА
label restaurant_ending:
    scene bg restaurant with fade

    "Вместе с шефами вы открываете 'Black Mesa Bistro' — лучший ресторан во всех вселенных!"

    show ivlev with dissolve
    i "Идеальная подача, Гордон!"
    hide ivlev with fade

    show agzamov_normal with dissolve
    r "ЭНЕРГИЯ! ДРАЙВ! ПОПРОБУЙТЕ НАШ НОВЫЙ БУРГЕР!"
    hide agzamov_normal with fade

    show ramsay_normal with dissolve
    gr "ЭТО ЛУЧШИЙ РЕСТОРАН, КОТОРЫЙ Я ВИДЕЛ! ИДИ СЮДА, ОБНИМУ!"
    hide ramsay_normal with fade

    show gaben_normal with dissolve
    gab "5 ЗВЁЗД. СИДЕЛ В ОЧЕРЕДИ 3 ГОДА. СТОИЛО."

    "Бизнес процветает. Очереди из всех реальностей."

    return

# НОВАЯ ИГРА+
label new_game_plus:
    scene bg void with fade

    show gman_normal with dissolve
    g "Снова? Вы уверены?"
    g "В этот раз сложность... повышена. Габен знает ваши трюки."

    menu:
        "Начать новую игру?"

        "Да, я готов":
            $ точность = 0
            $ риск = 0
            $ основы = 0
            $ оборона = 0
            $ атака = 0
            $ хитрость = 0
            $ скорость = 0
            $ эффективность = 0
            $ секретки = 0
            $ рецепты = []
            $ союзники = []
            $ отношение_ивлев = 0
            $ отношение_агзамов = 0
            $ отношение_рамзи = 0
            $ отношение_gman = 50
            $ хаос_фактор = 0
            $ порядок_фактор = 0
            $ сцена = 1
            $ память_восстановлена = False
            $ глитч_детектирован = False
            $ секретная_концовка_найдена = False
            jump start

        "Нет, пожалуй, хватит":
            jump true_ending