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
                          <button id="plant_ifo">
                            <img id ="`+data[i]["identified_img"]+`" width=100 >
                          </button>
                          <div id="data">
                            <p id="identified_date">identified_date :`+ data[i]["identified_date"]+`</p>
                            <a id="delete_button" value="`+[data[i]["id"],data[i]["account_id"]]+`" onclick="handleClickDelete(this)">🗑️</a>
                          </div>
                        </div>`
                var temp = document.getElementById('history_container');
              $("#history_container").prepend(x);
              console.log("1234")
            }
            
        }
    }
    $(document).ready(function () {
        $.getJSON("/history/data", function (data) {

            createbox(data);
      })
    });