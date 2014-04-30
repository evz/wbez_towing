(function(){
    var grid_layer;
    var jenks_cutoffs;
    var map = L.map('map').fitBounds([[41.644286009999995, -87.94010087999999], [42.023134979999995, -87.52366115999999]]);
    L.tileLayer('https://{s}.tiles.mapbox.com/v3/ericvanzanten.map-3ofkoxuh/{z}/{x}/{y}.png', {
        attribution: '<a href="http://www.mapbox.com/about/maps/" target="_blank">Terms &amp; Feedback</a>'
    }).addTo(map);
    var legend = L.control({position: 'bottomleft'});
    legend.onAdd = function(map){
        var div = L.DomUtil.create('div', 'legend')
        var labels = [];
        var from;
        var to;
        $.each(jenks_cutoffs, function(i, grade){
            from = grade
            to = jenks_cutoffs[i + 1];
            labels.push('<i style="background:' + getColor(from) + '"></i>' +
                       from + (to ? '&ndash;' + to : '+'));
        });
        div.innerHTML = '<div><strong>' + grid_data['human_name'] + '</strong><br />' + labels.join('<br />') + '</div>';
        return div
    }
    var map_colors = [
        '#deebf7',
        '#c6dbef',
        '#9ecae1',
        '#6baed6',
        '#4292c6',
        '#2171b5',
        '#084594'
    ]
    var dataDir = 'data/finished_files/'
    var data = {
        key: '2012/towing_year_500m.geojson',
        resolution: 0.01,
        groupBy: 'month'
    }
    loadLayer(dataDir + data['key'])
    function loadLayer(path){
        $.when($.getJSON(path)).then(
            function(grid){
                $('#map').spin(false);
                var values = [];
                $.each(grid['features'], function(i, val){
                    values.push(val['properties']['TOW_COUNT']);
                });
                try{legend.removeFrom(map);}catch(e){};
                if (typeof grid_layer !== 'undefined'){
                    map.removeLayer(grid_layer);
                }
                if (values.length > 0){
                    jenks_cutoffs = jenks(values, 6);
                    jenks_cutoffs[0] = 0;
                    jenks_cutoffs.pop();
                    grid_layer = L.geoJson(grid, {
                        pointToLayer: function(feature, latlng){
                            var res = data['resolution'] / 2;
                            var sw = [latlng.lat + res, latlng.lng - res]
                            var ne = [latlng.lat - res, latlng.lng + res]
                            var style = styleGrid(feature)
                            return  L.rectangle([sw, ne], style);
                        },
                        onEachFeature: function(feature, layer){
                            var content = '<h4>Count: ' + feature.properties['TOW_COUNT'] + '</h4>';
                            layer.bindLabel(content);
                        }
                    }).addTo(map);
                }
            }
        );
    }
    function getColor(d){
        return d >= jenks_cutoffs[5] ? map_colors[6] :
               d >= jenks_cutoffs[4] ? map_colors[5] :
               d >= jenks_cutoffs[3] ? map_colors[4] :
               d >= jenks_cutoffs[2] ? map_colors[3] :
               d >= jenks_cutoffs[1] ? map_colors[2] :
               d >= jenks_cutoffs[0] ? map_colors[1] :
                                       map_colors[0];
    }

    function styleGrid(feature){
        return {
            fillColor: getColor(feature.properties['TOW_COUNT']),
            weight: 0.3,
            opacity: 1,
            color: 'white',
            fillOpacity: 0.7
        };
    }
})()
