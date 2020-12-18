// const url_api = 'http://localhost:8080/',
// const url_api = 'https://7m8a45lded.execute-api.us-east-1.amazonaws.com/tfe/',
// const url_api = 'http://54.84.79.47/',
const url_api = 'https://ec2-54-84-79-47.compute-1.amazonaws.com/',
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
    
    let info = `
    Hola ${data['facebook_result'].name} de acuerdo a la información que se encuentra publicada en tu Facebook
    podemos identificar lo siguiente: <hr>
    El siguiente es un mensaje que llevas en tu perfil: <b> ${data['facebook_result'].name_user_sub} </b>, además sabemos que tienes ${data['facebook_result'].number_friends},
    número de amigos.<br>
    Que actualmente estudias en: ${data['facebook_result'].study_actually}.

    <b>Consideramos que tu perfil no es válido para Facebook en un XX%</>
    `

    $('#text_result').html(info)
    console.log(data)
}

function tryAgain(){
    $('#div_query').show()
    $('#div_result').hide()

    $('#btn_search').html(resources.svg.btn_search)
}