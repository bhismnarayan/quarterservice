$(document).ready(function() {
    //$('.form-group').addClass("row");
    
    // $('#id_Repair_type')[0].addEventListener('change', (event) => {
    //     let sequelField = $('#id_sequel').parents('p');
    //     if (event.target.checked) {
    //         sequelField.show();
    //     } else {
    //         sequelField.hide();
    //     }
    // })

    $("#id_Repair_type")[0].addEventListener('change', (event) =>{
        var url = "/myResidenceService/ajax/load-repairSubtype"  // get the url of the `load_cities` view
        var repairId = $(id_Repair_type).val();  // get the selected country ID from the HTML input
    
        $.ajax({                       // initialize an AJAX request
          url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
          data: {
            'Repair': repairId       // add the country id to the GET parameters
          },
          success: function (data) {   
            $("#id_Repair_sub_type").html(data);  
          }
        });
    
      });
})

