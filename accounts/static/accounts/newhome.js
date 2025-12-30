class BillManager {
    constructor(){
        this.addingBill = false;
        this.editingBill = false;

        this.addButton = document.getElementById("bill_trigger");
        this.editButton = document.getElementById("edit_bill_trigger");
        console.log(this.editButton);

        this.tbody = document.querySelector(".bills-body");
        this.setupEvents();
        this.updateUI();
    }
    setupEvents() {
        this.addButton.addEventListener("click", () => {
            this.addBillRow();
        })
        this.editButton.addEventListener("click", () => {
        this.editBillRow();
        });
    }

    updateUI() {
        if (this.addingBill) {
            this.addButton.hidden = true;
        } else {
            this.addButton.hidden = false;
        }
        if (this.editingBill) {
            this.editButton.hidden = true;
        } else {
            this.editButton.hidden = false;
        }

    }


    addBillRow(){
        this.addingBill = true;
        this.updateUI();
        const row = document.createElement("tr")
        row.innerHTML = `
        <td><input type="text" name="bill_name" placeholder="Name"></td>
        <td><input type="number" name="bill_amount" placeholder="Amount"></td>
        <td><input type="number" name="bill_pay_day" placeholder="Pay Day"></td>
        <td>
            <button type="button" name="action" value="add_bill">Save</button>
            <button type="button" class="cancel-bill">Cancel</button>
        </td>
        `
        this.tbody.appendChild(row);

        const cancelButton = row.querySelector(".cancel-bill");

        cancelButton.addEventListener("click", () => {
            row.remove();
            this.addingBill = false;
            this.updateUI();
        })
    }
    editBillRow() {
        console.log("editing Bill");
        this.editingBill = true;
        this.updateUI();
        const row = document.getElementById("{{ bill.name }} row");
        row.innerHTML =
        `<td><input type="text" name="bill_name" placeholder="Name"></td>
        <td><input type="number" name="bill_amount" placeholder="Amount"></td>
        <td><input type="number" name="bill_pay_day" placeholder="Pay Day"></td>
        <td>
            <button type="button" name="action" value="add_bill">Save</button>
            <button type="button" class="cancel-bill">Cancel</button>
        </td>`;



    }
}

document.addEventListener("DOMContentLoaded", () => {
    new BillManager();
})