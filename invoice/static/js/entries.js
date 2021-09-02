$(document).ready(function () {
    $('.table').DataTable({
        "pagingType": "simple",

        lengthMenu: [
            [15, 25, 100, -1],
            [15, 25, 100, "All"]
        ],
        pageLength: 15,
        dom: 'lBfrtip',
        buttons: [{
            extend: 'collection',
            text: 'Export',
            align: 'right',
            buttons: [
                'copy',
                'excel',
                'csv',
                'pdf',
                'print'
            ]
        }],
    });


    $('.table').DataTable({
        "pagingType": "simple",

        lengthMenu: [
            [15, 25, 100, -1],
            [15, 25, 100, "All"]
        ],
        pageLength: 15,
        dom: 'lBfrtip',
        buttons: [{
            extend: 'collection',
            text: 'Export',
            align: 'right',
            buttons: [
                'copy',
                'excel',
                'csv',
                'pdf',
                'print'
            ]
        }],
    });
});
$(document).ready(function () {
    quantity = $('.s_quantity')
    for (i = 0; i < quantity.length; i++) {
        quantity[i].innerHTML = quantity[i].textContent.split('/n').reduce(function (a, b) {
            return parseFloat(a) + parseFloat(b)
        })
    }
})
$(document).ready(function () {
    for (i = 0; i < $('.item').length; i++) {
        $('.item')[i].innerHTML = $('.item')[i].textContent.split('/n').join('<br>');
        $('.description')[i].innerHTML = $('.description')[i].textContent.split('/n').join('<br>');
        $('.alt_quantity')[i].innerHTML = $('.alt_quantity')[i].textContent.split('/n').join('<br>');
        $('.quantity')[i].innerHTML = $('.quantity')[i].textContent.split('/n').join('<br>');
        $('.rate')[i].innerHTML = '<td>' + $('.rate')[i].textContent.split('/n').join('<br>') + '<td>';
        $('.per')[i].innerHTML = $('.per')[i].textContent.split('/n').join('<br>');
        $('.amount')[i].innerHTML = $('.amount')[i].textContent.split('/n').join('<br>')
    }
    $('.switch_small').click(function () {
        if ($('.small_view').hasClass('no_display')) {
            $('.switch_large').removeClass('active')
            $('.switch_small').addClass('active')
            $('.small_view').removeClass('no_display');
            $('.large_view').addClass('no_display')
        }
    })
    $('.switch_large').click(function () {
        if ($('.large_view').hasClass('no_display')) {
            $('.switch_large').addClass('active')
            $('.switch_small').removeClass('active')
            $('.large_view').removeClass('no_display');
            $('.small_view').addClass('no_display')
        }
    })
})