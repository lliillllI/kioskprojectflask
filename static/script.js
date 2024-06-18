function navigateTo(path) {
    saveCartData();
    window.location.href = path;
}

function navigateToPay2(path) {
    if (isCartEmpty()) {
        alert('카트에 담긴 제품이 없습니다.');
        return;
    }
    saveCartData2();
    window.location.href = path;
}

function navigateToPay(path) {
    if (isCartEmpty()) {
        alert('카트에 담긴 제품이 없습니다.');
        return;
    }
    saveCartData();
    window.location.href = path;
}

function isCartEmpty() {
    const cartList = document.getElementById('cart-list');
    return cartList.children.length === 0;
}


// 장바구니 데이터 저장
function saveCartData() {
    const cartItems = document.querySelectorAll('#cart-list .cart-item');
    const cartData = [];

    cartItems.forEach(item => {
        const name = item.getAttribute('data-name');
        const price = item.getAttribute('data-price-hidden');
        const image = item.getAttribute('data-image');
        const idx = item.getAttribute('data-idx');
        let quantity = item.querySelector('.quantity').textContent;
        cartData.push({ name, price, image, quantity, idx });
    });

    sessionStorage.setItem('cartData', JSON.stringify(cartData));
}

function saveCartData2(){
            const cartItems = document.querySelectorAll('#boardlist tbody .cart-item');
            const cartData = [];
            cartItems.forEach(item => {
                const name = item.getAttribute('data-name');
                const price = item.getAttribute('data-price-hidden');
                const image = item.getAttribute('data-image');
                const idx = item.getAttribute('data-idx');
                let quantity = item.querySelector('.quantity').textContent;
                cartData.push({ name, price, image, quantity, idx });
            });
            sessionStorage.setItem('cartData', JSON.stringify(cartData));
}



// 장바구니 데이터 로드
function loadCartData() {
    const cartData = JSON.parse(sessionStorage.getItem('cartData')) || [];

    cartData.forEach(item => {
        addToCart(item.name, item.price, item.image, item.quantity, item.idx);
    });
}

function updateCartData() {
    saveCartData();
    updateTotalPrice();
}

function updateCartData2() {
    saveCartData2();
    updateTotalPrice2();
}

document.addEventListener('DOMContentLoaded', function() {
    loadCartData();
    document.querySelectorAll('.product').forEach(item => {
        item.addEventListener('click', function() {
            const productName = this.getAttribute('data-name');
            const productPrice = this.getAttribute('data-price');
            const productImage = this.getAttribute('data-image');
            const productIdx = this.getAttribute('data-idx');
            const modal = document.getElementById('confirmationModal');

            if (prediction == 2) {
                if (modal == null){
                    addToCart(productName, productPrice, productImage, 1, productIdx);
                }
                else{
                    showModal(productName, productPrice, productImage, productIdx);
                }
            } else {
                addToCart(productName, productPrice, productImage, 1, productIdx);
            }
        });
    });


    const closeBtn = document.querySelector('.close_btn')
    if(closeBtn != null){
        closeBtn.addEventListener('click', function(){
            document.querySelector('.modalpop').style.display = 'none';
        })
    };

});

function calculateTotalPrice() {
    const cartItems = document.querySelectorAll('#cart-list .cart-item');
    let totalPrice = 0;

    cartItems.forEach(item => {
        const price = parseInt(item.getAttribute('data-price-hidden'));
        let quantity = parseInt(item.querySelector('.quantity').textContent);
        totalPrice += price * quantity;
    });

    return totalPrice;
}

function updateTotalPrice() {
    const totalPriceElement = document.getElementById('total-price');
    const totalPrice = calculateTotalPrice();
    totalPriceElement.textContent = `결제 금액: ${totalPrice}원`;
}


function calculateTotalPrice2() {
    const cartItems = document.querySelectorAll('#boardlist tbody .cart-item');
    let totalPrice = 0;

    cartItems.forEach(item => {
        const price = parseInt(item.getAttribute('data-price-hidden'));
        let quantity = parseInt(item.querySelector('.quantity').textContent);
        totalPrice += price * quantity;
    });

    return totalPrice;
}

