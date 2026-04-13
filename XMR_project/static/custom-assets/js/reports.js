$(document).ready(function () {
  getReportData();
});

$("#site").select2();

function getReportData() {
  var URL = "/sensor-data";
  $.ajax({
    type: "GET",
    url: URL,
    contentType: "text/plain",
    dataType: "json",
    success: function (data) {
      populateDataTable(data["data"], "report_table");
      populateConfigTable(data["configured_data"], "config_data_table");
    },
    error: function (e) {
      console.log("There was an error with your request...");
      console.log("error: " + JSON.stringify(e));
    },
  });
}

function populateDataTable(data, table_id) {
  let columns = [];
  $.each(data[0], function (name, value) {
    var column = {
      data: name,
      title: name,
    };
    columns.push(column);
  });

  $("#" + table_id).DataTable({
    columns: columns,
    data: data,
    aLengthMenu: [
      [20, 50, 100, -1],
      [20, 50, 100, "All"],
    ],
    fnRowCallback: function (nRow, aData, iDisplayIndex) {
      // Bind click event
      $(nRow).click(function () {
        alert("You clicked on " + aData.name + "'s row");
      });
      return nRow;
    },
  });
}

function populateConfigTable(data, table_id) {
  $('#device_config_table').empty();

  var $tbody = $("<tbody>");
  for (let key in data) {
    let $headerCols = $("<tr>");

    $headerCols.append(
      $("<td>", {
        text: key,
        class: 'text-capitalize'
      })
    );

    $headerCols.append(
      $("<td>", {
        text: data[key],
      })
    );
    $tbody.append($headerCols);
  }
  $tbody.appendTo('#device_config_table');
}
