$("#rebound").submit(function(e) {
  var url = "/jaundice.py"; // the script where you handle the form input.
	$('#rebound').hide();
  $('#result').show();
  $.ajax({
    type: "POST",
    url: url,
    data: $("#rebound").serialize(), // serializes the form's elements.
    success: function(data)
    {
      $("#result-body").html(data); // show response from the php script.
    }
  });
  e.preventDefault(); // avoid to execute the actual submit of the form.
});
$( document ).ready(function() {
  $("#recalculate").click(function(e) {
    $('#rebound').show();
    $('#result').hide();
    $("#result-body").html('<img src="/loading.svg" class="mx-auto d-block">');
  });
  $("#mols").click(function(e) {
    $("#units").html($(this).html());
    $("#unitCode").val('0');
  });
  $("#mgs").click(function(e) {
    $("#units").html($(this).html());
    $("#unitCode").val('1');
  });
});