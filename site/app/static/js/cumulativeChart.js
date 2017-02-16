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

            // call it again after one second
            setTimeout(requestData, 1000);
        },
        cache: false
    });
}

$(document).ready(function() {
    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'data-container',
            defaultSeriesType: 'spline',
            events: {
                load: requestData
            }
        },
        title: {
            text: 'Demand'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 50,
            maxZoom: 20 * 10000
            // minRange = 100000
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'Value',
                margin: 80
            }
        },
        series: [{
            name: 'hello',
            data: []
        }]

        // rangeSelector: {
        // buttons: [{
        //     count: 1,
        //     type: 'minute',
        //     text: '1M'
        // }, {
        //     count: 5,
        //     type: 'minute',
        //     text: '5M'
        // }, {
        //     type: 'all',
        //     text: 'All'
        // }],
        // inputEnabled: false,
        // selected: 0
        // },
    });
});