$(document).ready(function () {
    $("div[data-includeHTML]").each(function () {                
        $(this).load($(this).attr("data-includeHTML"));
    });
});