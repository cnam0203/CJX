var importData = [];
var matchColumns = {};
var table = document.getElementById('tbl-csv-data');
var mappingTypeDiv = document.getElementById('select-mapping-type');
var submitBtn = document.getElementById("submit-file");
var touchpointFields = {};
var matchedColumns = [];
var headers = [];
var sendData =[];



function isNumeric(str) {
    if (typeof str != "string") return false // we only process strings!  
    return !isNaN(str) && // use type coercion to parse the _entirety_ of the string (`parseFloat` alone does not do this)...
           !isNaN(parseFloat(str)) // ...and ensure strings of whitespace fail
}

function isDate(dateStr) {
    return !isNaN(new Date(dateStr).getDate());
}

function importFile(allFields, allMatchedColumns) {
    refreshUpload();

    mappingTypeDiv.style.display = "block";
    submitBtn.style.display = "inline-block";

    var inputFile = document.getElementById('upload-csv').files[0];
    var report = document.getElementById('report');

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

function generateCSVData(importData, keys, data) {
    var newData = {};

    keys.map(field => { newData[field] = data[field] ? data[field] : null; })
    importData.push(newData);
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
            alert('Duplicate matching column');
            e.target.value = 'None';
            changeHeaderBackgroundColor(currentColumn, '#666', '#f8f8f8');
            return
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
            alert(message);
            e.target.value = 'None';
            changeHeaderBackgroundColor(currentColumn, '#666', '#f8f8f8');
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

function showMessage(message, time) {
    setTimeout(function() {
        alert(message);
    }, time);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function isEmpty(obj) {
    return Object.keys(obj).length === 0;
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

    console.log(sendData);

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

function readInstruction(selectObj) {
    var dataSrc = selectObj.value;

    if (dataSrc != '') {
        window.location.href = '/admin/journey/read-instruction/' + dataSrc;
    }
}

function submitMappingFile(reports, journeyColumns) {
    var datasrc = document.getElementById("data-source-name").value

    if (datasrc == '') {
        alert('Fill out Data Source Name');
        return;
    }

    if (reports.includes(datasrc)) {
        alert('Duplicate Data Source Name');
        return;
    }

    

    var matchingColumns = [];
    var count = 0;

    for (let journey_column of journeyColumns) {
        var report_column = document.getElementById('report-column-' + journey_column).value;
        var function_name = document.getElementById('instruction-' + journey_column).value
        if (report_column == '' && function_name != '') {
            alert('Must be fill out ' + journey_column + ' field');
            return;
        }

        if (report_column != '') {
            matchingColumns.push({
                'journey_column': journey_column,
                'report_column': report_column,
                'function': function_name
            })

            count += 1;
        }
    }

    if (count == 0) {
        alert('Must map at least 1 columns');
        return;
    }

    var instructionImg = document.getElementById('upload-instruction').files;

    if (instructionImg.length != 0)
        instructionImg = instructionImg[0]
    else
        instructionImg = null

    var formData = new FormData();
    formData.append('dataSrc', datasrc)
    formData.append('matchingColumns', JSON.stringify(matchingColumns))
    formData.append('files[]', instructionImg)

    const csrftoken = getCookie('csrftoken');
    fetch('/admin/journey/upload-mapping-file', {
            method: 'post',
            mode: 'same-origin',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            body: formData
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
    matchColumns = {};
    sendData = [];

    var dataSrc = selectObj.value;

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

        generateMatchedData(dataSrcMatchColumns);

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
            return;
        }
    }

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
                sendData = [];
                var message = 'At row ' + i.toString() + ',' + 'cannot match ' + row.report_column + ' to ' + row.journey_column;
                alert(message);

                return [];
            }

            validData[row.journey_column] = data;
        }

        sendData.push(validData);
    }
}

function convertDataType(functionName, data) {
    if (functionName == 'lower') 
        data = data.toLowerCase()
    else if (functionName == 'upper')
        data = data.toUpperCase()
    else if (functionName == 'datetime')
        data = new Date(data)
    else if (functionName == 'string')
        data = data.toString()
    else if (functionName == 'int')
        data = parseInt(data)
    else if (functionName == 'float')
        data = parseFloat(data)

    return data
}