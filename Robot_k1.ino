#include <Servo.h>

Servo servo9;  // Rotación de la mano
Servo servo6;  // Posición de la muñeca
Servo servo5;
Servo servo3;
Servo servo11; // Apertura/cierre de la mano

void setup() {
    Serial.begin(9600);
    servo9.attach(9);
    servo6.attach(6);
    servo5.attach(5);
    servo3.attach(3);
    servo11.attach(11);
}

void loop() {
    if (Serial.available() > 0) {
        String input = Serial.readStringUntil('\n');
        int values[3];

        int i = 0;
        char *token = strtok((char*)input.c_str(), ",");
        while (token != NULL && i < 3) {
            values[i++] = atoi(token);
            token = strtok(NULL, ",");
        }

        // Mover los servos
        servo9.write(values[0]);  // Rotación lateral de la mano
        servo6.write(values[1]);  
        servo5.write(values[1]);  
        servo3.write(values[1]);  // Posición de la muñeca
        servo11.write(values[2]); // Apertura de la mano
    }
}
