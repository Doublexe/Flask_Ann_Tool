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



function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}


$('.horizontal-scroll-wrapper').on('mousewheel DOMMouseScroll', async function(event){

    var delta = Math.max(-1, Math.min(1, (event.originalEvent.wheelDelta || -event.originalEvent.detail)));
    var i = 1;
    while (i<35){
      $(this).scrollLeft( $(this).scrollLeft() - ( delta * 1) );
      event.preventDefault();
      i+=1;
      await sleep(1);
    };

});


function count_annotated (box_id) {
  var count = 0;
  $('#'+box_id+">.img").each(function () {
    if ($(this).hasClass('bg-success')
        ||
        $(this).hasClass('bg-warning')){
          count += 1;
        }
  })
  return count;
}

$(window).on('load', function () {
  $('.box').each(function(){
    if (count_annotated($(this)[0].id)>=3) {
      $(this).addClass('bg-secondary');
    } else {
      if ($(this).hasClass('bg-secondary')) {
        $(this).removeClass('bg-secondary');
      }
    }
  });

  $('.img').each(function(){
      if ($(this).hasClass('bg-warning')||$(this).hasClass('bg-success')) {
        $('#anchor_img').attr('src',$(this)[0].src);
        return false;
      }
  })
})


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

  if (count_annotated($(this).parent()[0].id)>=3) {
    $(this).parent().addClass('bg-secondary');
  } else {
    if ($(this).parent().hasClass('bg-secondary')) {
      $(this).parent().removeClass('bg-secondary');
    }
  }

  $('.img').each(function(){
      if ($(this).hasClass('bg-warning')||$(this).hasClass('bg-success')) {
        $('#anchor_img').attr('src',$(this)[0].src);
        return false;
      }
  })
});


$(document).on('click', '#small', function() {
  var active = $("#camera_func>b").text();
  $("#"+active+'>.img').css('height', '100px');
  $.data($('#'+active)[0], 'value').size = '#small';
});

$(document).on('click', '#meddium', function() {
  var active = $("#camera_func>b").text();
  $("#"+active+'>.img').css('height', '200px');
  $.data($('#'+active)[0], 'value').size = '#meddium';
});

$(document).on('click', '#big', function() {
  var active = $("#camera_func>b").text();
  $("#"+active+'>.img').css('height', '300px');
  $.data($('#'+active)[0], 'value').size = '#big';
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
