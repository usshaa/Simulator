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
    var pressureValue = Math.floor(Math.random() * 100) + 900;
    var temperatureValue = Math.floor(Math.random() * 50) + 100;
    var flowRateValue = Math.floor(Math.random() * 10) + 40;

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

function predictFailure() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'predict-failure/', true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            var prediction = response.prediction;

            document.getElementById('prediction-result').innerText = prediction;
        }
    };
    xhr.send();
}

function performPrediction() {
    var pressure = document.getElementById('pressure-input').value;
    var temperature = document.getElementById('temperature-input').value;
    var flowRate = document.getElementById('flow-rate-input').value;

    // Make an AJAX request to get the prediction result
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'predict-failure/?pressure=' + pressure + '&temperature=' + temperature + '&flow_rate=' + flowRate, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            var prediction = response.prediction;

            document.getElementById('prediction').innerText = prediction;
        }
    };
    xhr.send();
}
