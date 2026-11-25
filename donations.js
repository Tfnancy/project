// Set this to the public HTTPS checkout URL issued to the home's payment account.
const donationCheckout = "";

const amount = document.getElementById("amount");
for (const button of document.querySelectorAll("[data-amount]")) {
  button.addEventListener("click", () => {
    amount.value = button.dataset.amount;
    amount.focus();
  });
}

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
