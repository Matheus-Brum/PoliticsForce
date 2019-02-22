$(function(){
var countryOptions="";
var stateOptions="";
var cityOptions="";
var country="";
	$.getJSON('/static/json/countries1.json',function(result){
		countryOptions += "<option selected='selected'></option>";
		$.each(result, function(i,country) {
			//<option value='countrycode'>contryname</option>
			countryOptions+="<option id='"+country.code+"' " + "value='"
			+country.code+
			"'>"
			+country.name+
			"</option>";
			 $('#country').html(countryOptions);
             $('#city')
                .empty()
			 });
	});
	$("#country").change(function(){
    stateOptions="";
    country = $(this).val();
	if(country=="US"){
            $('#city')
                .empty()
			$.getJSON('/static/json/americanStates.json',function(result){
			$.each(result, function(stateCode,stateName) {
				//<option value='stateCode'>stateName</option>
				stateOptions+="<option id='" + stateCode +"' "+ "value='"
				+stateCode+
				"'>"
				+stateName+
				"</option>";
				 });
				 $('#province').html(stateOptions);
			});
		}
	if(country=="CA"){
            $('#city')
                .empty()
			$.getJSON('/static/json/canadianStates.json',function(result){
			$.each(result, function(stateCode,stateName) {
				//<option value='stateCode'>stateName</option>
				stateOptions+="<option id='" + stateCode +"' "+ "value='"
				+stateCode+
				"'>"
				+stateName+
				"</option>";
				 });
				 $('#province').html(stateOptions);
			});
		}

    if(country != "CA" && country != "US") {
        $('#province')
            .empty()
        $('#city')
            .empty()
    }
	});

	
	$("#province").change(function(){
        cityOptions="";
        var code = $(this).val();
        var state;
        if(country == "US"){
            $.getJSON('/static/json/americanStates.json',function(result){
                state = result[code];
            });
            $.getJSON('/static/json/americanCities.json',function(result){
            $.each(result, function(i,city) {
                //<option value='cityName'>cityName</option>
                $.each(city, function(key, value) {
                    if(i == state) {
                        cityOptions+="<option id='"+value+"' "+ "value='"
                        +value+
                        "'>"
                        +value+
                        "</option>";
                    }
                });
            });
                $('#city').html(cityOptions);
            });
        }
        if(country == "CA") {
            $.getJSON('/static/json/canadianStates.json',function(result){
                state = result[code];
            });
            $.getJSON('/static/json/canadianCities.json',function(result){
            $.each(result, function(i,city) {
                //<option value='cityName'>cityName</option>
                $.each(city, function(key, value) {
                    if(i == state) {
                        cityOptions+="<option id='"+value+"' "+ "value='"
                        +value+
                        "'>"
                        +value+
                        "</option>";
                    }
                });
            });
                $('#city').html(cityOptions);
            });
        }
    });
});
