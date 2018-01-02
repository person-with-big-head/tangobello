function showSearchForm() {
    var search_form = document.getElementById("search-form");
    var display_val = search_form.style.display;
    if (!display_val || display_val == "none"){
        search_form.style.display = "block";
    }else{
        search_form.style.display = "none";
    }
}


function initFooter(){

  var ftBg = jQuery('#ft-tg-bg');
  var hideTimeout;
  var activeTimeout;
  jQuery('#footer-tags a').each(function(i,e){
     var lnk = jQuery(e);
     var lnkWidth = lnk.width();
     var lnkHalfWidth = lnkWidth * 0.5;

     lnk.mouseenter(function(e){
       ftBg.css({
           'width': lnk.outerWidth() - 2,
           'height' : lnk.outerHeight() - 2,
           'top' : lnk.position().top,
           'left' : lnk.position().left + 5 }
       );
       ftBg.addClass('active');
       clearTimeout(hideTimeout);

     });

     lnk.mouseleave(function(e){

       hideTimeout = setTimeout(function(){
        ftBg.removeClass('active');
       }, 300 );
     });

  });
}

$( function(){
    initFooter();
});

