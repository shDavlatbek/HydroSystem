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
  
  $(document).ready(function () {
    // EXCEL
    // $("#excel_file").change(function () {
    //   var formData = new FormData();
    //   formData.append("files", $("#excel_file")[0].files[0]);
  
    //   $.ajax({
    //     type: "POST",
    //     url: "/hydromelioratical/import/", // URL to your Django view for file upload
    //     data: formData,
    //     processData: false,
    //     contentType: false,
    //     beforeSend: function (xhr, settings) {
    //       showLoading();
    //       xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    //     },
    //     success: function (response) {
    //       hideLoading();
    //       if (response.status === "success") {
    //         addRowsToTable(JSON.parse(response.data));
    //       } else {
    //         alert("Failed to process file: " + response.error_message);
    //       }
    //     },
    //     error: function (xhr, status, error) {
    //       hideLoading();
    //       alert("Error uploading file: " + error);
    //     },
    //   });
    // });
  
    $("#water_level_table_form").on("submit", function (event) {
      event.preventDefault(); // Prevent default form submission
  
      // Extract data from the table
      // var data = [];
      // $('.water_level_table tbody tr').each(function() {
      //     var rowData = [];
      //     $(this).find('td input').each(function() {
      //         rowData.push($(this).val());
      //     });
      //     data.push(rowData);
      // });
      var table = document.querySelector(".water_level_table");
      var rows = table.querySelectorAll("tbody tr");
      var hydropost = Number(document.querySelector("select[name=hydropost]").value);
      var region = Number(document.querySelector("select[name=region]").value);
      var type = Number(document.querySelector("select[name=object_type]").value);
      var mode = Number(document.querySelector("select[name=mode]").value);
      var data = [];
  
      rows.forEach((row) => {
        var inputs = row.querySelectorAll("input");
        var rowData = {
          hydropost: hydropost,
          region: region,
          object_type: type,
          mode: mode,
          year: inputs[0].value,
          I: inputs[1].value,
          II: inputs[2].value,
          III: inputs[3].value,
          IV: inputs[4].value,
          V: inputs[5].value,
          VI: inputs[6].value,
          VII: inputs[7].value,
          VIII: inputs[8].value,
          IX: inputs[9].value,
          X: inputs[10].value,
          XI: inputs[11].value,
          XII: inputs[12].value,
        };
        data.push(rowData);
      });
      // Send data to the server
      $.ajax({
        type: "POST",
        url: "/hydrometeorological/hydrometria/", // Replace with your backend endpoint
        data: { data: JSON.stringify(data) },
        beforeSend: function (xhr, settings) {
          showLoading();
          xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        },
        success: function (response) {
          hideLoading();
          window.location.reload();
          // Optionally, redirect to a success page or perform additional actions
        },
        error: function (error) {
          hideLoading();
          alert("Error submitting data");
        },
      });
    });
    // END EXCEl
  
    // expedicion, WELL SELECTION
    var expedicionSelect = $(".expedicion_select");
    var wellSelect = $(".well_select");
  
    expedicionSelect.empty().append('<option value="">---------</option>');
    wellSelect.empty();
  
    $.ajax({
      url: "/hydromelioratical/expedicion/",
      method: "GET",
    })
      .done(function (response) {
        var expedicionRequests = response.expedicions.map(function (expedicion) {
          return $.ajax({
            url: "/hydromelioratical/expedicion-well/",
            method: "GET",
            data: { expedicion_id: expedicion.id },
          })
            .done(function (wellResponse) {
              var wellCount = wellResponse.wells ? wellResponse.wells.length : 0;
              expedicionSelect.append(
                $("<option></option>")
                  .attr("value", expedicion.id)
                  .text(expedicion.name + " (" + wellCount + ")")
              );
            })
            .fail(function () {
              expedicionSelect.append(
                $("<option></option>")
                  .attr("value", expedicion.id)
                  .text(expedicion.name + " (0)")
              );
            });
        });
  
        $.when.apply($, expedicionRequests).then(function () {
          // This function will be executed after all AJAX requests have completed.
          
        });
      })
      .fail(function () {
        alert("Failed to load expedicions");
      });
  
    expedicionSelect.on("change", function () {
      var expedicionId = $(this).val();
  
      if (expedicionId && !$(this).hasClass("single-selection")) {
        $.ajax({
          url: "/hydromelioratical/expedicion-well/",
          method: "GET",
          data: {
            expedicion_id: expedicionId,
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
    // END expedicion, WELL SELECTION
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
  
  $(document).ready(function () {
    var regionSelect = $(".region_select");
  
    var expedicionSelect = $(".expedicion_select");
  
    if ($(document).has(regionSelect).length && $(document).has(expedicionSelect).length) {
      console.log("There are regionSelect or expedicionSelect");
      expedicionSelect.empty();
      expedicionSelect.append('<option value="">---------</option>');
      regionSelect.empty();
      regionSelect.append('<option value="">---------</option>');
  
      $.ajax({
        url: "/common/regions/",
        method: "GET",
        success: function (response) {
          var regions = response.regions;
  
          $.each(regions, function (index, region) {
            var option = $("<option></option>").attr("value", region.id).text(region.name);
            regionSelect.append(option);
          });
        },
        error: function (response) {
          alert("Failed to load regions");
        },
      });
  
      // Load districts based on selected region
      $(".region_select").on("change", function () {
        var regionId = $(this).val();
  
        if (regionId && $(this).hasClass("expedicion-region-select")) {
          $.ajax({
            url: "/hydromelioratical/region-expedicion",
            method: "GET",
            data: {
              region_id: regionId,
            },
            success: function (response) {
              var expedicions = response.expedicions;
              expedicionSelect.empty();
              expedicions.forEach(function (expedicion) {
                var option = $("<option></option>").attr("value", expedicion.id).text(expedicion.name);
                expedicionSelect.append(option);
              });
            },
            error: function (response) {
              console.error("Failed to load expedicions");
            },
          });
        }
      });
    }
  });
  