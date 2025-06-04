document.addEventListener('click', function(event) {
    // Check if the clicked element is a delete button
    if (event.target && event.target.matches('.delete-button')) {
        const forecastId = event.target.dataset.id;

        // Find the closest <details> element containing this button
        const detailsElement = event.target.closest('details');

        // Ensure the <details> element exists before trying to remove it
        if (detailsElement) {
            detailsElement.remove();
            console.log(`Deleted <details> with forecast id: ${forecastId}`);
        }
        else 
        {
            console.warn(`No matching <details> found for forecast id: ${forecastId}`);
        }

        fetch("/api/delete_forecast", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ id: forecastId}) // Send the id as JSON
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Server responded with ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Delete successfully:', data);
        });
    }

});