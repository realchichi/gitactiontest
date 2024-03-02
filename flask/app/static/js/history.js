
function handleClickDelete(element) {
      var value = element.getAttribute("value");
      value = value.split(",")
      let data = {"id":value[0] , "account_id":value[1]}
      if (!confirm("Delete " + "sure" + '?')) {
      return false;
    }
    // console.log(value)
      $.post("/delete/history", data, function (data_his) {
        location.reload()
      });
      
}
function createbox(data){
    for(let i=0;i<data.length;i++){
        if(!(data[i]["removed_date"])){
            console.log(data[i])
            var x ='<div class="col-3" id="box_add_history">' +
            '<div class="card">' +
                '<button id="plant_ifo" class="card-img-top">' +
                    '<img id="identified_img" src="' + data[i]["identified_img"].slice(4) + '" max-width="100" onclick="redirectToResult(this)">' +
                '</button>' +
                '<div id="data" class="card-body">' +
                    '<p id="identified_date" class="card-text">Identified date :<br>'+ data[i]["identified_date"] + '</p>' +
                    '<a id="delete_button" class="btn" value="' + [data[i]["id"], data[i]["account_id"]] + '" onclick="handleClickDelete(this)"><i class="fa-solid fa-trash-can"></a>' +
                '</div>' +
            '</div>' +
        '</div>';
        $("#history_container").append(x);
        }
        
    }
}
$(document).ready(function () {
    $.getJSON("/history/data", function (data) {

        createbox(data);
  })
});


function redirectToResult(element){
  var val = element.getAttribute("src");
  var plant_data = (val.split("/")[3]).split(".")[0]
  window.location.href = "/result?plant_data=" + encodeURIComponent(plant_data);

}