# Интерактивная карта заказов
### Цель  
Карта с постоянно актуальной информацией о заказах. 
Необходима возможность отследить статус каждого заказа и дополнительную информацию (дата заключения договора, кадастровый номер и так далее), а также возможность фильтровать заказы по статусам.

### Стэк 
flask, folium, pandas, REST API, SQLite, threading.

### Описание приложения
При добавлении, удалении, изменени задач приложение обновляет БД и тригерит рендер карты с помощью вэбхуков. А так также каждый час выполняет проверку актуальности принудительно, потому что исходящие хуки в Битрике работают через раз.  
<a href="https://atryfvfd.pythonanywhere.com/">Пример страницы.</a>


