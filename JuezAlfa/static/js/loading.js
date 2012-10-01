
var url="http://127.0.0.1:8000/";
$("#formEnvio").submit(function(){
    load();
});
funtion load(){
     var data;
     data = new FormData();
     data.append( 'archivo', $( '#file' )[0].files[0] );
     data.append('concurso',$('#concurso').val());
     data.append('titulo',$('#titulo').val());
     data.append('problema',$('#problema').val());
     $("#load").html("Loader...");
          $.ajax({
              url: url+"judge/concurso/problema/",
              data: data,
              processData: false,
              type: 'POST',
              success: function ( data ) {
                 $("#load").html(data);
               }
          });

}