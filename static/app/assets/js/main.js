/**
* Template Name: NiceAdmin
* Template URL: https://bootstrapmade.com/nice-admin-bootstrap-admin-html-template/
* Updated: Apr 20 2024 with Bootstrap v5.3.3
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/

(function() {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    if (all) {
      select(el, all).forEach(e => e.addEventListener(type, listener))
    } else {
      select(el, all).addEventListener(type, listener)
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Sidebar toggle
   */
  if (select('.toggle-sidebar-btn')) {
    on('click', '.toggle-sidebar-btn', function(e) {
      select('body').classList.toggle('toggle-sidebar')
    })
  }

  /**
   * Search bar toggle
   */
  if (select('.search-bar-toggle')) {
    on('click', '.search-bar-toggle', function(e) {
      select('.search-bar').classList.toggle('search-bar-show')
    })
  }

  /**
   * Navbar links active state on scroll
   */
  let navbarlinks = select('#navbar .scrollto', true)
  const navbarlinksActive = () => {
    let position = window.scrollY + 200
    navbarlinks.forEach(navbarlink => {
      if (!navbarlink.hash) return
      let section = select(navbarlink.hash)
      if (!section) return
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        navbarlink.classList.add('active')
      } else {
        navbarlink.classList.remove('active')
      }
    })
  }
  window.addEventListener('load', navbarlinksActive)
  onscroll(document, navbarlinksActive)

  /**
   * Toggle .header-scrolled class to #header when page is scrolled
   */
  let selectHeader = select('#header')
  if (selectHeader) {
    const headerScrolled = () => {
      if (window.scrollY > 100) {
        selectHeader.classList.add('header-scrolled')
      } else {
        selectHeader.classList.remove('header-scrolled')
      }
    }
    window.addEventListener('load', headerScrolled)
    onscroll(document, headerScrolled)
  }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  /**
   * Initiate tooltips
   */
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  })

  /**
   * Initiate quill editors
   */
  if (select('.quill-editor-default')) {
    new Quill('.quill-editor-default', {
      theme: 'snow'
    });
  }

  if (select('.quill-editor-bubble')) {
    new Quill('.quill-editor-bubble', {
      theme: 'bubble'
    });
  }

  if (select('.quill-editor-full')) {
    new Quill(".quill-editor-full", {
      modules: {
        toolbar: [
          [{
            font: []
          }, {
            size: []
          }],
          ["bold", "italic", "underline", "strike"],
          [{
              color: []
            },
            {
              background: []
            }
          ],
          [{
              script: "super"
            },
            {
              script: "sub"
            }
          ],
          [{
              list: "ordered"
            },
            {
              list: "bullet"
            },
            {
              indent: "-1"
            },
            {
              indent: "+1"
            }
          ],
          ["direction", {
            align: []
          }],
          ["link", "image", "video"],
          ["clean"]
        ]
      },
      theme: "snow"
    });
  }


  /**
   * Initiate Bootstrap validation check
   */
  var needsValidation = document.querySelectorAll('.needs-validation')

  Array.prototype.slice.call(needsValidation)
    .forEach(function(form) {
      form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })

  /**
   * Initiate Datatables
   */
  const datatables = select('.datatable', true)
  datatables.forEach(datatable => {
    new simpleDatatables.DataTable(datatable, {
      perPageSelect: [5, 10, 15, ["All", -1]],
      
    });
  })

  /**
   * Autoresize echart charts
   */
  const mainContainer = select('#main');
  if (mainContainer) {
    setTimeout(() => {
      new ResizeObserver(function() {
        select('.echart', true).forEach(getEchart => {
          echarts.getInstanceByDom(getEchart).resize();
        })
      }).observe(mainContainer);
    }, 200);
  }

})();

