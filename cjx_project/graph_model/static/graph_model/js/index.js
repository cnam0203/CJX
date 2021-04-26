function validateGraphForm() {
    var startDate = Date.parse(document.forms["graphForm"]["startDate"].value);
    var endDate = Date.parse(document.forms["graphForm"]["endDate"].value);
    if (startDate > endDate) {
        alert("Start date must be earlier than end date !");
        return false;
    }
}

function validateClusterUserForm() {
    var startDate = Date.parse(document.forms["clusterUserForm"]["startDate"].value);
    var endDate = Date.parse(document.forms["clusterUserForm"]["endDate"].value);
    if (startDate > endDate) {
        alert("Start date must be earlier than end date !");
        return false;
    }
}

function validateClusterForm() {
    var startDate = Date.parse(document.forms["clusterForm"]["startDate"].value);
    var endDate = Date.parse(document.forms["clusterForm"]["endDate"].value);
    var numClusters = document.forms["clusterForm"]["numClusters"].value;
    if (startDate > endDate) {
        alert("Start date must be earlier than end date !");
        return false;
    }

    if (numClusters < 2 || numClusters > 10 || isNaN(numClusters)) {
        alert("Number of clusters must be in range (2, 10)");
        return false;
    }

}