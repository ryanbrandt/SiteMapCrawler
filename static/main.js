/* form submission handler */
$(document).on('submit', function(e){
    e.preventDefault();
    // get necessary elements, display loader, pass to AJAX utility
    var spinner = document.getElementById('spinner');
    var resFrame = document.getElementsByClassName('result-frame')[0];
    spinner.style.display = 'block';
    getMap(e.target['domain'].value);
    // on return show resFrame, hide loader
    spinner.style.display = 'none';
    resFrame.style.display = 'block';
})

/* AJAX utility to pass submitted domain to server-side make_map() */
function getMap(domain){
    console.log(domain);
    $.ajax({
        url: '/make-map',
        type: 'POST',
        data: domain,

        success: function(){
            // todo
        }

    });
}