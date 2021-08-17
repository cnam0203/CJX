/* eslint-disable no-unused-vars */
/* eslint-disable require-jsdoc */
function convertDataType(functionName, data) {
  if (functionName == 'lower') {
    data = data.toLowerCase();
  } else if (functionName == 'upper') {
    data = data.toUpperCase();
  } else if (functionName == 'datetime') {
    data = new Date(data);
  } else if (functionName == 'string') {
    data = data.toString();
  } else if (functionName == 'int') {
    data = parseInt(data);
  } else if (functionName == 'float') {
    data = parseFloat(data);
  }

  return data;
}

function isEmpty(obj) {
  return Object.keys(obj).length === 0;
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

function isNumeric(str) {
  if (typeof str != 'string') return false; // we only process strings!
  return !isNaN(str) && !isNaN(parseFloat(str));
}

function isDate(dateStr) {
  return !isNaN(new Date(dateStr).getDate());
}
