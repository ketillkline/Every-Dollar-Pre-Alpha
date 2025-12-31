class BillManager {
    constructor(){
        this.table = document.getElementById("bills-table");
        this.form = this.table.closest("form");

        this.addButton = document.getElementById("bill_trigger");
        this.updateUI(this.addButton, "show");
        this.editingRow = null;

        this.tbody = document.querySelector(".bills-body");
        this.setupEvents();
    }
    setupEvents() {
        this.addButton.addEventListener("click", () => {
            this.addBillRow();
        })
        this.table.addEventListener("click", (e) => {
            if (e.target.classList.contains("edit_bill_trigger")){
                const row = e.target.closest("tr");

            const old_info = [ // name, amount, payday
                row.dataset.name, row.dataset.amount, row.dataset.payday,
                row.dataset.id];

            const editButton = e.target.closest(".edit_bill_trigger");
            const deleteButton = row.querySelector(".delete_button");
            const elements = [editButton, deleteButton];
            this.editBillRow(elements, old_info, row);
            }
        });
        this.form.addEventListener("submit", (e) => {
            this.handleSubmit(e);
        });
    }

    updateUI(element, action) {
        if (action == "show") {
            element.hidden = false;
        } else if (action == "hide"){
            element.hidden = true;
        }


    }


    addBillRow(){
        this.updateUI(this.addButton, "hide");
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
            this.updateUI(this.addButton, "show");
        })
    }


    editBillRow(elements, old_info, row) {
        this.editingRow = row;
        for (const element of elements){
            this.updateUI(element, "hide");
        }

        const originalHTML = row.innerHTML;

        row.innerHTML =
       `
       <td><input type="text" name="edited_bill_name" value="${old_info[0]}"></td>
        <td><input type="number" name="edited_bill_amount" value="${old_info[1]}"></td>
        <td><input type="number" name="edited_bill_payday" value="${old_info[2]}"></td>
        <td>
            <button type="submit" class="save_edits_button" name="action" value="save_edited_bill">Save Edits</button>
            <button type="button" class="cancel_edits_button">Cancel</button>
            <input type="hidden" name="bill_id" value="${old_info[3]}">
        </td>
        `;

        const cancelButton = row.querySelector(".cancel_edits_button");
        cancelButton.addEventListener("click", () => {
            row.innerHTML = originalHTML;
            elements = row.querySelectorAll(".delete_button, .edit_bill_trigger");
            for (const element of elements){
                this.updateUI(element, "show");
            }

        });


    }

    handleSubmit(e){
        const action = e.submitter?.value;
        if (action == "delete_bill"){
            return;
        }


        const activeRow =
            action == "save_edited_bill"
                ? this.editingRow
                : this.tbody.querySelector("tr:last-child");

        if (!activeRow) return;

        if (action == "save_edited_bill"){

            const nameInput = activeRow.querySelector('[name="edited_bill_name"]');
            const amountInput = activeRow.querySelector('[name="edited_bill_amount"]');
            const paydayInput = activeRow.querySelector('[name="edited_bill_payday"]');

            const name = nameInput?.value.trim();
            const amount = amountInput?.value.trim();
            const payday = paydayInput?.value.trim();
            console.log("Editing", name, amount, payday)

            if (!name || !amount || !payday){
            e.preventDefault();
            alert("Please fill in all required fields");
            return;
        }
        return;
        }



        const nameInput = activeRow.querySelector('[name="bill_name"]');
        const amountInput = activeRow.querySelector('[name="bill_amount"]');
        const paydayInput = activeRow.querySelector('[name="bill_payday"]');

        const name = nameInput?.value.trim();
        const amount = amountInput?.value.trim();
        const payday = paydayInput?.value.trim();
        console.log("Saving New", name, amount, payday)

        if (!name || !amount || !payday){
            e.preventDefault();
            alert("Please fill in all required fields");
            return;
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    new BillManager();
})