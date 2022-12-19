//Variables decleration
var assetList = [];

var investmentLineGraph = undefined;
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
document.getElementById('purchaseAmount').value = 50;
document.getElementById('periodInput').value = 6;
document.getElementById('endDate').valueAsDate = new Date();

var assetListDiv = $(".assets-selected")[0],
assetSelector = document.getElementById('assetSelect'),
assetInput = [],
purchaseAmountInput = document.getElementById('purchaseAmount').value,
intervalInput = document.getElementById('intervalSelect').value;
periodInput = document.getElementById('periodInput').value;
periodScopeInput = document.getElementById('periodSelect').value;
endDateInput = document.getElementById('endDate').valueAsDate,
startDateInput = null,
dataInput = 'A';

updateStartDate();
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
  if (assetInput && purchaseAmountInput && startDateInput && endDateInput && intervalInput && dataInput){
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

    var asset = {id:value, name:name, indexColor:indexColor, assetColor:assetColor};
    assetList.push(asset);

    updateAssetData(asset);
  }
}

function removeAsset(assetElement, id){
  assetListDiv.removeChild(assetElement);
  assetList = assetList.filter(a => a.id != id);
  removeChartData(investmentLineGraph, id);
  removeChartData(historyLineGraph, id);
  removeTableData(id)
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
        if (investmentLineGraph != undefined && !reload){
          addChartData(investmentLineGraph, asset.id, asset.name, assetBackgroundColors[asset.indexColor], assetColors[asset.indexColor], results.results.map(a => a.amount));
        }
        else {
          drawInvestmentGraph(asset, results.results, "resultsChart");
        }
        if (historyLineGraph != undefined && !reload){
          addChartData(historyLineGraph, asset.id, asset.name, assetBackgroundColors[asset.indexColor], assetColors[asset.indexColor], results.raw_data.map(a => a.amount));
        }
        else {
          drawHistoricGraph(asset, results.raw_data, "dataUsedChart");
        }
        updateTableData(asset, results)
      }
    });
  }
}

function updateStartDate(){
  switch(periodScopeInput){
    case '1':
      startDateInput = new Date(
        endDateInput.getFullYear(),
        endDateInput.getMonth(),
        endDateInput.getDate() - (7 * periodInput)
      );
      break;
    case '2':
      startDateInput = new Date(
        endDateInput.getFullYear(),
        endDateInput.getMonth() - periodInput,
        endDateInput.getDate()
      );
      break;
    case '3':
      startDateInput = new Date(
        endDateInput.getFullYear() - periodInput,
        endDateInput.getMonth(),
        endDateInput.getDate()
      );
      break;
  }
  console.log(startDateInput)  
}

//SETTINGS
function onChangeSettings(onChangeObject){
  var id = onChangeObject.id,
  value = onChangeObject.value,
  valueAsDate = onChangeObject.valueAsDate;
  if (id && (value || valueAsDate)){
    switch(id){
      case 'purchaseAmount':
        if (purchaseAmountInput != value){
          purchaseAmountInput = value;
          updateAssetListData();
        }
        break;
      case 'periodInput':
        if (periodInput != value){
          periodInput = value;
          updateStartDate();
          updateAssetListData();
        }
        break;
      case 'periodSelect':
        if (periodScopeInput != value){
          periodScopeInput = value;
          updateStartDate()
          updateAssetListData();
        }
        break;
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
      case 'intervalSelect':
        if (intervalInput != value){
          intervalInput = value;
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
  end = new Date(end)
  end = new Date(end.getTime() - (end.getTimezoneOffset() * 60000))
  if (endDateInput != end){
    endDateInput = end;
    document.getElementById('endDate').valueAsDate = end;
  }
}

//CHART JS
function drawHistoricGraph(asset, data, id){
  var labels = data.map(a => a.date);
  var chartdata = data.map(a => a.amount);
  var ctx = document.getElementById(id).getContext('2d');
  if(historyLineGraph != undefined){
    historyLineGraph.destroy();
  }
  historyLineGraph = drawLineGraph(ctx, labels, chartdata, asset)
}

function drawInvestmentGraph(asset, data, id){
  var labels = data.map(a => a.date);
  var chartdata = data.map(a => a.amount);
  var ctx = document.getElementById(id).getContext('2d');
  if(investmentLineGraph != undefined){
    investmentLineGraph.destroy();
  }
  investmentLineGraph = drawLineGraph(ctx, labels, chartdata, asset)
}

function drawLineGraph(ctx, labels, chartdata, asset){
  return new Chart(ctx ,{
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        id: asset.id,
        label: asset.name,
        data: chartdata,
        backgroundColor: assetBackgroundColors[asset.indexColor],
        fill: false,
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
    fill: false,
    borderWidth: 1,
    data: data
  });
  chart.update();
}

function removeChartData(chart, id){
  chart.data.datasets = chart.data.datasets.filter(a => a.id != id);
  chart.update()
}

//Tables
function addTableData(asset, data) {
  $('#asset-stat-table > tbody:last-child').append(`
    <tr id='${asset.id}' style="background-color:${assetBackgroundColors[asset.indexColor]}">
      <th scope="row" style="color:${assetColors[asset.indexColor]}">${asset.name}</th>
      <td>${data.total_amount}</td>
      <td>${data.total_invested}</td>
      <td>${data.total_value}</td>
      <td>${data.percent_change}%</td>
    </tr>
  `);
}

function updateTableData(asset, data){
  var existing_row = $(`#${asset.id}`);
  if(existing_row.length !== 0){
    var cols = existing_row.children();
    cols[1].innerHTML = data.total_amount;
    cols[2].innerHTML = data.total_invested;
    cols[3].innerHTML = data.total_value;
    cols[4].innerHTML = data.percent_change;
  } else {
    addTableData(asset, data);
  }
}
function removeTableData(id) {
  $(`#${id}`).remove();
}