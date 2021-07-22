/* eslint-disable require-jsdoc */
let importData = [];
let matchedColumns = [];
let headers = [];
let sendData = [];

let matchColumns = {};
let touchpointFields = {};

const table = document.getElementById('tbl-csv-data');
const mappingTypeDiv = document.getElementById('select-mapping-type');
const submitBtn = document.getElementById('submit-file');

// eslint-disable-next-line no-unused-vars
function importFile(allFields, allMatchedColumns) {
  refreshUpload();

  if (document.getElementById('upload-csv').files.length == 1) {
    const inputFile = document.getElementById('upload-csv').files[0];
    const report = document.getElementById('report');
    const importContainer = document.getElementById('import-container');

    importContainer.className += ' border-container';
    mappingTypeDiv.style.display = 'block';
    submitBtn.style.display = 'inline-block';

    touchpointFields = allFields;
    matchedColumns = allMatchedColumns;
    report.value = '';

    if (checkCSVFile(inputFile)) importCSV(inputFile);
    else importJSON(inputFile);
  }
}

function importCSV(inputFile) {
  Papa.parse(inputFile, {
    download: true,
    header: true,
    complete: function(results) {
      headers = results.meta.fields;
      importData = results.data;
      generateTable(headers, importData);
    },
  });
}

function generateTable(headerNames, datas) {
  table.innerHTML = '';

  generateTableHead(headerNames, true);

  datas.map((data) => {
    generateTableRows(headerNames, data);
  });
}

function importJSON(inputFile) {
  const reader = new FileReader();
  reader.addEventListener('load', function() {
    const jsonFile = JSON.parse(reader.result);
    if (jsonFile && Array.isArray(jsonFile)) {
      const results = jsonFile;
      const matchCount = generateJSONData(results);

      if (matchCount > 0) {
        const msg = matchCount.toString() + ' object(s) matched';

        generateTableHead(table, keys, keys, false);
        importData.map((data) => {
          generateTableRows(table, keys, data);
        });

        showMessage(msg, 1200);
        submitBtn.style.display = 'inline-block';
      } else alert('No data to import');
    } else alert('Please follow JSON File Format');
  });
  reader.readAsText(inputFile);
}

function checkCSVFile(file) {
  const fileExtension = file.name.split('.').pop();
  if (fileExtension === 'csv') return true;
  return false;
}

function refreshUpload() {
  importData = [];
  matchColumns = {};
  sendData = [];
  headers = [];

  table.innerHTML = '';
  submitBtn.style.display = 'none';
  mappingTypeDiv.style.display = 'none';
}

function generateJSONData(results) {
  results.every((data, index) => {
    let checkAvailable = true;
    const newData = {};

    Object.keys(data).every((field) => {
      if (keys.includes(field)) {
        if (data[field] == null || typeof data[field] !== 'object') {
          newData[field] = data[field];
        } else {
          const msg =
            'At touchpoint ' +
            index.toString() +
            ', field ' +
            field +
            ' wrong data type';
          checkAvailable = false;
          alert(msg);
          return false;
        }
        return true;
      }
      return true;
    });

    if (!checkAvailable) {
      importData = [];
      return false;
    } else if (!isEmpty(newData)) {
      importData.push(newData);
    }
    return true;
  });

  return importData.length;
}

function changeHeaderBackgroundColor(headerName, color, backgroundColor) {
  const header = document.getElementById('header_' + headerName);
  header.style.backgroundColor = backgroundColor;
  header.style.color = color;
}

function generateTableHeadSelectors() {
  const thead = table.createTHead();
  const row = thead.insertRow();

  row.setAttribute('id', 'header-selectors');

  for (let i = 0; i < headers.length; i++) {
    const th = document.createElement('th');
    th.style.textAlign = 'center';
    th.style.border = '1px solid #000000';
    row.appendChild(th);

    if (i !== 0) {
      const select = document.createElement('select');
      select.setAttribute('name', headers[i]);
      select.setAttribute('id', headers[i]);
      select.addEventListener('change', matchColumn);

      const nullOptionElement = document.createElement('option');
      const nullOptionText = document.createTextNode('None');

      nullOptionElement.setAttribute('value', 'None');
      nullOptionElement.appendChild(nullOptionText);
      select.appendChild(nullOptionElement);

      // eslint-disable-next-line guard-for-in
      for (const option in touchpointFields) {
        const optionElement = document.createElement('option');
        const optionText = document.createTextNode(option);

        optionElement.setAttribute('value', option);
        optionElement.appendChild(optionText);
        select.appendChild(optionElement);
      }

      th.appendChild(select);
    }
  }
}

function generateTableHead(headerNames, isCsv) {
  const row = table.insertRow();

  for (const field of headerNames) {
    const th = document.createElement('th');
    th.setAttribute('id', 'header_' + field);
    th.style.textAlign = 'center';
    th.style.border = '1px solid #000000';

    const text = document.createTextNode(field);

    th.appendChild(text);
    row.appendChild(th);
  }
}

