var data = source.data;
var filetext=source.column_names.toString().concat('\n')

nb_lines=data[source.column_names[0]].length;
for (i=0; i < nb_lines; i++) {
   var currRow="";
   for(j=0; j< source.column_names.length-1;j++){
        currRow=currRow.concat( data[source.column_names[j]][i].toString()).concat(",");
   }
   currRow=currRow.concat(data[source.column_names[source.column_names.length-1]][i].toString()).concat('\n');
   filetext = filetext.concat(currRow);
}

var filename = 'result.csv';
var blob = new Blob([filetext], { type: 'text/csv;charset=utf-8;' });

//addresses IE
if (navigator.msSaveBlob) {
    navigator.msSaveBlob(blob, filename);
}

else {
    var link = document.createElement("a");
    link = document.createElement('a')
    link.href = URL.createObjectURL(blob);
    link.download = filename
    link.target = "_blank";
    link.style.visibility = 'hidden';
    link.dispatchEvent(new MouseEvent('click'))
}
