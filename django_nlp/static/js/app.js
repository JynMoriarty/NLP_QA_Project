// const dropZone = document.getElementById('pdf');

// dropZone.addEventListener('dragover', function(e) {
//     e.preventDefault();
//     this.classList.add('dragover');
// });

// dropZone.addEventListener('dragleave', function(e) {
//     this.classList.remove('dragover');
// });

// dropZone.addEventListener('drop', function(e) {
//     e.preventDefault();
//     this.classList.remove('dragover');

//     const file = e.dataTransfer.files[0];
    
//     if (file.type == 'application/pdf') {
//         var reader = new FileReader();

//         reader.onload = function(event) {

//             result = event.target.result

//             console.log(result);
//         };

//         reader.readAsDataURL(file);
        
//     } else {
//         alert("Merci d'insérer un fichier pdf");
//     }
// });
