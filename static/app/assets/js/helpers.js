function addRowsToTable(data) {
    const tbody = $(".water_level_table tbody");
    // const tbody = $(className);
    const numColumns = Object.keys(data[0]).length - 1;

    data.forEach(row => {
        if (Object.values(row).some(value => value !== "")) {
            const cells = Object.values(row)
                .slice(0, numColumns)
                .map(value => `<td><input type="number" class="form-control" value="${value || ''}"></td>`)
                .join('');
            
            const newRow = `<tr>${cells}<td><button type="button" class="btn btn-danger" onclick="deleteTR(this)"><i class="bi bi-trash"></i></button></td></tr>`;
            tbody.append(newRow);
        }
    });
}

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
