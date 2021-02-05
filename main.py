from tkinter import *
from tkinter import ttk
import time
import datetime
import configparser
import json
import movementsDB
import api_acces
from tkinter import messagebox


_width='1200'
_lblwidth = 10
font='Verdana 10 bold'
_pady=8
_padx=4

config = configparser.ConfigParser()
config.read("config.ini")

api_key = config['default']['API_KEY']
cryptos = config['default']['GET_CRYPTOS_EP']
price_conversion = config['default']['VALUE_CRYPTO_EP']


class Movements(ttk.Frame):
    _head = ['Fecha', 'Hora', 'From', 'Q', 'To', 'Q', 'P.U']
    newTransaccion =NONE

    def __init__(self, parent, **kwargs):
        #creamos el Scrollbar y pintamos los movimientos obtenidos de movementsDB
        ttk.Frame.__init__(self, height=kwargs['height'],width = kwargs['width'])

        self.printHeaders()

        self.marcoFrame= Frame(self, bd=2, bg="white", relief=GROOVE)
        self.marcoFrame.grid(column=0, row=1, columnspan=18)
        
        self.verticaScrollbar = Scrollbar(self.marcoFrame)
        self.verticaScrollbar.grid(row=0, column=1,sticky=N+S)
        self.verticaScrollbar.grid_columnconfigure(1,weight=1)
        self.canvas = Canvas(self.marcoFrame, yscrollcommand=self.verticaScrollbar.set)
        
        self.canvas.grid(row=0, column=0, sticky=N+S+E+W)
        self.canvas.config(width=801,height= 180)
        self.canvas.grid_propagate(0)
        self.verticaScrollbar.config(command=self.canvas.yview)

        self.frame = Frame(self.canvas, width=801, height= 180)
        
        self.printMovements()
        
        self.windows=self.canvas.create_window(0,0, anchor=NW, window=self.frame)
        
        self.frame.update_idletasks()
        self.canvas.config(scrollregion= self.canvas.bbox('all'))
 
    def printHeaders(self): 
        #pintando cabeceras   
        for i in range (0, 7):
            self.lblDisplay = ttk.Label(self, text=self._head[i], font='verdana, 10', width = 16, background ='white', borderwidth=1, relief=GROOVE, anchor=CENTER)
            self.lblDisplay.grid(row=0, column=i, pady=1)
            self.lblDisplay.grid_propagate(0)
        self.lblDisplay = ttk.Label(self, font='verdana, 10', width = 2)
        self.lblDisplay.grid(row=0, column=7, pady=1)
        self.lblDisplay.grid_propagate(0)        

    def addUnitPriceIntoMovements(self):
        #Calcula y añade el coste unidad y cambia la id_crypto por symbol_crypto
        self.movements=movementsDB.printMovementsDB()
        for movement in self.movements:
            i=0
            while i <=6:
                if i ==6:
                    unitPrice=movement[3]/(movement[5])
                    movement.append(unitPrice)
                if i == 2 or i == 4:
                    movement[i] = movementsDB.getIdFromToCryptoDB(movement[i],FALSE)
                i += 1
    
    def printMovements(self): 
        #Define el formato de salidas a 5 decimales máximo y pinta los movimientos actualizando el scrollregion con el nuevo movimiento 
        self.addUnitPriceIntoMovements()
        j=0
        for movement in self.movements:
            i=0
            while i <=6:
                if i == 3 or i == 5 or i == 6:
                    movement[i]='{0:.6f}'.format(movement[i])
                self.lblDisplay = ttk.Label(self.frame, text=movement[i], font='Verdana, 10',width= 16, background ='white', foreground ='black', borderwidth=1, relief=GROOVE, anchor=CENTER)
                self.lblDisplay.grid(row=j, column=i)
                self.lblDisplay.grid_propagate(0)
                if i == 3 or i == 5 or i == 6:
                    self.lblDisplay.config(anchor= E)
                i+=1
            j += 1
        self.canvas.config(scrollregion= self.canvas.bbox('all'))             

    def actualizarScrollregion(self):
        #actualiza scrollregion muestrando última transacción
        self.frame.update_idletasks()
        self.canvas.config(scrollregion= self.canvas.bbox('all'))             


