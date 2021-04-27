var importData = [];
var matchedColumns = [];
var headers = [];
var sendData =[];

var matchColumns = {};
var touchpointFields = {};

var table = document.getElementById('tbl-csv-data');
var mappingTypeDiv = document.getElementById('select-mapping-type');
var submitBtn = document.getElementById("submit-file");

function importFile(allFields, allMatchedColumns) {
    refreshUpload();

    var inputFile = document.getElementById('upload-csv').files[0];
    var report = document.getElementById('report');

    mappingTypeDiv.style.display = "block";
    submitBtn.style.display = "inline-block";

    touchpointFields = allFields;
    matchedColumns = allMatchedColumns;
    report.value = '';

    if (checkCSVFile(inputFile)) 
        importCSV(inputFile)
    else
        importJSON(inputFile)
}

function importCSV(inputFile) {
    Papa.parse(inputFile, {
        download: true,
        header: true,
        complete: function(results) {
            headers = results.meta.fields;
            importData = results.data;
            generateTable(headers, importData);
        }
    });
}

function generateTable(headerNames, datas) {
    table.innerHTML = '';

    generateTableHead(headerNames, true);

    datas.map((data)=> {
        generateTableRows(headerNames, data);
    }); 
}

function importJSON(inputFile) {
    var reader = new FileReader();
    reader.addEventListener('load', function() {
        var jsonFile = JSON.parse(reader.result);
        if (jsonFile && Array.isArray(jsonFile)) {
            var results = jsonFile;
            var matchCount = generateJSONData(results);
            
            if (matchCount > 0) {
                var msg = matchCount.toString() + " object(s) matched";

                generateTableHead(table, keys, keys, false);
                importData.map((data) => {
                    generateTableRows(table, keys, data)
                })

                showMessage(msg, 1200);
                submitBtn.style.display = "inline-block";
            }
            else
                alert("No data to import")
        }
        else
            alert("Please follow JSON File Format")
    })
    reader.readAsText(inputFile);
}

