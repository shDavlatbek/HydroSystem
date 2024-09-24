

$(document).ready(function () {

  // EXCEL
  $("#excel_file").change(function () {
    var formData = new FormData();
    formData.append("files", $("#excel_file")[0].files[0]);

    $.ajax({
      type: "POST",
      url: "/import/", // URL to your Django view for file upload
      data: formData,
      processData: false,
      contentType: false,
      beforeSend: function (xhr, settings) {
        showLoading();
        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
      },
      success: function (response) {
        hideLoading();
        if (response.status === "success") {
          addRowsToTable(JSON.parse(response.data))
        } else {
          alert("Failed to process file: " + response.error_message);
        }
      },
      error: function (xhr, status, error) {
        hideLoading();
        alert("Error uploading file: " + error);
      },
    });
  });

  $('#water_level_table_form').on('submit', function(event) {
    event.preventDefault();  // Prevent default form submission
    
    // Extract data from the table
    // var data = [];
    // $('.water_level_table tbody tr').each(function() {
    //     var rowData = [];
    //     $(this).find('td input').each(function() {
    //         rowData.push($(this).val());
    //     });
    //     data.push(rowData);
    // });
    var table = document.querySelector('.water_level_table');
    var rows = table.querySelectorAll('tbody tr');
    var well = Number(document.querySelector('.well_select').value);
    var data = [];

    rows.forEach(row => {
        var inputs = row.querySelectorAll('input');
        var rowData = {
            'well': well,
            'year': inputs[0].value,
            'I': inputs[1].value,
            'II': inputs[2].value,
            'III': inputs[3].value,
            'IV': inputs[4].value,
            'V': inputs[5].value,
            'VI': inputs[6].value,
            'VII': inputs[7].value,
            'VIII': inputs[8].value,
            'IX': inputs[9].value,
            'X': inputs[10].value,
            'XI': inputs[11].value,
            'XII': inputs[12].value
        };
        data.push(rowData);
    });
    // Send data to the server
    $.ajax({
        type: 'POST',
        url: '/hydrogeological/water-level/',  // Replace with your backend endpoint
        data: { 'data': JSON.stringify(data) },
        beforeSend: function (xhr, settings) {
          showLoading();
          xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        },
        success: function(response) {
            hideLoading();
            window.location.reload();
            // Optionally, redirect to a success page or perform additional actions
        },
        error: function(error) {
            hideLoading();
            alert('Error submitting data');
        }
    });
  });
  // END EXCEl

  // STATION, WELL SELECTION
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
  // END STATION, WELL SELECTION
  let levelTable = $(".water_level_table");
  // WATER LEVEL TABLE PROCESSING
  $(".add_row").on("click", function () {
    var rowData = [];
    $.each(levelTable.find("tbody tr"), function (index, tr) {
      rowData.push(
        $(tr)
          .find("td input")
          .map(function () {
            return $(this).val();
          })
          .get()
      );
    });
  });

  $(".add_row").on("click", function () {
    levelTable.find("tbody").append(`
    <tr>
      <td><input type="number" name="year" class='form-control'></td>
      <td><input type="number" name="I" class='form-control'></td>
      <td><input type="number" name="II" class='form-control'></td>
      <td><input type="number" name="III" class='form-control'></td>
      <td><input type="number" name="IV" class='form-control'></td>
      <td><input type="number" name="V" class='form-control'></td>
      <td><input type="number" name="VI" class='form-control'></td>
      <td><input type="number" name="VII" class='form-control'></td>
      <td><input type="number" name="VIII" class='form-control'></td>
      <td><input type="number" name="IX" class='form-control'></td>
      <td><input type="number" name="X" class='form-control'></td>
      <td><input type="number" name="XI" class='form-control'></td>
      <td><input type="number" name="XII" class='form-control'></td>
      <td><button type="button" class="btn btn-danger" onclick="deleteTR(this)"><i class="bi bi-trash"></i></button></td>
    </tr>
    `);
    let tableDiv = levelTable.closest(".row")
    $(tableDiv).scrollTop($(tableDiv)[0].scrollHeight);
  });
  // END WATER LEVEL TABLE PROCESSING
});
