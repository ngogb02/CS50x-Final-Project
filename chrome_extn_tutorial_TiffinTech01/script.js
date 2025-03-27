async function fetchData() {
    const url = 'https://concerts-artists-events-tracker.p.rapidapi.com/location?name=Paris&minDate=2025-03-31&maxDate=2025-04-04&page=1';
    const options = {
        method: 'GET',
        headers: {
            'x-rapidapi-key': '2298de7d8bmshc01524c106fb916p177002jsn1fc4bae4c3f6',
            'x-rapidapi-host': 'concerts-artists-events-tracker.p.rapidapi.com'
        }
    };
    
    try {
        const response = await fetch(url, options);
        const record = await response.json();
        console.log('record', record);

        if (record.data) {
            document.getElementById("concerts").innerHTML = record.data.map(item => `<li>${item.name}</li>`).join('');
        } else {
            console.error('No data property found in the record');
            document.getElementById("concerts").innerHTML = 'No concert data available';
        }
    } catch (error) {
        console.error('Error fetching data:', error);
        document.getElementById("concerts").innerHTML = 'Failed to fetch concert data.';
    }
}
fetchData();