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
import datetime

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)

# def header(payload,current_p, total_p):

#     payload_size = payload.to_bytes(4, byteorder='big')
#     payload_number = current_p.to_bytes(2, byteorder='big')
#     total_number = total_p.to_bytes(4,byteorder='big')

#     header = payload_size + payload_number + total_number

#     return header

def main():



	def retry(fun, max_tries=5):
			tentativa = 2 
			for i in range(max_tries):
				print("tentativa numero {}.".format(tentativa))
				print("proxima tentativa em 5 segundos")
				tentativa+=1
				try:
				   time.sleep(5)

				   fun()
				   break
				except Exception:
					continue
			print("tempo esgotado!")
			log.write('{} / envio / 5\n'.format(datetime.datetime.now()))


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
		server_id = 1
		log = open('server_log.txt','w')
		TIMEOUT = False

		while comms:


			if STATE == "Start":

				handshake = True

				while handshake:



					# rxBuffer, nRx = retry(com.getData(14),max_tries=3)
					rxBuffer, nRx = com.getData(14)
					
					log.write('{} / recebimento / 1 /{}\n'.format(datetime.datetime.now(),len(rxBuffer)))
					print('{} / recebimento / 1 /{}\n'.format(datetime.datetime.now(),len(rxBuffer)))

					time.sleep(0.1)
					print('recebeu {} bytes de dados' .format(len(rxBuffer)))


					if rxBuffer[0] == 1 and rxBuffer[2] == 0:

						print("tipo de mensagem e identificador corretos!")


						h0 = (2).to_bytes(1, byteorder='big')
						h1 = (0).to_bytes(1, byteorder='big')
						h2 = server_id.to_bytes(1,byteorder='big')
						h3 = rxBuffer[3].to_bytes(1,byteorder='big')
						h4 = (0).to_bytes(1, byteorder='big')
						h5 = (0).to_bytes(1,byteorder='big')
						h6 = (0).to_bytes(1,byteorder='big')
						h7 = (0).to_bytes(1,byteorder='big')
						h8 = (0).to_bytes(1,byteorder='big')
						h9 = (0).to_bytes(1,byteorder='big')

						header = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9

						print("header ok!")
						eop = (0).to_bytes(4,byteorder='big')
						pkt = header + eop
						print("pkt ok!")
						# time.sleep(12)
						com.sendData(pkt)
						print("handshake enviado...")
						log.write('{} / envio / 2 / 0 / {}\n'.format(datetime.datetime.now(),int.from_bytes(h3,byteorder='big')))
						print('{} / envio / 2 / 0 / {}\n'.format(datetime.datetime.now(),int.from_bytes(h3,byteorder='big')))
						STATE = "Connected"
						print("mudando para estado: {}".format(STATE))
						handshake = False

					else: 
						print("tipo de mensagem ou identificador incorreto.")

			if STATE == "Connected" and TIMEOUT == False:

				print("Conectado!")

				rxBuffer, nRx = com.getData(10)

				print("mensagem recebida!")
				print("header recebido!")



				if rxBuffer == "TIMEOUT":

					print("TIMEOUT")
					h0 = (5).to_bytes(1, byteorder='big')
					h1 = (0).to_bytes(1, byteorder='big')
					h2 = (0).to_bytes(1, byteorder='big')
					h3 = (0).to_bytes(1,byteorder='big')
					h4 = (0).to_bytes(1, byteorder='big')
					h5 = (0).to_bytes(1, byteorder='big')
					h6 = (0).to_bytes(1,byteorder='big')
					h7 = (0).to_bytes(1,byteorder='big')
					h8 = (0).to_bytes(1,byteorder='big')
					h9 = (0).to_bytes(1,byteorder='big')

					pkt_timeout = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9 + eop
					print("Timeout package ok!")

					# com.sendData(pkt_timeout)
					log.write("{} / envio / 5\n".format(datetime.datetime.now()))
					print(("{} / 5 - LOGGED".format(datetime.datetime.now())))

					TIMEOUT = True
					print("TIMEOUT TRUE")
					# com.disable()
					# print("COM DISABLED.")
					STATE = "Disconnected"
					print("mudando para estado DISCONNECTED")
					comms = False
				else:

				

					mgs_type = rxBuffer[0]
					client_id = rxBuffer[2]
					total_p = rxBuffer[3]
					current_p = rxBuffer[4]
					print("Pacote Atual: {}".format(current_p))
					size = rxBuffer[5]
					restart_p = rxBuffer[6]
					last_p = rxBuffer[7]
					CRC1 = rxBuffer[8]
					CRC2 = rxBuffer[9]
					print("size: {}".format(size))


					txBuffer, nTx = com.getData(size)


					imagem += txBuffer

					print("payload size: {}".format(len(txBuffer)))

					eop, nEop = com.getData(4)

					log.write('{} / recebimento / 3 / {} / {} / 0 / {}\n'.format(datetime.datetime.now(),size, current_p, total_p))


					h0 = (4).to_bytes(1, byteorder='big')
					h1 = (0).to_bytes(1, byteorder='big')
					h2 = server_id.to_bytes(1, byteorder='big')
					h3 = total_p.to_bytes(1, byteorder='big')
					print("total_p ok!")
					h4 = current_p.to_bytes(1, byteorder='big')
					h5 = size.to_bytes(1, byteorder='big')
					h6 = restart_p.to_bytes(1, byteorder='big')
					h7 =  last_p.to_bytes(1, byteorder='big')
					h8 = CRC1.to_bytes(1, byteorder='big')
					h9 = CRC2.to_bytes(1, byteorder='big')

					header = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9
					payload = 0

					print("header ok!")
				


					pkt = header + eop

					print("pacote ok!")


					if current_p == p_anterior + 1:
						p_anterior +=1
						com.sendData(pkt)
						log.write('{} / envio / 4 / 14\n'.format(datetime.datetime.now()))
						print('{} / envio / 4 / 14\n - LOGGED'.format(datetime.datetime.now()))
					else:
						print("ordem dos pacotes incorreta.")
						h0 = (6).to_bytes(1,byteorder='big')
						h1 = (0).to_bytes(1, byteorder='big')
						h2 = server_id.to_bytes(1, byteorder='big')
						h3 = total_p.to_bytes(1, byteorder='big')
						print("total_p ok!")
						h4 = current_p.to_bytes(1, byteorder='big')
						h5 = size.to_bytes(1, byteorder='big')
						h6 = restart_p.to_bytes(1, byteorder='big')
						h7 =  last_p.to_bytes(1, byteorder='big')
						h8 = CRC1.to_bytes(1, byteorder='big')
						h9 = CRC2.to_bytes(1, byteorder='big')
						header6 = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9 				
						pkt6 = header6 + eop 
						com.sendData(pkt6)
						log.write("'{} / envio / 6 / {}".format(datetime.datetime.now(), restart_p))
						

					if size < 114:

						com.disable()
						print("Fim")
						break

		if STATE == "Disconnected":

			print("Tempo esgotado! encerrando...")
			log.close()
			com.disable()






		# size = int.from_bytes(rxBuffer, byteorder='big')
		# time.sleep(0.1)

		# rxBuffer, nRx = com.getData(size)


		# time.sleep(0.1)
		# print("Tamanho recebido: {}".format(size))
		
		# com.sendData(size.to_bytes(4,byteorder="big"))

		log.close()

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
		log.close()
		print("fechando log")
		com.disable()

	#so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
	main()
