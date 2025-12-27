class BillManager {
    constructor(){
        this.addButton = document.getElementById("bill_trigger");
        this.tbody = document.querySelector(".bills-body");
        this.setupEvents();
    }
    setupEvents() {
        this.addButton.addEventListener("click", () => {
            this.addBillRow();
        })
    }

    addBillRow(){
        const row = document.createElement("tr")
        row.innerHTML = `
        <td><input type="text" name="bill_name" placeholder="Name"></td>
        <td><input type="number" name="bill_amount" placeholder="Amount"></td>
        <td><input type="number" name="bill_pay_day" placeholder="Pay Day"></td>
        <td>
            <button type="submit" name="action" value="add_bill">Save</button>
            <button type="button" class="cancel-bill">Cancel</button>
        </td>
        `
        this.tbody.appendChild(row);

        const cancelButton = row.querySelector(".cancel-bill");

        cancelButton.addEventListener("click", () => {
            row.remove();
        })
    }
}

document.addEventListener("DOMContentLoaded", () => {
    new BillManager();
})