/* eslint-disable no-unused-vars */
// eslint-disable-next-line require-jsdoc
function validateGraphForm() {
  const startDate = Date.parse(document.forms['graphForm']['startDate'].value);
  const endDate = Date.parse(document.forms['graphForm']['endDate'].value);
  if (startDate > endDate) {
    alert('Start date must be earlier than end date !');
    return false;
  }

  const loadingModal = document.getElementById('loading-modal');
  loadingModal.style.display = 'flex';
}

// eslint-disable-next-line require-jsdoc
function validateClusterUserForm() {
  // eslint-disable-next-line max-len
  const startDate = Date.parse(document.forms['clusterUserForm']['startDate'].value);
  // eslint-disable-next-line max-len
  const endDate = Date.parse(document.forms['clusterUserForm']['endDate'].value);
  if (startDate > endDate) {
    alert('Start date must be earlier than end date !');
    return false;
  }

  const loadingModal = document.getElementById('loading-modal');
  loadingModal.style.display = 'flex';
}

// eslint-disable-next-line require-jsdoc
function validateClusterForm() {
  // eslint-disable-next-line max-len
  const startDate = Date.parse(document.forms['clusterForm']['startDate'].value);
  const endDate = Date.parse(document.forms['clusterForm']['endDate'].value);
  const numClusters = document.forms['clusterForm']['numClusters'].value;
  if (startDate > endDate) {
    alert('Start date must be earlier than end date !');
    return false;
  }

  if (numClusters < 2 || numClusters > 10 || isNaN(numClusters)) {
    alert('Number of clusters must be in range (2, 10)');
    return false;
  }

  const loadingModal = document.getElementById('loading-modal');
  loadingModal.style.display = 'flex';
}

// eslint-disable-next-line require-jsdoc
function validateDecisionForm() {
  // eslint-disable-next-line max-len
  const startDate = Date.parse(document.forms['decisionForm']['startDate'].value);
  const endDate = Date.parse(document.forms['decisionForm']['endDate'].value);
  if (startDate > endDate) {
    alert('Start date must be earlier than end date !');
    return false;
  }

  const loadingModal = document.getElementById('loading-modal');
  loadingModal.style.display = 'flex';
}
