function navigateTo(path) {
    saveCartData();
    window.location.href = path;
}

// 장바구니 데이터 저장
function saveCartData() {
    const cartItems = document.querySelectorAll('#cart-list .cart-item');
    const cartData = [];

    cartItems.forEach(item => {
        const name = item.getAttribute('data-name');
        const price = item.getAttribute('data-price-hidden');
        const image = item.getAttribute('data-image');
        let quantity = item.querySelector('.quantity').textContent;
        cartData.push({ name, price, image, quantity });
    });

    sessionStorage.setItem('cartData', JSON.stringify(cartData));
}

// 장바구니 데이터 로드
function loadCartData() {
    const cartData = JSON.parse(sessionStorage.getItem('cartData')) || [];

    cartData.forEach(item => {
        addToCart(item.name, item.price, item.image, item.quantity);
    });
}

function updateCartData() {
    saveCartData();
    updateTotalPrice();
}

document.addEventListener('DOMContentLoaded', function() {
    loadCartData();

    document.querySelectorAll('.product').forEach(item => {
        item.addEventListener('click', function() {
            const productName = this.getAttribute('data-name');
            const productPrice = this.getAttribute('data-price');
            const productImage = this.getAttribute('data-image');
            addToCart(productName, productPrice, productImage);
        });
    });


    const closeBtn = document.querySelector('.close_btn')
    if(closeBtn != null){
        closeBtn.addEventListener('click', function(){
            document.querySelector('.modal').style.display = 'none';
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



function addToCart(name, price, image, quantity = 1) {
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
        deleteBtn.onclick = function() {
            this.parentElement.parentElement.remove();
            updateCartData();
        };

        const plusBtn = listItem.querySelector('.plus-btn');
        plusBtn.onclick = function() {
            let quantityElement = this.parentElement.querySelector('.quantity');
            let newQuantity = parseInt(quantityElement.textContent) + 1;
            quantityElement.textContent = newQuantity.toString();
            // 총 가격 업데이트
            let totalPrice = this.parentElement.parentElement.querySelector('.product-price');
            let priceHidden = this.parentElement.parentElement.parentElement.getAttribute('data-price-hidden');
            totalPrice.textContent = `${parseInt(priceHidden) * newQuantity}`;
            updateCartData();
        };

        const minusBtn = listItem.querySelector('.minus-btn');
        minusBtn.onclick = function() {
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
        };

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