$(document).ready(function () {
  // Load regions on page load
  var regionSelect = $(".region_select");

  var districtSelect = $(".district_select");
  
  if ($(document).has(regionSelect).length || $(document).has(districtSelect).length) {
    console.log('There are regionSelect or districtSelect');
    districtSelect.empty();
    districtSelect.append('<option value="">---------</option>');
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
    $(".region_select").on('change', function () {
      var regionId = $(this).val();

      if (regionId && !$(this).hasClass("single-selection")) {
        $.ajax({
          url: "/common/districts/",
          method: "GET",
          data: {
            region_id: regionId,
          },
          success: function (response) {
            var districts = response.districts;
            districtSelect.empty();
            districtSelect.append('<option value="">---------</option>');
            districts.forEach(function (district) {
              var option = $("<option></option>").attr("value", district.id).text(district.name);
              districtSelect.append(option);
            });
          },
          error: function (response) {
            console.error("Failed to load districts");
          },
        });
      }
    });
  }
  $('#hydrogeologicalPasportModal').on('shown.bs.modal', ()=> {
    const formData = new FormData(document.getElementsByTagName('form')[1]);
    const formDataObject = {};
    formData.forEach((val, key) => {
        let select = document.getElementsByName(key)[0];
        if (select.type === 'select-one') {
          formDataObject[key] = select.options[select.selectedIndex].text
        }else{
          formDataObject[key] = val;
        }
    })
    // show as html
    $('#hydrogeologicalPasportModal .modal-body table.well tbody tr').empty().append(
      `<td>${formDataObject.organization}</td>
      <td>${formDataObject.station}</td>
      <td>${formDataObject.well_number}</td>
      <td>${formDataObject.type}</td>
      <td>${formDataObject.region}</td>
      <td>${formDataObject.district}</td>
      <td>${formDataObject.address}</td>
      <td>${formDataObject.location}</td>
      <td>${formDataObject.created_at}</td>`
    )
    $('#hydrogeologicalPasportModal .modal-body table.coordinate tbody tr').empty().append(
      `<td>${formDataObject.well_number}</td>
      <td>${formDataObject.lat_degree}</td>
      <td>${formDataObject.lat_minute}</td>
      <td>${formDataObject.lat_second}</td>
      <td>${formDataObject.lon_degree}</td>
      <td>${formDataObject.lon_minute}</td>
      <td>${formDataObject.lon_second}</td>
      <td>${formDataObject.x}</td>
      <td>${formDataObject.y}</td>`
    )
  })

  $('#hydromelioraticalPasportModal').on('shown.bs.modal', ()=> {
    const formData = new FormData(document.getElementsByTagName('form')[1]);
    const formDataObject = {};
    formData.forEach((val, key) => {
        let select = document.getElementsByName(key)[0];
        if (select.type === 'select-one') {
          formDataObject[key] = select.options[select.selectedIndex].text
        }else{
          formDataObject[key] = val;
        }
    })
    // show as html
    $('#hydromelioraticalPasportModal .modal-body table.well tbody tr').empty().append(
      `<td>${formDataObject.organization}</td>
      <td>${formDataObject.expedicion}</td>
      <td>${formDataObject.well_number}</td>
      <td>${formDataObject.type}</td>
      <td>${formDataObject.region}</td>
      <td>${formDataObject.district}</td>
      <td>${formDataObject.address}</td>
      <td>${formDataObject.location}</td>
      <td>${formDataObject.created_at}</td>`
    )
    $('#hydromelioraticalPasportModal .modal-body table.coordinate tbody tr').empty().append(
      `<td>${formDataObject.well_number}</td>
      <td>${formDataObject.lat_degree}</td>
      <td>${formDataObject.lat_minute}</td>
      <td>${formDataObject.lat_second}</td>
      <td>${formDataObject.lon_degree}</td>
      <td>${formDataObject.lon_minute}</td>
      <td>${formDataObject.lon_second}</td>
      <td>${formDataObject.x}</td>
      <td>${formDataObject.y}</td>`
    )
  })
});

function addModal(row) {
  const modalDiv = document.createElement('div');
    modalDiv.classList.add('modal', 'fade');
    modalDiv.id = 'deleteTRModal';
    modalDiv.tabIndex = '-1';
    modalDiv.role = 'dialog';
    modalDiv.setAttribute('aria-labelledby', 'deleteTRModalLabel');
    modalDiv.setAttribute('aria-hidden', 'true');

    const modalDialog = document.createElement('div');
    modalDialog.classList.add('modal-dialog', 'modal-dialog-centered', 'modal-custom');
    modalDialog.role = 'document';

    const modalContent = document.createElement('div');
    modalContent.classList.add('modal-content');
    
    // Добавляем заголовок, тело и кнопки в модальное окно
    modalContent.innerHTML = `
        <div class="modal-header">
        <h1 class="modal-title fs-5" id="deleteTRModalLabel">O'chirishni tasdiqlang</h1>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body" aria-disabled="true" tabindex="-1">
        <table class="table table-bordered mb-0">
          <thead class="table-light sticky-top">
            <tr>
              <th scope="col">Yil</th>
              <th scope="col">I</th>
              <th scope="col">II</th>
              <th scope="col">III</th>
              <th scope="col">IV</th>
              <th scope="col">V</th>
              <th scope="col">VI</th>
              <th scope="col">VII</th>
              <th scope="col">VIII</th>
              <th scope="col">IX</th>
              <th scope="col">X</th>
              <th scope="col">XI</th>
              <th scope="col">XII</th>
            </tr>
          </thead>
          <tbody>
            ${row.innerHTML}
          </tbody>
        </table>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Yopish</button>
        <button type="button" class="btn btn-primary" type='button' onclick="confirmDelete()">Tasdiqlash</button>
      </div>
    `;

    // Добавляем модальное окно на страницу
    modalDialog.appendChild(modalContent);
    modalDiv.appendChild(modalDialog);
    document.body.appendChild(modalDiv);
    $(modalContent).find('td:last').remove()
    $(modalContent).find('td').each(function(){
      let value = $(this).find('input').val()
      console.log(this);
      console.log(value);
      $(this).find('input').remove()
      $(this).text(value)
    })
}

function deleteTR(e) {
  const row = e.closest('tr');
  $('#deleteTRModal').remove();
  addModal(row)
  console.log(row)
  $('#deleteTRModal').modal('show');
  $('#deleteTRModal').data('row', row);
}

function confirmDelete() {
  // Получаем сохраненную ссылку на строку
  const row = $('#deleteTRModal').data('row');
  row.remove();

  // Закрываем модальное окно
  $('#deleteTRModal').modal('hide');
}

  