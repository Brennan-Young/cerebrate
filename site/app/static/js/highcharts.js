var chart;

/**
 * Request data from the server, add it to the graph and set a timeout
 * to request again
 */
function requestData() {
    $.ajax({
        url: '/live-data',
        success: function(point) {
            var series = chart.series[0],
                shift = series.data.length > 100; // shift if the series is
                                                 // longer than 20

            // add the point
            chart.series[0].addPoint(point, true, shift);
            requestData2();
            // call it again after one second
            setTimeout(requestData, 25);

        },
        cache: false
    });
}

$(document).ready(function() {
    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'data-container',
            defaultSeriesType: 'scatter',
            events: {
                load: requestData
            }
        },
        title: {
            text: 'Requests at Node 0 over the previous 2 seconds'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 50,
            maxZoom: 20 * 10000
            // title: {
            //     text: 'Time',
            //     margin: 80
            // }
            // minRange = 100000
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'Requests',
                margin: 80
            }
        },
        series: [{
            name: 'Node 0',
            data: []
        }],

        rangeSelector: {
        buttons: [{
            count: 1,
            type: 'minute',
            text: '1M'
        }, {
            count: 5,
            type: 'minute',
            text: '5M'
        }, {
            type: 'all',
            text: 'All'
        }],
        inputEnabled: false,
        selected: 0
        }
    });
});