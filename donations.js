// Set this to the public HTTPS checkout URL issued to the home's payment account.
const donationCheckout = "";

const amount = document.getElementById("amount");
const presets = document.querySelectorAll("[data-amount]");
const frequencies = document.querySelectorAll('[name="frequency"]');
const amountError = document.getElementById("amount-error");
const summary = document.getElementById("donation-summary");
const formatAmount = new Intl.NumberFormat("en-KE");

function updatePresets() {
  for (const button of presets) {
    button.setAttribute("aria-pressed", String(button.dataset.amount === amount.value));
  }
}

function updateSummary() {
  const valid = amount.validity.valid && Number.isSafeInteger(amount.valueAsNumber);
  amountError.textContent = valid ? "" : "Enter a whole amount of at least KES 1.";
  if (valid) {
    amount.removeAttribute("aria-invalid");
    const frequency = document.querySelector('[name="frequency"]:checked').value;
    summary.value = `KES ${formatAmount.format(amount.valueAsNumber)} · ${frequency === "monthly" ? "Monthly" : "One time"}`;
  } else {
    amount.setAttribute("aria-invalid", "true");
    summary.value = "Awaiting a valid amount";
  }
}

for (const button of presets) {
  button.addEventListener("click", () => {
    amount.value = button.dataset.amount;
    updatePresets();
    updateSummary();
  });
}
amount.addEventListener("input", updatePresets);
amount.addEventListener("change", updateSummary);
amount.addEventListener("blur", updateSummary);
for (const frequency of frequencies) frequency.addEventListener("change", updateSummary);
updatePresets();

if (URL.canParse(donationCheckout)) {
  const checkout = new URL(donationCheckout);
  if (checkout.protocol === "https:" && !checkout.username && !checkout.password) {
    const link = document.getElementById("checkout-link");
    link.href = checkout.href;
    link.hidden = false;
    document.getElementById("giving-preview").hidden = true;
    document.getElementById("checkout-unavailable").hidden = true;
    document.getElementById("checkout-status").textContent =
      "Enter your donation amount and payment details on the payment provider’s checkout page.";
  }
}
