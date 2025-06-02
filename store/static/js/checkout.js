$(document).ready(function () {
    $('.paywithrazorpay').click(function (e) {
        e.preventDefault();

        let firstname = $("[name='firstname']").val();
        let lastname = $("[name='lastname']").val();
        let email = $("[name='email']").val();
        let phone = $("[name='phone']").val();
        let address = $("[name='address']").val();
        let city = $("[name='city']").val();
        let state = $("[name='state']").val();
        let country = $("[name='country']").val();
        let pinCode = $("[name='pinCode']").val();
        let token = $("[name='csrfmiddlewaretoken']").val();
        let razorpayKey = $(this).data("rzp-key");

        // Validate fields
        if (!firstname || !lastname || !email || !phone || !address || !city || !state || !country || !pinCode) {
            swal("Alert!", "All fields are mandatory!", "error");
            return false;
        }

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const phoneRegex = /^[6-9]\d{9}$/;

        if (!emailRegex.test(email)) {
            swal("Invalid Email!", "Please enter a valid email address.", "error");
            return false;
        }

        if (!phoneRegex.test(phone)) {
            swal("Invalid Phone!", "Enter a valid 10-digit mobile number.", "error");
            return false;
        }

        $.ajax({
            type: "GET",
            url: "/proceed-to-pay/",
            success: function (response) {
                let options = {
                    "key": razorpayKey,
                    "amount": Math.round(parseFloat(response.total_price) * 100),
                    "currency": "INR",
                    "name": "Electrolyze",
                    "description": "Thank you for buying from us",
                    "image": "https://example.com/your_logo",
                    "handler": function (responseb) {
                        let data = {
                            firstname,
                            lastname,
                            email,
                            phone,
                            address,
                            city,
                            state,
                            country,
                            pinCode,
                            payment_mode: "Paid by Razorpay",
                            payment_id: responseb.razorpay_payment_id,
                            csrfmiddlewaretoken: token
                        };

                        $.ajax({
                            method: "POST",
                            url: "/place-order",
                            data: data,
                            success: function (responsec) {
                                swal("Congratulations!", responsec.status, "success")
                                    .then(() => window.location.href = '/my-orders');
                            },
                            error: function () {
                                swal("Order Failed!", "Something went wrong while placing your order.", "error");
                            }
                        });
                    },
                    "prefill": {
                        name: `${firstname} ${lastname}`,
                        email: email,
                        contact: phone
                    },
                    "theme": {
                        color: "#3399cc"
                    }
                };

                let rzp1 = new Razorpay(options);
                rzp1.open();
            },
            error: function (xhr) {
                console.error(xhr.responseText);
                swal("Error!", "Could not proceed to payment.", "error");
            }
        });
    });
});