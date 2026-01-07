// STATIC DATA //

const paycheck_amount =  parseFloat(
    document.getElementById("paycheck_amount")?.value || 0
    );

const bills = document.getElementById("total_bills")
let bills_amount = bills ? parseFloat(bills.value) : 0;


// DYNAMICS

const free_amount = paycheck_amount - bills_amount;

const bills_percent = (bills_amount) / paycheck_amount;
const free_percent = 1 - bills_percent


const bills_degrees = bills_percent * 360;
const free_degrees = 360 - bills_degrees;

const wheel = document.getElementById("money-wheel");
wheel.style.setProperty("--bill-deg", bills_degrees + "deg")
wheel.style.setProperty("--free-deg", "360deg")

const expenseZone = document.querySelector(".hover-zone.expenses");
const remainingZone = document.querySelector(".hover-zone.remaining");

const tooltip = document.getElementById("wheel-tooltip");
const container = document.getElementById("money-wheel-container");
const wrapper = document.querySelector(".wheel-wrapper");

function showTooltip(text, e) {
  tooltip.textContent = text;

  const padding = 8;
  const rect = container.getBoundingClientRect();

  tooltip.style.left = (e.clientX - rect.left + padding) + "px";
  tooltip.style.top  = (e.clientY - rect.top  + padding) + "px";
  tooltip.style.opacity = 1;
}

function hideTooltip() {
  tooltip.style.opacity = 0;
}

wrapper.addEventListener("mousemove", (e) => {
  const r = wrapper.getBoundingClientRect();

  const x = e.clientX - r.left;
  const y = e.clientY - r.top;

  const radius = r.width / 2;
  const dx = x - radius;
  const dy = y - radius;

  // If cursor is outside the circle, do nothing
  if (dx * dx + dy * dy > radius * radius) {
    hideTooltip();
    return;
  }

  // Inside circle: left half = remaining, right half = expenses
  if (x < radius) {
    showTooltip(`Remaining: $${free_amount.toFixed(2)}`, e);
  } else {
    showTooltip(`Expenses: $${bills_amount.toFixed(2)}`, e);
  }
});

wrapper.addEventListener("mouseleave", hideTooltip);
