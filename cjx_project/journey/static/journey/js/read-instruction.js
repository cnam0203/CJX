function readInstruction(selectObj) {
    var dataSrc = selectObj.value;

    if (dataSrc != '') {
        window.location.href = '/admin/journey/read-instruction/' + dataSrc;
    }
}