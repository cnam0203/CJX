/* eslint-disable no-unused-vars */
// eslint-disable-next-line require-jsdoc
function validateForm() {
  const startDate = Date.parse(document.forms['form']['startDate'].value);
  const endDate = Date.parse(document.forms['form']['endDate'].value);
  if (startDate > endDate) {
    alert('Start date must be earlier than end date !');
    return false;
  }
}
