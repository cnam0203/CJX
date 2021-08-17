/* eslint-disable no-unused-vars */
/* eslint-disable require-jsdoc */
function readInstruction(selectObj) {
  const dataSrc = selectObj.value;

  if (dataSrc != '') {
    window.location.href = '/journey/import/review-mapping-file/' + dataSrc;
  }
}
