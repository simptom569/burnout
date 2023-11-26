const pk = document.getElementById('pk').innerHTML;
var frequencyData = [];
var volumeData = [];
var settingData = [];
var commitFrequencyData = [];
var commitIntensityData = [];
var commitTask_statusData = [];
var commitPriority_changesData = [];
var commitDuration_activityyData = [];
var commitActivity_nightData = [];

$.ajax({
    url: pk,
    type: 'GET',
    success: function(html){
        data_7_days = html.data_7_days;
        average_data = html.average_data;
        console.log(average_data);
        for (var date in data_7_days) {
            if (data_7_days.hasOwnProperty(date)) {
                var entry = data_7_days[date];
                frequencyData.push(entry.frequencyData);
                volumeData.push(entry.volumeData);
                settingData.push(entry.settingData);
                commitFrequencyData.push(entry.commitFrequencyData);
                commitIntensityData.push(entry.commitIntensityData);
                commitTask_statusData.push(entry.commitTask_statusData);
                commitPriority_changesData.push(entry.commitPriority_changesData);
                commitDuration_activityyData.push(entry.commitDuration_activityyData);
                commitActivity_nightData.push(entry.commitActivity_nightData);
            }
        }
        
        AVG_frequencyData = average_data.frequencyData;
        AVG_volumeData = average_data.volumeData;
        AVG_settingData = average_data.settingData;
        AVG_commitFrequencyData = average_data.commitFrequencyData;
        AVG_commitIntensityData = average_data.commitIntensityData;
        AVG_commitTask_statusData = average_data.commitTask_statusData;
        AVG_commitPriority_changesData = average_data.commitPriority_changesData;
        AVG_commitDuration_activityyData = average_data.commitDuration_activityyData;
        AVG_commitActivity_nightData = average_data.commitActivity_nightData;

        createGraph('frequencyGraph', 'Частота сообщения', frequencyData, AVG_frequencyData);
        createGraph('volumeGraph', 'Объем сообщения', volumeData, AVG_volumeData);
        createGraph('settingGraph', 'Настрой сообщения', settingData, AVG_settingData);
        createGraph('commitFrequencyGraph', 'Регулярность коммитов', commitFrequencyData, AVG_commitFrequencyData);
        createGraph('commitIntensityGraph', 'Интенсивность коммитов', commitIntensityData, AVG_commitIntensityData);
        createGraph('taskStatusGraph', 'Статус задачи', commitTask_statusData, AVG_commitTask_statusData);
        createGraph('priorityChangesGraph', 'Приоритетные изменения', commitPriority_changesData, AVG_commitPriority_changesData);
        createGraph('activityDurationGraph', 'Продолжительность активности', commitDuration_activityyData, AVG_commitDuration_activityyData);
        createGraph('nightActivityGraph', 'Активность ночью', commitActivity_nightData, AVG_commitActivity_nightData);
  }
})


function createGraph(graphId, label, data, horizontalLineValue) {
  var graphContainer = document.getElementById(graphId);
  var canvas = graphContainer.querySelector('canvas');
  var ctx = canvas.getContext('2d');

  var minDataValue = Math.min(...data);
  var maxDataValue = Math.max(...data);

  var yAxisMin = Math.min(minDataValue, horizontalLineValue)-5;
  var yAxisMax = Math.max(maxDataValue, horizontalLineValue)+5;

  canvas.width = canvas.clientWidth * 1.5;
  canvas.height = 200;

  var gradientBlueToRed = ctx.createLinearGradient(0, 0, 0, canvas.height);
  gradientBlueToRed.addColorStop(0, 'orange');
  gradientBlueToRed.addColorStop(1, 'red');

  var gradientBlackToGray = ctx.createLinearGradient(0, 0, 0, canvas.height);
  gradientBlackToGray.addColorStop(0, 'black');
  gradientBlackToGray.addColorStop(1, 'gray');

  var graph = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7'],
      datasets: [{
        label: label,
        data: data,
        borderColor: gradientBlueToRed,
        backgroundColor: 'rgba(255, 165, 0, 0.06)', // Градиент с прозрачностью 80%
        borderWidth: 2,
        fill: 'start',
        tension: 0.4
      },
      {
        label: 'Среднее значение',
        data: Array(data.length).fill(horizontalLineValue),
        borderColor: gradientBlackToGray,
        borderWidth: 2,
        borderDash: [5, 5],
        fill: false
      }]
    },
    options: {
      responsive: false,
      maintainAspectRatio: false,
      layout: {
        padding: {
          left: 5, // Регулировка отступа слева
          right: 20, // Регулировка отступа справа
          top: 20, // Регулировка отступа сверху
          bottom: 15 // Регулировка отступа снизу
        }
      },
      scales: {
        y: {
          min: yAxisMin,
          max: yAxisMax,
          beginAtZero: false
        },
        x: {
          grid: {
            color: 'rgba(0, 0, 0, 0.02)' // Цвет вертикальных линий сетки с прозрачностью 20%
          }
        }
      },
      elements: {
        point: {
          radius: 0,
          hitRadius: 10,
          hoverRadius: 5
        }
      },
      plugins: {
        legend: {
          display: false
        }
      }
    }
  });

  canvas.addEventListener('mouseover', function () {
    // Подсветка canvas при наведении
    canvas.style.boxShadow = '0 0 10px rgba(255, 165, 0, 0.8)';
    canvas.style.transition = 'box-shadow 0.3s ease-in-out';
  });

  canvas.addEventListener('mouseout', function () {
    // Убираем подсветку при уходе курсора
    canvas.style.boxShadow = 'none';
  });

  // Помечаем каждую точку на графике
  var points = graphContainer.querySelectorAll('.chartjs-line .chartjs-point');
  points.forEach(function (point, index) {
    point.setAttribute('data-point', true);
    // Добавляем атрибут для точек на горизонтальной линии
    if (data[index] === horizontalLineValue) {
      point.setAttribute('data-horizontal-line', true);
    }
  });
}
