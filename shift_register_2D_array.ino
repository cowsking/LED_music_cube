int latchPin = 3;  // Latch pin (12) of 74HC595 is connected to Digital pin 5
int clockPin = 4; // Clock pin (11) of 74HC595 is connected to Digital pin 6
int dataPin = 2;  // Data pin (14) of 74HC595 is connected to Digital pin 4
//int outputEnablePin = 3;  // OE pin of 74HC595 is connected to PWM pin 3


byte green[5];    // Variable to hold the pattern of which LEDs are currently turned on or off
byte ground[6];

/*
 * setup() - this function runs once when you turn your Arduino on
 * We initialize the serial connection with the computer
 */
void setup() 
{
  // Set all the pins of 74HC595 as OUTPUT
  Serial.begin(9600);
  pinMode(latchPin, OUTPUT);
  pinMode(dataPin, OUTPUT);  
  pinMode(clockPin, OUTPUT);
  ground[0]=B00000001;   // Directly write to first shift register
  ground[1]=B00000010;
  ground[2]=B00000100;
  ground[3]=B00001000;
  ground[4]=B00010000;
  ground[5]=B00100000;
  digitalWrite(latchPin, LOW);
  //pinMode(outputEnablePin, OUTPUT); 
}

/*
 * loop() - this function runs over and over again
 */
void loop() 
{
    if (Serial.available() > 0) {
      // read the incoming byte:
      String data = Serial.readStringUntil('\n');
      Serial.println(data);
      
      for (int i = 0; i < 36; i++){
        char c = data[i];
        //Serial.println(c);
        int value = i / 6; 
        int remain = i % 6;
        //Serial.println(value);
        //Serial.println(remain);
        if (c == '1'){
          //Serial.println("aaaaa");
          LED(value, remain);
        }
      }
      updateShiftRegister();
     }
}
    

/*
 * updateShiftRegister() - This function sets the latchPin to low, then calls the Arduino function 'shiftOut' to shift out contents of variable 'leds' in the shift register before putting the 'latchPin' high again.
 */
void updateShiftRegister()
{
   
    for (int k = 0; k < 6; k ++){
    digitalWrite(latchPin, LOW);
    shiftOut(dataPin, clockPin, LSBFIRST, green[4]);  // upload the data in green to the shift registers
    shiftOut(dataPin, clockPin, LSBFIRST, green[3]);
    shiftOut(dataPin, clockPin, LSBFIRST, green[2]);
    shiftOut(dataPin, clockPin, LSBFIRST, green[1]);
    shiftOut(dataPin, clockPin, LSBFIRST, green[0]);
    
    shiftOut(dataPin, clockPin, LSBFIRST, ground[k]);  // connect each layer to ground separately to create the moving animation
    digitalWrite(latchPin, HIGH);
    delay(50);
    }

    for (int m = 0; m < 6; m++){
      for (int n = 0; n < 8; n++){
        bitWrite(green[m], n, 0);  // clear the value in shift registers after one data upload
      }
    }
    digitalWrite(latchPin, HIGH);
    digitalWrite(latchPin, LOW);    
    shiftOut(dataPin, clockPin, LSBFIRST, ground[0]);
    digitalWrite(latchPin, HIGH);
}

void LED (int row, int col)
{
  digitalWrite(latchPin, LOW);

  if(row<0)
    row=0;
  if(row>5)
    row=5;
  if(col<0)
    col=0;
  if(col>5)
    col=5;

   int whichbyte = int (((row*6)+col)/8);
   int wholebyte=(row*6)+col;
   
   bitWrite(green[whichbyte], wholebyte-(8*whichbyte), 1);
}
