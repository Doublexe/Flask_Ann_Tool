var active_box;


$(".box").each(function () {
  $.data(this, 'value', {
    'id':this.id,
    'skip': '1',
    'size': '#meddium',
  });
});



$(".box").on('click', function() {
  if (active_box) {
    $('#'+active_box).toggleClass('box_active');
  };
  active_box = $.data(this, 'value').id;
  $("#camera_func>b").text(active_box);
  $("#camera_func").removeClass('none');
  $('#'+active_box).toggleClass('box_active');
  $('#skip').val($.data(this, 'value').skip);
  $($.data(this, 'value').size).trigger('click');
})

$('#skip').on('change', function () {
  var skip_str = this.value;
  var skip = parseInt(this.value);
  $.data($('#'+active_box)[0], 'value').skip = skip_str;
  $('#'+active_box+">.img").removeClass('kill');
  $('#'+active_box+">.img").each(
    function (idx) {
      if (idx%skip!=0) {
        if ($("#"+this.id.split('.').join("\\.")).hasClass('bg-success')
            ||
            $("#"+this.id.split('.').join("\\.")).hasClass('bg-warning')
            ||
            $("#"+this.id.split('.').join("\\.")).hasClass('bg-secondary')
          ) {
          // skip
        } else {
          $("#"+this.id.split('.').join("\\.")).addClass('kill');
        }
      };
    }
  );

});
