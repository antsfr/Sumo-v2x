## Требования
Для пользования скриптом нужно:  
1. Установить SUMO, следуя инструкции: https://sumo.dlr.de/docs/Downloads.php
2. В файле **config.yaml** изменить значение параметра **sumoPath** на путь, по которому SUMO был установлен.


## Запуск скрипта
1. Сконфигурировать программу в файле **config.yaml**.
   1) Выбрать интересующий сценарий. Для этого изменить значение параметра **scenairo**.  
   Доступные сценарии соответствуют именам папок в sumo_example/scenarios/
   2) Изменить параметры **hostname** и **port**, если производится отправка NMEA-сообщений на устройства OBU.
   3) Убедиться, что значение параметра **sumoPath** соответствует пути с установленным SUMO.
   4) Поставить параметру **GUI** значение true, если нужна SUMO-визуализация, false - в противном случае.
   5) В параметре **vehID** задать все ТС, которые нужно отслеживать. **Кол-во ТС здесь должно соответствовать кол-ву хостов и портов.**
   6) Изменить параметры **steps** (кол-во шагов симуляции) и **NMEAFreq** (частота отправки NMEA), если требуется.  
2. Предварительно запустив прошивки (если не требуется отправка на OBU - можно без них), запустить sumoRetriever.py командой: 
   
        python sumoRetriever.py
   <p>

3. Скрипт завершит работу, когда все сообщения будут отправлены.

4. Также возможно аварийное завершение в случае, если для очередного шага отслеживаемое ТС покинуло симуляцию.

## Регулировка основных параметров

* Во внешних файлах:  
  * **osm.sumocfg** сценария:  
    step-length -- Частота Генерации Шагов
    collision.action -- действие SUMO при коллизии
  * **osm.view.xml** сценария:  
    viewport -- дефолтный зум  
    delay value --  дефолтная задержка  
    <br/>
* В **config.yaml**:
  * GUI -- визуализация симуляции
  * scenario -- имя симулируемого сценария (= имя директории в scenarios/)
  * NMEAFreq -- Частота Отправки NMEA на OBU
  * steps -- Количество Шагов Симуляции
  * vehID -- id отслеживаемого ТС
  * sumoPath -- путь к директории, содержащей папку tools/


## Создание сценариев

  1. Сгенерировать конфигурацию карты, используя OsmWebWizard.  
     (Краткий туториал: https://sumo.dlr.de/docs/Tutorials/OSMWebWizard.html)  
        Для этого:

    1. Из консоли перейти в директорию ~\Sumo\tools
    2. Запустить команду: python OsmWebWizard.py
    3. В открывшейся вкладке найти нужный участок карты. Ткнуть галку в "Select Area" (на панели справа) и захватить нужную область.
    4. Здесь же можно управлять генерацией ТС. Для этого переключиться на вкладку "Vehicles", выбрать нужные типы авто и задать параметры:
        Параметр Through Traffic Factor - чем больше, тем длиннее генерируемые маршруты ТС
        Параметр Count - чем больше, тем чаще генерация ТС
        (Подробнее - в туториале: https://sumo.dlr.de/docs/Tutorials/OSMWebWizard.html#demand_generation)
    5. Ткнуть "Generate Scenario" (на панели справа)
  2. В директории ~\Sumo\tools\ появится папка с именем вида "yyyy-mm-dd-hh-mm-ss". Она содержит все сгенерированные файлы.  
        Из этих файлов наиболее важными являются:  
        1. **osm.passengers.trips.xml**  
        Содержит информацию о маршрутах сгенерированных ТС. Отсюда также можно управлять поведением водителей.
        
                Здесь можно:
                1. Добавлять/удалять ТС и их маршруты.
                2. Задавать время отправления ТС (в секундах): depart="0.00"
                3. Задавать скорость ТС в момент спавна (в м/с): departSpeed="15"
                4. Задавать lanes отправления и назначения: from="-172955879#1" to="-133321828#5"
                    * lane - линия движения между двумя junction'ами (подробнее - https://sumo.dlr.de/docs/Tutorials/quick_start.html)
                5. Задавать конкретную позицию отправления/прибытия на lane'е (по умолчанию - спавн в начале lane'а, финиширование - в его конце) (в метрах): departPos="30"
                    * Каждая точка lane'а имеет характеристики pos и height. В стартовом junction'e pos=0. Чтобы узнать pos, в SUMO нужно тыкнуть ПКМ на интересующую точку lane'а.
                6. Задавать параметры целого класса ТС: <vType id="veh_passenger" jmDriveAfterRedTime ="0" jmCrossingGap="0" jmIgnoreFoeSpeed="1" jmIgnoreFoeProb ="1" jmTimegapMinor ="0" jmIgnoreKeepClearTime ="0" jmStoplineGap ="0" impatience ="1" jmSigmaMinor="1" tau="0.0001" vClass="passenger"/>
                    Подбронее об этих и других доступных параметрах: https://sumo.dlr.de/docs/Definition_of_Vehicles%2C_Vehicle_Types%2C_and_Routes.html#vehicle_types
        <p>

        2. **osm.sumocfg**  
        Отсюда управлять частотой шагов симуляции и пр.
           
                Здесь можно:
                1) Задать частоту шагов симуляции (в секундах):
                    <time>
                        <step-length value="0.1"/>
                    </time>
                2) Активировать генерацию лога коллизий:
                    <output>
                        <collision-output value="collisions.xml"/>
                    </output>
                3) Выбрать реакцию SUMO на коллизию (по умолчанию - телепорт одного из ТС):
                    <processing>
                        <collision.action value="warn"/>
                    </processing>
                
                И многое другое.
                Полный перечень параметров: https://sumo.dlr.de/docs/sumo.html
        <p>
    
        3. **osm.view.xml**  
        Отсюда управлять дефолтными зумом/скоростью симуляции.
    
                Здесь можно:
                1) Задать дефолтную скорость симуляции (в милисекундах):
                        <delay value="3000"/>
                2) Задать дефолтные зум и точку, на которой открывается SUMO:
                        <viewport zoom="10000" x="1730" y="8280"/>
           
                Полный перечень параметров: https://sumo.dlr.de/docs/sumo-gui.html
        <p>

        4. **osm.net.xml**  
        Содержит все элементы карты.

                Здесь эти элементы можно убирать/добавлять.
                Например, для удаления светофора можно в SUMO посмотреть id junction'а, на котором светофор расположен, найти этот id в osm.net.xml, и удалить запись, содержающую "traffic_light".
                (А добавлять элементы удобнее через графический редактор netedit, подробнее о нем - https://sumo.dlr.de/docs/Netedit/index.html)
                Подробнее о .net.xml: https://sumo.dlr.de/docs/Networks/PlainXML.html , https://sumo.dlr.de/docs/Networks/SUMO_Road_Networks.html
        <p>

  3. Внести желаемые изменения в упомянутые файлы.  
    Придумать имя сценария, создать в директории sumo_example/scenarios/ папку с этим именем.  
     В нее поместить все ранее созданные файлы.
     Сценарий готов к использованию.
     
## Функционал TraCI
* Vehicle Value Retrieval -- https://sumo.dlr.de/docs/TraCI/Vehicle_Value_Retrieval.html
* Traffic Lights Value Retrieval -- https://sumo.dlr.de/docs/TraCI/Traffic_Lights_Value_Retrieval.html
* Vehicle Signaling -- описание битсета: https://sumo.dlr.de/docs/TraCI/Vehicle_Signalling.html#defined_signals
    