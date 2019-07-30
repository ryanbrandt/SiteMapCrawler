/* form submission handler */
$(document).on('submit', function(e){
    e.preventDefault();
    // if valid domain do AJAX call, else alert
    if(isValidDomain(e.target['domain'].value)){
        document.getElementById('spinner').style.display = 'block';
        document.getElementsByClassName('result-frame')[0].style.display = 'none';
        getMap(e.target['domain'].value);
    } else {
        alert('Improperly formatted domain!\n Please follow format: https://www.ADomainHere.com');
    }
})

/* simple validator */
function isValidDomain(domain){
    var re = /(http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/;
    return re.test(domain);
}

/* AJAX utility to pass submitted domain to server-side make_map() */
function getMap(domain){
    console.log(domain);
    $.ajax({
        url: '/',
        type: 'POST',
        data: domain,

        success: function(res){
            console.log(JSON.stringify(res, null, 4));
            document.getElementById('resContainer').innerHTML = '<pre><code>' + JSON.stringify(res, null, 2) + '</code></pre>';
            document.getElementById('spinner').style.display = 'none';
            document.getElementsByClassName('result-frame')[0].style.display = 'block';
        }

    });
}