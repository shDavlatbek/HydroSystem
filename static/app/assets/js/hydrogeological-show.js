/// <reference path="../../../../node_modules/@types/jquery/index.d.ts" />
// Function to get CSRF cookie value

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function fillPasportData(well){
  console.log(well);
  $.each(['well_number', 'organization', 'station', 'type', 
          'region', 'district', 'address', 'location', 'created_at'], function(index, field){
    if (well[field]){
      $('#'+field).html(well[field])
    }
  })
  $.each(['lat_degree', 'lat_minute', 'lat_second',
    'lon_degree', 'lon_minute', 'lon_second',
    'x', 'y'
  ], function(index, field){
    if (well.coordinate[field]){
      $('#'+field).val(well.coordinate[field])
    }
  })
}

$(document).ready(function () {

  var stationSelect = $(".station_select");

  var wellSelect = $(".well_select");
  stationSelect.empty().append('<option value="">---------</option>');
  wellSelect.empty();

  $.ajax({
    url: "/hydrogeological/station/",
    method: "GET",
    success: function (response) {
      var stations = response.stations;

      $.each(stations, function (index, station) {
        $.ajax({
          url: "/hydrogeological/station-well/",
          method: "GET",
          data: {
            station_id: station.id,
          },
          success: function (response) {
            if (response.wells) {
              var option = $("<option></option>")
                .attr("value", station.id)
                .text(station.name + " (" + response.wells.length + ")");
              stationSelect.append(option);
            } else {
              var option = $("<option></option>")
                .attr("value", station.id)
                .text(station.name + " (0)");
              stationSelect.append(option);
            }
          },
          error: function (response) {
            var option = $("<option></option>")
              .attr("value", station.id)
              .text(station.name + " (0)");
            stationSelect.append(option);
          },
        });
      });
    },
    error: function (response) {
      alert("Failed to load stations");
    },
  });

  stationSelect.on("change", function () {
    var stationId = $(this).val();

    if (stationId && !$(this).hasClass("single-selection")) {
      $.ajax({
        url: "/hydrogeological/station-well/",
        method: "GET",
        data: {
          station_id: stationId,
        },
        success: function (response) {
          var wells = response.wells;
          wellSelect.empty();
          wellSelect.append('<option value="">---------</option>');
          if (wells) {
            wells.forEach(function (well) {
              var option = $("<option></option>").attr("value", well.id).text(well.well_number);
              wellSelect.append(option);
            });
          }
        },
        error: function (response) {
          console.error("Failed to load wells");
        },
      });
    } else {
      wellSelect.empty();
    }
  });

  wellSelect.on('change', function () {
    var wellId = $(this).val();
    if (wellId) {
      $.ajax({
        url: '/hydrogeological/show/pasport/',
        method: 'POST',
        data: {
          well_id: wellId
        },
        beforeSend: function (xhr, settings) {
          showLoading();
          xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        },
        success: function (response) {
          hideLoading();
          if (response.success) {
            var well = response.well;
            fillPasportData(well);
            $('.wrapper').css('visibility', 'visible')
          }else{
            alert(response.message);
          }
          
        },
        error: function (response) {
          hideLoading();
          alert('Failed to load well data');
          console.error('Failed to load well data');
        }
      });
    }
  });
});
