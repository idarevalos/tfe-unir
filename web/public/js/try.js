const url_api = 'http://localhost:8080/',
m = 'queryProfile/'



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
        queryProfile(btoa(i)) // consutar el perfil
})

/** Consulta perfil */
function queryProfile(profile){
    fetch(url_api+m+profile)
    .then(response => response.json())
    .then(data => {
        swal('En proceso',data.description,'info')
    })
}