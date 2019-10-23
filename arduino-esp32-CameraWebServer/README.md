# CameraWebServer Example for ESP32-CAM in Arduino IDE

Project instructions: https://randomnerdtutorials.com/esp32-cam-video-streaming-face-recognition-arduino-ide/

Where to get an ESP32-CAM: https://makeradvisor.com/tools/esp32-cam/

This code is from Arduino ESP32 Repository: https://github.com/espressif/arduino-esp32/tree/master/libraries/ESP32/examples/Camera/CameraWebServer


## 下载步骤

烧录工具使用Arduino IDE，首先需要添加ESP32的芯片支持  
打开首选项，在附加开发板管理器网址里填上：https://dl.espressif.com/dl/package_esp32_index.json ，然后单击 好 。

然后在工具里打开开发板管理器，等待索引做完之后找到ESP32并安装。

硬件连接，注意需要将GPIO0和边上的GND短接进入烧录模式

| USB-TTL    |   ESP32-CAM    |
|  :----:    | :----:         |
| 3.3V       |   VCC          |
| GND        |   GND          |
| RX         |   U0T          |
| TX         |   U0R          |
|            |   IO0和GND短接  |

在开发板里面选对我们需要的开发板和相关设置，然后点击上传就好。

| 开发板 |        ESP32 Wrover Module|
|  :----:    | :----:         |
| Flash Mode|     QIO|
| Flash Frequrncy| 80MHz|
| Partition Scheme| Huge APP(3MB No OTA)|
| Upload Speed | 921600|
| Conr Debug Level | 无 |

