function SaveToPC(){
	var table = tableToJson($('#print')[0]);
	var doc = new jsPDF('l','pt','letter',true);

	$.each(table, function(i, row){
		$.each(row, function(j,cell){
			if(j=="No membre" || j=="Member id" || j==0){
				member_id=cell;
			}else if(j=="Nom" || j=="First name" || j==1){
				member_f_name="";
				height_f_name=1;
				while(cell.length>10){
					member_f_name += cell.substring(0,10)+"\n";
					cell = cell.substring(11);
					++height_f_name;
				}
				member_f_name += cell;
			}else if(j=="Prénom" || j=="Last name" || j==2){
				member_l_name="";
				height_l_name=1;
				while(cell.length>10){
					member_l_name += cell.substring(0,10)+"\n";
					cell = cell.substring(11);
					++height_l_name;
				}
				member_l_name += cell;
			}else if(j=="No telephone" || j=="Phone number" || j==3){
				member_tel=cell;
			}else if(j=="Dernier don" || j=="Last donation" || j==4){
				member_date_don=cell;
			}else if(j=="Montant" || j=="Amount" || j==5){
				member_montant_don=cell;
			}else if(j=="Membership expire" || j=="Membership expired" || j==6){
				member_expire=cell;
			}
	
		});
		if(height_f_name>height_l_name){
			height=height_f_name*25;
		}else{
			height=height_l_name*25;
		}
		doc.cell(20,20,100,height,member_id,i);
		doc.cell(20,20,100,height,member_f_name,i);
		doc.cell(20,20,100,height,member_l_name,i);
		doc.cell(20,20,120,height,member_tel,i);
		doc.cell(20,20,100,height,member_date_don,i);
		doc.cell(20,20,80,height,member_montant_don,i);
		doc.cell(20,20,150,height,member_expire,i);
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
	var reponse = true;
	if (mydate.getTime() > date.getTime()){
		reponse = false;
	}
    return reponse;
}
