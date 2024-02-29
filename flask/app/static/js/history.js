
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
            var x =`<div id="box_add_history">
                      <button id="plant_ifo" >
                        <img id='identified_img' src="`+data[i]["identified_img"].slice(4)+`" width=100 onclick="redirectToResult(this)">
                      </button>
                      <div id="data">
                        <p id="identified_date">identified_date :`+ data[i]["identified_date"]+`</p>
                        <a id="delete_button" value="`+[data[i]["id"],data[i]["account_id"]]+`" onclick="handleClickDelete(this)">🗑️</a>
                      </div>
                    </div>`
          $("#history_container").prepend(x);
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