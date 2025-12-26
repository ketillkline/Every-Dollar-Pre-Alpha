console.log("✅ newhome.js loaded");
document.addEventListener("DOMContentLoaded", () => {
    const addButton = document.getElementById("bill_trigger");
    const table = document.getElementById("bills-table");
    const addRow = document.getElementById("add-row");

    addButton.addEventListener("click", () => {
        // create new table row
        const newRow = document.createElement("tr");

        //create cells with input fields
        newRow.innerHTML= `
        <td><input type="text" name="bill_name" placeholder="Name"></td>
        <td><input type="text" name="bill_amount" placeholder="Amount"></td>
        <td><input type="text" name="bill_pay_day" placeholder="Pay Day"></td>
        <td><button type="submit" id="save-bill-button" name="action" value="add_bill">Save</button></td>
        `;

        const tbody = addRow.parentElement;
        tbody.insertBefore(newRow, addRow);
    });

});