/**
 * Insert Libraries
 */
const libraries = [
    'https://unpkg.com/sweetalert/dist/sweetalert.min.js',
    'js/resources.js'
]
libraries.forEach((l)=>{
    let s = `<script src="${l}"></script>`
    $('body').append(s)
})