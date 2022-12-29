function searchCriteriaCollection(inputids) {
    var result = {};
    $("input.form-control").each(function (index) {
        var key = $(this).attr('id')
        if (typeof key === "undefined") {
            return
        }
        key = key.slice(3,key.length)

         //avoid empty shadowed parameters
         if($(this).val() != ''){
            result[key] = $(this).val();
         }
    });
	console.log(result)
    return result;
}
