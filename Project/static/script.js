// Retrieve cart from localStorage or initialize
let cart = JSON.parse(localStorage.getItem('cart')) || {};

// ✅ Add item to cart with price
function addToCart(itemName, price) {
  if (cart[itemName]) {
    cart[itemName].quantity += 1;
  } else {
    cart[itemName] = { quantity: 1, price: price };
  }

  localStorage.setItem('cart', JSON.stringify(cart));
  alert(`${itemName} has been added to your cart.`);
}

// ✅ Add to cart and redirect to /cart
function addToCartAndRedirect(itemName, price) {
  addToCart(itemName, price);
  window.location.href = "/cart";
}

// ✅ Remove an item from the cart
function removeFromCart(itemName) {
  if (cart[itemName]) {
    delete cart[itemName];
    localStorage.setItem('cart', JSON.stringify(cart));
  }
  // Optional: if this function is used inside cart.html, refresh display:
  if (typeof loadCart === 'function') {
    loadCart();
  }
}

// ✅ Clear entire cart (used after successful checkout)
function clearCart() {
  localStorage.removeItem('cart');
}

