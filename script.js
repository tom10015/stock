const BACKEND_URL = "https://stock-wwd3.onrender.com";

const symbols = [
  "CLSK","SOFI","ASST",
  "AAPL","MSFT","TSLA","NVDA","META","AMZN","GOOGL",
  "AMD","INTC","PLTR","RIVN","LCID","F","BAC","JPM","T","KO",
  "DIS","NIO","COIN","SNAP","UBER","LYFT","SHOP","SQ","PYPL",
  "CVNA","WBD","HOOD","MARA","RIOT","DKNG","SPY","QQQ"
];

// add more up to 100 if you want

async function loadData() {
  const body = document.getElementById("tableBody");
  body.innerHTML = "<tr><td colspan='7'>Loading...</td></tr>";

  const res = await fetch(`${BACKEND_URL}/api/top`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({symbols})
  });

  const data = await res.json();
  body.innerHTML = "";

  data.forEach(stock => {
    const isHighlight = ["CLSK","SOFI","ASST"].includes(stock.symbol);

    const row = document.createElement("tr");
    if (isHighlight) row.classList.add("highlight");

    row.innerHTML = `
      <td>${stock.symbol}</td>
      <td>${stock.stockPrice ?? "N/A"}</td>
      <td>${stock.expirationDate ?? "N/A"}</td>
      <td>${stock.strike ?? "N/A"}</td>
      <td>${stock.bid ?? "N/A"}</td>
      <td>${stock.volume ?? "N/A"}</td>
      <td>${stock.openInterest ?? "N/A"}</td>
    `;

    body.appendChild(row);
  });
}

loadData();
