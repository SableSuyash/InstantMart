document.addEventListener("DOMContentLoaded", function() {
    // Calling the element.
    var $slogan = document.getElementById("slogan");

    // Setting an array with several strings.
    var sloganArray = [
        '"Because Who Has Time for Grocery Lines?"',
        '"Fresh Groceries in a Flash!"',
        '"Skip the Trip, Click for a Zip!"',
        '"InstantMart: Groceries Without the Groan!"',
        '"Speedy Delivery, Zero Calories!"',
        '"'+"Your Pantry's Secret Weapon!"+'"',
        '"'+"The Only Line You'll Cross is the Checkout Line!"+'"',
        '"Groceries Without the Dirty Looks!"',
        '"Stock Up Before the Next Disaster!"',
        '"Because Parking Lots are War Zones!"'
    ];

    // Setting variable to control the index.
    var sloganIndex = 0;

    /* This function (only when called) replaces the text of the element called before with text contained on the strings of the array, each time incrementing one and going through every array position. */
    function changeSlogan() {
        $slogan.classList.remove('fadeInUp');
        $slogan.classList.add('fadeOutUp');

        setTimeout(() => {
            $slogan.innerHTML = sloganArray[sloganIndex];
            $slogan.classList.add('fadeInUp');
            $slogan.classList.remove('fadeOutUp');

            ++sloganIndex;
            if (sloganIndex >= sloganArray.length) {
                sloganIndex = 0;
            }
        }, 500); // Match this with your CSS animation duration (0.5s)
    }

    // Initial call to set the first slogan and start the loop
    changeSlogan();
    setInterval(changeSlogan, 4000);
});

function updateQuantity(pk, action) {
    fetch(`/cart/update/${pk}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: new URLSearchParams({
            'action': action
        })
    }).then(response => {
        if (response.ok) {
            location.reload();
        }
    });
}

document.querySelector('.close').addEventListener('click',function(){
    this.parentElement.remove();
});