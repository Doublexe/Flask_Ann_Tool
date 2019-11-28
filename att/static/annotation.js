var FLOCK = false;
var annotated_mode = false;

$(window).on('load', function() {
  window.setInterval(function() {
    if (!FLOCK) {
      var annotation = [];
      $('.img.bg-success').map(function() {
        annotation.push([$(this).parent().attr('id'), $(this).attr('id')]);
      })
      $.ajax({
        url: '/submit',
        dataType: 'json',
        contentType: 'application/json',
        method: 'POST',
        data: JSON.stringify({
          'annotated': annotation,
          'finished': false,
        }),
      });
    }
  }, 10000); /// call your function every n ms
});


$('#record_selected').on('change', function() {
  var record = $('#record_selected')[0].value;
  window.location.href = "./"+record;
});



$(document).on('click', '#submit', function() {
    var annotation = [];
    if (!FLOCK) {
      $('.img.bg-success').map(function() {
        annotation.push([$(this).parent().attr('id'), $(this).attr('id')]);
      })
      $.ajax({
        url: '/submit',
        dataType: 'json',
        contentType: 'application/json',
        method: 'POST',
        data: JSON.stringify({
          'annotated': annotation,
          'finished': false,
        }),
      });
    }
  }
);

// $(document).on('click', '#request', function() {
//     var annotation = [];
//     if (!FLOCK) {
//       FLOCK = true;
//       $('.img.bg-success').map(function() {
//         annotation.push([$(this).parent().attr('id'), $(this).attr('id')]);
//       });
//       $.ajax({
//         url: 'submit',
//         dataType: 'json',
//         contentType: 'application/json',
//         method: 'POST',
//         data: JSON.stringify({
//           'annotated': annotation,
//           'finished': true,
//         }),
//         success: function (msg) {
//           if (msg.status='finished') {
//             window.location.reload(false);
//             // If we needed to pull the document from
//             //  the web-server again (such as where the document contents
//             //  change dynamically) we would pass the argument as 'true'.
//           }
//         }
//       });
//     }
//   }
// );


function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}


$('.horizontal-scroll-wrapper').on('mousewheel DOMMouseScroll', async function(event){

    var delta = Math.max(-1, Math.min(1, (event.originalEvent.wheelDelta || -event.originalEvent.detail)));
    var i = 1;
    while (i<60){
      $(this).scrollLeft( $(this).scrollLeft() - ( delta * 1 ) );
      event.preventDefault();
      i+=1;
      await sleep(4);
    };

});

$(document).on( 'click', '.img', function() {
  $(this).toggleClass('bg-success');
  if (annotated_mode) {
    $(this).toggleClass('item');
    $(this).toggleClass('none');
  };
});


$(document).on('change', '#small', function() {
  var active = $("#camera_func>b").text();
  $("#"+active+'>.img').css('height', '100px');
});

$(document).on('change', '#meddium', function() {
  var active = $("#camera_func>b").text();
  $("#"+active+'>.img').css('height', '200px');
});

$(document).on('change', '#big', function() {
  var active = $("#camera_func>b").text();
  $("#"+active+'>.img').css('height', '300px');
});

$(document).on('change', '#annotated_only', function() {
  $('.img:not(.bg-success)').toggleClass('none');
  $('.img:not(.bg-success)').toggleClass('item');
  if (annotated_mode) {
    annotated_mode = false;
  } else {
    annotated_mode = true;
  }
});

$(document).on('change', '#hover_anchor', function() {
  $('#anchor').toggleClass('none');
});
