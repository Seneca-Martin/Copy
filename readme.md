# Invierte en Cryptos

Bienvenid@ al simulador de inversiones en cryptos, esta aplicación consulta el valor real en euros de las doce cryptomonedas con mayor volumen de negocios en la actualidad (2021).

Para poder utilizar la aplicación debes de seguir los siguiente pasos para su correcta instalación y uso.

# Instalación

1. Para comenzar debes de instalar las dependencias necesarias como se indica seguidamente:
    ```
    pip install -r requirements.txt
    ```

2. Crea ahora tu base de datos necesaria, para ello ejecuta el archivo: **createDB.py**

3. Crea en este momento tu fichero config.ini

    * Para ello usa el fichero **config_Reference.ini** como referencia.
    * Además debes tener tu apiKey de coinmarketcap que puedes obtener desde [aquí](https://coinmarketcap.com/api/)

4. Si ya has cumplimentado los pasos anteriores, ya puedes ejecutar la aplicación desde **main.py**


# Utilizando el simulador de inversión en cryptos

Esta es la aplicación que simula inversiones en crytomonedas en el momento de su ejecución, estas inversiones funcionan de la siguiente manera:

* Para comenzar a operar debemos crear una transacción para ello pulsaremos en el botón "+ Nueva transación"

* En este punto se activaran los combos y campos de la zona "Nueva transación" para poder realizar las conversiones.

* Las cryptos además de EUR (Euros) que podemos seleccionar en los combos son:

    | Cryptos               |                   |                         |                   |                   
    |-----------------------|:----------------- |:------------------------|:------------------| 
    | ADA - Cardano         |   ETH - Ethereum  |   BSV - Bitcoin SV      |   USDT - Tether   |
    | BCH - Bitcoin Cash    |   LTC - Litecoin  |   BTC - Bitcoin         |   XLM - Stellar   |                     
    | BNB - Binance Coin    |   TRX - TRON      |   EOS - EOS             |   XRP - XRP       |           

* La aplicación nos permite realizar las siguientes conversiones:
    * **De euros a caulquier crypto**: Dipones de EUR infinitos para invertir. Además esta conversión una vez aceptada se considerará inversión. El total de euros invertidos se mostrará en "€ invertidos" en la zona de "Tu Inversión" una vez pulses el botón "Calcular". 
    * **De crypto a otra crypto**: Estos movimientos los haremos en función de su valor relativo de manera que podemos incrementar el valor de la inversión que tenemos.
    * **De cualquier crypto a euros**: Esta transación se considerará retorno de inversión y se descontará del total de € invertidos cuando queramos hacer balance.

* La primera transación solo nos permitirá una conversión desde (From:) EUR a (To:) otra Crypto, y posteriormente podremos invertir desde EUR o cryptos en la que ya hemos invertido hacia cualquier otra crypto o EUR.
* Deberemos introducir la cantidad a invertir en el campo "Q" habilitado. Se aceptan cantidades con decimales separados por ".", además el formato de la salida de las cryptos de "From_Q", "To_Q" y precio unitario ("P.U."), es de 5 decimales, debido a que en algunos casos, en determinadas cryptos el valor es muy bajo.
* Una vez escogida la moneda a invertir y su cantidad y seleccionar la moneda para su conversión, pulsaremos en el botón "Comprobar" para comprobar el valor de la conversión, en este momento podemos elgir entre "Aceptar" o "Cancelar" la transacción.
* Una vez aceptadas cada una de estas transaciones se grabarán en la base de datos registrando la fecha y hora en la que se produjeron.
* La aplicación se conectará a la API de coinmarketcap, para indicarnos el valor real de nuestras transacciones registradas en la base de datos devolviendonos así:
    * Cuantos euros se invirtieron.
    * El valor actual en euros de nuestras cryptos en el momento de la consulta.

# Estructura del proyecto

Consta de diferentes ficheros:
* api_acces.py: gestiona llamadas y posibles errores a la API de coinmarketcap.
* createDB.py: crea la base de datos inicial esta debe de crearse en 'data/movements.db'
* movementsDB.py: gestiona llamadas a la base de datos **movements.db**
* config.ini: contiene los endpoints y la api_key.
* requierements.txt: Facilita las librerías necesarias para la ejecución de la aplicación.
* main.py: archivo principal que lanza la aplicación.

Cada archivo dispone de comentarios explicativos sobre la función de cada uno de ellos.
Se ha implementado un control de errores con mensajes sobre estos.





   
    
    
    
    

