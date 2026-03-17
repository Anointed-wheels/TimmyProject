const fileInput = document.getElementById("csvFile");
const fileName = document.getElementById("fileName");

if(fileInput){

fileInput.addEventListener("change",function(){

    if(this.files.length > 0){

        fileName.textContent =
        "Selected file: " + this.files[0].name;

    }

});

}