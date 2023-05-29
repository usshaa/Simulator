from django.shortcuts import render
from django.http import JsonResponse
from .models import SensorData, FailureData
import joblib
import random
from sklearn.ensemble import RandomForestClassifier
import os
from django.views.decorators.csrf import csrf_exempt
import winsound

# Set the range and criteria for failure conditions
MAX_PRESSURE = 100  # Maximum pressure threshold for failure
MAX_TEMPERATURE = 150  # Maximum temperature threshold for failure
MIN_FLOW_RATE = 10  # Minimum flow rate threshold for failure


def generate_random_failure():
    # Generate random values for pressure, temperature, and flow rate
    pressure = random.uniform(0, MAX_PRESSURE)
    temperature = random.uniform(0, MAX_TEMPERATURE)
    flow_rate = random.uniform(MIN_FLOW_RATE, 100)

    # Check if the generated values meet the failure criteria
    is_failure = pressure > MAX_PRESSURE or temperature > MAX_TEMPERATURE or flow_rate < MIN_FLOW_RATE

    return {
        'pressure': pressure,
        'temperature': temperature,
        'flow_rate': flow_rate,
        'is_failure': is_failure,
    }


def index(request):
    return render(request, 'index.html')


def build_and_save_model():
    # Fetch all the sensor data from the database
    sensor_data = SensorData.objects.all()
    failure_data = FailureData.objects.all()

    # Check if the number of sensor data points is equal to the number of failure data points
    if len(sensor_data) != len(failure_data):
        raise ValueError("Number of sensor data points and failure data points are not equal.")

    # Prepare the input features and target variable
    features = []
    target = []

    # Convert queryset dictionaries into lists of values
    for data_point in sensor_data:
        features.append([data_point.pressure, data_point.temperature, data_point.flow_rate])

    for failure_entry in failure_data:
        target.append(failure_entry.is_failure)

    # Perform necessary data preprocessing and feature engineering
    # ...

    # Build and train the Random Forest Classifier
    model = RandomForestClassifier()
    model.fit(features, target)

    # Define the directory path for saving the trained model
    directory_path = os.path.dirname(os.path.abspath(__file__))

    # Define the file path for saving the trained model
    file_path = os.path.join(directory_path, 'MLModels/trained_model.joblib')

    # Save the trained model to the specified file path
    joblib.dump(model, file_path)


# def predict_failure(request):
#     if request.method == 'GET':
#         # Define the directory path for loading the trained model
#         directory_path = os.path.dirname(os.path.abspath(__file__))
#
#         # Define the file path for loading the trained model
#         file_path = os.path.join(directory_path, 'MLModels/trained_model.joblib')
#
#         # Load the trained model
#         model = joblib.load(file_path)
#
#         # Fetch the latest sensor data
#         latest_data = SensorData.objects.latest('timestamp')
#         pressure = latest_data.pressure
#         temperature = latest_data.temperature
#         flow_rate = latest_data.flow_rate
#
#         # Perform prediction using the model
#         prediction = model.predict([[pressure, temperature, flow_rate]])
#
#         # Convert the prediction ndarray to a Python list
#         prediction = prediction.tolist()
#
#         if prediction[0] == 1:
#             # Play a sound indicating a failure
#             winsound.PlaySound('beep-01a.wav', winsound.SND_FILENAME)
#
#         return JsonResponse({'prediction': prediction})
#     else:
#         return JsonResponse({'status': 'error'})


@csrf_exempt
def save_data(request):
    if request.method == 'POST':
        # Clear existing data in the database
        SensorData.objects.all().delete()
        FailureData.objects.all().delete()

        # Start the simulation
        for _ in range(10):  # Simulate 10 data points
            # Generate random sensor data
            pressure = random.uniform(0, MAX_PRESSURE)
            temperature = random.uniform(0, MAX_TEMPERATURE)
            flow_rate = random.uniform(MIN_FLOW_RATE, 100)

            # Save the data in the database
            sensor_data = SensorData(pressure=pressure, temperature=temperature, flow_rate=flow_rate)
            sensor_data.save()

            # Generate failure data
            failure_data = generate_random_failure()
            failure_pressure = failure_data['pressure']
            failure_temperature = failure_data['temperature']
            failure_flow_rate = failure_data['flow_rate']
            is_failure = failure_data['is_failure']

            # Save the failure data in the database
            failure_entry = FailureData(pressure=failure_pressure, temperature=failure_temperature,
                                        flow_rate=failure_flow_rate, is_failure=is_failure)
            failure_entry.save()

        # Build and save the model using the updated data
        build_and_save_model()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})


def check_prediction(request):
    return render(request, 'prediction.html')


def predict_failure(request):
    if request.method == 'GET':
        # Define the directory path for loading the trained model
        directory_path = os.path.dirname(os.path.abspath(__file__))

        # Define the file path for loading the trained model
        file_path = os.path.join(directory_path, 'MLModels/trained_model.joblib')

        # Load the trained model
        model = joblib.load(file_path)

        # Get the test data from the query parameters
        pressure_str = request.GET.get('pressure')
        temperature_str = request.GET.get('temperature')
        flow_rate_str = request.GET.get('flow_rate')

        # Check if any of the query parameters are missing
        if pressure_str is None or temperature_str is None or flow_rate_str is None:
            return JsonResponse({'status': 'error', 'message': 'Missing query parameters.'})

        try:
            # Convert the query parameters to float
            pressure = float(pressure_str)
            temperature = float(temperature_str)
            flow_rate = float(flow_rate_str)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid query parameter value(s).'})

        # Perform prediction using the model
        prediction = model.predict([[pressure, temperature, flow_rate]])

        # Convert the prediction ndarray to a Python list
        prediction = prediction.tolist()

        if prediction[0] == 1:
            # Play a sound indicating a failure
            winsound.PlaySound('beep-01a.wav', winsound.SND_FILENAME)

        return JsonResponse({'prediction': prediction})
    else:
        return JsonResponse({'status': 'error'})
