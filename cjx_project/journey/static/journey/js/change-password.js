/* eslint-disable require-jsdoc */
// eslint-disable-next-line no-unused-vars
function submitChangePassword() {
  const currentPassword = document.getElementById('currentPassword').value;
  const newPassword = document.getElementById('newPassword').value;

  if (currentPassword == '') {
    alert('Fill out current password');
    return;
  }

  if (newPassword == '') {
    alert('Fill out new password');
    return;
  }
}
