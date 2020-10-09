#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM2"                  # Windows(variacao de)

# def header(payload,current_p, total_p):

#     payload_size = payload.to_bytes(4, byteorder='big')
#     payload_number = current_p.to_bytes(2, byteorder='big')
#     total_number = total_p.to_bytes(4,byteorder='big')

#     header = payload_size + payload_number + total_number

#     return header

def main():


	try:
   #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
		#para declarar esse objeto é o nome da porta.
		com = enlace(serialName)
	
		# Ativa comunicacao. Inicia os threads e a comunicação seiral 
		com.enable()
	
		#Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
		print("comunicação aberta com sucesso. porta {}".format(serialName))
		
		#aqui você deverá gerar os dados a serem transmitidos. 
		#seus dados a serem transmitidos são uma lista de bytes a serem transmitidos. Gere esta lista com o 
		#nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.


		comms = True
		STATE = "Start"
		imageW = "./recebidaTeste.png"
		p_anterior = 0 

		imagem = bytes(0)

		while comms:


			if STATE == "Start":

				handshake = True

				while handshake:



					rxBuffer, nRx = com.getData(14)
					time.sleep(0.1)
					print('recebeu {} bytes de dados' .format(len(rxBuffer)))


					payload_size = (1).to_bytes(4, byteorder='big')
					print("payload size ok!")
					payload_number = (0).to_bytes(2, byteorder='big')
					print("payload number ok!")
					total_number = (0).to_bytes(4,byteorder='big')
					print("total number ok!")

					header = payload_size + payload_number + total_number
					print("header ok!")
					eop = (0).to_bytes(4,byteorder='big')
					pkt = header + eop
					print("pkt ok!")
					com.sendData(pkt)
					print("handshake enviado...")
					STATE = "Connected"
					print("mudando para estado: {}".format(STATE))
					handshake = False

			if STATE == "Connected":

				rxBuffer, nRx = com.getData(10)

				print("header recebido!")

				size = rxBuffer[0]
				current_p = rxBuffer[1]
				print("Pacote Atual: {}".format(current_p))
				total_p = rxBuffer[2]
				h3 = rxBuffer[3]
				h4 = rxBuffer[4]
				h5 = rxBuffer[5]
				h6 = rxBuffer[6]
				h7 = rxBuffer[7]
				h8 = rxBuffer[8]
				h9 = rxBuffer[9]
				print("size: {}".format(size))

				txBuffer, nTx = com.getData(size)


				imagem += txBuffer

				print("payload size: {}".format(len(txBuffer)))

				eop, nEop = com.getData(4)

				if current_p == p_anterior + 1:
					p_anterior +=1
					com.sendData(eop)
				else:
					print("ordem dos pacotes incorreta.")
					break

				if size < 114:

					com.disable()
					print("Fim")
					break





		# size = int.from_bytes(rxBuffer, byteorder='big')
		# time.sleep(0.1)

		# rxBuffer, nRx = com.getData(size)


		# time.sleep(0.1)
		# print("Tamanho recebido: {}".format(size))
		
		# com.sendData(size.to_bytes(4,byteorder="big"))

		print ("Salvando dados no arquivo :")
		print (" - {}".format(imageW))
		f = open(imageW, 'wb')
		f.write(imagem)
		print("imagem salva.")

		com.sendData((0).to_bytes(1, byteorder='big'))
		print("resposta final enviada")
		print("----------------------")
		print("Comunicação encerrada")
		print("----------------------")

		# time.sleep(0.1)
	
		
	
		# # Encerra comunicação
		# print("-------------------------")
		# print("Comunicação encerrada")
		# print("-------------------------")
		# com.disable()
	except:
		print("ops! :-\\")
		com.disable()

	#so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
	main()
