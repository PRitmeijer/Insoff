$('#assetSelect').selectpicker();
document.getElementById('startDate').valueAsDate = new Date(
                                                    new Date().getFullYear(),
                                                    new Date().getMonth() - 2, 
                                                    new Date().getDate()
                                                  );
document.getElementById('endDate').valueAsDate = new Date();
var assetInput = $("#assetSelect").val(),
startDateInput = document.getElementById('startDate').valueAsDate,
endDateInput = document.getElementById('endDate').valueAsDate,
scopeInput = document.getElementById('scopeSelect').value;
dataInput = document.querySelector('input[name="dataOptions"]:checked').value;
updateData();

function onChangeSettings(e){
  var id = e.target.id,
  value = e.target.value,
  valueAsDate = e.target.valueAsDate;
  if (id && (value || valueAsDate)){
    switch(id){
      case 'assetSelect':
        if (assetInput != value){
          assetInput = value;
          updateData();
        }
        break;
      case 'startDate':
        if (startDateInput != valueAsDate){
          startDateInput = valueAsDate;
          updateData();
        }
        break;
      case 'endDate':
        if (endDateInput != valueAsDate){
          endDateInput = valueAsDate;
          updateData();
        }
        break;
      case 'scopeSelect':
        if (scopeInput != value){
          scopeInput = value;
          updateData();
        }
        break;
      default:
        if (dataInput != value){
          dataInput = value;
          updateData();
        }
        break;
    }
  }
}

function get_data(){
  return $.ajax({
      type: "POST",
      url: "{% url 'api_raw_data' %}", 
      data: {
        'csrfmiddlewaretoken': '{{csrf_token}}',
        'from_date': startDateInput.toJSON(),
        'to_date': endDateInput.toJSON(),
        'asset':assetInput,
        'scope':scopeInput,
        'pricedata':dataInput
      },
      success : function(data) {
        console.log(data)
        return data
      }
  });
}

function updateData(){
  if (assetInput && startDateInput && endDateInput && scopeInput && dataInput){
    console.log('compleet');
    get_data().then(function(results){
      console.log(results)
      var graph_data = results.results;
      correctSettings(results.start, results.end)
      drawBarGraph(graph_data, "myChartBar");
    });
  }
}

function correctSettings(start, end){
  start = new Date(start)
  end = new Date(end)
  if (startDateInput != start){
    document.getElementById('startDate').valueAsDate = start
    
  }
  if (endDateInput != end){
    document.getElementById('endDate').valueAsDate = end;
  }
}

function drawBarGraph(data, id) {
  var labels = data.map(a => a.date);
  var chartdata = data.map(a => a.amount);
  var ctx = document.getElementById(id).getContext('2d');
  var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        data: chartdata,
        backgroundColor: [
          'rgba(201, 0, 118, 0.2)',
          'rgba(201, 0, 118, 0.2)',
          'rgba(201, 0, 118, 0.2)',
          'rgba(201, 0, 118, 0.2)',
          'rgba(201, 0, 118, 0.2)',
          'rgba(201, 0, 118, 0.2)',
          'rgba(201, 0, 118, 0.2)'
        ],
        borderColor: [
          'rgba(201, 0, 118, 1)',
          'rgba(201, 0, 118, 1)',
          'rgba(201, 0, 118, 1)',
          'rgba(201, 0, 118, 1)',
          'rgba(201, 0, 118, 1)',
          'rgba(201, 0, 118, 1)',
          'rgba(201, 0, 118, 1)'
        ],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true
          }
        }]
      },
      legend: {
        display: false
      }
    }
  });
}