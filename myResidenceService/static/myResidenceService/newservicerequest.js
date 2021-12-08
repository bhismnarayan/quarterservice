$(document).ready(function() {
    //$('.form-group').addClass("row");
    
    $('#id_Repair_type')[0].addEventListener('change', (event) => {
        let sequelField = $('#id_sequel').parents('p');
        if (event.target.checked) {
            sequelField.show();
        } else {
            sequelField.hide();
        }
    })
})