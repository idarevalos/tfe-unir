const url_api = 'http://localhost:8080/',
// const url_api = 'https://7m8a45lded.execute-api.us-east-1.amazonaws.com/tfe/',
m = 'getDataProfile/'


/**
 * Listeners
 */
$('#btn_search').on('click', function(){
    let i = $('#input_url').val()
    if (!i || !i.includes('acebook')) {
     
        swal("Ingrese una dirección en Facebook válida", {
            dangerMode: true
        })

    }else
        $(this).html(resources.svg.loading)
        let pr = i.split('facebook.com/')
        queryProfile(pr[1]) // consutar el perfil
})

/** Consulta perfil */
function queryProfile(profile){
    fetch(url_api+m+profile)
    .then(response => response.json())
    .then(data => {
        processResponde(data)
    }).catch(()=>{
        swal("Oh oh!",'Ha ocurrido un error inesperado, inténtelo más tarde por favor.','warning')
        $('#btn_search').html(resources.svg.btn_search)
    })
}

function processResponde(data){
    $('#div_query').hide()
    $('#div_result').show()
    
    $('#text_result').html(`El resultado para el perfil <b>${data['data']}</b>`)
}

function tryAgain(){
    $('#div_query').show()
    $('#div_result').hide()

    $('#btn_search').html(resources.svg.btn_search)
}