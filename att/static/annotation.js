var FLOCK = false;
var annotated_mode = false;


$.fn.removeClassRegExp = function (regexp) {
            if(regexp && (typeof regexp==='string' || typeof regexp==='object')) {
                regexp = typeof regexp === 'string' ? regexp = new RegExp(regexp) : regexp;
                $(this).each(function () {
                    $(this).removeClass(function(i,c) {
                        var classes = [];
                        $.each(c.split(' '), function(i,c) {
                            if(regexp.test(c)) { classes.push(c); }
                        });
                        return classes.join(' ');
                    });
                });
            }
            return this;
};


$('#record_selected').on('change', function() {
  var record = $('#record_selected')[0].value;
  var fn = $('#record_selected>#select_'+record);
  if (fn.hasClass('bg-success')) {
    $('#record_selected').addClass('bg-success').removeClass('bg-light');
  } else {
    $('#record_selected').removeClass('bg-success').addClass('bg-light');
  }
  window.location.href = "./"+record;
});



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
  if ($(this).hasClass('bg-warning')||$(this).hasClass('bg-secondary')) {
      $(this).toggleClass('bg-warning');
      $(this).toggleClass('bg-secondary');
    if (annotated_mode) {
      $(this).toggleClass('item');
      $(this).toggleClass('none');
    };
  } else {
    $(this).toggleClass('bg-success');
    if (annotated_mode) {
      $(this).toggleClass('item');
      $(this).toggleClass('none');
    };
  }
});


$(document).on('click', '#small', function() {
  var active = $("#camera_func>b").text();
  $("#"+active+'>.img').css('height', '100px');
});

$(document).on('click', '#meddium', function() {
  var active = $("#camera_func>b").text();
  $("#"+active+'>.img').css('height', '200px');
});

$(document).on('click', '#big', function() {
  var active = $("#camera_func>b").text();
  $("#"+active+'>.img').css('height', '300px');
});

$(document).on('change', '#annotated_only', function() {
  $('.img:not(.bg-success,.bg-warning)').toggleClass('none');
  $('.img:not(.bg-success,.bg-warning)').toggleClass('item');
  if (annotated_mode) {
    annotated_mode = false;
  } else {
    annotated_mode = true;
  }
});

$(document).on('change', '#hover_anchor', function() {
  $('#anchor').toggleClass('none');
});