class NewTransaction(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, height=100, width =_width, borderwidth=2, relief= GROOVE)
        self.simulador=parent

        #self.s = ttk.Style() #Creamos el style paa este frame ------
        #self.s.configure('TFrame', background='blue') #aplicamos el stylo---------

        #variables de control
        self.strFrom_Q = StringVar(value='')
        self.strOldFrom_Q = self.strFrom_Q.get()
        self.strFrom_Q.trace('w', self.entryValidationFrom)

        self.getFromCrypto = StringVar()
        self.getToCrypto = StringVar()

        ttk.Label(self, text='Nueva transacción', width=20,font=font, anchor=CENTER).grid(column=0,row=0, columnspan=2, ipadx=20, padx=1, pady=20, sticky=W)
        ttk.Label(self, text='From:', width=_lblwidth, font=font, anchor=E).grid(column=0, row=1, padx=_padx, pady=_pady)
        ttk.Label(self, text='Q:', width=_lblwidth, font=font, anchor=E).grid( column=0, row =2, padx=_padx, pady=_pady)
        ttk.Label(self, text='To:', width=_lblwidth, font=font, anchor=E).grid(column=2, row=1, padx=_padx, pady=_pady)
        ttk.Label(self, text='Q:', width=_lblwidth, font=font, anchor=E).grid(column=2, row=2, padx=_padx, pady=_pady)
        ttk.Label(self, text='P.U:', width=_lblwidth, font=font, anchor=E).grid(column=2, row=3)
        
        self.pULbl = ttk.Label(self, text='', font=font, width=22, anchor=E, background='whitesmoke', relief=GROOVE)
        self.pULbl.grid(column=3, row=3, padx=_padx, pady=_pady)
        self.to_QLbl = ttk.Label(self,text='', font=font, width=22, anchor=E, background='whitesmoke', relief=GROOVE)
        self.to_QLbl.grid(column=3, row=2)
        self.controlErrorCryptos = ttk.Label(self, font='Verdana 8', foreground='red', anchor=CENTER, text='')
        self.controlErrorCryptos.grid(column=0, row=4, columnspan=5)
        
        self.from_Q = ttk.Entry(self, text='', font=font, width=22, textvariable=self.strFrom_Q, justify=RIGHT, state='disable')
        self.from_Q.grid(column=1,row=2)
        
        self.fromCryptoCombo = ttk.Combobox(self, width=20, font=font, textvariable=self.getFromCrypto,values=NONE, state='disable')
        self.fromCryptoCombo.grid(column=1, row=1)
        self.fromCryptoCombo.bind("<<ComboboxSelected>>", self.selectNewCryptoInComboBox)
        self.toCryptoCombo = ttk.Combobox(self, width=20, font=font, textvariable= self.getToCrypto, values=NONE, state='disable')
        self.toCryptoCombo.grid(column=3, row=1)
        self.toCryptoCombo.bind("<<ComboboxSelected>>", self.selectNewCryptoInComboBox)
        self.valuesComboBoxIni()
        self.valuesComboBox()

        self.cancelButton = ttk.Button(self, text='Cancelar', command=lambda: self.switchNewTransaction(FALSE,TRUE), state='disable')
        self.cancelButton.grid(column=4, row=1, ipadx="8", padx=10, pady=_pady, sticky="W")
        self.checkButton = ttk.Button(self, text = 'Comprobar', command =lambda: self.checkTransaction(FALSE), state='disable')
        self.checkButton.grid(column=4, row=2, padx=10, pady=_pady, sticky="W")
        self.acceptButton = ttk.Button(self, text='Aceptar', command=lambda: self.checkTransaction(), state='disable')
        self.acceptButton.grid(column=4, row=3, ipadx="8", padx=10, pady=_pady, sticky="W")
    
    def selectNewCryptoInComboBox(self, event):
        #reactivar boton aceptar y limpia label 
        self.acceptButton.config(state='enable')
        self.controlErrorCryptos.config(text=' ')

    def whatCrypto(self,crypto):
        #while para obtener el symbol de la crypto seleccionada
        i=0
        symbolCrypto=''
        while crypto[i] != ' ':
            symbolCrypto +=crypto[i]
            i+=1
        return(symbolCrypto)
    
    def strCleaner(self):
        #eliminamos espacios
        strcleaned=''
        for i in range (len(self.strFrom_Q.get())):
            if self.strFrom_Q.get()[i] != ' ':
                strcleaned += self.strFrom_Q.get()[i]
        return(strcleaned) 
    
    def entryValidationFrom(self, *args):
        #validar entradas con valores numéricos y sin espacios
        if self.strFrom_Q.get()=='':
                self.strOldFrom_Q = self.strFrom_Q.get()
        else:
            try:
                self.floatFrom_Q = float(self.strFrom_Q.get())
                self.strFrom_Q.set(self.strCleaner())
                self.strOldFrom_Q = self.strFrom_Q.get()
                #if float(self.strFrom_Q.get())<= self.cryptoInvertida:
                self.acceptButton.config(state= 'enable')
                self.controlErrorCryptos.config(text=' ')
            except:
                self.strFrom_Q.set(self.strOldFrom_Q)
    
    def processingApiInfo(self, response, cryptoname):
        #procesar informacion para conseguir precio y calcular el unitario
        values= json.loads(response)
        valorQ = values['data']['quote'][cryptoname]['price']
        priceU = float(self.strFrom_Q.get())/valorQ
        self.to_QLbl.config(text=valorQ)
        self.pULbl.config(text=priceU)
        return(valorQ)
    
    def informedAndDiferentCombo(self):
        #comprueba los combos que esten informados, sean diferentes y que el valor de Q sea distinto a 0
        if len(self.getFromCrypto.get()) != 0 and len(self.getToCrypto.get()) != 0:
            self._from = self.whatCrypto(self.getFromCrypto.get())
            self._to = self.whatCrypto(self.getToCrypto.get())
            if self._from != self._to and self.strFrom_Q.get() != '0' and self.strFrom_Q.get() !='':
                return (TRUE)
            else:
                if self._from == self._to:
                    #self.controlErrorCryptos.config(text='Los campos From y To deben ser distintos')
                    self.controlErrorCryptos.config(messagebox.showinfo(message="¿De veras quieres invertir en la misma moneda? Los campos From y To deben ser distintos", title="¡¡Ups, algo falla!!"))
                if self.strFrom_Q.get() == '0' or self.strFrom_Q.get() =='':
                    #self.controlErrorCryptos.config(text='{} El valor Q debe ser mayor que 0. '.format(self.controlErrorCryptos.config('text')[4]))
                    self.controlErrorCryptos.config(messagebox.showinfo(message="¡Que pasa!, ¿no encuentras nada en la hucha? Para invertir el valor Q debe ser mayor que 0", title="¡¡Ups, algo falla!!"))
                self.acceptButton.config(state='disable')
                return(FALSE)    
        else:
            #self.controlErrorCryptos.config(text ='Los campos From y To deben estar informados.')
            self.controlErrorCryptos.config(messagebox.showerror(message="Los campos From y To deben estar informados", title="¡¡Ups, algo falla!!"))
            return(FALSE)   
        
    def valueFromQValidate(self):
        #controla el valor de from_Q para que no sea superior al maximo permitido por la api y que podamos disponer de las cryptos seleccionadas para su compra
        maximumValueApi = 1000000000
        if float(self.strFrom_Q.get())<= maximumValueApi and self._from == 'EUR':
            return(TRUE)
        elif self._from != 'EUR' and float(self.strFrom_Q.get())<= maximumValueApi:
            calculateCryptoto=movementsDB.MoneySpend(self._from,FALSE)
            calculateCryptofrom=movementsDB.MoneySpend(self._from)
            self.cryptoInvertida = calculateCryptoto - calculateCryptofrom
            if self.cryptoInvertida < float(self.strFrom_Q.get()):
                self.acceptButton.config(state= 'disable')
                #self.controlErrorCryptos.config(text='Actualmente dispones de {} {}. Modifique el valor para realizar la transacción'.format(self.cryptoInvertida,self._from))
                self.controlErrorCryptos.config(messagebox.showinfo(message="Actualmente dispones de {} {}. Modifica el valor para realizar la transacción".format(self.cryptoInvertida,self._from), title="¡¡Ups, algo falla!!"))
                return(FALSE)
            else:
                return(TRUE)  
        else:
            return(FALSE)
        
    def validateAllValues(self):
        #valida los campos para realizar la llamada
        fromAndToDiferentBol = self.informedAndDiferentCombo()
        if fromAndToDiferentBol:
            valueStatus = self.valueFromQValidate()
            if valueStatus:
                return(TRUE)
            else:
                return(FALSE)
        else:
            return(FALSE)
    
    def checkTransaction(self, addDB=TRUE):
        #comprueba que los combos sean distintos y su valor no sea 0 y hace la llamada a la api
        allValuesValidate = self.validateAllValues()
        if allValuesValidate:
            self.acceptButton.config(state= 'enable')
            self.controlErrorCryptos.config(text=' ')
            try:
                url= price_conversion.format(self.strFrom_Q.get(),self._from, self._to, api_key)
                response=api_acces.accesoAPI(url)
                self.cryptoPriceTo=self.processingApiInfo(response,self._to)
                if addDB == TRUE:
                    #graba datos en DB y resetea los campos y los desactiva
                    self.addNewTransactionIntoDB(self._from, self._to)
                    self.switchNewTransaction(FALSE,TRUE)
                    self.simulador.addNewMovementintoMovement()
                    self.valuesComboBox()
            except Exception as e:
                error=('Se ha producido una incidencia:',e)
                #self.controlErrorCryptos.config(text=error)
                self.controlErrorCryptos.config(messagebox.showerror(message="Se ha producido una Incidencia", title="¡¡Ups, algo falla!!"))

    def addNewTransactionIntoDB(self,symbolCrypto_from, symbolCrypto_to):
        #procesa y obtiene la información que se necesita para la DB
        data = time.strftime('%Y-%m-%d')
        hour=datetime.datetime.now().strftime("%H:%M:%S.%f")
        hour = hour[:(len(hour)-3)]
        from_currency = movementsDB.getIdFromToCryptoDB(symbolCrypto_from)
        to_currency = movementsDB.getIdFromToCryptoDB(symbolCrypto_to)
        from_quantity= float(self.strFrom_Q.get())
        movementsDB.addNewMovement(data, hour, from_currency,to_currency,self.strFrom_Q.get(), self.cryptoPriceTo)

    def valuesComboBoxIni(self):
        #informa ComboBox con el EUR en From y con todas las cryptos en el To
        result = movementsDB.listCryptos()
        resultFrom = movementsDB.listCryptosIni()
        self.toCryptoCombo.config(values=result)
        self.fromCryptoCombo.config(values=resultFrom)

    def valuesComboBox(self):
        #informa ComboBox con las cryptos
        result = movementsDB.listCryptos()
        resultFrom = movementsDB.listCryptosInvert()
        self.toCryptoCombo.config(values=result)
        self.fromCryptoCombo.config(values=resultFrom)
    
    def switchNewTransaction(self, switch_On = FALSE , transactionButton=FALSE):
        #interruptor que activa y desactiva el frame newtransaction, tambien desactiva el boton de nueva transacción hasta que cancela o se realiza la nueva transaccion
        if switch_On:
            switch_state='enable'
            colorbg = 'white'
            switch_combo = 'readonly'
        else:
            switch_state='disable'
            colorbg='whitesmoke'
            switch_combo='disable'

        self.pULbl.config(background= colorbg)
        self.to_QLbl.config(background= colorbg)
        self.from_Q.config(state= switch_state)
        self.fromCryptoCombo.config(state= switch_combo)
        self.toCryptoCombo.config(state= switch_combo)
        self.cancelButton.config(state= switch_state)
        self.acceptButton.config(state= switch_state)
        self.checkButton.config(state=switch_state)
        
        if transactionButton:
            self.resetVariables()    
        
    def resetVariables(self):
        self.controlErrorCryptos.config(text='')
        self.toCryptoCombo.set('')
        self.fromCryptoCombo.set('')
        self.to_QLbl.config(text='')
        self.pULbl.config(text='')
        self.cryptoInvertida=0
        self.strOldFrom_Q=''
        self.strFrom_Q.set(self.strOldFrom_Q)


