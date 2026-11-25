// Set this to the public HTTPS checkout URL issued to the home's payment account.
const donationCheckout = "";

const amount = document.getElementById("amount");
const presets = document.querySelectorAll("[data-amount]");

function updatePresets() {
  for (const button of presets) {
    button.setAttribute("aria-pressed", String(button.dataset.amount === amount.value));
  }
}

for (const button of presets) {
  button.addEventListener("click", () => {
    amount.value = button.dataset.amount;
    updatePresets();
  });
}
amount.addEventListener("input", updatePresets);
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
