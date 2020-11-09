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
    
})