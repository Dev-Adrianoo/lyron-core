#include <Servo.h>
#include <LiquidCrystal.h>

const int LCD_RS = 12, LCD_E = 11, LCD_D4 = 5, LCD_D5 = 4, LCD_D6 = 3, LCD_D7 = 2;
const int SERVO_BASE = 9, SERVO_DIREITO = 10, SERVO_ESQUERDO = 6;


LiquidCrystal lcd(LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7)
Servo servoBase, servoDireito, servoEsquerdo;


void showHappy() { lcd.clear(); lcd.print("( ^ - ^ )"); }
void showConfused() { lcd.clear(); lcd.print(" ( o _ O )?"); }
void doWave() {
  servoDireito.write(45); delay(400);
  servoDireito.write(135); delay(400);
  servoDireito.write(90);
}

void setup() {

  Serial.begin(9600);
  
  lcd.begin(16, 2);
  servoBase.attach(SERVO_BASE);
  servoDireito.attach(SERVO_DIREITO);
  servoEsquerdo.attach(SERVO_ESQUERDO);

  servoBase.write(90);
  servoDireito.write(90);
  servoEsquerdo.write(90);

  lcd.print("Lyron project");
  lcd.setCursor(0,1);
  lcd.print("Online!");
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "ACENAR") { doWave() }
    else if (comando == "FELIZ") { showHappy(); } 
    else if (comando == "CONFUSO") { showConfused(); }
  }
}