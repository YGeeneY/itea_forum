$(document).ready(function() {

    $(document).on("scroll", function () {
        var scrollHeight = window.scrollY,
            header = $("#header"),
            headerHeight = parseInt(header.css("height")),
            opacity = scrollHeight - headerHeight,
            $btt = $('#back-to-top');

        if (scrollHeight > 400){
            $btt.show()
        } else {
            $btt.hide()
        }

        header.css("background", "rgba(25, 118, 210, " + opacity / 200 + ")");
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
});

