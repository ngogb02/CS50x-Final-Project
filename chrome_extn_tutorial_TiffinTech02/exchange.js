async function fetchData() {
    // User inputed amount of base currency
    const amount = document.getElementById('amount');

    // User selected base currency 
    const baseCurrency = document.getElementById('baseCurrency');

    // User selected forex currency 
    const forexCurrency = document.getElementById('forexCurrency');

    // User Button (should trigger API call on click)
    const convert = document.getElementById('convert');

    // Dispplay result from API to this element
    const result = document.getElementById('result');

    convert.addEventListener('click', async () => {
        const amountTotal = amount.value;
        const selectedBaseCurrency = baseCurrency.value;
        const selectedForexCurrency = forexCurrency.value;
        
        console.log('base currency:', baseCurrency);
        console.log('forex currency:', forexCurrency);

        const baseUrl = 'https://crypto-market-prices.p.rapidapi.com/currencies/convert';
        const url = `${baseUrl}?from=${selectedBaseCurrency}&to=${selectedForexCurrency}&amount=${amountTotal}`;
        console.log('url', url);

        const options = {
            method: 'GET',
            headers: {
                'x-rapidapi-key': '2298de7d8bmshc01524c106fb916p177002jsn1fc4bae4c3f6',
                'x-rapidapi-host': 'crypto-market-prices.p.rapidapi.com'
            }
        };
        
        try {
            const response = await fetch(url, options);
            const record = await response.json();
            console.log('record', record);

            if (record.data) {
                document.getElementById("result").innerHTML = record.data.value
            } else {
                console.error('No data property found in the record');
                document.getElementById("result").innerHTML = 'No exchange rate data found';
            }

        } catch (error) {
            console.error('Error fetching data:', error);
            document.getElementById("result").innerHTML = 'Failed to fetch exchange rate data.';
        }

    })
}
fetchData();