function updateTotalPrice2() {
    const totalPriceElement = document.getElementById('total-price');
    const totalPrice = calculateTotalPrice2();
    totalPriceElement.textContent = `결제 금액: ${totalPrice}원`;
}


function addToCart(name, price, image, quantity = 1, idx) {
    const cartList = document.getElementById('cart-list');
    let isProductAdded = false;

    document.querySelectorAll('#cart-list .cart-item').forEach(item => {
        if (item.getAttribute('data-name') === name) {
            isProductAdded = true;
            let quantityElement = item.querySelector('.quantity');
            let newQuantity = parseInt(quantityElement.textContent) + parseInt(quantity);
            quantityElement.textContent = newQuantity.toString();
            // 총 가격 업데이트
            item.querySelector('.product-price').textContent = `${parseInt(price) * newQuantity}`;
            updateCartData();
        }
    });

    if (!isProductAdded) {
        const listItem = document.createElement('div');
        listItem.setAttribute('class', 'cart-item');
        listItem.setAttribute('data-name', name);
        listItem.setAttribute('data-price-hidden', price);
        listItem.setAttribute('data-image', image);
        listItem.setAttribute('data-idx', idx);
        listItem.innerHTML = `
          <img src="data:image/jpeg;base64,${image}" alt="Product Image" class="cart-item-image">
          <div class="product-info">
            <p class="product-name">${name}</p>
            <p class="product-price">${price * quantity}</p>
            <div class="quantity-controls">
                <button class="minus-btn">-</button>
                <span class="quantity">${quantity}</span>
                <button class="plus-btn">+</button>
            </div>
            <button class="delete-btn">삭제</button>
          </div>
        `;

        const deleteBtn = listItem.querySelector('.delete-btn');
        deleteBtn.addEventListener('click', function() {
            this.parentElement.parentElement.remove();
            updateCartData();
        });

        const plusBtn = listItem.querySelector('.plus-btn');
        plusBtn.addEventListener('click', function() {
            let quantityElement = this.parentElement.querySelector('.quantity');
            let newQuantity = parseInt(quantityElement.textContent) + 1;
            quantityElement.textContent = newQuantity.toString();
            // 총 가격 업데이트
            let totalPrice = this.parentElement.parentElement.querySelector('.product-price');
            let priceHidden = this.parentElement.parentElement.parentElement.getAttribute('data-price-hidden');
            totalPrice.textContent = `${parseInt(priceHidden) * newQuantity}`;
            updateCartData();
        });

        const minusBtn = listItem.querySelector('.minus-btn');
        minusBtn.addEventListener('click', function() {
            let quantityElement = this.parentElement.querySelector('.quantity');
            let newQuantity = parseInt(quantityElement.textContent) - 1;
            if (newQuantity > 0) {
                quantityElement.textContent = newQuantity.toString();
                // 총 가격 업데이트
                let totalPrice = this.parentElement.parentElement.querySelector('.product-price');
                let priceHidden = this.parentElement.parentElement.parentElement.getAttribute('data-price-hidden');
                totalPrice.textContent = `${parseInt(priceHidden) * newQuantity}`;
                updateCartData();
            } else {
                this.parentElement.parentElement.parentElement.remove();
                updateCartData();
            }
        });

        cartList.appendChild(listItem);
        updateCartData();
    }
}




let timeLeft = 60;
let timerId = null;

function startTimer() {
    if (timerId !== null) {
        return; // 타이머가 이미 실행 중이면 중복 시작을 방지
    }
    timerId = setInterval(() => {
        timeLeft--;
        document.getElementById('timer').textContent = timeLeft;
        if (timeLeft === 0) {
            resetSessionAndRedirect(); // 시간 초과 시 페이지 초기화 함수 호출
        }
    }, 1000);
}

function resetTimer() {
    clearInterval(timerId);
    timeLeft = 60;
    document.getElementById('timer').textContent = timeLeft;
    timerId = null;
    startTimer();
}

function resetSessionAndRedirect() {
    sessionStorage.clear();
    window.location.href = '/';
}


