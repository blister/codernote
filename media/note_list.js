$(document).ready(function() {
    create_notes(displayed, "#list");
    $(".sort").change(sort_changed);
    $(".filter").change(filter_changed);
    
  });
