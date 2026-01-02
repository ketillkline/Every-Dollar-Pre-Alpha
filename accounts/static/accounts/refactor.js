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
            editElements: []
        }
        this.form = this.elements.table.closest("form");

    }

    setupEvents(){
        this.elements.addButton.addEventListener("click", () => {
            this.addBill();
        });

        this.elements.table.addEventListener("click", (e) => {
            if (e.target.classList.contains("edit_bill_trigger")){
                const row = e.target.closest("tr");

                const old_info = [
                    row.dataset.name, row.dataset.amount, row.dataset.payday,
                    row.dataset.id
                ];

                const editButton = e.target.closest(".edit_button_trigger");
                const deleteButton = e.target.closest(".delete_button");
                this.elements.editElements.push(editButton, deleteButton);
                this.editBill(elements, old_info, row);
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
        this.updateUI(this.elements.incomeSubmitButton, "hide");
        this.updateUI(this.table.addButton, "hide");
    }

    editingUI(){
        this.updateUI(this.elements.addButton, "hide");
        this.updateUI(this.elements.incomeSubmitButton, "hide");
        for (const element in this.table.editElements){
            this.updateUI(element, "hide");
        }

    }

    idleUI(){
        for (const element of Object.values(this.elements)){
            if (!element) continue;
            this.updateUI(element, "show");
        }
        if (this.table.editElements){
            for (const element in this.table.editElements){
                this.updateUI(element, "show");
            }
        }
    }

    addBill(){
        this.changeState("ADDING");

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
        this.table.tbody.appendChild(row);

        const cancelButton = row.querySelector(".cancel-bill");

        cancelButton.addEventListener("click", () => {
            row.remove();
            this.changeState("IDLE");
        });

    }

    editBill(old_info, row) {
        this.changeState("EDITING");
        this.table.editingRow = row;

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
            this.table.editElements = Array.from(row.querySelectorAll(".edit_bill_trigger, .delete_button"));
            this.changeState("IDLE");
            this.table.editElements = [];
        });
    }

    handleSubmit(event){
        const action = event.submitter?.value;

    }

}