function saveToDB() {
  const cartData = JSON.parse(sessionStorage.getItem('cartData')) || [];
  const custnum = sessionStorage.getItem('custnum');
  fetch('/save', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ cartData: cartData, custnum: custnum })
  })
  .then(response => {
    // 요청 성공 시 처리
    console.log('Data saved successfully!');
    sessionStorage.clear();
    window.location.href = '/finish';
  })
  .catch(error => {
    // 요청 실패 시 처리
    console.error('Error saving data:', error);
  });
}

function addToCartInTable(name, price, image, quantity = 1, idx) {
    const cartList2 = document.querySelector('#boardlist tbody');
    const newRow = document.createElement('tr');
    newRow.setAttribute('class', 'cart-item');
    newRow.setAttribute('data-name', name);
    newRow.setAttribute('data-price-hidden', price);
    newRow.setAttribute('data-image', image);
    newRow.setAttribute('data-idx', idx);
    newRow.innerHTML = `
            <td class="item_image"><img src="data:image/jpeg;base64,${image}" style="width: 100px; height: 100px;"></td>
            <td class="item_name">${name}</td>
            <td class="item_quantity">
                <button class="minus-btn"><span class="minus">-</span></button>
                <span class="quantity">${quantity}</span>
                <button class="plus-btn"><span class="plus">+</span></button>
            </td>
            <td class="item_price">${price * quantity}</td>
            <td><button class="delete-btn">삭제</button></td>
    `;

    const deleteBtn = newRow.querySelector('.delete-btn');
    deleteBtn.addEventListener('click', function() {
        this.parentElement.parentElement.remove();
        updateCartData2();


    });

    const plusBtn = newRow.querySelector('.plus-btn');
    plusBtn.addEventListener('click', function() {
        let quantityElement = this.parentElement.querySelector('.quantity');
        let newQuantity = parseInt(quantityElement.textContent) + 1;
        quantityElement.textContent = newQuantity.toString();
        // 총 가격 업데이트
        let totalPrice = this.parentElement.parentElement.querySelector('.item_price');
        let priceHidden = this.parentElement.parentElement.getAttribute('data-price-hidden');
        totalPrice.textContent = `${parseInt(priceHidden) * newQuantity}`;
        updateCartData2();
    });

    const minusBtn = newRow.querySelector('.minus-btn');
    minusBtn.addEventListener('click', function() {
        let quantityElement = this.parentElement.querySelector('.quantity');
        let newQuantity = parseInt(quantityElement.textContent) - 1;
        if (newQuantity > 0) {
            quantityElement.textContent = newQuantity.toString();
            // 총 가격 업데이트
            let totalPrice = this.parentElement.parentElement.querySelector('.item_price');
            let priceHidden = this.parentElement.parentElement.getAttribute('data-price-hidden');
            totalPrice.textContent = `${parseInt(priceHidden) * newQuantity}`;
            updateCartData2();
        } else {
            this.parentElement.parentElement.remove();
            updateCartData2();
        }
    });

    cartList2.appendChild(newRow);
    updateCartData2();
}

    function filterProducts(type) {
        const allProducts = document.querySelectorAll('.product');
        allProducts.forEach(product => {
            const productType = product.getAttribute('data-type');
            if (type === 'all' || productType === type) {
                product.style.display = 'block';
            } else {
                product.style.display = 'none';
            }
        });
    }

window.onload = function() {
    filterProducts('all');
};


function showModal(productName, productPrice, productImage, productIdx) {
    const modal = document.getElementById('confirmationModal');
    const confirmButton = document.getElementById('confirmAddToCart');
    const cancelButton = document.getElementById('cancelAddToCart');
    const closeButton = document.querySelector('.close-button');
    const modalText = document.getElementById('modaltext');
    const modalimg = document.getElementById('modalimg');
    modalimg.innerHTML=`<img src="data:image/jpeg;base64,${productImage}" style="width: 300px; height: 300px;">`

    modalText.textContent = `${productName}가 담겼습니다`;

    modal.style.display = 'block';

    confirmButton.onclick = function() {
        addToCart(productName, productPrice, productImage, 1, productIdx);
        modal.style.display = 'none';
    };

    cancelButton.onclick = function() {
        modal.style.display = 'none';
    };

    closeButton.onclick = function() {
        modal.style.display = 'none';
    };

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    };
}