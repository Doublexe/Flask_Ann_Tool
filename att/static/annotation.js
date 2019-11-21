$(window).on('load', function() {
  window.setInterval(function() {
    var annotation = [];
    $('.img.bg-success').map(function() {
      annotation.push($(this).attr('id'));
    })
    $.ajax({
      url: 'submit',
      dataType: 'json',
      contentType: 'application/json',
      method: 'POST',
      data: JSON.stringify({
        'annotated': annotation,
        'finished': false,
      }),
    });
  }, 7000); /// call your function every n ms
});

$(document).on('click', '#submit', function() {
    var annotation = [];
    $('.img.bg-success').map(function() {
      annotation.push($(this).attr('id'));
    })
    $.ajax({
      url: 'submit',
      dataType: 'json',
      contentType: 'application/json',
      method: 'POST',
      data: JSON.stringify({
        'annotated': annotation,
        'finished': true,
      }),
      success: function (msg) {
        if (msg.status='finished') {
          window.location.reload(false);
          // If we needed to pull the document from
          //  the web-server again (such as where the document contents
          //  change dynamically) we would pass the argument as 'true'.
        }
      }
    });
  }
);


$(document).on('change', '#small', function() {
  $('.img').css('height', '200px');
});

$(document).on('change', '#meddium', function() {
  $('.img').css('height', '300px');
});

$(document).on('change', '#big', function() {
  $('.img').css('height', '400px');
});

$(document).on('change', '#annotated_only', function() {
  $('.img:not(.bg-success)').toggleClass('none');
});

$(document).on('change', '#hover_anchor', function() {
  $('#anchor').toggleClass('none');
});
