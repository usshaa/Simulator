var simulationInterval;

function startSimulation() {
    document.getElementById('start-button').disabled = true;
    document.getElementById('stop-button').disabled = false;

    simulationInterval = setInterval(updateValues, 1000);
}

function stopSimulation() {
    document.getElementById('start-button').disabled = false;
    document.getElementById('stop-button').disabled = true;

    clearInterval(simulationInterval);
}

function updateValues() {
    var pressureValue = Math.floor(Math.random() * (70 - 20 + 1)) + 20;
    var temperatureValue = Math.floor(Math.random() * (120 - 60 + 1)) + 60;
    var flowRateValue = Math.floor(Math.random() * (1000 - 200 + 1)) + 200;

    document.getElementById('pressure-value').innerText = pressureValue;
    document.getElementById('temperature-value').innerText = temperatureValue;
    document.getElementById('flow-rate-value').innerText = flowRateValue;

    // Send data to the server
    var data = {
        pressure: pressureValue,
        temperature: temperatureValue,
        flow_rate: flowRateValue
    };

    // Make an AJAX request to save the data
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'save-data/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            console.log('Data saved successfully!');
        }
    };
    xhr.send(JSON.stringify(data));
}

function manualController() {
    var pressureInput = document.getElementById('pressure-input');
    var temperatureInput = document.getElementById('temperature-input');
    var flowRateInput = document.getElementById('flow-rate-input');

    var pressureValue = parseFloat(pressureInput.value);
    var temperatureValue = parseFloat(temperatureInput.value);
    var flowRateValue = parseFloat(flowRateInput.value);

    // Update the displayed values
    document.getElementById('pressure-value').innerText = pressureValue;
    document.getElementById('temperature-value').innerText = temperatureValue;
    document.getElementById('flow-rate-value').innerText = flowRateValue;

    // Send data to the server
    var data = {
        pressure: pressureValue,
        temperature: temperatureValue,
        flow_rate: flowRateValue
    };

    // Make an AJAX request to save the data
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'save-data/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            console.log('Data saved successfully!');
        }
    };
    xhr.send(JSON.stringify(data));
}
