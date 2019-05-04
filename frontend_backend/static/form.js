$(document).ready(function(){

  $('form').on('submit', function(event){
    var my_data= new FormData();
    my_data.append('url' ,$('#url_input' ).val());
    my_data.append('file' ,$("#file_input").prop('files')[0]);
    $('#errorAlert').hide();
    $('#out_img').hide();
    $('#in_img').hide();
    $('#in_label').hide();
    $('#out_label').hide();
    $('#loader').show();
    $('#loader_label').show();
    $('#file_input').val(null);
    $('#url_input').val(null);

    //console.log($("#file_input").prop('files')[0]);
    //for (var pair of my_data.entries()) {
    //  console.log(pair[0]+ ', ' + pair[1]);
    //}
    $.ajax({
      data: my_data,
      type: 'POST',
      url: '/output',
      contentType: false,
      processData: false,
      cache: false
    })
    .done(function(data) {
      $('#loader').hide();
      $('#loader_label').hide();
      if(data.error){
        $('#errorAlert').text(data.error).show()
      }
      else{
        $('#out_label').show();
        $('#in_label').show();
        $('#out_img').attr("src", data.img_path +"?t="+ new Date().getTime()).attr("style", "margin-left:auto;margin-right:auto;display:block;max-width:450px;");
        $('#in_img').attr("src", data.input_path +"?t="+ new Date().getTime()).attr("style", "margin-left:auto;margin-right:auto;display:block;max-width:450px;")
      }
    });
    event.preventDefault();
  });

  // Initialize Tooltip
  $('[data-toggle="tooltip"]').tooltip();

  // Add smooth scrolling to all links in navbar + footer link
  $(".navbar a, footer a[href='#myPage']").on('click', function(event) {

    // Make sure this.hash has a value before overriding default behavior
    if (this.hash !== "") {

      // Prevent default anchor click behavior
      event.preventDefault();

      // Store hash
      var hash = this.hash;

      // Using jQuery's animate() method to add smooth page scroll
      // The optional number (900) specifies the number of milliseconds it takes to scroll to the specified area
      $('html, body').animate({
        scrollTop: $(hash).offset().top
      }, 900, function(){

        // Add hash (#) to URL when done scrolling (default click behavior)
        window.location.hash = hash;
      });
    } // End if
  });
});
