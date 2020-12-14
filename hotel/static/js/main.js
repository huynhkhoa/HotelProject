function addToCart(roomdetailId, roomdetailName, price) {
    fetch('/api/cart', {
        method: 'POST',
        body: JSON.stringify({
            "id": roomdetailId,
            "name": roomdetailName,
            "price": price
        }),
        headers: {
            "Content-Type": 'application/json'
        }
    }).then(res => res.json()).then(data => {
        var cart = document.getElementById('cart-stats');
        cart.innerText = `${data.total_quantity} - ${data.total_amount} VNĐ`
    })
}

function pay() {
    fetch('/payment', {
        method: 'POST',
        headers: {
            "Content-Type": 'application/json'
        }
    }).then(res => res.json()).then(data => {
        alert(data.message);
    }).catch(res => {
        console.log(res);
    })
}