// STATIC DATA //

const paycheck_amount = 2000;
const bills_amount = 1000;
const savings_amount = 200;

// DYNAMICS

const free_amount = paycheck_amount-bills_amount-savings_amount;

const bills_percent = (bills_amount + savings_amount) / paycheck_amount;
const free_percent = 1 - bills_percent

console.log("Free percent:", free_percent);

const bills_degrees = bills_percent * 360;
const free_degrees = 360 - bills_degrees;

const wheel = document.getElementById("money-wheel");
wheel.style.setProperty("--bill-deg", bills_degrees + "deg")
wheel.style.setProperty("--free-deg", "360deg")

console.log(bills_degrees, free_degrees)