class Results(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, height=kwargs['height'],width = kwargs['width'], relief= GROOVE)
        
        ttk.Label(self, text='Tu inversión', font= font, anchor=E, width =_lblwidth).grid(column=0,row =3, ipady=1, ipadx=1, pady=3, padx=5)
        ttk.Label(self, text='€ invertidos:', font= font, anchor=E, width = _lblwidth).grid(column=0,row =4, padx=_padx)
        ttk.Label(self, text='Valor actual:', font= font, anchor=E, width = _lblwidth).grid(column=2,row=4, padx=_padx)
        
        self.moneySpendLbl=ttk.Label(self, font=font,background ='white', anchor=E, relief=GROOVE, width=22)
        self.moneySpendLbl.grid(column=1, row=4, padx=_padx)
        self.currentValueLbl=ttk.Label(self, font=font,background ='white', relief=GROOVE, anchor=E, width=22)
        self.currentValueLbl.grid(column=3, row=4, padx=_padx)
        self.calculateButton=ttk.Button(self, text='Calcular', command=lambda: self.earnings())
        self.calculateButton.grid(column=4, row=4, ipadx= "8", padx= 10, pady=_pady)
    
    def moneySpend(self):
        #calcula el total de euros invertidos
        eurosFrom=movementsDB.MoneySpend('EUR')
        eurosTo=movementsDB.MoneySpend('EUR',FALSE)
        totalMoneySpend = eurosFrom - eurosTo
        totalMoneySpend = ('{0:.2f}€'.format(totalMoneySpend))
        self.moneySpendLbl.config(text=totalMoneySpend)

    def calculateCurrentValueApi(self, resultCurrentValue,cryptoSymbolFrom):
        #verifica que se haya invertido en la crypto elegida, si es asi se llama a la api para obtener su valor en euros
        if resultCurrentValue != 0:
            try:
                url= price_conversion.format(resultCurrentValue,cryptoSymbolFrom, 'EUR', api_key)
                response=api_acces.accesoAPI(url)
                resultCryptoToEuro= json.loads(response)
                currentValueResult = resultCryptoToEuro['data']['quote']['EUR']['price']
                return (currentValueResult)
            except Exception as e:
                print('Fallo acceso:',e)
        else:
            return(0)
    
    def currentValue(self,cryptos):
        #el bucle for recorre las cryptos excepto EUR y calcula por cada crypto en from y to
        totalCurrentValuesResults = 0
        for i in range (len(cryptos)-1):
            sumatorioFromCrypto= movementsDB.MoneySpend(cryptos[i])
            sumatorioToCrypto = movementsDB.MoneySpend(cryptos[i], FALSE)
            result= sumatorioToCrypto - sumatorioFromCrypto       
            totalCurrentValuesResults += self.calculateCurrentValueApi(result,cryptos[i])
        totalCurrentValuesResults = ('{0:.2f}€'.format(totalCurrentValuesResults))   
        self.currentValueLbl.config(text=totalCurrentValuesResults)
    
    def earnings(self):
        #obtiene symbols de cryptos en base de datos y calcula la inversión realizada y su resultado 
        cryptoSymbol=movementsDB.symbolCrytpo()
        
        self.moneySpend()
        self.currentValue(cryptoSymbol)
    
    def resetLabels(self):
        #si se desea hacer un nuevo movimiento se resetean las labels de resultado
        self.moneySpendLbl.config(text='')
        self.currentValueLbl.config(text='')


