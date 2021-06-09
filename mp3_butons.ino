#include <Arduino_FreeRTOS.h>
#include "task.h"
#include <Keypad.h>

struct taskID{
  String id;     //tipo tarea
  uint16_t value = 0; //estado actual del pin
  uint16_t prev_value = 0;
};

//Teclado
//----------------
const byte n = 4;
const byte m = 4;
 
char keys[n][m] = {
  
   { '1','2','3', 'A' },
   { '4','5','6', 'B' },
   { '7','8','9', 'C' },
   { '*','0','#', 'D' }
   
};
 
const byte rowPins[n] = { 13, 12, 11, 10 };
const byte columnPins[m] = { 9, 8, 7, 6 };
 
Keypad keypad = Keypad(makeKeymap(keys), rowPins, columnPins, n, m);

// Definimos el tiempo de espera
const TickType_t xTicksToWait = pdMS_TO_TICKS(100);

// constantes
const int play_pin = 5;
const int stop_pin = 4;
const int prev_pin = 3;
const int next_pin = 2;
bool temp;

//Acciones de los botones
//-----------------------

void sendData(String data){
    
       Serial.println(data);
       delay(500);
    
}

void sendPlayP(void *pvParameters){

  struct taskID p_button;
  bool temp = false;

  while(1){

    p_button.prev_value = p_button.value;
    p_button.value = digitalRead(play_pin);
    
    if(p_button.prev_value == 0 && p_button.value == 1){
    
      if(temp == false){
      
        p_button.id = "Play";  
        temp = true;
      
      }else{
      
        p_button.id = "Pause";
        temp = false;
      
      }

      taskENTER_CRITICAL();  
      sendData(p_button.id);
      taskEXIT_CRITICAL();
      
    }
   
    vTaskDelay(pdMS_TO_TICKS(100));
    
  }
  
}

void sendStop(void *pvParameters){

  struct taskID stopB;

  stopB.id = "Stop";

  while(1){

    stopB.prev_value = stopB.value;
    stopB.value = digitalRead(stop_pin);

    if(stopB.prev_value == 0 && stopB.value == 1){
      
      taskENTER_CRITICAL();  
      sendData(stopB.id);
      taskEXIT_CRITICAL();
      
    }
    
    vTaskDelay(pdMS_TO_TICKS(100));
    
  }
  
}

void sendNext(void *pvParameters){

  struct taskID next;
  
  next.id = "Next Song";

  while(1){

    next.prev_value = next.value;
    next.value = digitalRead(next_pin);

    if(next.prev_value == 0 && next.value == 1){
      
      taskENTER_CRITICAL();  
      sendData(next.id);
      taskEXIT_CRITICAL();
      
    }
    
    vTaskDelay(pdMS_TO_TICKS(100));
    
  }
  
}

void sendPrev(void *pvParameters){

  struct taskID prev;
  prev.id = "Prev Song";

  while(1){

    prev.prev_value = prev.value;
    prev.value = digitalRead(prev_pin);

    if(prev.prev_value == 0 && prev.value == 1){
      
      taskENTER_CRITICAL();  
      sendData(prev.id);
      taskEXIT_CRITICAL();
      
    }
    
    vTaskDelay(pdMS_TO_TICKS(100));
    
  }
  
}

void song_select(void *pvParameters){

  struct taskID song;
  String song_num = "";
  uint16_t num;

   while(1){
  
     char option = keypad.getKey();

     if(option != 'A' && option != 'B' && option != 'C' && option != 'D' && option != '#'&&  option != NULL){

      if(option == '*'){

      taskENTER_CRITICAL(); 
      
      num = song_num.toInt();
      
      if(num <= 100){
        
        sendData(song_num);
        
      }else{
        
        sendData("Not_selection");  
        
      }
        
      song_num = ""; 
      
      taskEXIT_CRITICAL();
        
      }else{

        song_num += option;
          
        }
        
      }

        option = NULL;

        vTaskDelay(pdMS_TO_TICKS(100));

     }
            
}

void setup(){
 
  //initialize serial
  Serial.begin(9600);

  
  
  pinMode(play_pin, INPUT);
  pinMode(stop_pin, INPUT);
  pinMode(prev_pin, INPUT);
  pinMode(next_pin, INPUT);

  //create tasks
  xTaskCreate (sendPlayP,   "Play/Pausa"  , 100, NULL, 2, NULL);
  xTaskCreate (sendStop,    "Stop"        , 100, NULL, 2, NULL);
  xTaskCreate (sendNext,    "Nxt Song"    , 100, NULL, 2, NULL);
  xTaskCreate (sendPrev,    "Prev Song"   , 100, NULL, 2, NULL);
  xTaskCreate (song_select, "Song Number" , 100, NULL, 2, NULL);
  
}

void loop(){}
