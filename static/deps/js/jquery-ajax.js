$(document).ready(function () {

    // Берем из разметки элемент по id - оповещения от django
    var notification = $('#notification');
    if (notification.length > 0) {
        setTimeout(function () {notification.alert('close');}, 3000);
    }
});