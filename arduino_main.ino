# include<Servo.h>

Servo s;

int angle=3;

#define trigger 7
#define echo 6

void setup() {
  s.attach(9);
  Serial.begin(9600);
  pinMode(trigger,OUTPUT);
  pinMode(echo,INPUT);
}

void us()
{

  long value,distance;
  digitalWrite(trigger,LOW);
  delayMicroseconds(1);

  digitalWrite(trigger,HIGH);
  delayMicroseconds(5);

  digitalWrite(trigger,LOW);
  value=pulseIn(echo,HIGH);

  distance=value/58.2;

  Serial.println(distance);

 // delay(10);

}

void loop() {

for(angle=3;angle<180;angle+=20)
 {
  s.write(angle);
  us();
  //delay(10);
 }
  delay(1000);
 
 for(angle=180;angle>=3;angle-=10)
 {
  s.write(angle);
  us();
  //delay(10);
 }
   delay(1000);



}
