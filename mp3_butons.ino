#include <Arduino_FreeRTOS.h>
#include "task.h"
#include <Keypad.h>

// Buttons Struct
struct taskID{

  String id;                // Task id
  uint16_t value = 0;       // Actual state for pin
  uint16_t prev_value = 0;  // Preview state for pin

};

//---Keypad---

const byte n = 4; // Rows number
const byte m = 4; // Colums number

// Keypad data
char keys[n][m] = {

   { '1','2','3', 'A' },
   { '4','5','6', 'B' },
   { '7','8','9', 'C' },
   { '*','0','#', 'D' }

};

// Set digital pin for rows and columns
const byte rowPins[n] = { 13, 12, 11, 10 };
const byte columnPins[m] = { 9, 8, 7, 6 };
Keypad keypad = Keypad(makeKeymap(keys), rowPins, columnPins, n, m);

// Set digital pin for buttons
const int play_pin = 5;
const int stop_pin = 4;
const int prev_pin = 3;
const int next_pin = 2;

// Variable to toggle the play/pause button
bool temp;

// ---Critical function (Serial Print)---
void sendData(String data){

       Serial.println(data);

}

//---Buttons---

// Play/pause task
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

      // Start Critical Seccion
      taskENTER_CRITICAL();

      // Critical function
      sendData(p_button.id);

      // End Critical Seccion
      taskEXIT_CRITICAL();

    }

    // Set the number of ticks to send the task to block state
    vTaskDelay(pdMS_TO_TICKS(100));

  }

}

// Stop button task
void sendStop(void *pvParameters){

  struct taskID stopB;

  stopB.id = "Stop";

  while(1){

    stopB.prev_value = stopB.value;
    stopB.value = digitalRead(stop_pin);

    if(stopB.prev_value == 0 && stopB.value == 1){

      // Start Critical Seccion
      taskENTER_CRITICAL();

      // Critical function
      sendData(stopB.id);

      // End Critical Seccion
      taskEXIT_CRITICAL();

    }

    // Set the number of ticks to send the task to block state
    vTaskDelay(pdMS_TO_TICKS(100));

  }

}

// Next button task
void sendNext(void *pvParameters){

  struct taskID next;

  next.id = "Next Song";

  while(1){

    next.prev_value = next.value;
    next.value = digitalRead(next_pin);

    if(next.prev_value == 0 && next.value == 1){

      // Start Critical Seccion
      taskENTER_CRITICAL();

      // Critical function
      sendData(next.id);

      // End Critical Seccion
      taskEXIT_CRITICAL();

    }

    // Set the number of ticks to send the task to block state
    vTaskDelay(pdMS_TO_TICKS(100));

  }

}

// Preview button task
void sendPrev(void *pvParameters){

  struct taskID prev;
  prev.id = "Prev Song";

  while(1){

    prev.prev_value = prev.value;
    prev.value = digitalRead(prev_pin);

    if(prev.prev_value == 0 && prev.value == 1){

      // Start Critical Seccion
      taskENTER_CRITICAL();

      // Critical function
      sendData(prev.id);

      // End Critical Seccion
      taskEXIT_CRITICAL();

    }

    // Set the number of ticks to send the task to block state
    vTaskDelay(pdMS_TO_TICKS(100));

  }

}

// Keypad seleccion task
void song_select(void *pvParameters){

  struct taskID song;
  String song_num = "";
  uint16_t num;

   while(1){

     // Get the key pressed
     char option = keypad.getKey();

     if(option != 'A' && option != 'B' && option != 'C' && option != 'D' && option != '#'&&  option != NULL){

      // The character '*' simulates the confirm operation
      if(option == '*'){

      // Start Critical Seccion
      taskENTER_CRITICAL();

      // Convert the song_num variable to int
      num = song_num.toInt();

      if(num <= 100){

        // Critical function
        sendData(song_num);

      }else{

        sendData("Not_selection");

      }

      // Reset the song_numn variable
      song_num = "";

      // End Critical Seccion
      taskEXIT_CRITICAL();

      }else{

        // Append to song_num variable the pressed key
        song_num += option;

        }

      }

        // Clear the option variable
        option = NULL;

        // Set the number of ticks to send the task to block state
        vTaskDelay(pdMS_TO_TICKS(100));

     }

}

void setup(){

  // Initialize serial
  Serial.begin(9600);

  // Set the buttons pins as a input
  pinMode(play_pin, INPUT);
  pinMode(stop_pin, INPUT);
  pinMode(prev_pin, INPUT);
  pinMode(next_pin, INPUT);

  // Create tasks
  xTaskCreate (sendPlayP,   "Play/Pausa"  , 100, NULL, 2, NULL);
  xTaskCreate (sendStop,    "Stop"        , 100, NULL, 2, NULL);
  xTaskCreate (sendNext,    "Nxt Song"    , 100, NULL, 2, NULL);
  xTaskCreate (sendPrev,    "Prev Song"   , 100, NULL, 2, NULL);
  xTaskCreate (song_select, "Song Number" , 100, NULL, 2, NULL);

}

void loop(){}
