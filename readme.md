# ***VKinder***
##### Бот сообщества ВКонтакте для поиска пользователей по заданным параметрам
***
***Перед началом работы:***

- установить пакеты _requirements.txt_
- сохранить токены (сообщества и персональный)  в файл _config.py_
- создать БД Postgresql 
- сохранить параметры БД в файл _config.py_
- запустить файл _main.py_
- перейти в сообщество https://vk.com/public216899382
- работа с ботом начинается после команды: _/start_

***При первом запуске:***
- написать в сообщество сообщение: _/new db_ (команда пересоздает БД)
***
### Работа с ботом 

        Навигация по меню бота:
        -----------------------------
        <Новый поиск> - подбор анкет по вашим параметрам
        <Избранное> - показ анкет из папки "Избранное"
        <Анкеты> - показ найденных анкет
        <Добавить в избранное> добавить анкету в Избранное. 
        Анкеты добавляются с последней показанной в обратном порядке.
        -----------------------------
        <Настройки> - установка параметров поиска
        установка параметров: /<команда> <значение>  
        <Пол> - пол в искомых анкета [0-любой, 1-женщина, 2-мужчина] | /sex 1
        <Возраст> - возрастной интервал (мин. значение от: 18) | /age 25-30
        <Статус> - семейный статус пользователя (0-8) | /status 5
        <Интересы> - поля в анкете [книги, фильмы, музыка, о себе, интересы]
        | /inter  <знач1, знач2, ..> | перечислите через запятую ключевые слова(необязательное поле)
        
        <Город> - город в анкете | /city Москва --> /id 1 | 
        команду /city используйте, если не знаете id города 
        -----------------------------
        <Очистка> -> <Избранное> - полностью очищает ваш список избранного
        <Очистка> - <Текущее> - очистка списка текущего поиска
        <Очистка> -> <Просмотренное> - очищает ваш список показанного. Эти анкеты 
        снова будут появляться в поиске
                
        Просмотренные анкеты, автоматически добавляются в "Просмотренное" 
        и больше не выводятся в показах.
