#!/usr/bin/python
# -*- coding: utf-8 -*-

# Jesús Galán Barba
# Ing. en Sistemas de Telecomunicaciones

import webapp
import sys

hostname = "localhost"
port = 1234

class calculadora_REST(webapp.webApp):

    def parse(self, request):
        try:
            metodo = request.split(' ',2)[0]
            recurso = request.split(' ',2)[1]
            try:
                cuerpo = request.split('\r\n\r\n')[1]
            except IndexError:
                cuerpo =""
        except IndexError:
            return None

        elementos_peticion = [metodo, recurso, cuerpo]
        return elementos_peticion

    def sumador(self, num1, num2):
        resultado = num1 + num2
        return resultado

    def restador(self, num1, num2):
        resultado = num1 - num2
        return resultado

    def multiplicador(self, num1, num2):
        resultado = num1 * num2
        return resultado

    def dividor(self, num1, num2):
        try:
            resultado = num1 / num2
        except ZeroDivisionError:
            resultado = None

        return resultado

    def process(self, elementos_peticion):

        operaciones = ["suma", "resta", "multiplicacion", "division"]
        try:
            metodo = elementos_peticion[0]
            recurso = elementos_peticion[1][1:]
            cuerpo = elementos_peticion[2]
        except TypeError:
            httpCode = "400 Bad Request"
            htmlResp = "Error en la solitud!"
            return (httpCode, htmlResp)

        if metodo == "GET":
            try:
                result_final = self.result
                info_get = self.resp_get
                httpCode = "200 OK"
                htmlResp = "<html><body><h3>" + info_get + "</h3></body></html>"
            except AttributeError:
                httpCode = "400 Bad Request"
                htmlResp = "<html><body><h3><font color='red'>Error! " +\
                            "No has realizado ninguna operacion.\n" +\
                            "Primero tienes que hacer un PUT con dos numeros!" +\
                            "</font></h3></body></html>"

        elif metodo == "PUT":
            # En el cuerpo es donde se indican los numeros a tener en cuenta para
            # realizar las operaciones deseadas. En el cuerpo, los numeros vendran
            # separados por un espacio en blanco
            try:
                self.num1 = float(cuerpo.split(" ")[0])
                self.num2 = float(cuerpo.split(" ")[1])
            except ValueError:
                httpCode = "400 Bad Request"
                htmlResp = "Error: Solo se permiten poner numeros separados por un " +\
                            "espacio en blanco. Vuelve a intentarlo!"
                return (httpCode, htmlResp)

            if recurso == operaciones[0]:
                self.result = self.sumador(self.num1, self.num2)
                self.resp_get = "Suma: " + str(self.num1) + " + " + str(self.num2 ) + \
                                " = " + str(self.result)
                httpCode = "200 OK"
                htmlResp = "Suma realizada con exito. Comprueba el resultado " +\
                            "mediante el metodo GET"
            elif recurso == operaciones[1]:
                self.result = self.restador(self.num1, self.num2)
                self.resp_get = "Resta: " + str(self.num1) + " - " + str(self.num2 ) + \
                                " = " + str(self.result)
                httpCode = "200 OK"
                htmlResp = "Resta realizada con exito. Comprueba el resultado " +\
                            "mediante el metodo GET"
            elif recurso == operaciones[2]:
                self.result = self.multiplicador(self.num1, self.num2)
                self.resp_get = "Multipliacion: " + str(self.num1) + " * " + str(self.num2 ) + \
                                " = " + str(self.result)
                httpCode = "200 OK"
                htmlResp = "Multipliacion realizada con exito. Comprueba el resultado " +\
                            "mediante el metodo GET"
            elif recurso == operaciones[3]:
                self.result = self.dividor(self.num1, self.num2)
                if self.result == None:
                    httpCode = "400 Bad Request"
                    htmlResp = "Error! Intento de dividor por 0"
                else:
                    self.resp_get = "Division: " + str(self.num1) + " / " + str(self.num2 ) + \
                                    " = " + str(self.result)
                    httpCode = "200 OK"
                    htmlResp = "Division realizada con exito. Comprueba el resultado " +\
                                "mediante el metodo GET"
            else:
                httpCode = "404 Not Found"
                htmlResp = "Operacion no valida\n" +\
                            "Recursos aceptables: suma, resta, multipliacion, division"

        else:
            httpCode = "405 Method Not Allowed"
            htmlResp = "Metodo no identificado!"

        return (httpCode, htmlResp)

if __name__ == "__main__":
    try:
        Test_calc_REST = calculadora_REST(hostname, port)
    except KeyboardInterrupt:
        print "\nAplicación cerrada por el usuario en el terminal!\n"
        sys.exit()
