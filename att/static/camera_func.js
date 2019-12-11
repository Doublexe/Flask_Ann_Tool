var active_box;


$(".box").each(function () {
  $.data(this, 'value', {
    'id':this.id,
    'skip': 5,
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

  // Back to default settings
  $('#meddium').trigger("click");
  $('#skip').val('5');
  $('#skip').trigger("change");
})

$('#skip').on('change', function () {
  var skip = parseInt(this.value);
  $('#'+active_box+">.img").removeClass('kill');
  $('#'+active_box+">.img").each(
    function (idx) {
      if (idx%skip!=0) {
        if ($("#"+this.id.split('.').join("\\.")).hasClass('bg-success')
            ||
            $("#"+this.id.split('.').join("\\.")).hasClass('bg-warning')) {
          // skip
        } else {
          $("#"+this.id.split('.').join("\\.")).addClass('kill');
        }
      };
    }
  );

});
