$(document).ready(function() {

    $(document).on("scroll", function () {
        var scrollHeight = window.scrollY,
            header = $("#header"),
            headerHeight = parseInt(header.css("height")),
            opacity = scrollHeight - headerHeight,
            $btt = $('#back-to-top');

        if (scrollHeight > 250){
            $btt.show()
        } else {
            $btt.hide()
        }

        header.css("background", "rgba(25, 118, 210, " + opacity / 100 + ")");
    });

    $('.toggle-topic').on("click", function(){
        var thead = $(this).parents('thead')[0],
            tbody = thead.nextElementSibling;

        $(this).toggleClass('fa-minus-circle fa-plus-circle');
        $(tbody).toggle()
    });

    $('#back-to-top').on("click", function(e) {
        e.preventDefault();
        $('html, body').animate({
            scrollTop: 0
        }, 300);
    });

    $('#popup').on("click", function (e) {
        e.preventDefault();
        $('#popup-login').slideToggle()
    });


    $('.message-alert')
        .animate({bottom: "40px"}, 300, 'swing')
        .delay(2000).fadeOut(500, 'swing');

    (function(){
        var $close = $('.close'),
            messageClass = $close.attr('class').split(' ')[1];

        if (messageClass === 'error'){
            $close.parent().css({
                background: 'red',
                border: '1px solid red',
                color: 'white'
            });
        }

        $close.on('click', function(e){
            e.preventDefault();
            $(this).parent().hide()
        });

    })();

    (function(){
        var location = window.location.pathname,
            $popUpLogin = $("#popup-login"),
            currentAction = $popUpLogin.attr('action');

        $popUpLogin.attr('action', currentAction + '?next=' + location)

    })();

    setInterval(function(){
        $('#blink')
            .animate({opacity: '0'}, 1000, 'swing')
            .animate({opacity: '1'}, 1000, 'swing')
    }, 1000);
});

