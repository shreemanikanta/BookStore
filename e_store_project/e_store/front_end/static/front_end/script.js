$(document).ready(function() {
    $.ajax({
        type: "GET",
        url: "/session_token/",
        dataType: "json",
        success: function(response) {
            if (response.access_token) {
                sessionStorage.setItem('access_token', response.access_token);
                console.log('Access token stored in session storage');
            } else {
                console.log('Error: ' + response.error);
            }
        },
        error: function(textStatus, errorThrown) {
            console.log('AJAX request failed: ' + textStatus + ', ' + errorThrown);
        }
    });
    
      $('#submit_form').click(function(event) {
        event.preventDefault();
        var access_token = sessionStorage.getItem('access_token')
        var formdata = new FormData();
        var image = $('#image')[0].files[0];
        if (image) {
          formdata.append('image', image);
        }
        formdata.append('title', $('#title').val());
        formdata.append('description', $('#description').val());
        formdata.append('author', $('#author').val());
        formdata.append('quantity', $('#quantity').val());
        formdata.append('price', $('#price').val());
        formdata.append('language', $('#language').val());

        
        $.ajax({
          processData: false,
          contentType: false,
          method: 'POST',
          url: `/e_store/add_book/`,
          data: formdata,
          headers: {'Authorization': 'Bearer ' + access_token},
          success: function(response) {
            alert('Book Added successfully');
            window.location.href="/home_page/"
  
          },
          error: function(response) {
            window.location.href="http://127.0.0.1:8002/add_book/"
              var errorMessage = "Error Adding book.";
              if (response && response.responseText) {
                  errorMessage += "\n" + response.responseText;
              }
              console.log(errorMessage);
              alert(errorMessage);
          }
        });
      });
    });