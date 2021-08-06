// Show photo
function showPhoto() {
  fields = document.querySelectorAll("input[type=file]");
  for (var i=0; i<fields.length; i++) {
    if (fields[i].accept.indexOf("image")>-1) fields[i].onchange = function () {
      var src = URL.createObjectURL(this.files[0]);
      document.getElementById('id_show_image').src = src;
    }
  }
}
