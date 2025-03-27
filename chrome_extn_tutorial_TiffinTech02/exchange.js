async function fetchData() {
    const amount = document.getElementById('amount');
    const currency = document.getElementById('currency');
    const convert = document.getElementById('convert');
    const result = document.getElementById('result');

    const API_KEY="2298de7d8bmshc01524c106fb916p177002jsn1fc4bae4c3f6"
    const API_HOST="currency-conversion-and-exchange-rates.p.rapidapi.com"
    const apiURL="https://currency-conversion-and-exchange-rates.p.rapidapi.com/latest?from=USD&to=EUR%2CGBP"

    convert.addEventListener('click', async () => {
        const amountTotal = amount.value;
        const currencyTotal = currency.value;
        // const url = apiURL + currencyTotal;
        const url = apiURL
        console.log('url', url);

        const options = {
            method: 'GET',
            headers: {
                'x-rapidapi-key': '2298de7d8bmshc01524c106fb916p177002jsn1fc4bae4c3f6',
                'x-rapidapi-host': 'currency-conversion-and-exchange-rates.p.rapidapi.com'
            }
        };
        
        try {
            const response = await fetch(url, options);
            const result = await response.json();
            console.log('result', result);
            
            if (result.rates) {
                
            } else {
                console.error('No data property found in the record');
                document.getElementById("result").innerHTML = 'failed';
            }

        } catch (error) {
            console.error('Error fetching data:', error);
            document.getElementById("result").innerHTML = 'Failed to fetch exchange rate data.';
        }

    })
}
fetchData();

// .then(response => response.json())
        // .then(data => {
        //     const rate = data.rates['currencyTotal'];
        //     console.log('rate', rate);
        //     const resultPrice = amountTotal * rate;
        //     result.innerHTML = `${amountTotal} ${currencyTotal} = ${resultPrice.toFixed(2)} USD`;
        // })
        // .catch(error => {
        //     console.error('Request failed:', error);
        //     result.innerHTML = 'An error occured, please try again later.'
        // })