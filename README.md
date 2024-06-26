Простенькая игра на языке программирования python. Throne of Shadows - пиксельная пошаговая игра. Цель игры - поддерживать уровень счастья граждан и дойти до концовки, сражаясь с непростыми босами и обычными мобами, обладающими минимальным искусственным интеллектом.

Чтобы помочь игроку в прохождении в игре присутствует магазин, в котором можно купить предметы, восстанавливающие жизнь, новые оружия, наносящие больше урона противникам, или специальные предметы, повышающие удачу игрока.

В Throne of Shadows есть три концовки: плохая, если счастье граждан упадёт ниже нуля, хорошая, если число монет в казне будет выше 2100, а также секретная, если победить особого противника. Если же игрок не справится с противниками на уровне, то его ждёт экран проигрыша. 
Выйти из подземелья можно благодаря специальным выходам, расположенным на карте, чтобы обновить снаряжение для нового захода. 

  Алгоритм игры «Throne of Shadows» реализован в программе следующим образом:
  
    1. Декларация глобальных переменных: При первом запуске игры создаётся база данных, далее ряд необходимых переменных, среди которых флаги (bool-переменные), массив классов кнопок, общая карта;
    
    2. Инициализация главного меню: В главном цикле pygame отображаются задний фон и кнопки взаимодействия («New game», «Continue», «Quit»), начинает играть общая музыка;
    
    3. Инициализация хаб-локации: При старте новой игры или при продолжении уже существующей в полный экран открывается окно хаб-локации. Там игры ожидает нажатие на «Замок», «Ферму», «Башню» или «Шахту» (подземелье), а также выводит необходимую информацию: «уровень счастья граждан», «долг», «капитал»;
    
    4. Взаимодействие игрока с торговцами: Нажав на «Замок», «Ферму» или «Башню» появляется ещё окно поверх предыдущего, при этом взаимодействие пользователя возможно только с новым окном 600 на 300 пикселей. Покупка осуществляется исходя из доступных средств игрока, сохранённых в базе данных;
    
    5. Основной игровой процесс: Игрок может перемещаться в любом из доступных четырёх направлений, если по пути движения не находится стены (белого пикселя), при этом при ходе пользователя в тот же миг двигаются и противники: обычные враги случайно, боссы стремятся добраться до игрока. Зайдя в ту же клетку, что и сундук (зелёный пиксель, отличный от похожего, являющемся мимиком), игроку начисляется случайное число монет от 1 до 4 включительно, информация о заработке отображается справа от основного игрового поля. Заходя же в клетку, являющейся мимиком, обычным врагом или боссом, карта «замораживается» и «скрывается», появляется интерфейс для боя. Попадая на клетку выхода, находящуюся по углам игрового поля, игрок возвращается в хаб-локацию, сохраняя всё «награбленное»;
    
    6. Обработка боевой механики: Начав бой с обычным противником, программа случайным образом генерирует картинку (внешний вид), шанс нанести урон оппонентом игроку и шанс побега от монстра игроком. Начав бой с другими оппонентами, мимиком или боссами, случайность генерации характеристик отсутствует. Первый ход всегда за игроком. Он в праве решать, какое действие предпринять: атаковать, сбежать, восстановить жизни или попытаться договориться. Время на обдумывание неограничено, восстановление жизней не приводит к передаче хода. «Throne of Shadows» внимательно следит за числом жизней, как игрока, так и оппонента, начисляя награду за убийство врага или показывая окно поражения при смерти пользователя. При этом, во всех вычислениях шансов учитываются особые предметы, купленные у торговцев;
    
    7. Проверка условий победы: Различные концовки достигаются при 1) уровне счастья ниже нуля; 2) при смерти игрока в подземелье; 3) при числе монет не менее 2100; 4) при победе над секретным боссом.

Демонстрация работы игры:
https://disk.yandex.ru/i/ILgqUB2k0zkSzQ
