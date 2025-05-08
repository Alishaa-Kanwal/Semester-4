let priceChart;
const ctx = document.getElementById('priceChart').getContext('2d');
const currencySelector = document.getElementById('currencySelector');
const searchInput = document.getElementById('searchInput');
const intervalButtons = document.querySelectorAll('.interval-buttons button');

let coinsList = [];
let selectedCoinId = 'bitcoin';
let selectedInterval = '1';

async function fetchCoinsList() {
  const response = await fetch('https://api.coingecko.com/api/v3/coins/list');
  coinsList = await response.json();
  populateCurrencySelector(coinsList);
}

function populateCurrencySelector(coins) {
  currencySelector.innerHTML = '';
  coins.forEach(coin => {
    const option = document.createElement('option');
    option.value = coin.id;
    option.textContent = `${coin.name} (${coin.symbol.toUpperCase()})`;
    currencySelector.appendChild(option);
  });
  currencySelector.value = selectedCoinId;
}

searchInput.addEventListener('input', () => {
  const query = searchInput.value.toLowerCase();
  const filteredCoins = coinsList.filter(coin =>
    coin.name.toLowerCase().includes(query) || coin.symbol.toLowerCase().includes(query)
  );
  populateCurrencySelector(filteredCoins);
});

currencySelector.addEventListener('change', () => {
  selectedCoinId = currencySelector.value;
  fetchAndRenderChart();
});

intervalButtons.forEach(button => {
  button.addEventListener('click', () => {
    selectedInterval = button.getAttribute('data-interval');
    fetchAndRenderChart();
  });
});

async function fetchAndRenderChart() {
  const response = await fetch('/get_price_data', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      coin_id: selectedCoinId,
      interval: selectedInterval
    })
  });

  const data = await response.json();
  if (!data.prices) {
    alert('Failed to fetch data.');
    return;
  }

  const timestamps = data.prices.map(p => new Date(p[0]).toLocaleString());
  const prices = data.prices.map(p => p[1]);

  if (priceChart) {
    priceChart.destroy();
  }

  priceChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: timestamps,
      datasets: [{
        label: `${selectedCoinId.toUpperCase()} Price (USD)`,
        data: prices,
        borderColor: '#00d4ff',
        fill: false,
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  });
}

window.onload = () => {
  fetchCoinsList().then(() => {
    fetchAndRenderChart();
  });
};
