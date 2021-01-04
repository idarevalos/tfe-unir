
// const url_api = 'http://localhost:8080/',
const url_api = 'http://ec2-54-84-79-47.compute-1.amazonaws.com/',
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
        return false
    }else{

        $(this).html(resources.svg.loading)
        let pr = i.split('facebook.com/')
        queryProfile(pr[1]) // consutar el perfil

        let h__ = `<div class="progress_div"><hr>${resources.progess.bar}<br><em>El proceso puede tartar unos segundos ...</em></div>`
        $('#div_query').append(h__)
    }

    let porcent = 6,
    interval_ =  setInterval(() => {
        $('#bar_progess_1').css('width', porcent+'%')
        $('#bar_progess_1').text(Math.floor(porcent)+'%')
        porcent = porcent + 0.45
        
        // Die interval
        if (porcent >= 100) {
            clearInterval(interval_);    
        }
        
    }, 150);
        
})

function processResponde(data){
    console.log(data)
    $('#div_query').hide()
    $('#div_result').show()
    
    function processText(tx, tag, class_ = '', addText=''){
        let ft = ''
        if (tx) {
            ft = `<${tag} class="${class_}">${addText} ${tx}</${tag}>`
        }
        return ft
    }


    let info = `
    <div class="card user-card bg-dark">
    <div class="card-header">
        <h5>Perfil</h5>
    </div>
    <div class="card-block">
        <div class="user-image">
            <img src="${data['facebook_result']['profile_image']}" class="img-radius" alt="User-Profile-Image">
        </div>
        <hr>
        <h6 class="f-w-600 m-t-25 m-b-10">${data['facebook_result']['name']}</h6>
        ${processText(data['facebook_result']['name_user_sub'],'code')}
        <p class="text-muted m-t-15">De acuerdo a la información publicada su perfil es: <br><span class="badge badge-light">${data['result_prediction']}</span></p>        
        <p class="alert alert-info">La información de su perfil que nos ayudó a identificarlo es:</p>
        ${processText(data['result_process_data']['number_friends'],'p','','Amigos')}
        ${processText(data['result_process_data']['followers'],'p','', 'Seguidores')}
        ${processText(data['facebook_result']['job'],'p','','Dice que actualmente trabaja en: ')}
        ${processText(data['facebook_result']['live'],'p','')}
        ${processText(data['facebook_result']['study_finish'],'p','')}
        
        <div class="row justify-content-center user-social-link">
            <div class="col-auto"><a href="https://facebook.com/${data['facebook_path']}" target="_blank"> Visitar Perfil</a></div>
        </div>
    </div>
</div>
`

    $('#text_result').html(info)
}

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

function tryAgain(){
    $('#div_query').show()
    $('#div_result').hide()

    $('#btn_search').html(resources.svg.btn_search)
    $('.progress').remove()
    $('.progress_div').remove()
}