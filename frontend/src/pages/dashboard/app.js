const bills = [
    { description: 'Aluguel do Imóvel', supplier: 'Imobiliária Central', dueDate:
        '24/06/2024', amount: 3500, status: 'Hoje', statusClass: 'today'},
    { description: 'Conta de Luz', supplier: 'Enel', dueDate: '28/06/2026', 
        amount: 620, status: 'Em breve', statusClass: 'soon'},
    { description: 'Fornecedor de insumos', supplier: 'Distribuidora Fit',
        dueDate: '30/06/2024', amount: 2340, status: 'Em breve', statusClass: 
        'soon'},
    { description: 'Taxas de cartão', supplier: 'Stone', dueDate: '02/07/2025', 
        amount: 1250, status: 'Em breve', statusClass: 'soon'},
    { description: 'Folha de pagamento', supplier: 'Contabilidade', dueDate: '05/07/2025', 
        amount: 4800, status: 'Agendado', statusClass: 'scheduled'},
];

const documents = [
    { icon: '▧', color: 'red', title: 'Nota Fiscal - Distribuidora Fit', meta: 
        '24/06/2025 • Insumos', amount: 1230 },
    { icon: '▤', color: 'blue', title: 'Extrato Bancário - Banco do Brasil', 
        meta: '24/06/2025 • Movimento', amount: 8450 },
    { icon: '◉', color: 'green', title: 'Comprovante PIX - Fornecedor', meta: 
        '23/06/2025 • Insumos', amount: 980 },
    { icon: '▦', color: 'purple', title: 'Boleto - Aluguel', meta: 
        '22/06/2025 • Aluguel', amount: 3500 },
    { icon: '▧', color: 'red', title: 'Nota Fiscal - Folha de pagamento', meta: 
        '20/06/2025 • Pessoal', amount: 4800 }
]

const categories = [
    { name: 'Insumos', percentage: 42, color: 'green' },
    { name: 'Pessoal', percentage: 28, color: 'blue' },
    { name: 'Aluguel', percentage: 12, color: 'yellow' },
    { name: 'Taxas', percentage: 18, color: 'red' },
    { name: 'Outros', percentage: 14, color: 'purple' }
];

