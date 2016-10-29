function onSelectCard(e) {
  var img = document.getElementById(e.target.id + 'img');
  img.src = '/static/cards/' + e.target.value + '.jpg';
}
$(':radio').change(
  function(){
    console.log("Changed rating to ", this.value);
    $('#rating-form > input[name="rating"]').attr('value', this.value);
    $('#rating-form').submit();
  }
)
