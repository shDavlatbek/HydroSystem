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

function addAllTimeData(response) {
  console.log(response);
  $.each(['all_time_min', 'all_time_max', 'all_time_avg', 
    'all_time_variance', 'all_time_std_dev', 'all_time_cv'], function (index, field) {
      
    if (response[field]) {
      $("#" + field).html(response[field]);
    }
  });
  $('#oneyear').val(response['start_year']);
  $('#secondyear').val(response['end_year']);
}

function downloadImage(response, filename) {
  var blob = new Blob([response]);
  var url = URL.createObjectURL(blob);
  $('#blobImageModal .modal-body img').attr('src', url)
  $('#blobImageModal .modal-footer a').attr('href', url)
  $('#blobImageModal .modal-footer a').attr('download', filename)
  // var a = document.createElement('a');
  var myModal = new bootstrap.Modal(document.getElementById('blobImageModal'));
  myModal.show();
  // a.href = url;
  // a.download = filename;
  // document.body.appendChild(a);
  // a.click();
  // document.body.removeChild(a);
  // URL.revokeObjectURL(url);
}

function addRowsToTable(data) {
  var tbody = $(".water_level_table tbody");
  // Clear existing rows except the first one
  // tbody.find('tr:not(:first)').remove();
  // Loop through JSON data and append rows to the table
  tbody.empty();
  $('.buttons-overlay').css('z-index', '-1')
  $.each(data, function (index, row) {
    // Check if the row contains only empty strings
    if (!Object.values(row).every((value) => value === "")) {
      var newRow = "<tr>";
      for (var key in row) {
        if (row.hasOwnProperty(key)) {
          if (row[key] === null || row[key] === "") {
            newRow += "<td></td>";
          } else {
            try {
              if (Number.isInteger(row[key])) {
                newRow += "<td>" + row[key] + "</td>";
              } else {
                newRow += "<td>" + parseFloat(row[key].toFixed(2)).toString() + "</td>";
              }
            } catch (error) {
              newRow += "<td>" + row[key] + "</td>";
            }
          }
        }
      }
      newRow += "</tr>";
      tbody.append(newRow);
    }
  });
}

$(document).ready(function () {
  var stationSelect = $(".station_select");

  var wellSelect = $(".well_select");
  stationSelect.empty();
  stationSelect.append('<option value="">---------</option>');
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

  wellSelect.on("change", function () {
    var wellId = $(this).val();
    if (wellId) {
      $.ajax({
        url: "/hydrogeological/show/water-level/",
        method: "POST",
        
        data: {
          well_id: wellId,
        },
        beforeSend: function (xhr, settings) {
          showLoading();
          xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        },
        success: function (response) {
          hideLoading();
          if (response.success) {
            addRowsToTable(response.data);
            $("#start_year").val(response.start_year);
            $("#end_year").val(response.end_year);
            $("#start_month").val(response.start_month);
            $("#end_month").val(response.end_month);
            $(".fullscreen-btn").css('visibility', 'visible');
            localStorage.setItem("filteredData", JSON.stringify(response.filtered_df));
            addAllTimeData(response);
            // $('.wrapper').css('visibility', 'visible')
          } else {
            alert(response.message);
          }
        },
        error: function (response) {
          hideLoading();
          alert("Failed to load well data");
          console.error("Failed to load well data");
        },
      });
    }
  });

  $("#filter-button").on("click", function () {
    var wellId = wellSelect.val();
    if (wellId) {
      $.ajax({
        url: "/hydrogeological/show/water-level/",
        method: "POST",
        data: {
          well_id: wellId,
          start_year: $("#start_year").val(),
          end_year: $("#end_year").val(),
          start_month: $("#start_month").val(),
          end_month: $("#end_month").val(),
        },
        beforeSend: function (xhr, settings) {
          showLoading();
          xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        },
        success: function (response) {
          hideLoading();
          if (response.success) {
            addRowsToTable(response.data);
            addAllTimeData(response);
            localStorage.setItem("filteredData", JSON.stringify(response.filtered_df));
          } else {
            alert(response.message);
          }
        },
        error: function (response) {
          hideLoading();
          console.log(response);
          alert("Failed to load well data");
          addRowsToTable([]);
        },
      });
    }
  });

  $('#fullscreenBtn').on('click', function() {
    var tableClone = $('.water_level_table').clone();
    tableClone.find('tbody').css('height', '100%');
    tableClone.find('thead').css('width', '100%');
    $('#modalBody').empty().append(tableClone);
    var myModal = new bootstrap.Modal(document.getElementById('fullscreenModal'));
    myModal.show();
  });

  $('#heatmap').on('click', function(){
    $.ajax({
      type: 'POST',
      url: '/hydrogeological/show/water-level/heatmap',  // Replace with your actual URL
      data: {data:localStorage.getItem('filteredData')},
      xhrFields: {
        responseType: 'blob'  // This is crucial for handling binary data
      },
      beforeSend: function (xhr, settings) {
        showLoading();
        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
      },
      success: function(response) {
          hideLoading();
          if(response.success == 'error'){
            alert(response.message);
          }else{
            downloadImage(response, 'heatmap.png');
          }
      },
      error: function(xhr, status, error) {
        hideLoading();
          console.error('AJAX Error:', status, error);
      }
  });
  })

  $('#graphOneYear').on('click', function(){
    $.ajax({
      type: 'POST',
      url: '/hydrogeological/show/water-level/one-year',  // Replace with your actual URL
      data: {
        data:localStorage.getItem('filteredData'),
        year:$('#oneyear').val(),
        well_id:wellSelect.val()
      },
      xhrFields: {
        responseType: 'blob'  // This is crucial for handling binary data
      },
      beforeSend: function (xhr, settings) {
        showLoading();
        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
      },
      success: function(response, status, xhr) {
          // Function to handle the response
          hideLoading();
          if(response.success == 'error'){
            alert(response.message);
          }else{
            const filename = xhr.getResponseHeader('Content-Disposition').split('filename=')[1].replace(/\"/g, '');
            downloadImage(response, filename);
          }
      },
      error: function(xhr, status, error) {
        hideLoading();
          console.error('AJAX Error:', status, error);
      }
  });
  })


  $('#graphCompare').on('click', function(){
    $.ajax({
      type: 'POST',
      url: '/hydrogeological/show/water-level/compare-year',  // Replace with your actual URL
      data: {
        data:localStorage.getItem('filteredData'),
        year:$('#oneyear').val(),
        compare_year:$('#secondyear').val(),
        well_id:wellSelect.val()
      },
      xhrFields: {
        responseType: 'blob'  // This is crucial for handling binary data
      },
      beforeSend: function (xhr, settings) {
        showLoading();
        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
      },
      success: function(response, status, xhr) {
          // Function to handle the response
          hideLoading();
          if(response.success == 'error'){
            alert(response.message);
          }else{
            const filename = xhr.getResponseHeader('Content-Disposition').split('filename=')[1].replace(/\"/g, '');
            downloadImage(response, filename);
          }
      },
      error: function(xhr, status, error) {
        hideLoading();
          console.error('AJAX Error:', status, error);
      }
  });
  })

});
