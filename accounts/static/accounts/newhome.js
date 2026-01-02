class BillManager {
    constructor() {
        this.validStates = ["IDLE", "ADDING", "EDITING"];
        this.state = {
            mode: "IDLE"
        };

        this.elements = {
            addButton: document.getElementById("bill_trigger"),
            incomeSubmitButton: document.getElementById("income_submit_button"),
            table: document.getElementById("bills-table"),
            tbody: document.querySelector(".bills-body"),
            editingRow: null,
            editElements: [],
            editButtons: [],
            deleteButtons: []
        }

        this.submitActions = ["delete_bill", "save_edited_bill", "add_income",
            "clear_all_incomes", "add_bill"];

        this.form = this.elements.table.closest("form");
        this.setupEvents();

    }

    setupEvents(){
        this.elements.addButton.addEventListener("click", () => {
            console.log("got to setup");
            this.addBill();
        });

        this.elements.table.addEventListener("click", (e) => {
            if (e.target.classList.contains("edit_bill_trigger")){
                const row = e.target.closest("tr");

                const old_info = [
                    row.dataset.name, row.dataset.amount, row.dataset.payday,
                    row.dataset.id
                ];

                const editButton = e.target.closest(".edit_bill_trigger");
                const deleteButton = row.querySelector(".delete_button");
                this.elements.editElements = [editButton, deleteButton];
                console.log(this.elements.editElements);
                this.editBill(old_info, row);
            }
            this.form.addEventListener("submit", (e) => {
                this.handleSubmit(e);
            });
        });
    }

    changeState(state){
        if (!this.validStates.includes(state)){
            throw new Error(`Invalid state: ${state}.`);
        }
        this.state.mode = state;
        switch (this.state.mode){
            case "IDLE":
                return this.idleUI();
            case "ADDING":
                return this.addingUI();
            case "EDITING":
                return this.editingUI();
        }
    }

    updateUI(element, action){
        switch (action){
            case "show":
                element.hidden = false;
                break;
            case "hide":
                element.hidden = true;
                break;
            default:
                throw new Error(`Error: Action '${action}' not valid.`);
                break;
        }

    }

    addingUI(){
        this.elements.editButtons = Array.from(document.querySelectorAll(".edit_bill_trigger"));
        this.elements.deleteButtons = Array.from(document.querySelectorAll(".delete_button"));
        for (const button of this.elements.editButtons){
            this.updateUI(button, "hide");
        }
        for (const button of this.elements.deleteButtons){
            this.updateUI(button, "hide");
        }
        this.updateUI(this.elements.incomeSubmitButton, "hide");
        this.updateUI(this.elements.addButton, "hide");
    }

    editingUI(){
        this.updateUI(this.elements.addButton, "hide");
        this.updateUI(this.elements.incomeSubmitButton, "hide");
        for (const element of this.elements.editElements){
            this.updateUI(element, "hide");
        }

    }

    idleUI(){
        for (const element of Object.values(this.elements)){
            if (!element) continue;
            if (Array.isArray(element)){
                for (const subElement of element){
                    this.updateUI(subElement, "show");
                }
            }
            this.updateUI(element, "show");
        }
    }

    addBill(){
        this.changeState("ADDING");
        console.log("changed state")

        const row = document.createElement("tr");

        row.innerHTML = `
        <td><input type="text" name="bill_name" placeholder="Name"></td>
        <td><input type="number" name="bill_amount" placeholder="Amount"></td>
        <td><input type="number" name="bill_pay_day" placeholder="Pay Day" min="1" max="31"></td>
        <td>
            <button type="submit" name="action" value="add_bill">Save</button>
            <button type="button" class="cancel-bill">Cancel</button>
        </td>
        `;

        const paydayInput = row.querySelector('[name="bill_pay_day"]');
        paydayInput.addEventListener("input", () => {
            const value = Number(paydayInput.value);

            if (value > 31) paydayInput.value = 31;
            if (value < 1) paydayInput.value = 1;
        });
        this.elements.tbody.appendChild(row);

        const cancelButton = row.querySelector(".cancel-bill");

        cancelButton.addEventListener("click", () => {
            row.remove();
            this.changeState("IDLE");
        });

    }

    editBill(old_info, row) {
        this.changeState("EDITING");
        this.elements.editingRow = row;

        const oldHTML = row.innerHTML;

        row.innerHTML =
       `
       <td><input type="text" name="edited_bill_name" value="${old_info[0]}"></td>
        <td><input type="number" name="edited_bill_amount" value="${old_info[1]}"></td>
        <td><input type="number" name="edited_bill_payday" value="${old_info[2]}" min="1" max="31"></td>
        <td>
            <button type="submit" class="save_edits_button" name="action" value="save_edited_bill">Save Edits</button>
            <button type="button" class="cancel_edits_button">Cancel</button>
            <input type="hidden" name="bill_id" value="${old_info[3]}">
        </td>
        `;

        const cancelButton = row.querySelector(".cancel_edits_button");
        cancelButton.addEventListener("click", () => {
            row.innerHTML = oldHTML;
            this.elements.editElements = Array.from(row.querySelectorAll(".edit_bill_trigger, .delete_button"));
            this.changeState("IDLE");
            this.elements.editElements = [];
        });
    }

    handleSubmit(event){
        const action = event.submitter?.value;
        switch (action){
            case "save_edited_bill":
                return this.saveEditedBill();
            case "add_bill":
                return this.saveNewBill();
            default:
                return;
        }
    }

    saveEditedBill(){
        const activeRow = this.editingRow;
        if (!activeRow) return;

        const nameInput = activeRow.querySelector('[name="edited_bill_name"]');
        const amountInput = activeRow.querySelector('[name="edited_bill_amount"]');
        const paydayInput = activeRow.querySelector('[name="edited_bill_payday"]');

        const name = nameInput?.value.trim();
        const amount = amountInput?.value.trim();
        const payday =paydayInput?.value.trim();

        if (!name || !amount || !payday){
            e.preventDefault();
            alert("Please fill in all required fields");
            return;
        }
    }

    saveNewBill(){
        const activeRow = this.elements.tbody.querySelector("tr:last-child");
        if (!activeRow) return;

        const nameInput = activeRow.querySelector('[name="bill_name"]');
        const amountInput = activeRow.querySelector('[name="bill_amount"]');
        const paydayInput = activeRow.querySelector('[name="bill_pay_day"]');

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