window.onload = function () {
  var container = document.getElementById('cov-img');
  var img = new Image();
  img.src = 'static/images/bg2.jpg';
  img.onload = function () {
    var containerWidth = container.offsetWidth;
    var imageRatio = img.width / img.height;
    var containerHeight = containerWidth / imageRatio;

    if (containerHeight > 800) { // Max height set in CSS
      containerHeight = 800;
    }

    container.style.height = containerHeight + 'px';
  };
};