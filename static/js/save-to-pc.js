function SaveToPC(){
	var table = tableToJson($('#print')[0]);
	var doc = new jsPDF('l','pt','letter',true);

	$.each(table, function(i, row){
		$.each(row, function(j,cell){
			if(j=="No telephone" || j==3){
				doc.cell(20,20,120,25,cell,i);
			}else if(j=="Montant" || j==5){
				doc.cell(20,20,80,25,cell,i);
			}else if(j=="Membership expire" || j==6){
				doc.cell(20,20,150,25,cell,i);
			}else{
				doc.cell(20,20,100,25,cell,i);
			}
	
		});
	});

	doc.save('resultat-recherche.pdf');
}

function tableToJson(table) {
    var data = [];

    var headers = [];
    for (var i=0; i<table.rows[0].cells.length; i++) {
        headers[i] = table.rows[0].cells[i].innerHTML;
    }
    
	data.push(headers);

    for (var i=1; i<table.rows.length; i++) {

        var tableRow = table.rows[i];
        var rowData = {};

        for (var j=0; j<tableRow.cells.length; j++) {

            rowData[ headers[j] ] = tableRow.cells[j].innerHTML;

        }

        data.push(rowData);
    }       

    return data;
}

function beforeToday(d, m, y){
	var date = new Date();
	var mydate = new Date(y,m,d);
	var reponse = "";
	if (mydate.getTime() > date.getTime()){
		reponse = "Non";
	} else {
		reponse = "Oui";
	}

return reponse;
}

function beforeTodayEN(d, m, y){
	var date = new Date();
	var mydate = new Date(y,m,d);
	var reponse = "";
	if (mydate.getTime() > date.getTime()){
		reponse = "No";
	} else {
		reponse = "Yes";
	}

return reponse;
}