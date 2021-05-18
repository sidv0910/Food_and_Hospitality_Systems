function validate() {
    var quantity = document.getElementById('quantity').value;
    var item_type = document.getElementById('item_type').value;

    if (quantity == "None") {
        alert("Please select quantity.");
        document.getElementById('quantity').focus;
        return false;
    }

    if (item_type == "None") {
        alert("Please select item type.");
        document.getElementById('item_type').focus;
        return false;
    }

    return true;
}