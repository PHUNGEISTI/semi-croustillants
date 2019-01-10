
		function createexcel(){

		    var excel = $JExcel.new("Calibri light 10 #333333");			// Default font
			
			// excel.set is the main function to generate content:
			// 		We can use parameter notation excel.set(sheetValue,columnValue,rowValue,cellValue,styleValue) 
			// 		Or object notation excel.set({sheet:sheetValue,column:columnValue,row:rowValue,value:cellValue,style:styleValue })
			// 		null or 0 are used as default values for undefined entries		
			
			excel.set( {sheet:0,value:"Livraisons Demandes Prédictions" } );
		   //excel.addSheet("Sheet 2");	

			
			var evenRow=excel.addStyle ( { 																	
				border: "none,none,none,thin #333333"});													

			var oddRow=excel.addStyle ( { 																	
				fill: "#ECECEC" , 																			
				border: "none,none,none,thin #333333"}); 
			
			
			for (var i=1;i<50;i++) excel.set({row:i,style: i%2==0 ? evenRow: oddRow  });					

 
			var headers=["Semaines","Dernières Demandes","Livraisons Réelles","Prédictions hw","Prédictions rg"];							
			var formatHeader=excel.addStyle ( { 															
					border: "none,none,none,thin #333333", 													
					font: "Calibri 12 #0000AA B"}); 														

			for (var i=0;i<headers.length;i++){																
				excel.set(0,i,0,headers[i],formatHeader);													
				excel.set(0,i,undefined,"auto");															
			}
			
			
			// on remplit l'excel
			var sema = {{sem | tojson}}
			var dem = {{dem | tojson}}
			var livr = {{liv | tojson}}
			var predi = {{pred | tojson}}
			var prevwinter = {{prevwinterr | tojson}}
			
			for (var i=0;i<sema.length;i++){																			
				excel.set(0,0,i+1,sema[i]);																														
				excel.set(0,1,i+1,dem[i][35]);														
				excel.set(0,2,i+1,livr[i]);
				excel.set(0,3,i+1,prevwinter[i]);
				if (i >= livr.length-predi.length) {
					excel.set(0,4,i+1,predi[i-(livr.length-predi.length)]);
				} else {			
					excel.set(0,4,i+1," ");																								
					}
			}
		    excel.generate("Livraisons_Demandes_Prédictions.xlsx");
		}	
	