// Generated by CoffeeScript 1.4.0
(function() {
  var dragging, otherX, otherY, upload, x, y;

  $('#file').change(function() {
    return $('#form').submit();
  });



  $('#lolimage, #lolimage1').click(function() {
    $('#form').attr('action', '/changeprofile');
    return $('#file').click();
  });


  $('#save_thumbnail_edit').click(function() {
    location.reload(true);
  });


  $('#set_as_profile_pic').click(function() {
      picid = $('#myModal .active img').attr('picid');
      return $.get('/setprofilepic/'+picid, function(response){
        location.reload(true);
      });
  });


  dragging = false;

  x = 0;

  y = 0;

  otherX = 0;

  otherY = 0;

  $('#user_pic_placeholder').mousedown(function(e) {
    var _ref;
      x = e.pageX;
      y = e.pageY;
      _ref = $(this).css('background-position').split(' '), otherX = _ref[0], otherY = _ref[1];
      return dragging = true;
  });

  $('body').mouseup(function() {
    var tempX, tempY, _ref;
    if (dragging) {
      dragging = false;
      _ref = $('#user_pic_placeholder').css('background-position').split(' '), otherX = _ref[0], otherY = _ref[1];
      tempX = parseInt(otherX.slice(0, +(otherX.length - 2) + 1 || 9e9));
      tempY = parseInt(otherY.slice(0, +(otherY.length - 2) + 1 || 9e9));
      return $.post('/changebgpos', {
        x: tempX,
        y: tempY
      });
    }
  });

  $('#user_pic_placeholder').mousemove(function(e) {
    var tempY;
    if (dragging) {
      upload = false;
      tempY = parseInt(otherY.slice(0, +(otherY.length - 2) + 1 || 9e9));
      if (tempY + (e.pageY - y) < 0) {
        return $(this).css('background-position', otherX + ' ' + (tempY + (e.pageY - y)) + 'px');
      }
    }
  });




}).call(this);