function showSearchForm() {
    var search_form = document.getElementById("search-form");
    var display_val = search_form.style.display;
    if (!display_val || display_val == "none"){
        search_form.style.display = "block";
    }else{
        search_form.style.display = "none";
    }
}