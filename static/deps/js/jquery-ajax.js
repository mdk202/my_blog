$(document).ready(function () {
    // берем в переменную элемент разметки с id jq-notification для оповещений от ajax
    var successMessage = $("#jq-notification");
    
    // Берем из разметки элемент по id - оповещения от django
    var notification = $('#notification');
    if (notification.length > 0) {
        setTimeout(function () {notification.alert('close');}, 5000);
    }

    $(document).on("click", ".like-button", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();
    
        // Получаем id статьи из атрибута data-article-id
        var article_id = $(this).data("article-id");

        // Из атрибута href берем ссылку на контроллер
        var likes_url = $(this).attr("href");
        
        // Получаем из скрытого input значение 1, если пользователь
        // лайкал статью, или значение 0, если пользователь лайк не ставил
        var likes_article = $(this).find('#likes-article').val();

        // Берем элемент счетчика количества лайков на статье и берем оттуда значение
        var articlesLikesCount = $(this).find('#likes-on-article-count');
        var likesCount = parseInt(articlesLikesCount.text() || 0);
        
        // Если пользователь лайкает статью, то увеличиваем кол-во
        // лайков на единицу и изменяем цвет кнопки на красный
        if (likes_article === "0"){
            likesCount++;
            articlesLikesCount.text(likesCount);
            $(this).css({"background-color":"red"});
            $(this).find("input[id=likes-article]").val("1");
        // Если пользователь убирает лайк, то уменьшаем кол-во
        // лайков на единицу и изменяем цвет кнопки на белый
        } else {
            likesCount--;
            articlesLikesCount.text(likesCount);
            $(this).css({"background-color":"white"});
            $(this).find("input[id=likes-article]").val("0");
        }

        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({
            type: "POST",
            url: likes_url,
            data: {
                article_id: article_id,
                csrfmiddlewaretoken: $(this).find("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Сообщение
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Через 5сек убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 5000);

                // Меняем разметку лайков на статье на ответ от django
                var likeItems = $(this).find(".like-items");
                likeItems.html(data.like_items_html);
            },
            error: function (data) {
                console.log("Ошибка при постановке лайка");
            },
        });
    });

    // Показать/скрыть пароль
    $(document).on("click", ".password-checkbox", function () {
        if ($(this).is(':checked')){
            $('input[id*="password"]').attr('type', 'text');
        } else {
            $('input[id*="password"]').attr('type', 'password');
        }
    });
});
