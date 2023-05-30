from django.shortcuts import render
from django.http import JsonResponse
from .models import SensorData, FailureData
import random
import csv
import json
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request,'index.html')
def generate_failure(pressure, temperature, flow_rate):
    # Define the failure criteria thresholds
    MAX_PRESSURE = 70
    MIN_PRESSURE = 20
    MAX_TEMPERATURE = 120
    MIN_TEMPERATURE = 60
    MAX_FLOW_RATE = 1000
    MIN_FLOW_RATE = 200

    # Check if the sensor data meets the failure criteria
    is_failure = (
        pressure < MIN_PRESSURE
        or pressure > MAX_PRESSURE
        or temperature < MIN_TEMPERATURE
        or temperature > MAX_TEMPERATURE
        or flow_rate < MIN_FLOW_RATE
        or flow_rate > MAX_FLOW_RATE
    )

    return {
        'pressure': pressure,
        'temperature': temperature,
        'flow_rate': flow_rate,
        'is_failure': is_failure,
    }

@csrf_exempt
def save_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        pressure = float(data.get('pressure', 0))
        temperature = float(data.get('temperature', 0))
        flow_rate = float(data.get('flow_rate', 0))

        # Generate failure data for the current sensor data point
        failure_data = generate_failure(pressure, temperature, flow_rate)
        is_failure = failure_data['is_failure']

        # Save the sensor data in the SensorData model
        sensor_entry = SensorData(pressure=pressure, temperature=temperature, flow_rate=flow_rate)
        sensor_entry.save()

        # Save the failure data in the FailureData model
        failure_pressure = failure_data['pressure']
        failure_temperature = failure_data['temperature']
        failure_flow_rate = failure_data['flow_rate']
        failure_entry = FailureData(pressure=failure_pressure, temperature=failure_temperature,
                                    flow_rate=failure_flow_rate, is_failure=is_failure)
        failure_entry.save()

        # Define the file path for saving the CSV file
        file_path = 'sensor_data.csv'

        try:
            # Open the CSV file in append mode
            with open(file_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)

                # Write the data row to the CSV file
                writer.writerow([pressure, temperature, flow_rate, is_failure])
        except Exception as e:
            # Handle any exceptions that may occur during file handling
            return JsonResponse({'status': 'error', 'message': str(e)})

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
