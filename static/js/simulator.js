document.getElementById('calculateButton').addEventListener('click', async () => {
  
  const elements = {
    calculateButton: document.getElementById('calculateButton'),
    resultContainer: document.getElementById('result-container'),
    containerSimulador: document.getElementById('container-simulador'),
    disclaimer: document.getElementById('disclaimer'),
    tituloSimulador: document.getElementById('titulo-simulador'),
  };
  
  const form = document.getElementById('simulator-form');
  const simulatorForm = new FormData(form);

  const allInputsValid = [...simulatorForm.values()].every(value => value.trim() !== '');

  if (!allInputsValid) {
    Swal.fire({
      title: 'Oops!',
      text: "Preencha todos os campos antes de submeter.",
      icon: 'warning',
      confirmButtonText: 'OK'
    });
    return;
  }

  try {
    const response = await simulateInvestment(simulatorForm);

    if (response.ok) {
        const responseData = await response.json();
        console.log(responseData);
        renderSimulationResults(responseData, elements);
    } else {
        const errorData = await response.json();
        Swal.fire({title:"Error",text:errorData.Erro || "Aconteceu um erro",icon:'error', confirmButtonText:'Ok'});
    }
  } catch (error) {
      console.error('Error while making the request:', error);
      Swal.fire({title:"Error",text:"Aconteceu um erro durante a solicitação.",icon:'error', confirmButtonText:'Ok'});
  }
});

async function simulateInvestment(simulatorForm) {
  return await fetch('financial/simular-investimento', {
      method: 'POST',
      body: simulatorForm,
  });
}

function renderSimulationResults(data, elements) {
  elements.resultContainer.innerHTML = ""; // Clear previous results

  const meses = data[0]?.meses;
  elements.tituloSimulador.innerHTML = meses <= 48
      ? `Em ${meses} meses, você terá:`
      : `Em aprox. ${(meses / 12).toFixed(0)} anos, você terá:`;

  data.forEach(item => {
      const card = createCard(item);
      elements.resultContainer.appendChild(card);

      animateNumber(`total_acumulado_${item.referencia}`, 0, item.montante_total, 1500);
      animateNumber(`total_investido_${item.referencia}`, 0, item.investidos, 1500);
      animateNumber(`juros_acumulado_${item.referencia}`, 0, item.juros_totais, 1500);
  });

  elements.containerSimulador.classList.remove('hidden');
  elements.disclaimer.classList.remove('hidden');
}

function createCard(item) {
  const div = document.createElement('div');
  const isCustomReference = !['CDI', 'SELIC', 'POUPANCA'].includes(item.referencia);

  div.innerHTML = `
      <div id="card space-y-2 ${isCustomReference ? '' : 'text-white'}">
          <h3 id="taxa_referencia" class="font-extrabold text-2xl text-start py-2">${item.referencia}</h3>
          <div class="flex gap-4 flex-col md:flex-row justify-around mx-auto">
              ${createCardColumn(item.referencia, 'total_acumulado', 'Total Acumulado', isCustomReference)}
              ${createCardColumn(item.referencia, 'total_investido', 'Total Investidos', isCustomReference)}
              ${createCardColumn(item.referencia, 'juros_acumulado', 'Juros Acumulados', isCustomReference)}
          </div>
      </div>
  `;
  return div;
}

function createCardColumn(reference, idSuffix, label, isCustom) {
  const bgColor = isCustom ? 'bg-azul-darkblue text-white' : '';
  return `
      <div class="border flex-1 border-black rounded-lg p-4 ${bgColor}">
          <h4 id="${idSuffix}_${reference}" class="text-4xl text-center">0</h4>
          <h4 class="text-center">${label}</h4>
      </div>
  `;
}

function animateNumber(elementId, start, end, duration) {
  const element = document.getElementById(elementId);
  const increment = (end - start) / (duration / 16); // Approx. 60 FPS
  let currentValue = start;

  function updateNumber() {
    currentValue += increment;
    if ((increment > 0 && currentValue >= end) || (increment < 0 && currentValue <= end)) {
      currentValue = end; // Clamp to final value
    }
    element.textContent = currentValue.toLocaleString('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    });

    if (currentValue !== end) {
      requestAnimationFrame(updateNumber);
    }
  }

  requestAnimationFrame(updateNumber);
}

async function handleError(response) {
  const error = await response.json();
  alert(`Error: ${error.error || 'Unknown'}`);
}