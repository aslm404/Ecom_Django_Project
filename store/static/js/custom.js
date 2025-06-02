$(document).ready(function () {

    // --- AJAX POST Wrapper ---
    function postAjaxRequest(url, data, successCallback) {
        $.ajax({
            method: "POST",
            url: url,
            data: data,
            success: successCallback,
            error: function (xhr) {
                console.error(xhr.responseText);
            }
        });
    }

    // --- Quantity Increment ---
    $('.increment-btn').click(function (e) {
        e.preventDefault();
        let $data = $(this).closest('.product_data');
        let $qtyInput = $data.find('.qty-input');
        let maxQty = parseInt($qtyInput.attr('max')) || 10;
        let qty = parseInt($qtyInput.val()) || 1;

        if (qty < maxQty) {
            qty += 1;
            $qtyInput.val(qty);
            updateCartQty($data, qty);  // 🔄 Call backend update
        }
    });

    // --- Quantity Decrement ---
    $('.decrement-btn').click(function (e) {
        e.preventDefault();
        let $data = $(this).closest('.product_data');
        let $qtyInput = $data.find('.qty-input');
        let qty = parseInt($qtyInput.val()) || 1;

        if (qty > 1) {
            qty -= 1;
            $qtyInput.val(qty);
            updateCartQty($data, qty);  // 🔄 Call backend update
        }
    });  

    // --- Add to Cart ---
    $('.btn-add-to-cart').click(function (e) {
        e.preventDefault();
        let $data = $(this).closest('.product_data');
        let url = $('#add-to-cart-url').val();
        let payload = {
            product_id: $data.find('.prod_id').val(),
            product_qty: $data.find('.qty-input').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        };
        postAjaxRequest(url, payload, function (response) {
            alertify.success(response.status);
        });
    });

    // --- Delete Cart Item ---
    $('.btn-delete-cart-item').click(function (e) {
        e.preventDefault();
        let $button = $(this);
        let $data = $button.closest('.product_data');

        let payload = {
            product_id: $data.find('.prod_id').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        };

        postAjaxRequest("/store/delete-cart-item/", payload, function (response) {
            alertify.success(response.status);

            // Remove the item DOM element directly
            $data.fadeOut(300, function () {
                $(this).remove();
            });

            // Then reload only totals if needed
            $('.cart-summary').load(location.href + " .cart-summary");
        });
    });


    // --- Wishlist Add ---
    $('.btn-add-to-wishlist').click(function (e) {
        e.preventDefault();
        let $data = $(this).closest('.product_data');
        let productId = $data.find('.prod_id').val();
        let payload = {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        };

        postAjaxRequest(`/store/add-to-wishlist/${productId}/`, payload, function (response) {
            alertify.success(response.status);
        });
    });


    // --- Wishlist Delete ---
    $('.btn-delete-wishlist-item').click(function (e) {
        e.preventDefault();
        let $data = $(this).closest('.product_data');
        let payload = {
            product_id: $data.find('.prod_id').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        };

        postAjaxRequest("/store/delete-wishlist-item/", payload, function (response) {
            alertify.success(response.status);

            $data.fadeOut(300, function () {
                $(this).remove();
            });
        });
    });

});