class Simulador(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, width="910", height="600") 

        #s = ttk.Style() #Creamos el style usado para este Frame ------
        #s.theme_use('clam')
        #self.s.configure('TFrame', background='#434346') #---------
        #self.s.configure('TLabel', background='#434346') #---------
        #self.s.configure('My.TButton', background='#434346') #---------
        #tab1 = ttk.Frame(Frame, style='Simulador.TFrame')
        #mainframe.add(tab1, text="Tab1")
        #self.config(background="#49A") #-----

        #comprueba si la tabla cryptos de DB está informada, sino lo está, la inicializamos 
        initDBCryptos= movementsDB.inicialVerification()
        if not initDBCryptos:
            self.initializationBDCryptos()

        #estructuración de la aplicación
        self.Button1 = ttk.Button(self, text ='+ Nueva transación', command=lambda: self.buttonSimulador(), width=15)
        self.Button1.place(x=700, y=245)

        self.movements =Movements(self, height=240, width=_width)
        #self.movements.grid(column=0, row=0, padx=20)
        self.movements.place(x=40,y=30)
        
        self.newTransaction= NewTransaction(self, height=220, width=_width)
        #self.newTransaction.grid(column=0, row=1, padx=20)
        self.newTransaction.place(x=40, y=280)
        

        self.results = Results(self, height=100, width=_width)
        #self.results.grid(column=0, row=2, pady=40)
        self.results.place(x=40, y=480)

    def addNewMovementintoMovement(self):
        #pinta los movimientos después de una transacción y actualiza la scrollbar
        self.movements.printMovements()
        self.movements.actualizarScrollregion()

    def buttonSimulador(self):
        #activa labels de newtransaction y limpia labels results
        self.newTransaction.switchNewTransaction(TRUE)
        self.results.resetLabels()

    def initializationBDCryptos(self):
        #llama a la api para conseguir el name y symbol de las cryptos que vamos a usar
        url = cryptos.format(api_key)
        try:
            callback= api_acces.accesoAPI(url)
        except api_acces.accesError as e:
            errorMessageLbl.config(text=e.cause)

        self.getCryptos(callback)    

    def getCryptos(self, txt):
        #procesa datos que nos devuelve apicall y los graba en DB y añadimos el euro
        currencies= json.loads(txt)
        results= {}
        symbols = currencies['data']
        
        i=0
        for symbol in symbols:
            results[i] = symbol['symbol'], symbol['name']
            i+=1
        results[i] = ('EUR', 'Euro')
        movementsDB.CryptosDBInformed(results)


class MainApp(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.geometry("910x600")
        self.title("INVIERTE EN CRYPTOS")
        self.resizable(0,0)
        self.simulador = Simulador(self)
        self.simulador.place(x=0, y=0)

        s = ttk.Style() # ------
        s.theme_use('aqua') # -------
    
    def start(self):
        self.mainloop()


if __name__ == '__main__':
    app = MainApp()
    app.start()
