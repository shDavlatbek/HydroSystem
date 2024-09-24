$(document).ready(function () {
    $("input[name=import-file-input]").change(function () {
        var formData = new FormData();
        formData.append("files", this.files[0]);

        $.ajax({
            type: "POST",
            url: "/import/",
            data: formData,
            processData: false,
            contentType: false,
            beforeSend: function (xhr, settings) {
                showLoading();
                xhr.setRequestHeader("X-CSRFToken", document.querySelector("input[name=csrfmiddlewaretoken]").value);
            },
            success: function (response) {
                hideLoading();
                if (response.status) {
                    addRowsToTable(JSON.parse(response.data));
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
});
