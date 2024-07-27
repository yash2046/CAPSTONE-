document.addEventListener("DOMContentLoaded", function() {
    const newSection = document.getElementById("new-section");
    const submenu = newSection.querySelector(".submenu");

    newSection.addEventListener("mouseenter", function() {
        submenu.style.display = "block";
    });

    newSection.addEventListener("mouseleave", function() {
        submenu.style.display = "none";
    });

    document.addEventListener("click", function(event) {
        if (!submenu.contains(event.target)) {
            submenu.style.display = "none";
        }
    });
});

function updateBtcPrice() {
    fetch("https://api.coindesk.com/v1/bpi/currentprice.json")
        .then(response => response.json())
        .then(data => {
            const btcPrice = data.bpi.USD.rate;
            document.getElementById("btc-price").textContent = btcPrice;
        })
        .catch(error => {
            console.error("Error fetching Bitcoin price:", error);
        });
}

function updateNiftyPrice() {
    fetch("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=^NSEI&interval=1min&apikey=${apiKey}")
        .then(response => response.json())
        .then(data => {
            const niftyPrice = data.quoteResponse.result[0].regularMarketPrice;
            document.getElementById("nifty-price").textContent = niftyPrice;
        })
        .catch(error => {
            console.error("Error fetching Nifty 50 value:", error);
        });
}

updateBtcPrice();
updateNiftyPrice();