function generateTableRows(headerNames, data) {
  const newRow = table.insertRow();
  for (const field of headerNames) {
    const newCell = newRow.insertCell();
    const txt = data[field] ? data[field] : null;
    const newText = document.createTextNode(txt);

    newCell.appendChild(newText);
    newCell.style.textAlign = 'center';
    newCell.style.border = '1px solid #000000';
  }
}

function generateMatchedData(dataSrcMatchColumns) {
  for (const row of dataSrcMatchColumns) {
    if (!headers.includes(row.report_column)) {
      alert('Import File not exist ' + row.report_column + ' field');
      return [];
    }
  }

  const validDatas = [];

  for (let i = 0; i < importData.length; i++) {
    validData = {};

    for (const row of dataSrcMatchColumns) {
      let data = importData[i][row.report_column];
      let checkDataType = true;

      data = convertDataType(row.function, data);

      if (
        touchpointFields[row.journey_column] == 'numeric' &&
          !isNumeric(data)
      ) {
        checkDataType = false;
      } else if (
        touchpointFields[row.journey_column] == 'date' &&
          !isDate(data)
      ) {
        checkDataType = false;
      }

      if (checkDataType == false) {
        const message =
            'At row ' +
            i.toString() +
            ',' +
            'cannot match ' +
            row.report_column +
            ' to ' +
            row.journey_column;
        alert(message);

        return [];
      }

      validData[row.journey_column] = data;
    }

    validDatas.push(validData);
  }

  return validDatas;
}

function matchColumn(e) {
  const currentColumn = e.target.name;
  const targetColumn = e.target.value;

  for (const field in matchColumns) {
    if (matchColumns[field] == currentColumn) delete matchColumns[field];
  }

  for (const field in matchColumns) {
    if (targetColumn == field) {
      e.target.value = 'None';
      changeHeaderBackgroundColor(currentColumn, '#666', '#f8f8f8');
      alert('Duplicate matching column');

      return;
    }
  }

  for (let i = 0; i < importData.length; i++) {
    const data = importData[i][currentColumn];
    let checkDataType = true;

    if (touchpointFields[targetColumn] == 'numeric' && !isNumeric(data)) {
      checkDataType = false;
    } else if (touchpointFields[targetColumn] == 'date' && !isDate(data)) {
      checkDataType = false;
    }

    if (checkDataType == false) {
      const message =
          'At row ' +
          i.toString() +
          ', data type is invalid, match column data type must be ' +
          touchpointFields[targetColumn];

      e.target.value = 'None';
      changeHeaderBackgroundColor(currentColumn, '#666', '#f8f8f8');
      alert(message);

      return;
    }
  }

  if (targetColumn != 'None') {
    matchColumns[targetColumn] = currentColumn;
    changeHeaderBackgroundColor(currentColumn, '#ffffff', '#FF8484');
  } else {
    changeHeaderBackgroundColor(currentColumn, '#666', '#f8f8f8');
  }
}

// eslint-disable-next-line no-unused-vars
function mapFile(selectObj) {
  const dataSrc = selectObj.value;

  matchColumns = {};
  sendData = [];

  if (dataSrc == 'manipulate') {
    generateTable(headers, importData);
    generateTableHeadSelectors();
  } else if (dataSrc == '') {
    generateTable(headers, importData);
  } else {
    const dataSrcMatchColumns = matchedColumns.filter((row) => {
      if (row.report_name == dataSrc) return true;
      else return false;
    });

    sendData = generateMatchedData(dataSrcMatchColumns);

    if (sendData.length > 0) {
      const matchHeaders = dataSrcMatchColumns.map((row) => {
        return row.journey_column;
      });

      generateTable(matchHeaders, sendData);
    }
  }
}

// eslint-disable-next-line no-unused-vars
function submitTouchpoint() {
  if (Object.keys(matchColumns).length != 0) {
    sendData = [];

    for (data of importData) {
      const validData = {};
      // eslint-disable-next-line guard-for-in
      for (key in matchColumns) {
        validData[key] = data[matchColumns[key]];
      }

      sendData.push(validData);
    }
  }

  if (sendData.length == 0) {
    alert('No data to import');
    return;
  }

  const loadingModal = document.getElementById('loading-modal');
  loadingModal.style.display = 'flex';

  const csrftoken = getCookie('csrftoken');
  fetch('/admin/journey/import-touchpoints', {
    method: 'post',
    mode: 'same-origin',
    headers: {
      'Accept': 'application/json',
      'Content-type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({data: sendData}),
  })
      .then(function(response) {
        return response.json();
      })
      .then(function(data) {
        alert(data.result);
        location.reload();
      })
      .catch(function(error) {
        alert(error);
        location.reload();
      });
}
