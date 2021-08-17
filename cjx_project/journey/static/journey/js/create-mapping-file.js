/* eslint-disable max-len */
/* eslint-disable require-jsdoc */
// eslint-disable-next-line no-unused-vars
function submitMappingFile(reports, journeyColumns) {
  const datasrc = document.getElementById('data-source-name').value;

  if (datasrc == '') {
    alert('Fill out Data Source Name');
    return;
  }

  if (reports.includes(datasrc)) {
    alert('Duplicate Data Source Name');
    return;
  }


  const matchingColumns = [];
  let count = 0;

  for (const journeyColumn of journeyColumns) {
    const reportColumn = document.getElementById('report-column-' + journeyColumn).value;
    const functionName = document.getElementById('instruction-' + journeyColumn).value;
    if (reportColumn == '' && functionName != '') {
      alert('Must be fill out ' + journeyColumn + ' field');
      return;
    }

    if (reportColumn != '') {
      matchingColumns.push({
        'journey_column': journeyColumn,
        'report_column': reportColumn,
        'function': functionName,
      });

      count += 1;
    }
  }

  if (count == 0) {
    alert('Must map at least 1 columns');
    return;
  }

  let instructionImg = document.getElementById('upload-instruction').files;

  if (instructionImg.length != 0) {
    instructionImg = instructionImg[0];
  } else {
    instructionImg = null;
  }

  const formData = new FormData();
  formData.append('mappingFileName', datasrc);
  formData.append('mappingColumns', JSON.stringify(matchingColumns));
  formData.append('files[]', instructionImg);

  const csrftoken = getCookie('csrftoken');
  fetch('/admin/journey/upload-mapping-file', {
    method: 'post',
    mode: 'same-origin',
    headers: {
      'X-CSRFToken': csrftoken,
    },
    body: formData,
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
