//Variables decleration
var assetList = [];

var bSBar = undefined;
var historyLineGraph = undefined;

var reloadChart = true;

var assetColors = [
  'rgba(201, 0, 118, 1)',
  'rgba(17, 221, 238, 1)',
  'rgba(238, 170, 119, 1)',
];

var assetBackgroundColors = [
  'rgba(201, 0, 118, 0.1)',
  'rgba(17, 221, 238, 0.15)',
  'rgba(238, 170, 119, 0.1)',
];

//Initial setup
document.getElementById('startDate').valueAsDate = new Date(
                                                    new Date().getFullYear(),
                                                    new Date().getMonth() - 2, 
                                                    new Date().getDate()
                                                  );
document.getElementById('endDate').valueAsDate = new Date();

var assetListDiv = $(".assets-selected")[0],
assetSelector = document.getElementById('assetSelect'),
assetInput = [],
startDateInput = document.getElementById('startDate').valueAsDate,
endDateInput = document.getElementById('endDate').valueAsDate,
scopeInput = document.getElementById('scopeSelect').value;
dataInput = document.querySelector('input[name="dataOptions"]:checked').value;

$('#assetSelect').selectpicker();
assetSelector.selectedIndex = 1;
addAsset(assetSelector);

//Color logic
function getColorIndex(){
  var usedIndexes = assetList.map(a => a.indexColor);
  for(var i = 0; i < assetColors.length; i++){
    if(!usedIndexes.includes(i)){
      return i;
    }
  }
  alert("You broke the system! :(");
}

//Input validation
function validateInput(){
  if (assetInput && startDateInput && endDateInput && scopeInput && dataInput){
    return true;
  }
  return false;
}

//Asset Add & Remove
function addAsset(assetObject){
  var value = assetObject.value,
  name = assetObject.options[assetObject.selectedIndex].text;

  $('.selectpicker').selectpicker('val', [0]); 

  if (!assetList.some(a => a.id == value) && assetList.length < 5){
    var indexColor = getColorIndex();
    var assetColor = assetColors[indexColor],
    assetBackgroundColor = assetBackgroundColors[indexColor];

    var newAsset = document.createElement("div");
    newAsset.classList.add("badge", "rounded-pill", "d-flex", "justify-content-between", "align-items-center", "col-12", "col-md-auto", "p-2", "m-1");
    newAsset.style.border = `1px solid ${assetColor}`;
    newAsset.style.color = assetColor;
    newAsset.style.backgroundColor = assetBackgroundColor;
    newAsset.style.textAlign = "center";

    var newAssetText = document.createTextNode(name);
    newAsset.appendChild(newAssetText);

    var newAssetRemoveBtn = document.createElement("a");
    newAssetRemoveBtn.href="javascript:javascript:void(0)";
    newAssetRemoveBtn.onclick = function(){ removeAsset(newAsset, value); };
    newAssetRemoveBtn.classList.add("ms-2","fa", "fa-times");
    newAssetRemoveBtn.style.color = assetColor;
    newAsset.appendChild(newAssetRemoveBtn);

    assetListDiv.appendChild(newAsset);

    var asset = {id:value, name:name, indexColor:indexColor, assetColor:assetColor, assetColor:assetColor};
    assetList.push(asset);

    updateAssetData(asset);
  }
}

function removeAsset(assetElement, id){
  assetListDiv.removeChild(assetElement);
  assetList = assetList.filter(a => a.id != id);
  removeChartData(bSBar,id);
  removeChartData(historyLineGraph, id);
}

function updateAssetListData(){
  reloadChart = true;
  assetList.forEach(function(asset){
      updateAssetData(asset)
    });
}

function getReloadChartBool(){
  if(reloadChart){
    reloadChart = false;
    return true
  }
  else false;
}

function updateAssetData(asset){
  if(validateInput()){
    get_data(asset).then(function(results){
      if (results){
        reload = getReloadChartBool();
        console.log(results)
        correctSettings(results.start, results.end)
        if (bSBar != undefined && !reload){
          addChartData(bSBar, asset.id, asset.name, assetBackgroundColors[asset.indexColor], assetColors[asset.indexColor], results.results.map(a => a.amount));
        }
        else {
          drawBSBarGraph(asset, results.results, "resultsChart");
        }
        if (historyLineGraph != undefined && !reload){
          addChartData(historyLineGraph, asset.id, asset.name, assetBackgroundColors[asset.indexColor], assetColors[asset.indexColor], results.raw_data.map(a => a.amount));
        }
        else {
          drawHistoryLineGraph(asset, results.raw_data, "dataUsedChart");
        }
      }
    });
  }
}

//SETTINGS
function onChangeSettings(onChangeObject){
  var id = onChangeObject.id,
  value = onChangeObject.value,
  valueAsDate = onChangeObject.valueAsDate;
  if (id && (value || valueAsDate)){
    switch(id){
      case 'startDate':
        if (startDateInput != valueAsDate){
          startDateInput = valueAsDate;
          updateAssetListData();
        }
        break;
      case 'endDate':
        if (endDateInput != valueAsDate){
          endDateInput = valueAsDate;
          updateAssetListData();
        }
        break;
      case 'scopeSelect':
        if (scopeInput != value){
          scopeInput = value;
          if(scopeInput == 1){
            $("#day-select").show();
          }
          else{
            $("#day-select").hide();
          }
          updateAssetListData();
        }
        break;
      default:
        if (dataInput != value){
          dataInput = value;
          updateAssetListData();
        }
        break;
    }
  }
}

function correctSettings(start, end){
  start = new Date(start)
  start = new Date(start.getTime() - (start.getTimezoneOffset() * 60000))
  end = new Date(end)
  end = new Date(end.getTime() - (end.getTimezoneOffset() * 60000))
  if (startDateInput != start){
    startDateInput = start;
    document.getElementById('startDate').valueAsDate = start;
    
  }
  if (endDateInput != end){
    endDateInput = end;
    document.getElementById('endDate').valueAsDate = end;
  }
}

//CHART JS
function drawBSBarGraph(asset, data, id) {
  var labels = data.map(a => a.date);
  var chartdata = data.map(a => a.amount);
  var ctx = document.getElementById(id).getContext('2d');
  if(bSBar != undefined){
    bSBar.destroy();
  }
  bSBar = new Chart(ctx ,{
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        id: asset.id,
        label: asset.name,
        data: chartdata,
        backgroundColor: assetBackgroundColors[asset.indexColor],
        borderColor: assetColors[asset.indexColor],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
    }
  });
}

function drawHistoryLineGraph(asset, data, id){
  var labels = data.map(a => a.date);
  var chartdata = data.map(a => a.amount);
  var ctx = document.getElementById(id).getContext('2d');
  if(historyLineGraph != undefined){
    historyLineGraph.destroy();
  }
  historyLineGraph = new Chart(ctx ,{
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        id: asset.id,
        label: asset.name,
        data: chartdata,
        backgroundColor: assetBackgroundColors[asset.indexColor],
        borderColor: assetColors[asset.indexColor],
        pointBackgroundColor: 'rgba(201, 0, 118, 1)',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
    },
  });
}

function addChartData(chart, id, label, backgroundcolor, color, data) {
  chart.data.datasets.push({
    id: id,
    label: label,
    backgroundColor: backgroundcolor,
    borderColor: color,
    borderWidth: 1,
    data: data
  });
  chart.update();
}

function removeChartData(chart, id){
  chart.data.datasets = chart.data.datasets.filter(a => a.id != id);
  chart.update()
}
