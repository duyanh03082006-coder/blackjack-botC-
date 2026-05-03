import streamlit.components.v1 as components

html_code = """
<style>
.container {
  display: flex;
  gap: 20px;
}

.column {
  flex: 1;
  min-height: 200px;
  border: 2px dashed #ccc;
  padding: 10px;
  border-radius: 10px;
}

.card {
  display: inline-block;
  padding: 10px;
  margin: 5px;
  background: #eee;
  border-radius: 8px;
  cursor: grab;
}
</style>

<div class="container">
  <div>
    <h4>🃏 Cards</h4>
    <div id="cards">
      <div class="card" draggable="true">2</div>
      <div class="card" draggable="true">3</div>
      <div class="card" draggable="true">4</div>
      <div class="card" draggable="true">5</div>
      <div class="card" draggable="true">6</div>
      <div class="card" draggable="true">7</div>
      <div class="card" draggable="true">8</div>
      <div class="card" draggable="true">9</div>
      <div class="card" draggable="true">10</div>
      <div class="card" draggable="true">J</div>
      <div class="card" draggable="true">Q</div>
      <div class="card" draggable="true">K</div>
      <div class="card" draggable="true">A</div>
    </div>
  </div>

  <div class="column" id="player">🧑 Player</div>
  <div class="column" id="dealer">🎩 Dealer</div>
  <div class="column" id="seen">🧾 Seen</div>
</div>

<script>
let dragged;

document.querySelectorAll('.card').forEach(card => {
  card.addEventListener('dragstart', e => {
    dragged = e.target.innerText;
  });
});

document.querySelectorAll('.column').forEach(col => {
  col.addEventListener('dragover', e => e.preventDefault());

  col.addEventListener('drop', e => {
    e.preventDefault();
    const newCard = document.createElement("div");
    newCard.className = "card";
    newCard.innerText = dragged;
    col.appendChild(newCard);

    // gửi dữ liệu về Streamlit
    window.parent.postMessage({
      type: "streamlit:setComponentValue",
      value: {card: dragged, target: col.id}
    }, "*");
  });
});
</script>
"""

result = components.html(html_code, height=400)