#define STEP_PIN_1 54
#define DIR_PIN_1 55
#define ENABLE_PIN_1 38

#define STEP_PIN_2 60
#define DIR_PIN_2 61
#define ENABLE_PIN_2 56

#define STEP_PIN_3 36
#define DIR_PIN_3 34
#define ENABLE_PIN_3 30

void setup() {
    Serial.begin(115200);
    Serial.println("Stepper Motor Controller Initialized");

    pinMode(STEP_PIN_1, OUTPUT);
    pinMode(DIR_PIN_1, OUTPUT);
    pinMode(ENABLE_PIN_1, OUTPUT);

    pinMode(STEP_PIN_2, OUTPUT);
    pinMode(DIR_PIN_2, OUTPUT);
    pinMode(ENABLE_PIN_2, OUTPUT);

    pinMode(STEP_PIN_3, OUTPUT);
    pinMode(DIR_PIN_3, OUTPUT);
    pinMode(ENABLE_PIN_3, OUTPUT);

    // Enable motors initially for self-locking
    // analogWrite(ENABLE_PIN_1, 50);
    // analogWrite(ENABLE_PIN_2, 50);
    // analogWrite(ENABLE_PIN_3, 50);
    // delay(300);

    // digitalWrite(ENABLE_PIN_1, HIGH);
    // digitalWrite(ENABLE_PIN_2, HIGH);
    // digitalWrite(ENABLE_PIN_3, HIGH);

    
}

void loop() {
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');
        command.trim();
        Serial.print("Received: ");
        Serial.println(command);
        processCommand(command);
    }
//     else{


//     // digitalWrite(ENABLE_PIN_1, HIGH);
//     // digitalWrite(ENABLE_PIN_2, HIGH);
//     // digitalWrite(ENABLE_PIN_3, HIGH);
//     // delay(10);

//     // digitalWrite(ENABLE_PIN_1, LOW);
//     // digitalWrite(ENABLE_PIN_2, LOW);
//     // digitalWrite(ENABLE_PIN_3, LOW);
//     // delay(10);
// }
}

void processCommand(String command) {
    char motorId;
    char direction[4];  // Buffer for "CW" or "CCW"
    int steps;

    if (sscanf(command.c_str(), "M%c %3s %d", &motorId, direction, &steps) == 3) {
        bool dir = (strcmp(direction, "CW") == 0);  // Compare with "CW"

        switch (motorId) {
            case '1':
                moveStepper(DIR_PIN_1, STEP_PIN_1, ENABLE_PIN_1, dir, steps);
                break;
            case '2':
                moveStepper(DIR_PIN_2, STEP_PIN_2, ENABLE_PIN_2, dir, steps);
                break;
            case '3':
                moveStepper(DIR_PIN_3, STEP_PIN_3, ENABLE_PIN_3, dir, steps);
                break;
            default:
                Serial.println("Invalid Motor ID");
        }
    } else {
        Serial.println("Invalid Command Format");
    }
}

void moveStepper(int dirPin, int stepPin, int enablePin, bool direction, int steps) {
    digitalWrite(enablePin, LOW);  // Enable motor
    digitalWrite(dirPin, direction);  // Set direction

    Serial.print("Moving ");
    Serial.print((direction) ? "CW" : "CCW");
    Serial.print(" for ");
    Serial.print(steps);
    Serial.println(" steps.");

    for (int i = 0; i < steps; i++) {
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(800);  // Optimized delay to avoid noise
        digitalWrite(stepPin, LOW);
        delayMicroseconds(800);
    }

    Serial.println("Movement complete.");
}
