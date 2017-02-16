var chart2;

/**
 * Request data from the server, add it to the graph and set a timeout
 * to request again
 */
function requestData2() {
    $.ajax({
        url: '/supply-data',
        success: function(point) {
            var series = chart2.series[0],
                shift = series.data.length > 300; // shift if the series is
                                                 // longer than 20

            // add the point
            chart2.series[0].addPoint(point, true, shift);

            // call it again after one second
            // setTimeout(requestData2, 500);
            return 
        },
        cache: false
    });
}

$(document).ready(function() {
    chart2 = new Highcharts.Chart({
        chart: {
            renderTo: 'supply-container',
            defaultSeriesType: 'scatter',
            events: {
                load: requestData2
            }
        },
        title: {
            text: 'Supply at node 0'
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
            name: 'Node 0',
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