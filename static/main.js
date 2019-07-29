/* form submission handler */
$(document).on('submit', function(e){
    e.preventDefault();
    // get necessary elements, display loader, pass to AJAX utility
    document.getElementById('spinner').style.display = 'block';;
    document.getElementsByClassName('result-frame')[0].style.display = 'none';;
    getMap(e.target['domain'].value);
})

/* AJAX utility to pass submitted domain to server-side make_map() */
function getMap(domain){
    console.log(domain);
    $.ajax({
        url: '/',
        type: 'POST',
        data: domain,

        success: function(res){
            // todo
        }

    });
}