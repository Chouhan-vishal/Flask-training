document.getElementById("account-btn").addEventListener("click", function(event) {
    id = event.target.attributes.data.value
    fetch("/", { method: "POST" }); // send a POST request to /my-endpoint
  });
// alert('ok')
// function change_method() {
//     debugger
    
// }