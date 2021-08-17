// eslint-disable-next-line require-jsdoc
function displaySubClass(btnId, subElementId) {
  const btn = document.getElementById(btnId);
  const element = document.getElementById(subElementId);

  btn.addEventListener('click', function() {
    if (element.style.display == 'none' || element.style.display == '') {
      element.style.display = 'block';
    } else {
      element.style.display = 'none';
    }
  });
}

displaySubClass('import-btn', 'import-subclass');
displaySubClass('table-btn', 'table-subclass');
displaySubClass('analytics-btn', 'analytics-subclass');
displaySubClass('discovery-btn', 'discovery-subclass');

