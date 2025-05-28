
document.addEventListener('DOMContentLoaded', function () {
    const detailsElements = document.querySelectorAll('details');

    detailsElements.forEach(detailsEl => {
        detailsEl.addEventListener('toggle', function () {
            // Check if the <details> element is now closed
            if (!this.open) {
                // Find the bootstrap collapse button inside the <detail> element that was just closed.
                const collapseButton = this.querySelector('button[data-bs-toggle="collapse"]');

                // Was a button found?
                if (collapseButton) {
                    // Assuming the button was found, then we need to see which image container it's supposed to control.
                    // The button has an attribute to it called 'data-bs-target' that tells us the ID of the image container. 
                    const targetId = collapseButton.getAttribute('data-bs-target');

                    // Did the button have that ID?
                    if (targetId) {
                        // Find the actual image container on the page using the targetID.
                        const collapseTarget = document.querySelector(targetId);

                        // Did we find the image container AND is it currently visible/open?
                        if (collapseTarget && collapseTarget.classList.contains('show')) {
                            // Set the button's aria-expanded to false
                            collapseButton.setAttribute('aria-expanded', 'false');
                            // Remove the 'show' class from the target to collapse it
                            collapseTarget.classList.remove('show');
                        }
                    }
                }
            }
        });
    });
});