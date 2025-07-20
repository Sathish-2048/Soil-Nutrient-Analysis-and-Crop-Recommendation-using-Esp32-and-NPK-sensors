# Soil-Nutrient-Analysis-and-Crop-Recommendation-using-Esp32-and-NPK-sensors
(Sathish-2048) Hardware integration: Assembled the ESP32 microcontroller with a 7-in-1 NPK soil sensor, MAX485 module, and 12V power supply, ensuring stable circuit design and accurate soil data acquisition. 
(Sathish-2048) Communication system: Implemented HTTP-based client-server communication over WiFi, enabling real-time data transfer from the ESP32 (client) to the local server. 
(Sathish-2048) Software development: Created client-side Embedded C code (Arduino) for sensor control and data transmission, and server-side Python-Flask code to receive data, process it, and run real-time predictions using the ML model. 
(Sathish-2048) ML model creation and evaluation: Developed Naive Bayes and SVM models, applied k-fold cross-validation for robustness checks, and used GridSearch for hyperparameter tuning to optimize model performance. 
(Sathish-2048) Model deployment: Integrated the Naive Bayes model pipeline into the server, exporting it as a .pkl file for live inference on incoming sensor data. 