// Formata números seguindo a moeda brasileira
function formatCurrency(value) {
    return value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

// Cria uma célula de tabela sem repetir o mesmo código
function createCell(text) {
    const cell = document.createElement('td');
    cell.textContent = text;
    return cell;
}

function renderBills(items = bills) {
    const body = document.querySelector('#bills-table-body');
    body.replaceChildren();

    items.forEach((bill) => {
        const row = document.createElement('tr');
        row.append(
            createCell(bill.description),
            createCell(bill.supplier),
            createCell(bill.dueDate),
            createCell(formatCurrency(bill.amount)),
        )

        const statusCell = document.createElement('td');
        const status = document.createElement('span');
        status.className = `status ${bill.statusClass}`;
        status.textContent = bill.status;
        statusCell.append(status);
        row.append(statusCell);
        body.append(row);
    });
}

function renderDocuments(items = documents) {
    const list = document.querySelector('#documents-list');
    list.replaceChildren();

    items.forEach((documentItem) => {
        const item = document.createElement('li');
        item.className = 'document-item';

        const icon = document.createElement('span');
        icon.className = `document-icon ${documentItem.color}`;
        icon.textContent = documentItem.icon;

        const info = document.createElement('span');
        info.className = 'document-info';
        const title = document.createElement('strong');
        title.textContent = documentItem.title;
        const meta = document.createElement('small');
        meta.textContent = documentItem.meta;
        info.append(title, meta);

        const amount = document.createElement('strong');
        amount.textContent = formatCurrency(documentItem.amount)
        item.append(icon, info, amount);
        list.append(item);
    });
}

function renderCategories() {
    const list = document.querySelector('#category-list');
    list.replaceChildren();

    categories.forEach((category) => {
        const item = document.createElement('li');
        const label = document.createElement('span');
        const dot = document.createElement('span');
        dot.className = `category-dot dot-${category.color}`;
        label.append(dot, document.createTextNode(category.name));
        const percentage = document.createElement('b');
        percentage.textContent = `${category.percentage}%`;
        item.append(label, percentage);
        list.append(item);
    });
}

function drawCashFlowChart() {
  const chart = document.querySelector('#cash-flow-chart');
  const entries = [105, 135, 120, 145, 125, 150, 132, 158, 143, 162, 151, 170];
  const exits = [58, 70, 66, 78, 69, 85, 73, 88, 76, 91, 79, 98];
  const width = 640;
  const height = 260;
  const padding = 12;

  // Transforma os valores do array em pontos x/y do SVG.
  function points(values) {
    return values.map((value, index) => {
      const x = padding + index * ((width - padding * 2) / (values.length - 1));
      const y = height - padding - value;
      return [x, y];
    });
  }

  function toPath(pointsArray) {
    return pointsArray.map(([x, y], index) => `${index === 0 ? 'M' : 'L'} ${x} ${y}`).join(' ');
  }

  function toArea(pointsArray) {
    const last = pointsArray.at(-1);
    const first = pointsArray[0];
    return `${toPath(pointsArray)} L ${last[0]} ${height} L ${first[0]} ${height} Z`;
  }

  const entryPoints = points(entries);
  const exitPoints = points(exits);

  chart.innerHTML = `
    <defs>
      <linearGradient id="entryFill" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stop-color="#10b995" stop-opacity=".27" /><stop offset="100%" stop-color="#10b995" stop-opacity="0" /></linearGradient>
      <linearGradient id="exitFill" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stop-color="#efa82b" stop-opacity=".18" /><stop offset="100%" stop-color="#efa82b" stop-opacity="0" /></linearGradient>
    </defs>
    ${[0, 52, 104, 156, 208].map((y) => `<line class="grid-line" x1="0" x2="${width}" y1="${y + 12}" y2="${y + 12}" />`).join('')}
    <path class="entry-area" d="${toArea(entryPoints)}" /><path class="exit-area" d="${toArea(exitPoints)}" />
    <path class="entry-line" d="${toPath(entryPoints)}" /><path class="exit-line" d="${toPath(exitPoints)}" />
    ${entryPoints.map(([x, y]) => `<circle class="chart-point" cx="${x}" cy="${y}" r="3" stroke="#0bb896" />`).join('')}
    ${exitPoints.map(([x, y]) => `<circle class="chart-point" cx="${x}" cy="${y}" r="3" stroke="#efa82b" />`).join('')}
  `;
}

function setupSearch() {
  const input = document.querySelector('#search-input');
  input.addEventListener('input', (event) => {
    const term = event.target.value.toLowerCase().trim();
    const filtered = bills.filter((bill) => `${bill.description} ${bill.supplier} ${bill.amount}`.toLowerCase().includes(term));
    renderBills(filtered);
  });
}

function setupEntryModal() {
  const dialog = document.querySelector('#entry-dialog');
  const openButton = document.querySelector('#new-entry-button');
  const form = document.querySelector('#entry-form');
  openButton.addEventListener('click', () => dialog.showModal());

  dialog.addEventListener('close', () => {
    if (dialog.returnValue !== 'default') return;
    const entry = {
      description: document.querySelector('#entry-description').value,
      type: document.querySelector('#entry-type').value,
      category: document.querySelector('#entry-category').value,
      amount: Number(document.querySelector('#entry-amount').value),
      date: document.querySelector('#entry-date').value
    };
    console.log('Novo lançamento preparado para a API:', entry);
    alert(`O lançamento de ${formatCurrency(entry.amount)} foi preparado. Na próxima etapa ele será enviado ao backend Java.`);
    form.reset();
  });
}

function setupUploadModal() {
  const dialog = document.querySelector('#upload-dialog');
  const openButton = document.querySelector('#upload-button');
  const form = document.querySelector('#upload-form');
  openButton.addEventListener('click', () => dialog.showModal());

  dialog.addEventListener('close', () => {
    if (dialog.returnValue !== 'default') return;
    const file = document.querySelector('#document-file').files[0];
    if (file) {
      console.log('Documento selecionado para a futura API:', { name: file.name, type: file.type, size: file.size });
      alert(`Arquivo "${file.name}" selecionado. O upload seguro será conectado na etapa de backend.`);
    }
    form.reset();
  });
}

// Ponto de entrada: executa tudo quando o script é carregado.
renderBills();
renderDocuments();
renderCategories();
drawCashFlowChart();
setupSearch();
setupEntryModal();
setupUploadModal();