function checkCSVFile(file) {
    var fileExtension = file.name.split('.').pop();
    if (fileExtension === "csv") 
        return true;
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
        var checkAvailable = true;
        var newData = {};

        Object.keys(data).every((field) => {
            if (keys.includes(field)) {
                if (data[field] == null || typeof(data[field]) !== "object") {
                    newData[field] = data[field];
                } else {
                    var msg = "At touchpoint " + index.toString() + ", field " + field + " wrong data type";
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
        }
        else
            if (!isEmpty(newData)) {
                importData.push(newData);
            }
        return true;
    })

    return importData.length;
}

function matchColumn(e) {
    var currentColumn = e.target.name;
    var targetColumn = e.target.value;

    for (let field in matchColumns) {
        if (matchColumns[field] == currentColumn)
            delete matchColumns[field]
    }
    
    for (let field in matchColumns) {
        if (targetColumn == field) {
            e.target.value = 'None';
            changeHeaderBackgroundColor(currentColumn, '#666', '#f8f8f8');
            alert('Duplicate matching column');

            return;
        }
    }

    for (let i=0; i < importData.length; i++) {
        var data = importData[i][currentColumn];
        var checkDataType = true;

        if (touchpointFields[targetColumn] == 'numeric' && !isNumeric(data)) {
            checkDataType = false
        } else if (touchpointFields[targetColumn] == 'date' && !isDate(data)) {
            checkDataType = false;
        }

        if (checkDataType == false) {
            var message = 'At row ' + i.toString() + ', data type is invalid, match column data type must be ' + touchpointFields[targetColumn];

            e.target.value = 'None';
            changeHeaderBackgroundColor(currentColumn, '#666', '#f8f8f8');
            alert(message);

            return
        }
    }

    if (targetColumn != 'None') {
        matchColumns[targetColumn] = currentColumn;
        changeHeaderBackgroundColor(currentColumn, '#ffffff', '#8de089');
    } else {
        changeHeaderBackgroundColor(currentColumn, '#666', '#f8f8f8');
    }
}

function changeHeaderBackgroundColor(headerName, color, backgroundColor) {
    let header = document.getElementById('header_' + headerName);
    header.style.backgroundColor = backgroundColor;
    header.style.color = color;
}

function generateTableHeadSelectors() {
    let thead = table.createTHead();
    let row = thead.insertRow();

    row.setAttribute("id", "header-selectors");

    for (var i = 0; i < headers.length; i++) {
        let th = document.createElement('th');
        th.style.textAlign = "center";
        th.style.border = "1px solid #000000";
    	row.appendChild(th);

        if (i !== 0) {
            let select = document.createElement('select');
            select.setAttribute('name', headers[i]);
            select.setAttribute('id', headers[i]);
            select.addEventListener('change', matchColumn);

            let nullOptionElement = document.createElement('option')
            let nullOptionText = document.createTextNode('None');

            nullOptionElement.setAttribute('value', 'None');
            nullOptionElement.appendChild(nullOptionText)
            select.appendChild(nullOptionElement);
    
            for (let option in touchpointFields) {
                let optionElement = document.createElement('option')
                let optionText = document.createTextNode(option);
    
                optionElement.setAttribute('value', option);
                optionElement.appendChild(optionText)
                select.appendChild(optionElement);
            }
    
            th.appendChild(select);
        }
    }
}

function generateTableHead(headerNames, isCsv) {
    let row = table.insertRow();

    for (let field of headerNames) {
        let th = document.createElement('th');
        th.setAttribute('id', 'header_' + field);
        th.style.textAlign = "center";
        th.style.border = "1px solid #000000";

    	let text = document.createTextNode(field);

    	th.appendChild(text);
    	row.appendChild(th);
    }
}

function generateTableRows(headerNames, data) {
    let newRow = table.insertRow();
    for(let field of headerNames) {
    	let newCell = newRow.insertCell();
        let txt = data[field] ? data[field] : null;
    	let newText = document.createTextNode(txt);

    	newCell.appendChild(newText);
        newCell.style.textAlign = "center";
        newCell.style.border = "1px solid #000000";

    }
}

function submitTouchpoint() {
    if (Object.keys(matchColumns).length != 0) {
        sendData = [];

        for (data of importData) {
            var validData = {};

            for (key in matchColumns) {
                validData[key] = data[matchColumns[key]];
            }

            sendData.push(validData);
        }
    }

    if (sendData.length == 0) {
        alert('No data to import')
        return;
    }

    const csrftoken = getCookie('csrftoken');
    fetch('/admin/journey/upload-touchpoint', {
        method: 'post',
        mode: 'same-origin',
        headers: {
            "Accept": 'application/json',
            "Content-type": 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({data: sendData})
        })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            alert(data.result);
            location.reload();
        })
        .catch(function (error) {
            alert(error);
            location.reload();
        });
}

function mapFile(selectObj) {
    var dataSrc = selectObj.value;

    matchColumns = {};
    sendData = [];

    if (dataSrc == 'manipulate') {
        generateTable(headers, importData);
        generateTableHeadSelectors();
    } else if (dataSrc == '') {
        generateTable(headers, importData);
    } else {
        var dataSrcMatchColumns = matchedColumns.filter((row) => {
            if (row.report_name == dataSrc)
                return true;
            else
                return false;
        })

        sendData = generateMatchedData(dataSrcMatchColumns);

        if (sendData.length > 0) {
            var matchHeaders = dataSrcMatchColumns.map((row) => {
                return row.journey_column;
            })

            generateTable(matchHeaders, sendData);
        }
    }
}

function generateMatchedData(dataSrcMatchColumns) {
    for (let row of dataSrcMatchColumns) {
        if (!headers.includes(row.report_column)) {
            alert("Import File not exist " + row.report_column + " field");
            return [];
        }
    }

    var validDatas = [];

    for (let i=0; i < importData.length; i++) {
        validData = {};

        for (let row of dataSrcMatchColumns) {
            var data = importData[i][row.report_column];
            var checkDataType = true;

            data = convertDataType(row.function, data);
            
            if (touchpointFields[row.journey_column] == 'numeric' && !isNumeric(data)) {
                checkDataType = false
            } else if (touchpointFields[row.journey_column] == 'date' && !isDate(data)) {
                checkDataType = false;
            }
    
            if (checkDataType == false) {
                var message = 'At row ' + i.toString() + ',' + 'cannot match ' + row.report_column + ' to ' + row.journey_column;
                alert(message);

                return [];
            }

            validData[row.journey_column] = data;
        }

        validDatas.push(validData);
    }

    return validDatas;
}

