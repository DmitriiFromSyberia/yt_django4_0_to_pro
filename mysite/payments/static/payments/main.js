// static/main.js

console.log("Sanity check!");

// Get Stripe publishable key
//var productId = submitBtn.getAttribute('data-product-id');

fetch("http://localhost:8000/payments/config/")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);

  // new
  // Event handler
  document.querySelector("#submitBtn").addEventListener("click", () => {
    // Get Checkout Session ID
    var index= submitBtn.getAttribute('data-product-id');
    var path="http://localhost:8000//payments/create-checkout-session/"+String(index)+"/";
    fetch(path)
    .then((result) => { return result.json(); })
    .then((data) => {
      console.log(data);
      // Redirect to Stripe Checkout
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
      console.log(res);
    });
  });
});