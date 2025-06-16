#include <Wire.h>
#include <U8g2lib.h>

// Constructor: for SH1106 128x64 I2C display
U8G2_SH1106_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);

void setup() {
  u8g2.begin();
}

void loop() {
  int myNumber = 12345;
  char buff[60];             // Make sure it's large enough for your integer
  itoa(myNumber, buff, 10);  // Convert int to string (base 10)
  u8g2.clearBuffer();                // Clear internal memory
  u8g2.setFont(u8g2_font_ncenB08_tr); // Choose a suitable font
  u8g2.drawStr(8, 24, "Hello U8g2!"); // Draw text (x, y, text)
  u8g2.drawStr(12, 36, "Hello U8g2!"); // Draw text (x, y, text)
  u8g2.drawStr(16, 48, "Hello U8g2!"); // Draw text (x, y, text)
  u8g2.drawStr(20, 64, "Hello U8g2!"); // Draw text (x, y, text)
  u8g2.setFont(u8g2_font_6x10_tf);
  sprintf(buff, "Top Line: %d", myNumber);
  u8g2.drawStr(0, 12, buff);
  //u8g2.drawStr(0, 12, "Top Line: "); // Draw text (x, y, text)
  //u8g2.drawStr(24, 12, buff);        // Display the text
  u8g2.sendBuffer();                 // Transfer internal buffer to display
  delay(2000);
}

